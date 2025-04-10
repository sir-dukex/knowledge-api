import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String, Text

from app.infrastructure.database.connection import Base


class DocumentModel(Base):
    """ドキュメントのデータベースモデル

    datasets 内の documents を管理するためのテーブル定義です。
    dataset_id は、どのデータセットに属するかを示すための外部キーとして利用できます（必要に応じて制約の追加を検討）。
    """

    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(
        String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
