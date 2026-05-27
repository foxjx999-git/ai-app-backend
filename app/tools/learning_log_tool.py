import uuid
from datetime import datetime

def create_learning_log_tool(
    topic: str,
    minutes: int,
    summary: str,
) -> dict:
    if not topic:
        raise ValueError("topic 不能为空")
    
    if minutes <= 0:
        raise ValueError("minutes 必须大于 0")

    if not summary:
        raise ValueError("summary 不能为空")
    
    return {
        "id": str(uuid.uuid4()),
        "topic": topic,
        "minutes": minutes,
        "summary": summary,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }