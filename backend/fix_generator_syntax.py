with open('app/services/generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(r'\}[\s]*\"\"\"[\s]*\"\"\"', '} \n\"\"\"', content)

with open('app/services/generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
