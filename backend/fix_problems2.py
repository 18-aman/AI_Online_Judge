with open('app/api/problems.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'custom_checker_code=problem.checker_code\n    )',
    'custom_checker_code=problem.checker_code,\n        signature_schema=problem.signature_schema\n    )'
)

with open('app/api/problems.py', 'w', encoding='utf-8') as f:
    f.write(content)
