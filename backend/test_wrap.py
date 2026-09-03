from app.services.generator import generate_executable_wrapper

schema = {
    "function_name": "mergeAlternately",
    "return_type": "string",
    "parameters": [
        {"name": "word1", "type": "string"},
        {"name": "word2", "type": "string"}
    ]
}

user_code = '''class Solution {
public:
    string mergeAlternately(string& word1, string& word2) {
        return "";
    }
};'''

wrapped = generate_executable_wrapper(schema, "cpp", user_code)
print("--- START ---")
print(wrapped)
print("--- END ---")
