from app.core.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text('ALTER TABLE problems ADD COLUMN signature_schema JSON;'))
    conn.commit()
print('Column added.')
