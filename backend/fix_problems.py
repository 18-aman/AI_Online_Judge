with open('app/api/problems.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'time_limit=problem.time_limit\n    )',
    'time_limit=problem.time_limit,\n        signature_schema=problem.signature_schema\n    )'
)

with open('app/api/problems.py', 'w', encoding='utf-8') as f:
    f.write(content)
