from app.core.database import SessionLocal
from app.models.problem import Problem

db = SessionLocal()
p = db.query(Problem).filter(Problem.title == 'Merge Strings Alternately').first()
if p:
    print("Schema in DB:", p.signature_schema)
else:
    print("Problem not found.")
