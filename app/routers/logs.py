import logging
 
from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.log import LearningLogResponse
from app.tools.log_storage import load_logs

router = APIRouter(prefix="/api", tags=["learning logs"])

logger = logging.getLogger(__name__)

@router.get("/logs", response_model=list[LearningLogResponse])
def get_logs() -> list[dict]:
    logger.info("开始查询学习记录列表")

    settings = get_settings()

    logs = load_logs(settings.learning_log_file)

    logger.info("学习记录查询成功，数量=%s", len(logs))

    return logs

