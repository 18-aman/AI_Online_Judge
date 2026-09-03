with open('app/services/generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_headers = '''#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <map>
#include <set>
#include <algorithm>
#include <queue>
#include <stack>
#include <cmath>
#include <numeric>'''

# Replace the exact block
content = content.replace(
    '#include <iostream>\n#include <vector>\n#include <string>\n#include <sstream>',
    new_headers
)

with open('app/services/generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
