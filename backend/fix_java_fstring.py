with open('app/services/generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'def _gen_java_exec(func_name, params, ret_type, user_code):\n    return """\nimport java.util.*;',
    'def _gen_java_exec(func_name, params, ret_type, user_code):\n    return f"""\nimport java.util.*;'
)

with open('app/services/generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
