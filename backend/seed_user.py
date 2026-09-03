import uuid
import bcrypt
from app.core.database import SessionLocal
from app.models.user import User, UserRole

db = SessionLocal()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

user = db.query(User).filter(User.email == 'user@example.com').first()
if not user:
    new_user = User(
        id=uuid.uuid4(),
        username='demo_user',
        email='user@example.com',
        password_hash=hash_password('user123'),
        role=UserRole.USER
    )
    db.add(new_user)
    db.commit()
    print('Normal Demo User created successfully.')
else:
    print('Normal User already exists.')
