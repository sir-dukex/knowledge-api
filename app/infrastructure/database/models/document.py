import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String, Text, Boolean

from app.infrastructure.database.connection import Base



class DocumentModel(Base):
    """
    ドキュメントのデータベースモデル

    datasets 内の documents を管理するためのテーブル定義です。
    dataset_id は、どのデータセットに属するかを示すための外部キーとして利用できます（必要に応じて制約の追加を検討）。

    Attributes:
        id: ドキュメントID
        dataset_id: 所属データセットID
        title: ドキュメントのタイトル
        content: ドキュメントの本文や内容
        meta_data: メタデータ
        is_active: 有効フラグ（True:有効, False:無効）
        created_at: 作成日時
        updated_at: 更新日時
    """

    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(
        String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    meta_data = Column(JSON, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
