import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True) # Optional for now
    
    language = Column(String, nullable=False)
    code = Column(Text, nullable=False)
    
    status = Column(String, default="PENDING") # PENDING, RUNNING, COMPLETED, FAILED
    verdict = Column(String, nullable=True) # Accepted, Wrong Answer, etc.
    results = Column(JSON, nullable=True) # Detailed test case results
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    problem = relationship("Problem")
