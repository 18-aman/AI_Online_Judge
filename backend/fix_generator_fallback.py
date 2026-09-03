with open('app/services/generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(r'    if not schema:\n        # Fallback if somehow there\'s no schema\n        from app.services.judge import generate_wrapper\n        return generate_wrapper\(language, user_code\)', '    if not schema:\n        return user_code', content)

with open('app/services/generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
