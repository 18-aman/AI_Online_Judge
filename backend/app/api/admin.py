from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import uuid

from app.core.database import get_db
from app.models.problem import Problem, TestCase
from app.services.judge import run_code_in_docker
from app.api.deps import get_current_admin_user

router = APIRouter(dependencies=[Depends(get_current_admin_user)])

class GenerateTestCasesRequest(BaseModel):
    reference_code: str
    language: str
    inputs: List[str]

@router.post("/problems/{problem_id}/generate-testcases")
def generate_testcases(problem_id: str, request: GenerateTestCasesRequest, db: Session = Depends(get_db)):
    # Verify problem exists
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
        
    mock_test_cases = []
    for idx, inp in enumerate(request.inputs):
        if not inp.strip():
            continue
        tc = TestCase(
            id=uuid.uuid4(),
            problem_id=problem.id,
            input_data=inp.strip(),
            expected_output="",  # Placeholder
            is_hidden=(idx >= 2)
        )
        mock_test_cases.append(tc)
        
    if not mock_test_cases:
        raise HTTPException(status_code=400, detail="No valid inputs provided")
        
    # Run the reference code
    result = run_code_in_docker(request.language, request.reference_code, mock_test_cases, time_limit=5.0, signature_schema=problem.signature_schema)
    
    if result["status"] == "Error":
        raise HTTPException(status_code=400, detail=result.get("message", "Compilation Error"))
        
    # Collect outputs and save to DB
    saved_cases = []
    # result["results"] should map 1-to-1 with mock_test_cases in order
    for idx, r in enumerate(result.get("results", [])):
        if r["status"] == "Runtime Error" or "error" in r:
            raise HTTPException(status_code=400, detail=f"Reference Solution Runtime Error: {r.get('error', '')}")
        if r["status"] == "Time Limit Exceeded or Error":
            raise HTTPException(status_code=400, detail="Reference Solution TLE or Crashed.")
            
        actual_output = r.get("output", "")
        
        db_tc = TestCase(
            problem_id=problem.id,
            input_data=mock_test_cases[idx].input_data,
            expected_output=actual_output.strip(),
            is_hidden=(idx >= 2)
        )
        db.add(db_tc)
        saved_cases.append({"input": db_tc.input_data, "generated_output": db_tc.expected_output})
        
    db.commit()
    
    return {
        "message": f"Successfully generated {len(saved_cases)} hidden test cases.",
        "cases": saved_cases
    }

class UpdateCheckerRequest(BaseModel):
    has_custom_checker: bool
    checker_code: str

@router.put("/problems/{problem_id}/checker")
def update_checker(problem_id: str, request: UpdateCheckerRequest, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
        
    problem.has_custom_checker = request.has_custom_checker
    problem.checker_code = request.checker_code
    db.commit()
    return {"message": "Custom checker updated successfully."}



from app.models.problem import Topic, ProblemTopic

class CreateProblemRequest(BaseModel):
    title: str
    description: str
    difficulty: str
    topics: str
    time_limit: float = 1.0
    memory_limit: int = 256
    signature_schema: dict = None

@router.post("/problems/")
def create_problem(request: CreateProblemRequest, db: Session = Depends(get_db)):
    prob = Problem(
        title=request.title,
        description=request.description,
        difficulty=request.difficulty,
        time_limit=request.time_limit,
        memory_limit=request.memory_limit,
        signature_schema=request.signature_schema
    )
    db.add(prob)
    db.flush()
    
    topic_names = [t.strip() for t in request.topics.split(",") if t.strip()]
    for tname in topic_names:
        topic = db.query(Topic).filter(Topic.name == tname).first()
        if not topic:
            topic = Topic(id=uuid.uuid4(), name=tname)
            db.add(topic)
            db.flush()
        db.add(ProblemTopic(problem_id=prob.id, topic_id=topic.id))
        
    db.commit()
    return {"id": str(prob.id), "message": "Problem created successfully"}


from app.models import User
from pydantic import BaseModel

class RoleUpdateRequest(BaseModel):
    role: str

class ProblemUpdateRequest(BaseModel):
    title: str
    description: str
    difficulty: str
    time_limit: float
    memory_limit: int
    topics: str

@router.put("/problems/{problem_id}")
def update_problem(problem_id: uuid.UUID, request: ProblemUpdateRequest, db: Session = Depends(get_db)):
    prob = db.query(Problem).filter(Problem.id == problem_id).first()
    if not prob:
        raise HTTPException(status_code=404, detail="Problem not found")
    prob.title = request.title
    prob.description = request.description
    prob.difficulty = request.difficulty
    prob.time_limit = request.time_limit
    prob.memory_limit = request.memory_limit
    
    # Update topics
    db.query(ProblemTopic).filter(ProblemTopic.problem_id == problem_id).delete()
    topic_names = [t.strip() for t in request.topics.split(",") if t.strip()]
    for tname in topic_names:
        topic = db.query(Topic).filter(Topic.name == tname).first()
        if not topic:
            topic = Topic(id=uuid.uuid4(), name=tname)
            db.add(topic)
            db.flush()
        db.add(ProblemTopic(problem_id=prob.id, topic_id=topic.id))
        
    db.commit()
    return {"message": "Problem updated successfully"}

@router.delete("/problems/{problem_id}")
def delete_problem(problem_id: uuid.UUID, db: Session = Depends(get_db)):
    prob = db.query(Problem).filter(Problem.id == problem_id).first()
    if not prob:
        raise HTTPException(status_code=404, detail="Problem not found")
    db.delete(prob)
    db.commit()
    return {"message": "Problem deleted"}

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": str(u.id), "username": u.username, "role": u.role, "created_at": u.created_at} for u in users]

@router.put("/users/{user_id}/role")
def update_user_role(user_id: uuid.UUID, request: RoleUpdateRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = request.role
    db.commit()
    return {"message": f"User role updated to {request.role}"}

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_problems = db.query(Problem).count()
    total_submissions = db.query(Submission).count()
    return {
        "total_users": total_users,
        "total_problems": total_problems,
        "total_submissions": total_submissions
    }

@router.get("/submissions")
def get_all_submissions(db: Session = Depends(get_db)):
    subs = db.query(Submission, User.username, Problem.title).join(User, User.id == Submission.user_id).join(Problem, Problem.id == Submission.problem_id).order_by(Submission.created_at.desc()).limit(50).all()
    return [{
        "id": str(s[0].id),
        "username": s[1],
        "problem": s[2],
        "verdict": s[0].verdict,
        "language": s[0].language,
        "created_at": s[0].created_at
    } for s in subs]
