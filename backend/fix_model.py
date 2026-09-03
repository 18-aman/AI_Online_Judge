with open('app/models/problem.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey, Boolean, DateTime, Enum',
    'from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey, Boolean, DateTime, Enum, JSON'
)

content = content.replace(
    'memory_limit = Column(Integer, default=256) # In MB\n    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))',
    'memory_limit = Column(Integer, default=256) # In MB\n    signature_schema = Column(JSON, nullable=True)\n    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))'
)

with open('app/models/problem.py', 'w', encoding='utf-8') as f:
    f.write(content)
