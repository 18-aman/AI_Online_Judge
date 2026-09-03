from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase
from app.models.submission import Submission

db = SessionLocal()

db.query(Submission).delete()
db.query(TestCase).delete()
db.query(Problem).delete()

db.commit()
print('All problems, test cases, and submissions deleted.')
