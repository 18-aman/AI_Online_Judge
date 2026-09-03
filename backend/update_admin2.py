import re

filepath = 'app/api/admin.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure the imports are present
if "RoleUpdateRequest" not in content:
    imports = '''
from app.models import User, Submission, ProblemTopic, Topic
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
'''
    content = content.replace("router = APIRouter(prefix=\"/admin\", tags=[\"Admin\"])", imports + "\nrouter = APIRouter(prefix=\"/admin\", tags=[\"Admin\"])\n")
    
    routes = '''
@router.put("/problems/{problem_id}")
def update_problem(problem_id: uuid.UUID, request: ProblemUpdateRequest, db: Session = Depends(get_db)):
    prob = db.query(Problem).filter(Problem.id == problem_id).first()
    prob.title = request.title
    prob.description = request.description
    prob.difficulty = request.difficulty
    prob.time_limit = request.time_limit
    prob.memory_limit = request.memory_limit
    
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
    return {"message": "Problem updated"}

@router.delete("/problems/{problem_id}")
def delete_problem(problem_id: uuid.UUID, db: Session = Depends(get_db)):
    prob = db.query(Problem).filter(Problem.id == problem_id).first()
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
    user.role = request.role
    db.commit()
    return {"message": f"Updated"}

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    return {
        "total_users": db.query(User).count(),
        "total_problems": db.query(Problem).count(),
        "total_submissions": db.query(Submission).count()
    }
'''
    content += "\n" + routes
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
