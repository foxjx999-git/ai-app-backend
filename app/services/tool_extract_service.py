import logging

from openai import OpenAI

from app.core.config import get_settings
from app.schemas.tool import LearningLogToolInput
from app.tools.message_parser import extract_minutes, extract_topic, extract_summary

logger = logging.getLogger(__name__)

def extract_learning_log_input(message: str) -> LearningLogToolInput:
    settings = get_settings()

    api_key = settings.openai_api_key.strip() if settings.openai_api_key else None

    if not api_key:
        logger.warning("OPENAI_API_KEY 未配置，使用规则解析工具参数")

        return LearningLogToolInput(
            topic=extract_topic(message),
            minutes=extract_minutes(message),
            summary=extract_summary(message),
        )
    
    try:
        logger.info("开始用 AI 提取学习记录工具参数")

        client = OpenAI(api_key=api_key)

        response = client.responses.parse(
            model=settings.model_name,
            input=[
                {
                    "role": "system",
                    "content":(
                        "你是一个学习记录信息提取助手。"
                        "请从用户输入中提取学习主题、学习分钟数和学习总结。"
                        "如果没有明确分钟数，默认 minutes=30。"
                        "如果没有明确主题，topic='未分类学习'。"
                    ),
                },
                {
                    "role": "user",
                    "content": message
                },
            ],
            text_format=LearningLogToolInput,
        )

        result = response.output_parsed

        logger.info(
            "AI 参数提取成功，topic=%s, minutes=%s, summary=%s",
            result.topic,
            result.minutes,
            result.summary,
        )

        return result

    except Exception as e:
        logger.error("AI 参数提取失败，改用规则解析：%s", str(e))

        return LearningLogToolInput(
            topic=extract_topic(message),
            minutes=extract_minutes(message),
            summary=extract_summary(message),
        )