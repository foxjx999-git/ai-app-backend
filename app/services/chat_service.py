from app.schemas.chat import ChatRequest, ChatResponse
from app.clients.ai_client import ask_ai
from app.services.rag_service import ask_with_rag
from app.services.tool_service import ask_with_tools
from app.services.rag_tool_service import ask_with_rag_and_tools

def process_chat(request: ChatRequest) -> ChatResponse:
    message = request.message.strip()

    tool_result = None

    if request.use_rag and request.use_tools:
        mode = "rag_with_tools"
        answer = ask_with_rag_and_tools(message)

    elif request.use_rag:
        mode = "rag"
        answer = ask_with_rag(message)

    elif request.use_tools:
        mode = "tools"
        answer, tool_result = ask_with_tools(message)

    else:
        mode = "normal"
        answer = ask_ai(message)

    return ChatResponse(
        answer=answer,
        mode=mode,
        tool_result=tool_result,
    )