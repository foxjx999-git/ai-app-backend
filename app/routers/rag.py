import logging

from fastapi import APIRouter

from app.services.rag_service import (
    build_rag_vector_store, 
    rebuild_rag_vector_store, 
    get_rag_status,
)

router = APIRouter(prefix="/api/rag", tags = ["rag"])

logger = logging.getLogger(__name__)

@router.post("/build")
def build_rag_index() -> dict:
    logger.info("收到构建 RAG 向量库请求")

    result = build_rag_vector_store()

    return{
        "message": "RAG 向量库构建完成",
        **result
    }

@router.post("/rebuild")
def rebuild_rag_index() -> dict:
    logger.info("收到重建 RAG 向量库请求")

    result =rebuild_rag_vector_store()

    return {
        "message": "RAG 向量库重建完成",
        **result,
    }

@router.get("/status")
def rag_status() -> dict:
    logger.info("收到查询 RAG 状态请求")
    return get_rag_status()