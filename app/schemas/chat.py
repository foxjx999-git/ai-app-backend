from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(...,min_length=1)
    use_rag: bool = False
    use_tools: bool = False

class ChatResponse(BaseModel):
    answer: str
    mode: str
    tool_result: dict | None = None