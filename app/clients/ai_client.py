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