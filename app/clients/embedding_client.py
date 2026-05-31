import logging

from openai import OpenAI

from app.core.config import get_settings

logger = logging.getLogger(__name__)

def get_embedding(text: str) -> list[float]:
    settings = get_settings()

    api_key = settings.openai_api_key.strip() if settings.openai_api_key else None

    if not api_key:
        logger.error("OPENAI_API_KEY 未配置，无法生成 embedding")
        return []
    
    try:
        logger.info("开始生成文本 embedding，model=%s", settings.embedding_model)

        client = OpenAI(api_key=api_key)

        response = client.embeddings.create(
            model=settings.embedding_model,
            input=text,
        )

        embedding = response.data[0].embedding

        logger.info("embedding 生成成功，维度=%s", len(embedding))

        return embedding

    except Exception as e:
        logger.error("embedding 生成失败：%s", str(e))
        return []
    
