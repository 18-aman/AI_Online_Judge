import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey, Boolean, DateTime, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class Difficulty(str, enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class Topic(Base):
    __tablename__ = "topics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)

class ProblemTopic(Base):
    __tablename__ = "problem_topics"
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id", ondelete="CASCADE"), primary_key=True)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True)

class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(Enum(Difficulty), nullable=False)
    time_limit = Column(Float, default=1.0) # In seconds
    memory_limit = Column(Integer, default=256) # In MB
    signature_schema = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Custom Checker / Special Judge
    has_custom_checker = Column(Boolean, default=False)
    checker_code = Column(Text, nullable=True)
    
    # Relationships
    test_cases = relationship("TestCase", back_populates="problem", cascade="all, delete-orphan")
    topics = relationship("Topic", secondary="problem_topics", backref="problems")

class TestCase(Base):
    __tablename__ = "test_cases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_hidden = Column(Boolean, default=False)
    
    problem = relationship("Problem", back_populates="test_cases")
