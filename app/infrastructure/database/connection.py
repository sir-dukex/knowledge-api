import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

"""
データベース接続管理モジュール

DATABASE_URL環境変数にSQLAlchemy用の接続文字列を指定することで、
PostgreSQL・SQL Serverなど任意のDBに簡単に切り替え可能な設計。
（例: postgresql+psycopg2://user:password@host:5432/dbname）
"""

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set.")
    raise RuntimeError("DATABASE_URL environment variable is not set.")

logger.info(f"Using database: {DATABASE_URL.split('://')[0]} -> {DATABASE_URL.split('/')[-1]}")

# エンジンの作成
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """DBセッションを取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """データベースの初期化"""
    # モデル定義のインポートを行って、Base.metadata に登録されるようにする
    from app.infrastructure.database import models

    logger.debug("Registered tables: %s", list(Base.metadata.tables.keys()))
    print("Registered tables:", list(Base.metadata.tables.keys()))
    Base.metadata.create_all(bind=engine)
