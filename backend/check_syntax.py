import ast
with open('app/services/generator.py', 'r', encoding='utf-8') as f:
    source = f.read()

try:
    ast.parse(source)
    print("Syntax is OK")
except SyntaxError as e:
    print(f"SyntaxError: {e}")
