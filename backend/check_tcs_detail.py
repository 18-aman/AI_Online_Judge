from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase

db = SessionLocal()
problems = db.query(Problem).all()

for p in problems:
    tcs = db.query(TestCase).filter(TestCase.problem_id == p.id).all()
    print(f"\n--- {p.title} ({p.time_limit}s) ---")
    for tc in tcs:
        in_data = tc.input_data
        if len(in_data) > 50:
            in_data = in_data[:50] + "... (len " + str(len(tc.input_data)) + ")"
        print(f"  Input: {in_data}")
