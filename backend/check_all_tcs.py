from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase

db = SessionLocal()
tcs = db.query(TestCase).filter(TestCase.problem_id == '3d97e2d4-b275-4837-b92f-747dd87b3556').order_by(TestCase.id).all()
for i, tc in enumerate(tcs):
    print(f"TC {i+1} [Hidden={tc.is_hidden}]: Expected: {tc.expected_output!r}")
