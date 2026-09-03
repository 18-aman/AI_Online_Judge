from groq import Groq
from app.core.config import settings

def get_mentor_hint(problem_title: str, problem_description: str, user_code: str, language: str) -> str:
    GROQ_API_KEY = settings.GROQ_API_KEY
    if not GROQ_API_KEY:
        return "Groq API Key is missing. Please configure GROQ_API_KEY in the backend."
    client = Groq(api_key=GROQ_API_KEY)
    system_prompt = (
        "You are an elite Socratic AI Coding Mentor for a competitive programming platform. "
        "Your goal is to guide the user to the solution ONE tiny step at a time. "
        "CRITICAL RULES: "
        "1. NEVER reveal the full algorithm (e.g., do not just say 'sort it and use two pointers'). "
        "2. Give exactly ONE small conceptual hint based on their current progress. "
        "3. Keep your response to a single short sentence or a thought-provoking question. "
        "4. If the code is already perfect, just say 'Your logic looks solid, try submitting!'"
    )
    user_prompt = f"Problem: {problem_title}\nDescription: {problem_description}\nUser Code ({language}):\n{user_code}\n\nWhat is the next hint?"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.3,
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting AI Mentor: {str(e)}"

def get_code_review(problem_title: str, user_code: str, language: str) -> str:
    GROQ_API_KEY = settings.GROQ_API_KEY
    if not GROQ_API_KEY:
        return "Groq API Key missing."
    client = Groq(api_key=GROQ_API_KEY)
    system_prompt = (
        "You are an expert Principal Engineer doing a Code Review. "
        "Review the provided code. Point out bad practices, variable naming issues, bugs, and edge cases. "
        "Use bullet points. Be brutal but constructive. DO NOT provide the fully solved code."
    )
    user_prompt = f"Problem: {problem_title}\nUser Code ({language}):\n{user_code}"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting AI: {str(e)}"

def get_complexity_analysis(user_code: str, language: str) -> str:
    GROQ_API_KEY = settings.GROQ_API_KEY
    if not GROQ_API_KEY:
        return "Groq API Key missing."
    client = Groq(api_key=GROQ_API_KEY)
    system_prompt = (
        "You are an algorithm analysis bot. "
        "Calculate the Big-O Time Complexity and Space Complexity of the user's code. "
        "Respond strictly in this format:\n\n**Time Complexity**: O(...)\n*Reason*: ...\n\n**Space Complexity**: O(...)\n*Reason*: ..."
    )
    user_prompt = f"User Code ({language}):\n{user_code}"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.1,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting AI: {str(e)}"




def get_code_explanation(user_code: str, language: str) -> str:
    GROQ_API_KEY = settings.GROQ_API_KEY
    if not GROQ_API_KEY:
        return "Groq API Key missing."
    client = Groq(api_key=GROQ_API_KEY)
    system_prompt = (
        "You are an expert coding instructor. Explain the provided code step-by-step."
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

def get_code_debug(user_code: str, language: str) -> str:
    GROQ_API_KEY = settings.GROQ_API_KEY
    if not GROQ_API_KEY:
        return "Groq API Key missing."
    client = Groq(api_key=GROQ_API_KEY)
    system_prompt = (
        "You are an expert debugger. Find the logical flaws or bugs in the provided code."
        "Explain WHY it fails and HOW to fix it, but DO NOT provide the complete rewritten code."
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
