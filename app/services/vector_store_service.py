import logging

import chromadb

from app.clients.embedding_client import get_embedding
from app.core.config import get_settings

logger =logging.getLogger(__name__)

def get_collection():
    settings = get_settings()

    client = chromadb.PersistentClient(
        path=settings.chroma_dir,
    )

    collection = client.get_or_create_collection(
        name=settings.chroma_collection_name,
    )
    return collection

def reset_vector_store() -> None:
    settings = get_settings()

    client = chromadb.PersistentClient(
        path=settings.chroma_dir,
    )

    try:
        client.delete_collection(
            name=settings.chroma_collection_name,
        )
        logger.info("旧向量库 collection 已删除：%s", settings.chroma_collection_name)

    except Exception as e:
        logger.warning(
            "删除旧向量库 collection 失败或 collection 不存在：%s",
            str(e),
        )
        
    client.get_or_create_collection(
        name=settings.chroma_collection_name,
    )

    logger.info("新的向量库 collection 已创建：%s", settings.chroma_collection_name)

def build_vector_store(chunks: list[dict]) -> int:
    collection = get_collection()

    saved_count = 0

    for index, chunk in enumerate(chunks):
        content = chunk["content"]
        source = chunk["source"]

        embedding =get_embedding(content)

        if not embedding:
            logger.warning("embedding 为空，跳过 chunk，source=%s", source)
            continue

        chunk_id = f"{source}-{index}"

        collection.upsert(
            ids=[chunk_id],
            documents=[content],
            metadatas=[
                {
                    "source": source,
                }
            ],
            embeddings=[embedding],
        )
        saved_count += 1

    logger.info("向量库构建完成，写入 chunk 数量=%s", saved_count)

    return saved_count
    
def query_vector_store(question: str, top_k: int = 3) -> list[dict]:
    collection = get_collection()

    query_embedding = get_embedding(question)

    if not query_embedding:
        logger.warning("问题 embedding 为空，无法检索向量库")
        return []
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    relevant_chunks = []

    for document, metadata, distance in zip(documents, metadatas, distances):
        relevant_chunks.append(
            {
                "distance": float(distance),
                "source": metadata.get("source", "unknown"),
                "content": document,
            }
        )

    logger.info("向量检索命中 chunk 数量=%s", len(relevant_chunks))

    return relevant_chunks

def get_vector_store_count() -> int:
    collection = get_collection()

    try:
        return collection.count()

    except Exception as e:
        logger.error("获取向量库记录数量失败：%s", str(e))
        return 0


    

