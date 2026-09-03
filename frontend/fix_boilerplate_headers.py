with open('src/utils/boilerplateGenerator.ts', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Remove C++ headers
content = content.replace(
    'return "#include <vector>\\\\n#include <string>\\\\nusing namespace std;\\\\n\\\\nclass Solution {\\\\npublic:\\\\n    " + sig + " {\\\\n        \\\\n    }\\\\n};";',
    'return "class Solution {\\\\npublic:\\\\n    " + sig + " {\\\\n        \\\\n    }\\\\n};";'
)

# Remove Java headers
content = content.replace(
    'return "import java.util.*;\\\\n\\\\nclass Solution {\\\\n    " + sig + " {\\\\n        \\\\n    }\\\\n}";',
    'return "class Solution {\\\\n    " + sig + " {\\\\n        \\\\n    }\\\\n}";'
)

# Remove Python headers
content = content.replace(
    'return "from typing import List\\\\n\\\\nclass Solution:\\\\n    " + sig + "\\\\n        pass";',
    'return "class Solution:\\\\n    " + sig + "\\\\n        pass";'
)

with open('src/utils/boilerplateGenerator.ts', 'w', encoding='utf-8') as f:
    f.write(content)
