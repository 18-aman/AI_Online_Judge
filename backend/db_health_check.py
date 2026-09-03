from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase

db = SessionLocal()
probs = db.query(Problem).all()

print(f"Total problems: {len(probs)}")
for p in probs:
    print(f"\nProblem: {p.title} (ID: {p.id})")
    print(f"  Schema: {p.signature_schema}")
    tcs = db.query(TestCase).filter(TestCase.problem_id == p.id).all()
    print(f"  Total Test Cases: {len(tcs)}")
    bad_tcs = []
    for tc in tcs:
        if tc.expected_output and ('SyntaxError' in tc.expected_output or 'NameError' in tc.expected_output or 'Exception' in tc.expected_output or 'File "/app' in tc.expected_output):
            bad_tcs.append(tc.id)
    if bad_tcs:
        print(f"  [!] FOUND {len(bad_tcs)} CORRUPTED TEST CASES")
    else:
        print("  Test cases look clean.")
