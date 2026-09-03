with open('src/pages/ProblemSolve.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "const DEFAULT_BOILERPLATES" in line:
        skip = True
    
    if "export default function ProblemSolve()" in line:
        skip = False
        
    if not skip:
        new_lines.append(line)

with open('src/pages/ProblemSolve.tsx', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
