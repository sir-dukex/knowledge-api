from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import logging

# テスト用ログ出力
logging.info("test log: FastAPI app startup")

# OpenTelemetry/Azure Monitor初期化
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter, AzureMonitorLogExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry import trace
import logging
import os

# Application Insightsの接続文字列
connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

# OpenTelemetryリソース
resource = Resource.create({"service.name": "knowledge-api"})

# TracerProviderとExporterの設定
trace_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(trace_provider)
if connection_string:
    trace_exporter = AzureMonitorTraceExporter(connection_string=connection_string)
    span_processor = BatchSpanProcessor(trace_exporter)
    trace_provider.add_span_processor(span_processor)

# LoggingのExporter設定
if connection_string:
    log_exporter = AzureMonitorLogExporter(connection_string=connection_string)
    LoggingInstrumentor().instrument(set_logging_format=True, log_exporter=log_exporter)
else:
    LoggingInstrumentor().instrument(set_logging_format=True)

from app.infrastructure.database.connection import init_db
from app.interfaces.api.v1 import datasets, documents

# logging設定（uvicornの--log-configで適用するため、ここでは不要）

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    """
    アプリケーションの起動・終了時の処理を管理するlifespanイベントハンドラ
    """
    # アプリケーション起動時の処理
    init_db()
    logging.info("Database initialized on startup.")
    yield
    # アプリケーション終了時の処理（必要に応じて追加）

# FastAPIアプリケーションの生成（lifespanを指定）
app = FastAPI(
    title="Knowledge API",
    description="DifyライクなナレッジベースシステムのバックエンドAPI",
    version="0.1.0",
    lifespan=lifespan,
)
FastAPIInstrumentor.instrument_app(app)

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
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])


@app.get("/")
def root():
    """ルートエンドポイント"""
    return {"message": "Welcome to Knowledge API"}

@app.get("/admin/host/ping")
def ping():
    """Functionsランタイムの死活監視用エンドポイント（ping）"""
    return {"status": "ok"}

@app.get("/admin/host/status")
def status():
    """Functionsランタイムの死活監視用エンドポイント（status）"""
    return {"status": "ok"}
