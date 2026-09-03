with open('src/pages/ProblemSolve.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(r'const DEFAULT_BOILERPLATES = \{.*?\};', '', content, flags=re.DOTALL)
content = re.sub(r'const PROBLEM_BOILERPLATES.*?};', '', content, flags=re.DOTALL)

content = content.replace('const [code, setCode] = useState(DEFAULT_BOILERPLATES["python"]);', 'const [code, setCode] = useState("");')

content = content.replace(
    '''        const templates = PROBLEM_BOILERPLATES[data.title] || DEFAULT_BOILERPLATES;\n        setCode(templates[language] || DEFAULT_BOILERPLATES[language]);''',
    '''        setCode(generateBoilerplate(data.signature_schema, language));'''
)

content = content.replace(
    '''              if (problem) {\n                const templates = PROBLEM_BOILERPLATES[problem.title] || DEFAULT_BOILERPLATES;\n                setCode(templates[newLang] || DEFAULT_BOILERPLATES[newLang]);\n              }''',
    '''              if (problem) {\n                setCode(generateBoilerplate(problem.signature_schema, newLang));\n              }'''
)

with open('src/pages/ProblemSolve.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
