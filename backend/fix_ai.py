with open('app/services/ai_mentor.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('user_prompt = f"User Code ({language}):\n{user_code}"', 'user_prompt = f"User Code ({language}):\\n{user_code}"')
# If there are any literal newlines inside the f-string, we replace them.
import re
content = re.sub(r'f"User Code \(\{language\}\):\n\{user_code\}"', r'f"User Code ({language}):\\n{user_code}"', content)

with open('app/services/ai_mentor.py', 'w', encoding='utf-8') as f:
    f.write(content)
