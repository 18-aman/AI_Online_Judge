import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.problem import Problem, TestCase
from app.models.submission import Submission
from app.models.user import User
from app.schemas.problem import ProblemResponse, ProblemDetailResponse, TestCaseResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProblemResponse])
def get_problems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    problems = db.query(Problem).offset(skip).limit(limit).all()
    
    # Check submissions for the current user
    user_submissions = db.query(
        Submission.problem_id, 
        Submission.verdict
    ).filter(Submission.user_id == current_user.id).all()
    
    # Map to find best status per problem
    status_map = {}
    for sub in user_submissions:
        pid = sub.problem_id
        # If already marked SOLVED, keep it.
        if status_map.get(pid) == "SOLVED":
            continue
        if sub.verdict == "Accepted":
            status_map[pid] = "SOLVED"
        else:
            status_map[pid] = "ATTEMPTED"
            
    # Attach to problem responses
    response = []
    for p in problems:
        p_dict = ProblemResponse.model_validate(p).model_dump()
        p_dict['user_status'] = status_map.get(p.id, "TODO")
        response.append(p_dict)
        
    return response

@router.get("/{problem_id}", response_model=ProblemDetailResponse)
def get_problem(problem_id: uuid.UUID, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
        
    public_test_cases = [tc for tc in problem.test_cases if not tc.is_hidden]
    response_data = ProblemDetailResponse.model_validate(problem)
    response_data.test_cases = [TestCaseResponse.model_validate(tc) for tc in public_test_cases]
    return response_data

class SubmitCodeRequest(BaseModel):
    code: str
    language: str

@router.post("/{problem_id}/submit")
def submit_code(problem_id: uuid.UUID, request: SubmitCodeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
        
    submission = Submission(
        id=uuid.uuid4(),
        problem_id=problem_id,
        user_id=current_user.id,
        code=request.code,
        language=request.language,
        status="PENDING"
    )
    db.add(submission)
    db.commit()
    
    # Trigger Celery worker
    from app.worker import execute_submission
    execute_submission.delay(str(submission.id))
    
    return {"submission_id": str(submission.id), "status": "PENDING"}

@router.get("/submissions/{submission_id}")
def get_submission_status(submission_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    if sub.user_id != current_user.id and current_user.role.value != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized to view this submission")
    
    return {
        "id": sub.id,
        "status": sub.status,
        "verdict": sub.verdict,
        "results": sub.results
    }

class AIActionRequest(BaseModel):
    code: str
    language: str

@router.post("/{problem_id}/review")
def review_code(problem_id: uuid.UUID, request: AIActionRequest, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
        
    from app.services.ai_mentor import get_code_review
    review = get_code_review(problem.title, request.code, request.language)
    return {"review": review}

@router.post("/{problem_id}/complexity")
def analyze_complexity(problem_id: uuid.UUID, request: AIActionRequest, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
        
    from app.services.ai_mentor import get_complexity_analysis
    analysis = get_complexity_analysis(request.code, request.language)
    return {"analysis": analysis}

@router.post("/{problem_id}/mentor")
def ask_mentor(problem_id: uuid.UUID, request: SubmitCodeRequest, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
        
    from app.services.ai_mentor import get_mentor_hint
    hint = get_mentor_hint(problem.title, problem.description, request.code, request.language)
    return {"hint": hint}

@router.post("/{problem_id}/run")
def run_code(problem_id: uuid.UUID, request: SubmitCodeRequest, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
        
    public_test_cases = [tc for tc in problem.test_cases if not tc.is_hidden]
    from app.services.judge import run_code_in_docker
    
    # We serialize testcases to dicts because execute_code expects it
    
    
    results = run_code_in_docker(
        code=request.code,
        language=request.language,
        test_cases=public_test_cases,
        time_limit=problem.time_limit,
        custom_checker_code=problem.checker_code,
        signature_schema=problem.signature_schema
    )
    
    return results






@router.post("/{problem_id}/explain")
def explain_code(problem_id: uuid.UUID, request: AIActionRequest, db: Session = Depends(get_db)):
    explanation = get_code_explanation(request.code, request.language)
    return {"message": explanation}

@router.post("/{problem_id}/debug")
def debug_code(problem_id: uuid.UUID, request: AIActionRequest, db: Session = Depends(get_db)):
    debug_info = get_code_debug(request.code, request.language)
    return {"message": debug_info}
