from pydantic import BaseModel

class LearningLogResponse(BaseModel):
    id: str
    topic: str
    minutes: int
    summary: str
    created_at: str