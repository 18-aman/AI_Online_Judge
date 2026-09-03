import os

filepath = 'app/api/problems.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("from app.services.ai_mentor import get_mentor_hint, get_code_review, get_complexity_analysis", "from app.services.ai_mentor import get_mentor_hint, get_code_review, get_complexity_analysis, get_code_explanation, get_code_debug")

new_endpoints = '''
@router.post("/{problem_id}/explain")
def explain_code(problem_id: uuid.UUID, request: AIActionRequest, db: Session = Depends(get_db)):
    explanation = get_code_explanation(request.code, request.language)
    return {"message": explanation}

@router.post("/{problem_id}/debug")
def debug_code(problem_id: uuid.UUID, request: AIActionRequest, db: Session = Depends(get_db)):
    debug_info = get_code_debug(request.code, request.language)
    return {"message": debug_info}
'''

if "def explain_code" not in content:
    content += "\n" + new_endpoints
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
