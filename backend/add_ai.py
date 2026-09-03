import os

filepath = 'app/services/ai_mentor.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_functions = '''
def get_code_explanation(user_code: str, language: str) -> str:
    GROQ_API_KEY = settings.GROQ_API_KEY
    if not GROQ_API_KEY:
        return "Groq API Key missing."
    client = Groq(api_key=GROQ_API_KEY)
    system_prompt = (
        "You are an expert coding instructor. Explain the provided code step-by-step. "
        "Break down the logic clearly so a beginner can understand it. Use bullet points."
    )
    user_prompt = f"User Code ({language}):\n{user_code}"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.3,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting AI: {str(e)}"

def get_code_debug(user_code: str, language: str, error_message: str = "") -> str:
    GROQ_API_KEY = settings.GROQ_API_KEY
    if not GROQ_API_KEY:
        return "Groq API Key missing."
    client = Groq(api_key=GROQ_API_KEY)
    system_prompt = (
        "You are an expert debugger. Find the logical flaws or bugs in the provided code. "
        "Explain WHY it fails and HOW to fix it, but DO NOT provide the complete rewritten code."
    )
    user_prompt = f"User Code ({language}):\n{user_code}\n\nError/Context:\n{error_message}"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.3,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting AI: {str(e)}"
'''

if "def get_code_explanation" not in content:
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write("\n" + new_functions)
