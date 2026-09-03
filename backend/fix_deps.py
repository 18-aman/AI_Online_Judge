import re

for filepath in ['app/api/users.py', 'app/api/admin.py']:
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    
    code = code.replace("from app.api.auth import get_current_user", "from app.api.deps import get_current_user")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
