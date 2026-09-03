import re

with open('app/api/users.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove execution_time_ms line completely
content = re.sub(r'\"execution_time_ms\":[^\n]*\n', '', content)

with open('app/api/users.py', 'w', encoding='utf-8') as f:
    f.write(content)
