with open('app/api/users.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("from sqlalchemy.orm import Session", "from sqlalchemy.orm import Session\nfrom sqlalchemy import func")
content = content.replace("db.func.count", "func.count")

with open('app/api/users.py', 'w', encoding='utf-8') as f:
    f.write(content)
