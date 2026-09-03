from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase

db = SessionLocal()
probs = db.query(Problem).filter(Problem.title.ilike('%Two Sum%')).all()
for p in probs:
    print(f"Problem: {p.title} (ID: {p.id})")
    tcs = db.query(TestCase).filter(TestCase.problem_id == p.id).order_by(TestCase.id).all()
    if tcs:
        print(f"  TC1 Expected: {tcs[0].expected_output!r}")
