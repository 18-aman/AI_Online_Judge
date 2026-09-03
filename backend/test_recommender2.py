from app.core.database import SessionLocal
from app.models.user import User
from app.api.recommendations import get_recommendations

db = SessionLocal()
user = db.query(User).first()

try:
    print(get_recommendations(db=db, current_user=user))
except Exception as e:
    print("ERROR:", str(e))
