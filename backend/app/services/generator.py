TYPE_TRANSLATOR = {
    'integer': {'cpp': 'int', 'java': 'int', 'python': 'int'},
    'string': {'cpp': 'string', 'java': 'String', 'python': 'str'},
    'boolean': {'cpp': 'bool', 'java': 'boolean', 'python': 'bool'},
    'list<integer>': {'cpp': 'vector<int>', 'java': 'int[]', 'python': 'List[int]'},
    'list<string>': {'cpp': 'vector<string>', 'java': 'String[]', 'python': 'List[str]'},
}

def generate_boilerplate(schema: dict, language: str) -> str:
    if not schema:
        # Fallback to empty class if no schema
        if language == 'cpp':
            return 'class Solution {\npublic:\n    // TODO: Write your code here\n};'
        elif language == 'java':
            return 'class Solution {\n    // TODO: Write your code here\n}'
        else:
            return 'class Solution:\n    # TODO: Write your code here\n    pass'
            
    func_name = schema.get('function_name', 'solve')
    ret_type = schema.get('return_type', 'integer')
    params = schema.get('parameters', [])
    
    # Translate return type
    t_ret = TYPE_TRANSLATOR.get(ret_type, {}).get(language, 'void')
    
    # Translate parameters
    t_params = []
    for p in params:
        p_name = p.get('name', 'arg')
        p_type = TYPE_TRANSLATOR.get(p.get('type'), {}).get(language, 'int')
        
        if language == 'cpp':
            if p.get('type', '').startswith('list') or p.get('type') == 'string':
                t_params.append(f"{p_type}& {p_name}")
            else:
                t_params.append(f"{p_type} {p_name}")
        elif language == 'java':
            t_params.append(f"{p_type} {p_name}")
        elif language == 'python':
            t_params.append(f"{p_name}: {p_type}")
            
    # Build signature
    if language == 'cpp':
        sig = f"{t_ret} {func_name}({', '.join(t_params)})"
        return f"#include <vector>\n#include <string>\nusing namespace std;\n\nclass Solution {{\npublic:\n    {sig} {{\n        \n    }}\n}};"
    elif language == 'java':
        sig = f"public {t_ret} {func_name}({', '.join(t_params)})"
        return f"import java.util.*;\n\nclass Solution {{\n    {sig} {{\n        \n    }}\n}}"
    else: # Python
        sig = f"def {func_name}(self, {', '.join(t_params)}) -> {t_ret}:"
        return f"from typing import List\n\nclass Solution:\n    {sig}\n        pass"

def generate_executable_wrapper(schema: dict, language: str, user_code: str) -> str:
    # This generates the full code string sent to Docker
    if not schema:
        return user_code

    func_name = schema.get('function_name', 'solve')
    params = schema.get('parameters', [])
    ret_type = schema.get('return_type', 'integer')
    
    if language == 'python':
        return _gen_python_exec(func_name, params, ret_type, user_code)
    elif language == 'cpp':
        return _gen_cpp_exec(func_name, params, ret_type, user_code)
    elif language == 'java':
        return _gen_java_exec(func_name, params, ret_type, user_code)
    return user_code

def _gen_python_exec(func_name, params, ret_type, user_code):
    lines = [
        "import sys, json, math, collections, itertools, heapq, re, bisect\nfrom typing import *",
        user_code,
        "if __name__ == '__main__':",
        "    try:",
        "        obj = Solution()"
    ]
    
    invoke_args = []
    for i, p in enumerate(params):
        ptype = p.get('type')
        lines.append(f"        line_{i} = sys.stdin.readline().strip()")
        if ptype in ['integer', 'boolean', 'list<integer>', 'list<string>']:
            lines.append(f"        arg_{i} = json.loads(line_{i})")
        else: # string
            lines.append(f"        arg_{i} = line_{i}") # Or json.loads if quoted
        invoke_args.append(f"arg_{i}")
        
    lines.append(f"        res = obj.{func_name}({', '.join(invoke_args)})")
    
    # Print result
    if ret_type == 'boolean':
        lines.append("        print(str(res).lower())")
    else:
        lines.append("        print(json.dumps(res).replace(' ', ''))")
    
    lines.append("    except Exception as e:")
    lines.append("        print(e)")
    return "\n".join(lines)

