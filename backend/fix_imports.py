import re

# Fix users.py
with open('app/api/users.py', 'r', encoding='utf-8') as f:
    users_code = f.read()

users_code = users_code.replace("from app.database import get_db", "from app.core.database import get_db")
users_code = users_code.replace("from app.models import User, Submission, Problem, ProblemTopic, Topic", "from app.models.user import User\nfrom app.models.submission import Submission\nfrom app.models.problem import Problem, Topic, ProblemTopic")

with open('app/api/users.py', 'w', encoding='utf-8') as f:
    f.write(users_code)

# Fix admin.py
with open('app/api/admin.py', 'r', encoding='utf-8') as f:
    admin_code = f.read()

admin_code = admin_code.replace("from app.models import User, Submission, ProblemTopic, Topic", "from app.models.user import User\nfrom app.models.submission import Submission\nfrom app.models.problem import Problem, Topic, ProblemTopic")
admin_code = admin_code.replace("from app.database import get_db", "from app.core.database import get_db")

with open('app/api/admin.py', 'w', encoding='utf-8') as f:
    f.write(admin_code)
