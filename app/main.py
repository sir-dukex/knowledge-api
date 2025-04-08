from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.infrastructure.database.connection import init_db
from app.interfaces.api.v1 import datasets

app = FastAPI(
    title="Knowledge API",
    description="DifyライクなナレッジベースシステムのバックエンドAPI",
    version="0.1.0"
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では具体的なオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(datasets.router, prefix="/api/v1/datasets", tags=["datasets"])


@app.on_event("startup")
def startup():
    """アプリケーション起動時の処理"""
    init_db()


@app.get("/")
def root():
    """ルートエンドポイント"""
    return {"message": "Welcome to Knowledge API"}