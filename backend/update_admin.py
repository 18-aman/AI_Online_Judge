import uuid
from fastapi import APIRouter, Depends, HTTPException

filepath = 'app/api/admin.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_routes = '''
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
'''

if "def update_problem" not in content:
    content += "\n" + new_routes
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
