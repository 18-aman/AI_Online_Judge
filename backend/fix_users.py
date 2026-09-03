import json
with open('app/api/users.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix types in users.py
content = content.replace('"attempted": attempted,', '"attempted": int(attempted),')
content = content.replace('"solved": solved', '"solved": int(solved)')
content = content.replace('"solved": t[1]', '"solved": int(t[1])')
content = content.replace('"execution_time_ms": sub.execution_time_ms,', '"execution_time_ms": float(sub.execution_time_ms) if sub.execution_time_ms is not None else None,')

with open('app/api/users.py', 'w', encoding='utf-8') as f:
    f.write(content)
