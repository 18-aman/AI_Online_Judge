from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase
from app.services.judge import run_code_in_docker
import json

db = SessionLocal()
p = db.query(Problem).filter(Problem.title.ilike('%Two Sum%')).first()

reference_solution = '''
def twoSum(self, nums, target):
    numMap = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in numMap:
            return [numMap[complement], i]
        numMap[num] = i
    return []
'''

tcs = db.query(TestCase).filter(TestCase.problem_id == p.id).order_by(TestCase.id).all()

results = run_code_in_docker(
    language='python',
    code=reference_solution,
    test_cases=tcs,
    time_limit=10.0,
    custom_checker_code=None,
    signature_schema=p.signature_schema
)

for i, res in enumerate(results['test_cases']):
    if res['status'] == 'Accepted' or res['status'] == 'Wrong Answer':
        # the output is what the reference solution produced
        tcs[i].expected_output = res['output']
        db.add(tcs[i])
        print(f"Updated TC {i+1} expected output to {res['output']}")

db.commit()
print("Database updated!")
