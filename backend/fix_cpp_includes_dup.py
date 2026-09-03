with open('app/services/generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Clean up duplicate headers
content = re.sub(r'#include <unordered_map>\n#include <unordered_set>\n#include <map>\n#include <set>\n#include <algorithm>\n#include <queue>\n#include <stack>\n#include <cmath>\n#include <numeric>\n#include <unordered_map>', '#include <unordered_map>', content)

with open('app/services/generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
