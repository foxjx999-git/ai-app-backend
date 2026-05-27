from pydantic import BaseModel, Field

class LearningLogToolInput(BaseModel):
    topic: str = Field(..., min_length=1)
    minutes: int = Field(..., gt=0)
    summary: str = Field(..., min_length=1)