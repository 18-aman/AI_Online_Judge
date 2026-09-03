from app.core.database import SessionLocal
from app.models.problem import Problem

db = SessionLocal()
p = db.query(Problem).filter(Problem.title.ilike('%Merge Strings Alternately%')).first()
if p:
    p.signature_schema = {
        "function_name": "mergeAlternately",
        "return_type": "string",
        "parameters": [
            {"name": "word1", "type": "string"},
            {"name": "word2", "type": "string"}
        ]
    }
    db.commit()
    print("Fixed the schema for existing problem.")
else:
    print("Problem not found.")
