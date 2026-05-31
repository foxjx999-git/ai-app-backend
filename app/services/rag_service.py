import logging
import re
from pathlib import Path

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import get_settings
from app.clients.ai_client import ask_ai_with_context
from app.services.vector_store_service import (
    build_vector_store, 
    query_vector_store,
    reset_vector_store,
    get_vector_store_count,
)
 
logger = logging.getLogger(__name__)

def split_text_into_chunks(text: str) -> list[str]:
    text =text.strip()

    if not text:
        return []
    
    paragraphs = re.split(r"\n\s*\n",text)

    chunks = []

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if paragraph:
            chunks.append(paragraph)

    if chunks:
        return chunks

    return [text]

def read_pdf_text(file_path: Path) -> str:
    try:
        reader = PdfReader(str(file_path))

        pages_text = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages_text.append(text)

        return "\n\n".join(pages_text)
    
    except Exception as e:
        logger.error("读取 PDF 失败，文件=%s，错误=%s", file_path.name, str(e))
        return ""

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

    for file_path in docs_dir.iterdir():
        if file_path.suffix.lower() not in[".txt", ".pdf"]:
            continue

        logger.info("读取文档：%s", file_path)
        try:
            if file_path.suffix.lower() == ".txt":
                text = file_path.read_text(encoding="utf-8")

            elif file_path.suffix.lower() == ".pdf":
                text = read_pdf_text(file_path)

            else:
                continue
        except Exception as e:
            logger.error("读取文档失败，文件=%s，错误=%s", file_path.name, str(e))
            continue

        logger.info("文档文本长度：%s，文件：%s", len(text), file_path.name)

        if not text.strip():
            logger.warning("文档内容为空，跳过文件：%s", file_path.name)
            continue

        chunks = split_text_into_chunks(text)

        logger.info("文档切分片段数量：%s，文件：%s", len(chunks), file_path.name)

        for chunk in chunks:
            all_chunks.append(
                {
                    "source": file_path.name,
                    "content": chunk,
                }
            )
        
    logger.info("成功加载文档片段数量：%s", len(all_chunks))
    return all_chunks





def retrieve_relevant_chunks_by_tfidf(
    question: str,
    chunks: list[dict],
    top_k: int = 3,
) -> list[dict]:
    if not chunks:
        return []
    
    documents = [chunk["content"] for chunk in chunks]

    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(2, 4),
    )
    document_vectors = vectorizer.fit_transform(documents)
    question_vector = vectorizer.transform([question])

    similarities = cosine_similarity(question_vector, document_vectors)[0]

    scored_chunks = []

    for index, score in enumerate(similarities):
        if score > 0:
            scored_chunks.append(
                {
                    "score": float(score),
                    "source": chunks[index]["source"],
                    "content": chunks[index]["content"],
                }
            )
    scored_chunks.sort(key=lambda item: item["score"], reverse=True)

    return scored_chunks[:top_k]

def ask_with_rag(message: str) -> tuple[str, list[str]]:
    settings = get_settings()

    if settings.rag_retrieval_mode == "vector":
        logger.info("RAG 检索模式：vector")
        return ask_with_vector_rag(message)
    
    if settings.rag_retrieval_mode == "tfidf":
        logger.info("RAG 检索模式：tfidf")
        return ask_with_tfidf_rag(message)
    
    logger.warning(
        "未知 RAG 检索模式：%s，默认使用 vector",
        settings.rag_retrieval_mode,
    )

    return ask_with_vector_rag(message)

def build_rag_vector_store() -> dict:
    logger.info("开始构建 RAG 向量库")

    settings = get_settings()

    chunks = load_document_chunks()
    chunks_count = len(chunks)

    if not chunks:
        logger.warning("没有可用文档片段，无法构建向量库")
        return {
            "chunks_count": 0,
            "saved_count": 0,
            "retrieval_mode": settings.rag_retrieval_mode,
        }
    
    saved_count = build_vector_store(chunks)

    logger.info("RAG 向量库构建完成，写入数量=%s", saved_count)

    return {
        "chunks_count": chunks_count,
        "saved_count": saved_count,
        "retrieval_mode": settings.rag_retrieval_mode,
    }

def ask_with_vector_rag(message: str) -> tuple[str, list[str]]:
    logger.info("开始执行 ChromaDB 向量 RAG 问答")

    settings = get_settings()

    relevant_chunks = query_vector_store(
        question=message,
        top_k=settings.rag_top_k,
    )

    if not relevant_chunks:
        return "没有从向量库中检索到相关文档内容。请先构建 RAG 向量库。", []
    
    for index, chunk in enumerate(relevant_chunks, start=1):
        logger.info(
            "向量 RAG 命中片段 %d, distance=%s，source=%s，content=%s",
            index,
            chunk["distance"],
            chunk["source"],
            chunk["content"][:100],
        )

    context = "\n\n".join(
        chunk["content"] for chunk in relevant_chunks
    )

    sources = list(
        dict.fromkeys(chunk["source"] for chunk in relevant_chunks)
    )

    logger.info("向量 RAG 来源文档：%s", sources)

    answer = ask_ai_with_context(
        message=message,
        context=context,
    )

    return answer, sources

def ask_with_tfidf_rag(message: str) -> tuple[str, list[str]]:
    logger.info("开始执行 TF-IDF RAG 问答")

    settings = get_settings()

    chunks = load_document_chunks()

    if not chunks:
        return "没有找到可用的知识库文档。", []

    logger.info("RAG 检索方式：TF-IDF")

    relevant_chunks = retrieve_relevant_chunks_by_tfidf(
        question=message,
        chunks=chunks,
        top_k=settings.rag_top_k,
    )

    if not relevant_chunks:
        return "没有找到与问题相关的文档内容。", []

    for index, chunk in enumerate(relevant_chunks, start=1):
        logger.info(
            "TF-IDF RAG 命中片段 %s，score=%s，source=%s，content=%s",
            index,
            chunk["score"],
            chunk["source"],
            chunk["content"][:100],
        )

    context = "\n\n".join(
        chunk["content"] for chunk in relevant_chunks
    )

    sources = list(
        dict.fromkeys(chunk["source"] for chunk in relevant_chunks)
    )

    logger.info("TF-IDF RAG 来源文档：%s", sources)

    answer = ask_ai_with_context(
        message=message,
        context=context,
    )

    return answer, sources

def rebuild_rag_vector_store() -> dict:
    logger.info("开始重建 RAG 向量库")

    settings = get_settings()

    chunks = load_document_chunks()
    chunks_count = len(chunks)

    if not chunks:
        logger.warning("没有可用文档片段，取消重建向量库")
        return {
            "chunks_count": 0,
            "saved_count": 0,
            "retrieval_mode": settings.rag_retrieval_mode,
        }

    reset_vector_store()

    saved_count = build_vector_store(chunks)

    logger.info("RAG 向量库重建完成，写入数量=%s", saved_count)

    return {
        "chunks_count": chunks_count,
        "saved_count": saved_count,
        "retrieval_mode": settings.rag_retrieval_mode,
    }

def get_rag_status() -> dict:
    settings = get_settings()

    vector_count = get_vector_store_count()

    return{
        "retrieval_mode": settings.rag_retrieval_mode,
        "docs_dir": settings.docs_dir,
        "rag_top_k": settings.rag_top_k,
        "embedding_model": settings.embedding_model,
        "chroma_dir": settings.chroma_dir,
        "collection_name": settings.chroma_collection_name,
        "vector_count": vector_count,
    }

