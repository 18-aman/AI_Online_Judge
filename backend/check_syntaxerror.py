from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase

db = SessionLocal()
tcs = db.query(TestCase).filter(TestCase.expected_output.ilike('%SyntaxError%')).all()
for tc in tcs:
    print(f"Problem ID: {tc.problem_id}, TC ID: {tc.id}, Expected: {tc.expected_output!r}")
