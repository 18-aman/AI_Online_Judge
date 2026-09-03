from app.core.database import engine
from sqlalchemy import text

with engine.begin() as conn:
    try:
        conn.execute(text("ALTER TABLE problems ADD COLUMN has_custom_checker BOOLEAN DEFAULT FALSE;"))
        print("Added has_custom_checker column.")
    except Exception as e:
        print(f"Column has_custom_checker might already exist: {e}")
        
    try:
        conn.execute(text("ALTER TABLE problems ADD COLUMN checker_code TEXT;"))
        print("Added checker_code column.")
    except Exception as e:
        print(f"Column checker_code might already exist: {e}")
