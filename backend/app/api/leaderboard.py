from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.submission import Submission
from app.models.user import User

router = APIRouter()

@router.get("/")
def get_global_leaderboard(db: Session = Depends(get_db)):
    """
    Computes a global leaderboard based on how many unique problems a user has solved.
    Each unique Accepted problem is worth 100 points.
    """
    # Since we don't have strict user associations on submissions during dev sometimes,
    # we'll query submissions that have a valid user_id.
    
    # We want: username, total accepted unique problems -> score
    query = (
        db.query(
            User.username,
            func.count(func.distinct(Submission.problem_id)).label("solved_count")
        )
        .join(Submission, User.id == Submission.user_id)
        .filter(Submission.verdict == "Accepted")
        .group_by(User.id)
        .order_by(func.count(func.distinct(Submission.problem_id)).desc())
        .limit(100)
    )
    
    results = query.all()
    
    leaderboard = []
    for rank, (username, solved) in enumerate(results, start=1):
        leaderboard.append({
            "rank": rank,
            "username": username,
            "score": solved * 100,
            "solved": solved
        })
        
    return leaderboard
