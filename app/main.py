from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.core.bastion import start_tunnel, stop_tunnel
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # ----- startup -----
    start_tunnel()
    yield
    # ----- shutdown -----
    stop_tunnel()


app = FastAPI(
    title="VIVAC API",
    description="캠퍼를 위한 장소 큐레이션 서비스",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["health"])
async def health() -> dict:
    return {"status": "ok", "environment": settings.ENVIRONMENT}
