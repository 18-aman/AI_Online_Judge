import uuid
import bcrypt
from app.core.database import SessionLocal
from app.models.user import User, UserRole

db = SessionLocal()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

admin = db.query(User).filter(User.email == 'admin@example.com').first()
if not admin:
    print('Admin not found. Creating...')
    admin = User(
        id=uuid.uuid4(),
        username='admin',
        email='admin@example.com',
        password_hash=hash_password('admin123'),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    print('Admin created successfully.')
else:
    print('Admin already exists. Updating password...')
    admin.password_hash = hash_password('admin123')
    admin.role = UserRole.ADMIN
    db.commit()
    print('Admin updated successfully.')
