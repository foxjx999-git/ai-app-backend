import logging

from openai import OpenAI

from app.core.config import get_settings

logger = logging.getLogger(__name__)

def ask_ai(message: str) -> str:
    settings = get_settings()

    if not settings.openai_api_key:
        logger.warning("OPENAI_API_KEY 未配置，返回模拟回答")
        return f"模拟 AI 回答：你刚才问的是：{message}"
    
    try:
        logger.info("开始调用 AI 模型，model=%s", settings.model_name)
        client = OpenAI(api_key=settings.openai_api_key)

        response = client.responses.create(
            model=settings.model_name,
            input=message,
        )

        logger.info("AI 模型调用成功")
        return response.output_text
    
    except Exception as e:
        logger.error("AI 模型调用失败：%s", str(e))
        return "AI 服务暂时不可用，请稍后再试。"
    

def ask_ai_with_context(message: str, context: str) -> str:
    settings = get_settings()

    api_key = settings.openai_api_key.strip() if settings.openai_api_key else None

    if not api_key:
        logger.warning("OPENAI_API_KEY 未配置，返回模拟 RAG 回答")
        return (
            "模拟 RAG 回答：我会基于以下知识库内容回答。\n\n"
            f"用户问题：{message}\n\n"
            f"知识库内容预览：{context[:500]}"
        )

    try:
        logger.info("开始调用 AI 模型进行 RAG 回答，model=%s", settings.model_name)

        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=settings.model_name,
            input=[
                {
                    "role": "system",
                    "content": (
                        "你是一个严谨的 RAG 问答助手。"
                        "请优先基于提供的知识库内容回答用户问题。"
                        "如果知识库中没有相关信息，请明确说明没有在文档中找到依据。"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"知识库内容：\n{context}\n\n"
                        f"用户问题：{message}"
                    ),
                },
            ],
        )

        logger.info("AI RAG 回答调用成功")

        return response.output_text

    except Exception as e:
        logger.error("AI RAG 回答调用失败：%s", str(e))
        return "AI RAG 服务暂时不可用，请稍后再试。"