def _gen_cpp_exec(func_name, params, ret_type, user_code):
    # C++ boilerplate with simple parsers
    return f"""
#include <iostream>
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
#include <numeric>
using namespace std;

// Quick parsers
vector<int> parseVectorInt(string s) {{
    vector<int> res;
    if(s.length() < 2) return res;
    s = s.substr(1, s.length()-2);
    stringstream ss(s);
    string item;
    while(getline(ss, item, ',')) {{
        res.push_back(stoi(item));
    }}
    return res;
}}

vector<string> parseVectorString(string s) {{
    vector<string> res;
    if(s.length() < 2) return res;
    s = s.substr(1, s.length()-2);
    stringstream ss(s);
    string item;
    // VERY simplified parsing for MVP (assumes no commas inside strings)
    while(getline(ss, item, ',')) {{
        if(item.length() >= 2 && item[0] == '"') item = item.substr(1, item.length()-2);
        res.push_back(item);
    }}
    return res;
}}

{user_code}

int main() {{
    Solution obj;
    // Read and parse each argument (Simplified MVP implementation)
    // Actually, to make it robust, we would inject exact reading blocks here based on params.
    // For now, let's keep it simple.
    
    // In a real system, we iterate through params.
    // I will write this out dynamically in the python builder:
""" + _gen_cpp_main_body(func_name, params, ret_type) + """
} 
"""

def _gen_cpp_main_body(func_name, params, ret_type):
    lines = []
    invoke_args = []
    for i, p in enumerate(params):
        ptype = p.get('type')
        lines.append(f"    string line_{i};")
        lines.append(f"    getline(cin, line_{i});")
        if ptype == 'integer':
            lines.append(f"    int arg_{i} = stoi(line_{i});")
        elif ptype == 'list<integer>':
            lines.append(f"    vector<int> arg_{i} = parseVectorInt(line_{i});")
        elif ptype == 'string':
            lines.append(f"    string arg_{i} = line_{i};")
        elif ptype == 'boolean':
            lines.append(f"    bool arg_{i} = (line_{i} == \"true\" || line_{i} == \"1\");")
        elif ptype == 'list<string>':
            lines.append(f"    vector<string> arg_{i} = parseVectorString(line_{i});")
        invoke_args.append(f"arg_{i}")
        
    lines.append(f"    auto res = obj.{func_name}({', '.join(invoke_args)});")
    
    # Print logic
    if ret_type == 'list<integer>' or ret_type == 'list<string>':
        lines.append("    cout << \"[\";")
        lines.append("    for(size_t i=0; i<res.size(); ++i) {")
        lines.append("        cout << res[i] << (i==res.size()-1 ? \"\" : \",\");")
        lines.append("    }")
        lines.append("    cout << \"]\" << endl;")
    elif ret_type == 'boolean':
        lines.append("    cout << (res ? \"true\" : \"false\") << endl;")
    else:
        lines.append("    cout << res << endl;")
        
    return "\n".join(lines)

def _gen_java_exec(func_name, params, ret_type, user_code):
    return f"""
import java.util.*;
import java.io.*;

{user_code}

public class Main {{
    public static int[] parseArrayInt(String s) {{
        if(s.length() < 2) return new int[0];
        s = s.substring(1, s.length() - 1);
        if(s.isEmpty()) return new int[0];
        String[] parts = s.split(",");
        int[] res = new int[parts.length];
        for(int i=0; i<parts.length; i++) {{
            res[i] = Integer.parseInt(parts[i].trim());
        }}
        return res;
    }}
    
    public static void main(String[] args) throws Exception {{
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        Solution obj = new Solution();
""" + _gen_java_main_body(func_name, params, ret_type) + """
    }
}
"""

def _gen_java_main_body(func_name, params, ret_type):
    lines = []
    invoke_args = []
    for i, p in enumerate(params):
        ptype = p.get('type')
        lines.append(f"        String line_{i} = br.readLine();")
        if ptype == 'integer':
            lines.append(f"        int arg_{i} = Integer.parseInt(line_{i}.trim());")
        elif ptype == 'list<integer>':
            lines.append(f"        int[] arg_{i} = parseArrayInt(line_{i});")
        elif ptype == 'string':
            lines.append(f"        String arg_{i} = line_{i};")
        elif ptype == 'boolean':
            lines.append(f"        boolean arg_{i} = Boolean.parseBoolean(line_{i}.trim());")
        invoke_args.append(f"arg_{i}")
        
    lines.append(f"        var res = obj.{func_name}({', '.join(invoke_args)});")
    
    # Print logic
    if ret_type == 'list<integer>':
        lines.append("        System.out.print(\"[\");")
        lines.append("        for(int i=0; i<res.length; i++) {")
        lines.append("            System.out.print(res[i] + (i==res.length-1 ? \"\" : \",\"));")
        lines.append("        }")
        lines.append("        System.out.println(\"]\");")
    else:
        lines.append("        System.out.println(res);")
        
    return "\n".join(lines)
