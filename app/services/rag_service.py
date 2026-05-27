import logging
 
logger = logging.getLogger(__name__)

def ask_with_rag(message: str) -> str:
    logger.info("开始执行 RAG 问答，占位版本")

    return f"模拟 RAG 回答：我会先检索知识库，再回答你的问题：{message}"