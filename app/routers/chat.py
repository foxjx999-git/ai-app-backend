import logging

from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_chat

router = APIRouter(prefix="/api", tags=["chat"])

logger = logging.getLogger(__name__)

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    logger.info(
        "chat 接口被调用，use_rag=%s, use_tools=%s",
        request.use_rag,
        request.use_tools,
    )

    response = process_chat(request)

    logger.info("chat 接口处理完成，mode=%s", response.mode)

    return response