from typing import List, Optional
from pydantic import BaseModel, Field, validator

class Source(BaseModel):
    doc: str
    snippet: Optional[str]

class AnswerResponse(BaseModel):
    answer: str
    category: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    sources: Optional[List[Source]] = []

    @validator("category")
    def validate_category(cls, value):
        allowed = ["api", "security", "pricing", "support", "other"]
        if value not in allowed:
            raise ValueError(f"Invalid category: {value}")
        return value
