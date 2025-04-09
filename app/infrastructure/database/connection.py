import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 環境変数から接続情報を取得
SERVER = os.getenv("AZURE_SQL_SERVER", "your-server.database.windows.net")
DATABASE = os.getenv("AZURE_SQL_DATABASE", "your-database")
USERNAME = os.getenv("AZURE_SQL_USER", "your-username")
PASSWORD = os.getenv("AZURE_SQL_PASSWORD", "your-password")

# pymssqlを使用した接続文字列
DATABASE_URL = f"mssql+pymssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}"

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
    Base.metadata.create_all(bind=engine)