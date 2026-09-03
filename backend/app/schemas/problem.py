import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.models.problem import Difficulty

# --- Topic Schemas ---
class TopicBase(BaseModel):
    name: str

class TopicCreate(TopicBase):
    pass

class TopicResponse(TopicBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

# --- TestCase Schemas ---
class TestCaseBase(BaseModel):
    input_data: str
    expected_output: str
    is_hidden: bool = False

class TestCaseCreate(TestCaseBase):
    pass

class TestCaseResponse(TestCaseBase):
    id: uuid.UUID
    problem_id: uuid.UUID

    class Config:
        from_attributes = True

# --- Problem Schemas ---
class ProblemBase(BaseModel):
    title: str
    description: str
    difficulty: Difficulty
    time_limit: float = 1.0
    memory_limit: int = 256

class ProblemCreate(ProblemBase):
    topic_ids: Optional[List[uuid.UUID]] = []
    signature_schema: Optional[Dict[str, Any]] = None

class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[Difficulty] = None
    time_limit: Optional[float] = None
    memory_limit: Optional[int] = None
    topic_ids: Optional[List[uuid.UUID]] = None
    signature_schema: Optional[Dict[str, Any]] = None

class ProblemResponse(ProblemBase):
    id: uuid.UUID
    created_at: datetime
    topics: List[TopicResponse] = []
    has_custom_checker: bool = False
    checker_code: Optional[str] = None
    user_status: Optional[str] = "TODO"
    signature_schema: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class ProblemDetailResponse(ProblemResponse):
    test_cases: List[TestCaseResponse] = []
