import logging
import re
from pathlib import Path

from app.core.config import get_settings
from app.clients.ai_client import ask_ai_with_context
 
logger = logging.getLogger(__name__)

def split_text_into_chunks(text: str) -> list[str]:
    chunks = []

    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()

        if paragraph:
            chunks.append(paragraph)

    return chunks

def load_document_chunks() -> list[dict]:
    settings = get_settings()

    project_root = Path(__file__).resolve().parents[2]
    docs_dir = project_root / settings.docs_dir

    logger.info("RAG 文档目录：%s", docs_dir)

    if not docs_dir.exists():
        logger.warning("文档目录不存在：%s", docs_dir)
        return []
    
    #logger.info("文档目录下的文件：%s", list(docs_dir.iterdir()))
    
    all_chunks = []

    for file_path in docs_dir.glob("*txt"):
        logger.info("读取文档：%s", file_path)

        text = file_path.read_text(encoding="utf-8")
        chunks = split_text_into_chunks(text)

        for chunk in chunks:
            all_chunks.append(
                {
                    "source": file_path.name,
                    "content": chunk,
                }
            )
        
    logger.info("成功加载文档片段数量：%s", len(all_chunks))
    return all_chunks

def extract_keywords(text: str) -> list[str]:
    english_words = re.findall(r"[A-Za-z0-9]+", text.lower())

    chinese_chars = [
        char for char in text
        if "\u4e00" <= char <= "\u9fff"
    ]

    return english_words + chinese_chars

def retrieve_relevant_chunks(
    question: str,
    chunks: list[dict],
    top_k: int = 3,
) -> list[dict]:
    keywords = extract_keywords(question)

    scored_chunks = []

    for chunk in chunks:
        content = chunk["content"].lower()

        score = 0

        for keyword in keywords:
            if keyword.lower() in content:
                score += 1

        if score > 0:
            scored_chunks.append(
                {
                    "score": score,
                    "source": chunk["source"],
                    "content": chunk["content"],
                }
            )

    scored_chunks.sort(key=lambda item: item["score"], reverse=True)

    return scored_chunks[:top_k]

def load_documents() -> str:
    settings = get_settings()
    
    project_root = Path(__file__).resolve().parents[2]
    docs_dir = project_root / settings.docs_dir

    if not docs_dir.exists():
        logger.warning("文档目录不存在：%s", docs_dir)
        return "",[]
    
    all_text = []
    sources = []

    for file_path in docs_dir.glob("*.txt"):
        logger.info("读取文档：%s", file_path)

        text = file_path.read_text(encoding="utf-8")
        all_text.append(text)
        sources.append(file_path.name)

    return "\n\n".join(all_text), sources

def ask_with_rag(message: str) -> tuple[str, list[str]]:
    logger.info("开始执行 RAG 问答")

    settings = get_settings()

    chunks = load_document_chunks()

    if not chunks:
        return "没有找到可用的知识库文档。", []

    relevant_chunks = retrieve_relevant_chunks(
        question=message,
        chunks=chunks,
        top_k=settings.rag_top_k
    )

    for index, chunk in enumerate(relevant_chunks, start=1):
        logger.info(
            "RAG 命中片段 %s，score=%s，source=%s，content=%s",
            index,
            chunk["score"],
            chunk["source"],
            chunk["content"][:100],
        )

    if not relevant_chunks:
        return "没有找到与问题相关的文档内容。", []

    context = "\n\n".join(
        chunk["content"] for chunk in relevant_chunks
    )

    sources = list(
        dict.fromkeys(chunk["source"] for chunk in relevant_chunks)
    )

    logger.info("RAG 检索命中文档片段数量：%s", len(relevant_chunks))
    logger.info("RAG 来源文档：%s", sources)

    answer = ask_ai_with_context(
        message=message,
        context=context,
    )

    return answer, sources