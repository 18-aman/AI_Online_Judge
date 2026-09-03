from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase

db = SessionLocal()
p = db.query(Problem).filter(Problem.title.ilike('%Merge Strings Alternately%')).first()
if p:
    # Delete old bad testcases
    db.query(TestCase).filter(TestCase.problem_id == p.id).delete()
    
    tcs = [
        ("abc\npqr", "apbqcr", False),
        ("ab\npqrs", "apbqrs", False),
        ("abcd\npq", "apbqcd", True)
    ]
    
    for inp, out, h in tcs:
        db.add(TestCase(problem_id=p.id, input_data=inp, expected_output=out, is_hidden=h))
        
    db.commit()
    print("Testcases fixed!")
