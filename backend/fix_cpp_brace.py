with open('app/services/generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('""" + _gen_cpp_main_body(func_name, params, ret_type) + """\n}}', '""" + _gen_cpp_main_body(func_name, params, ret_type) + """\n}\n"""')

with open('app/services/generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
