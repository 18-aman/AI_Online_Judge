from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase
import random

db = SessionLocal()

# Two Sum - O(N^2) should fail, O(N) should pass
p_two_sum = db.query(Problem).filter(Problem.title == 'Two Sum').first()
if p_two_sum:
    # 10,000 elements
    arr = list(range(1, 10001))
    target = arr[0] + arr[-1]
    input_data = f"[{','.join(map(str, arr))}]\n{target}"
    expected_out = "[0,9999]"
    tc = TestCase(problem_id=p_two_sum.id, input_data=input_data, expected_output=expected_out, is_hidden=True)
    db.add(tc)

# Contains Duplicate - O(N^2) should fail, O(N) should pass
p_contains_dup = db.query(Problem).filter(Problem.title == 'Contains Duplicate').first()
if p_contains_dup:
    # 50,000 unique elements + 1 duplicate at the very end
    arr = list(range(1, 50001))
    arr.append(50000)
    input_data = f"[{','.join(map(str, arr))}]"
    expected_out = "true"
    tc = TestCase(problem_id=p_contains_dup.id, input_data=input_data, expected_output=expected_out, is_hidden=True)
    db.add(tc)

# Maximum Subarray - O(N^2) should fail, O(N) should pass
p_max_sub = db.query(Problem).filter(Problem.title == 'Maximum Subarray').first()
if p_max_sub:
    # 50,000 elements alternating pos/neg
    arr = [1 if i % 2 == 0 else -1 for i in range(50000)]
    input_data = f"[{','.join(map(str, arr))}]"
    expected_out = "1"
    tc = TestCase(problem_id=p_max_sub.id, input_data=input_data, expected_output=expected_out, is_hidden=True)
    db.add(tc)

db.commit()
print('Added huge test cases successfully!')
