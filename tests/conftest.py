import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import engine, get_db
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """테스트 세션 시작 시 vivac_test DB에 마이그레이션 적용."""
    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")


@pytest.fixture
async def db_session():
    """각 테스트마다 트랜잭션을 롤백하여 DB 상태를 격리."""
    async with engine.connect() as conn:
        await conn.begin()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        try:
            yield session
        finally:
            await session.close()
            await conn.rollback()


@pytest.fixture
async def client() -> AsyncClient:
    """DB를 사용하지 않는 테스트용 HTTP 클라이언트."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


@pytest.fixture
async def db_client(db_session: AsyncSession) -> AsyncClient:
    """DB가 필요한 테스트용 HTTP 클라이언트 (트랜잭션 롤백 격리 적용)."""
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()
