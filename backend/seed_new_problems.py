from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase, Difficulty
import uuid

db = SessionLocal()

problems = [
    {
        "title": "Valid Parentheses",
        "description": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n\n**Example 1:**\n```\nInput: s = \"()\"\nOutput: true\n```",
        "difficulty": Difficulty.EASY,
        "time_limit": 2.0,
        "memory_limit": 128.0,
        "testcases": [
            ("()", "true", False),
            ("()[]{}", "true", False),
            ("(]", "false", True)
        ]
    },
    {
        "title": "Contains Duplicate",
        "description": "Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.\n\n**Example 1:**\n```\nInput: nums = [1,2,3,1]\nOutput: true\n```",
        "difficulty": Difficulty.EASY,
        "time_limit": 2.0,
        "memory_limit": 128.0,
        "testcases": [
            ("[1, 2, 3, 1]", "true", False),
            ("[1, 2, 3, 4]", "false", False)
        ]
    }
]

for p_data in problems:
    if db.query(Problem).filter(Problem.title == p_data["title"]).first():
        continue
    p = Problem(
        id=uuid.uuid4(),
        title=p_data["title"],
        description=p_data["description"],
        difficulty=p_data["difficulty"],
        time_limit=p_data["time_limit"],
        memory_limit=p_data["memory_limit"]
    )
    db.add(p)
    db.commit()
    
    for inp, out, hidden in p_data["testcases"]:
        tc = TestCase(
            id=uuid.uuid4(),
            problem_id=p.id,
            input_data=inp,
            expected_output=out,
            is_hidden=hidden
        )
        db.add(tc)
    db.commit()

print("New problems seeded successfully!")

