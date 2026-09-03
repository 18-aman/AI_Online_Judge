with open('app/api/admin.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'result = run_code_in_docker(request.language, request.reference_code, mock_test_cases, time_limit=5.0)',
    'result = run_code_in_docker(request.language, request.reference_code, mock_test_cases, time_limit=5.0, signature_schema=problem.signature_schema)'
)

with open('app/api/admin.py', 'w', encoding='utf-8') as f:
    f.write(content)
