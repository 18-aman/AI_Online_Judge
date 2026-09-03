import re
with open('src/pages/ProblemSolve.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix the last corrupted header
code = re.sub(r'\"\"Authorization\": Bearer \{token\}\', r'\"Authorization\": Bearer ', code)

with open('src/pages/ProblemSolve.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
