import re

filepath = 'app/main.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

if "from app.api import users" not in content:
    content = content.replace("from app.api import auth, problems, leaderboard, admin", "from app.api import auth, problems, leaderboard, admin, users")
    content = content.replace("app.include_router(admin.router)", "app.include_router(admin.router)\napp.include_router(users.router)")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
