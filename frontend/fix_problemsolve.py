with open('src/pages/ProblemSolve.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the static BOILERPLATES
import re
content = re.sub(r'const BOILERPLATES.*?};', '', content, flags=re.DOTALL)

# Add import
content = content.replace('import Editor from "@monaco-editor/react";', 'import Editor from "@monaco-editor/react";\nimport { generateBoilerplate } from "../utils/boilerplateGenerator";')

# Update code setting logic
content = content.replace('setCode(BOILERPLATES[language]);', 'if (problem) setCode(generateBoilerplate(problem.signature_schema, language));')
content = content.replace('setCode(BOILERPLATES[e.target.value]);', 'if (problem) setCode(generateBoilerplate(problem.signature_schema, e.target.value));')
content = content.replace('setCode(BOILERPLATES["python"]);', 'setCode(generateBoilerplate(data.signature_schema, "python"));')

with open('src/pages/ProblemSolve.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
