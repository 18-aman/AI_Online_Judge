with open('app/schemas/problem.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'from typing import List, Optional',
    'from typing import List, Optional, Dict, Any'
)

content = content.replace(
    'class ProblemCreate(ProblemBase):\n    topic_ids: Optional[List[uuid.UUID]] = []',
    'class ProblemCreate(ProblemBase):\n    topic_ids: Optional[List[uuid.UUID]] = []\n    signature_schema: Optional[Dict[str, Any]] = None'
)

content = content.replace(
    'memory_limit: Optional[int] = None\n    topic_ids: Optional[List[uuid.UUID]] = None',
    'memory_limit: Optional[int] = None\n    topic_ids: Optional[List[uuid.UUID]] = None\n    signature_schema: Optional[Dict[str, Any]] = None'
)

content = content.replace(
    'user_status: Optional[str] = "TODO"\n\n    class Config:',
    'user_status: Optional[str] = "TODO"\n    signature_schema: Optional[Dict[str, Any]] = None\n\n    class Config:'
)

with open('app/schemas/problem.py', 'w', encoding='utf-8') as f:
    f.write(content)
