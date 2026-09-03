with open('app/api/admin.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Add signature_schema to CreateProblemRequest
content = content.replace(
    'memory_limit: int = 256',
    'memory_limit: int = 256\n    signature_schema: dict = None'
)

# Pass signature_schema when instantiating Problem
content = content.replace(
    'memory_limit=request.memory_limit\n    )',
    'memory_limit=request.memory_limit,\n        signature_schema=request.signature_schema\n    )'
)

with open('app/api/admin.py', 'w', encoding='utf-8') as f:
    f.write(content)
