with open('src/utils/boilerplateGenerator.ts', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Remove C++ headers
content = re.sub(r'return "#include <vector>\\\\n#include <string>\\\\nusing namespace std;\\\\n\\\\nclass Solution', 'return "class Solution', content)

# Remove Java headers
content = re.sub(r'return "import java\.util\.\*;\\\\n\\\\nclass Solution', 'return "class Solution', content)

# Remove Python headers
content = re.sub(r'return "from typing import List\\\\n\\\\nclass Solution:', 'return "class Solution:', content)

with open('src/utils/boilerplateGenerator.ts', 'w', encoding='utf-8') as f:
    f.write(content)
