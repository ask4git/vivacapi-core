from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title="VIVAC API",
    description="캠퍼를 위한 장소 큐레이션 서비스",
    version="0.1.0",
)


@app.get("/health", tags=["health"])
async def health() -> dict:
    return {"status": "ok", "environment": settings.ENVIRONMENT}
