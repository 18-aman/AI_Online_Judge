from app.core.database import SessionLocal
from app.models.problem import Problem
import uuid

db = SessionLocal()

new_problem = Problem(
    id=uuid.uuid4(),
    title="Two Sum",
    description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.",
    difficulty="EASY",
    time_limit=1.0,
    memory_limit=256.0
)

db.add(new_problem)
db.commit()
print('Created fresh problem: Two Sum')
