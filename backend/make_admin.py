from app.core.database import SessionLocal
from app.models.user import User, UserRole
import sys

def make_admin(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        print(f"User with email {email} not found.")
        return
    user.role = UserRole.ADMIN
    db.commit()
    print(f"User {email} is now an ADMIN!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_admin.py <email>")
    else:
        make_admin(sys.argv[1])
