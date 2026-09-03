with open('app/services/generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Replace the double braces at the end of the Java generator string
content = content.replace(
    '""" + _gen_java_main_body(func_name, params, ret_type) + """\n    }}\n}}\n"""',
    '""" + _gen_java_main_body(func_name, params, ret_type) + """\n    }\n}\n"""'
)

with open('app/services/generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
