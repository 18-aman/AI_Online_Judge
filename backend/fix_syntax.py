with open('app/services/generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('f\\\"\\\"\\\"', 'f\"\"\"')
content = content.replace('\\\"\\\"\\\"', '\"\"\"')

with open('app/services/generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
