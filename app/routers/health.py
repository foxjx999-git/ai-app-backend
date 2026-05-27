from fastapi import APIRouter
import logging



router = APIRouter(tags=["health"])

logger = logging.getLogger(__name__)

@router.get("/health")
def health_check() -> dict:
    logger.info("健康检查接口被调用")
    return {
        "status": "ok",
        "message": "AI app backend is running",
    }