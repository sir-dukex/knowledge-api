import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database.models.dataset import Base

# テスト用のインメモリSQLiteデータベース
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """PyTest fixture for asyncio."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def engine():
    """テスト用エンジンのフィクスチャ"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.meta_data.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.meta_data.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(engine):
    """テスト用のデータベースセッション"""
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()