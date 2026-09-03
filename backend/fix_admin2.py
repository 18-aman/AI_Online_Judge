with open('app/api/admin.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('for inp in request.inputs:', 'for idx, inp in enumerate(request.inputs):')

with open('app/api/admin.py', 'w', encoding='utf-8') as f:
    f.write(content)
