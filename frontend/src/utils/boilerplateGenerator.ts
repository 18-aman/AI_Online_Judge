const TYPE_TRANSLATOR: Record<string, Record<string, string>> = {
    'integer': {'cpp': 'int', 'java': 'int', 'python': 'int'},
    'string': {'cpp': 'string', 'java': 'String', 'python': 'str'},
    'boolean': {'cpp': 'bool', 'java': 'boolean', 'python': 'bool'},
    'list<integer>': {'cpp': 'vector<int>', 'java': 'int[]', 'python': 'List[int]'},
    'list<string>': {'cpp': 'vector<string>', 'java': 'String[]', 'python': 'List[str]'},
};

export function generateBoilerplate(schema: any, language: string): string {
    if (!schema || !schema.function_name) {
        if (language === 'cpp') return 'class Solution {\npublic:\n    // TODO: Write your code here\n};';
        if (language === 'java') return 'class Solution {\n    // TODO: Write your code here\n}';
        return 'class Solution:\n    # TODO: Write your code here\n    pass';
    }

    const funcName = schema.function_name;
    const retType = schema.return_type || 'integer';
    const params = schema.parameters || [];

    const tRet = TYPE_TRANSLATOR[retType]?.[language] || 'void';
    
    const tParams: string[] = [];
    params.forEach((p: any) => {
        const pName = p.name || 'arg';
        const pType = TYPE_TRANSLATOR[p.type]?.[language] || 'int';
        
        if (language === 'cpp') {
            if (p.type && (p.type.startsWith('list') || p.type === 'string')) {
                tParams.push(pType + "& " + pName);
            } else {
                tParams.push(pType + " " + pName);
            }
        } else if (language === 'java') {
            tParams.push(pType + " " + pName);
        } else {
            tParams.push(pName + ": " + pType);
        }
    });

    if (language === 'cpp') {
        const sig = tRet + " " + funcName + "(" + tParams.join(', ') + ")";
        return "class Solution {\npublic:\n    " + sig + " {\n        \n    }\n};";
    } else if (language === 'java') {
        const sig = "public " + tRet + " " + funcName + "(" + tParams.join(', ') + ")";
        return "class Solution {\n    " + sig + " {\n        \n    }\n}";
    } else {
        const sig = "def " + funcName + "(self, " + tParams.join(', ') + ") -> " + tRet + ":";
        return "class Solution:\n    " + sig + "\n        pass";
    }
}
