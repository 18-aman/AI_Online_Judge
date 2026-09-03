from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase

db = SessionLocal()
problems = db.query(Problem).all()

for problem in problems:
    test_cases = db.query(TestCase).filter(TestCase.problem_id == problem.id).order_by(TestCase.id).all()
    for idx, tc in enumerate(test_cases):
        if idx < 2:
            tc.is_hidden = False
        else:
            tc.is_hidden = True

db.commit()
print('Test cases updated successfully!')
