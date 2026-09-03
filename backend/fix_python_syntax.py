with open('app/services/generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '        "import sys, json, math, collections, itertools, heapq, re, bisect\nfrom typing import *",',
    '        "import sys, json, math, collections, itertools, heapq, re, bisect\\nfrom typing import *",'
)

with open('app/services/generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
