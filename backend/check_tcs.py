from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase

db = SessionLocal()
p = db.query(Problem).filter(Problem.title.ilike('%Merge Strings Alternately%')).first()
if p:
    tcs = db.query(TestCase).filter(TestCase.problem_id == p.id).all()
    for tc in tcs:
        print(f"Input: {tc.input_data!r} -> Output: {tc.expected_output!r}")
else:
    print("Problem not found.")
