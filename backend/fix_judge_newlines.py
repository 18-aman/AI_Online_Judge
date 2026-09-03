with open('app/services/judge.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'with open(file_path, "w") as f:',
    'with open(file_path, "w", newline="\\n", encoding="utf-8") as f:'
)

content = content.replace(
    'with open(input_file_path, "w") as f:',
    'with open(input_file_path, "w", newline="\\n", encoding="utf-8") as f:'
)

with open('app/services/judge.py', 'w', encoding='utf-8') as f:
    f.write(content)
