with open('app/worker.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'custom_checker_code=problem.checker_code if problem.has_custom_checker else None',
    'custom_checker_code=problem.checker_code if problem.has_custom_checker else None,\n            signature_schema=problem.signature_schema'
)

with open('app/worker.py', 'w', encoding='utf-8') as f:
    f.write(content)
