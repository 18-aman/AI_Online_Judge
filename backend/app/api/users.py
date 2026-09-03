from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from app.core.database import get_db
from app.models.user import User
from app.models.submission import Submission
from app.models.problem import Problem, Topic, ProblemTopic
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/me/profile")
def get_user_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Total attempted problems
    attempted = db.query(Submission.problem_id).filter(Submission.user_id == current_user.id).distinct().count()
    
    # Total solved problems
    solved = db.query(Submission.problem_id).filter(Submission.user_id == current_user.id, Submission.verdict == "Accepted").distinct().count()

    # Topic-wise skills
    solved_problems_sq = db.query(Submission.problem_id).filter(
        Submission.user_id == current_user.id, 
        Submission.verdict == "Accepted"
    ).distinct().subquery()
    
    topic_counts = db.query(Topic.name, func.count(solved_problems_sq.c.problem_id)).join(
        ProblemTopic, ProblemTopic.topic_id == Topic.id
    ).join(
        solved_problems_sq, solved_problems_sq.c.problem_id == ProblemTopic.problem_id
    ).group_by(Topic.name).all()
    
    radar_data = [{"topic": t[0], "solved": int(t[1]), "fullMark": 10} for t in topic_counts]

    # Recent submissions
    recent_subs = db.query(Submission, Problem.title).join(
        Problem, Problem.id == Submission.problem_id
    ).filter(Submission.user_id == current_user.id).order_by(Submission.created_at.desc()).limit(10).all()
    
    submissions_list = []
    for sub, title in recent_subs:
        submissions_list.append({
            "id": str(sub.id),
            "problem_title": title,
            "verdict": sub.verdict,
                        "language": sub.language,
            "created_at": sub.created_at.isoformat()
        })
        
    return {
        "username": current_user.username,
        "role": current_user.role,
        "stats": {
            "attempted": int(attempted),
            "solved": int(solved)
        },
        "radarData": radar_data,
        "recentSubmissions": submissions_list
    }
