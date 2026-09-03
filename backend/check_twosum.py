from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase

db = SessionLocal()
p = db.query(Problem).filter(Problem.title.ilike('%Two Sum%')).first()
if p:
    tcs = db.query(TestCase).filter(TestCase.problem_id == p.id).order_by(TestCase.id).all()
    for i, tc in enumerate(tcs[:5]):
        print(f"TC {i+1} Expected: {tc.expected_output!r}")
    print("...")
    for i, tc in enumerate(tcs[-2:]):
        print(f"TC {len(tcs)-1+i} Expected: {tc.expected_output!r}")
else:
    print("Problem not found.")
