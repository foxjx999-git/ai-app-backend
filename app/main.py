from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging_config import setup_logging
from app.routers.health import router as health_router
from app.routers.chat import router as chat_router
from app.routers.logs import router as logs_router

setup_logging()

settings = get_settings()

#print(settings.model_name)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI 应用工程师后端框架练习项目",
)

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(logs_router)