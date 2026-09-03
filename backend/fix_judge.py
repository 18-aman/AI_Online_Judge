with open('app/services/judge.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all the hardcoded generate_* wrappers with import
import re

# Find everything from def generate_python_wrapper to def run_code_in_docker
# and replace it.
new_imports = '''import docker
import tempfile
import os
import time
from typing import List, Dict, Any
from app.models.problem import TestCase
from app.services.generator import generate_executable_wrapper

DOCKER_IMAGES = {
    "python": "python:3.9-slim",
    "cpp": "gcc:latest",
    "java": "openjdk:17-slim"
}

def run_code_in_docker(language: str, code: str, test_cases: List[TestCase], time_limit: float, custom_checker_code: str = None, signature_schema: dict = None) -> Dict[str, Any]:
    client = docker.from_env()
    image = DOCKER_IMAGES.get(language)
    
    if not image:
        return {"status": "Error", "message": f"Unsupported language: {language}"}

    wrapped_code = generate_executable_wrapper(signature_schema, language, code)
'''

content = re.sub(r'import docker.*?def run_code_in_docker.*?wrapped_code = generate_wrapper\(language, code\)', new_imports, content, flags=re.DOTALL)

with open('app/services/judge.py', 'w', encoding='utf-8') as f:
    f.write(content)
