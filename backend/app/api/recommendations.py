from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.user import User
from app.models.problem import Problem
from app.models.submission import Submission
from app.api.deps import get_current_user
import xgboost as xgb
import pandas as pd
import os

router = APIRouter()

# Load model globally
model = xgb.XGBClassifier()
model_path = os.path.join(os.path.dirname(__file__), '../../recommendation_model.json')
if os.path.exists(model_path):
    model.load_model(model_path)

@router.get("/")
def get_recommendations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Compute user features
    total_submissions = db.query(Submission).filter(Submission.user_id == current_user.id).count()
    if total_submissions == 0:
        user_success_rate = 0.5
    else:
        accepted_submissions = db.query(Submission).filter(Submission.user_id == current_user.id, Submission.verdict == 'Accepted').count()
        user_success_rate = accepted_submissions / total_submissions
    
    # Simple heuristic for skill tier based on success rate
    if user_success_rate < 0.3:
        user_skill_tier = 1
    elif user_success_rate < 0.7:
        user_skill_tier = 2
    else:
        user_skill_tier = 3
        
    # 2. Find unsolved problems
    solved_problem_ids = [
        sub.problem_id for sub in db.query(Submission.problem_id)
        .filter(Submission.user_id == current_user.id, Submission.verdict == 'Accepted').all()
    ]
    
    unsolved_problems = db.query(Problem).filter(~Problem.id.in_(solved_problem_ids)).all()
    
    if not unsolved_problems:
        return []
        
    if not os.path.exists(model_path):
        # Fallback if model doesn't exist
        return [{"id": p.id, "title": p.title, "difficulty": p.difficulty.value} for p in unsolved_problems[:3]]
    
    # 3. Score unsolved problems
    features_list = []
    for p in unsolved_problems:
        diff_val = 1 if p.difficulty.value == 'EASY' else (2 if p.difficulty.value == 'MEDIUM' else 3)
        # Mocking problem pass rate for now (could be computed in real system)
        prob_pass_rate = 0.6 if diff_val == 1 else (0.4 if diff_val == 2 else 0.2)
        
        features_list.append({
            'user_success_rate': user_success_rate,
            'user_skill_tier': user_skill_tier,
            'problem_difficulty': diff_val,
            'problem_pass_rate': prob_pass_rate
        })
        
    df = pd.DataFrame(features_list)
    
    # Predict probability of solving
    probabilities = model.predict_proba(df)[:, 1]
    
    # Combine with problems and rank by probability descending
    # V2 Recommendation Logic: The "Learning Sweet Spot"
    # Instead of recommending the easiest problems (highest probability), 
    # we target problems with a ~60-70% success probability (challenging but solvable).
    # We also apply a bonus if the problem is EXACTLY 1 difficulty tier above their current tier.
    
    scored_problems = []
    for p, prob in zip(unsolved_problems, probabilities):
        diff_val = 1 if p.difficulty.value == "EASY" else (2 if p.difficulty.value == "MEDIUM" else 3)
        
        # 1. Target the 65% probability sweet spot for optimal learning
        probability_penalty = abs(0.65 - prob) 
        
        # 2. Topic / Growth Bonus (Pushing them to the next difficulty)
        growth_bonus = 0
        if diff_val == min(user_skill_tier + 1, 3):
            growth_bonus = 0.15  # Heavy bonus for "just a little bit more difficult"
            
        # Final ranking score (Higher is better)
        # We start with 1.0, subtract the distance from the perfect 65% probability, and add growth bonuses
        final_score = 1.0 - probability_penalty + growth_bonus
        scored_problems.append((p, final_score, prob))
        
    ranked_problems = sorted(scored_problems, key=lambda x: x[1], reverse=True)
    
    # Return top 3
    results = []
    for p, final_score, raw_prob in ranked_problems[:3]:
        results.append({
            "id": p.id,
            "title": p.title,
            "difficulty": p.difficulty.value,
            "match_score": float(round(final_score * 100, 1)), "win_probability": float(round(raw_prob * 100, 1))
        })
        
    return results

