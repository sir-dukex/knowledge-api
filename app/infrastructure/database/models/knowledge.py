import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text, Boolean

from app.infrastructure.database.connection import Base



class KnowledgeModel(Base):
    """
    Knowledge（ページネーション情報）のデータベースモデル

    1つのドキュメントに複数のKnowledge（ページ情報）が紐付く構造。
    各Knowledgeはページ番号、画像パス、テキスト等を保持する。

    Attributes:
        id: Knowledge ID
        document_id: 紐付くドキュメントID
        page_number: ページ番号
        image_path: S3上の画像パス
        page_text: ページから抽出したテキスト
        meta_data: メタデータ
        is_active: 有効フラグ（True:有効, False:無効）
        created_at: 作成日時
        updated_at: 更新日時
    """

    __tablename__ = "knowledges"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(
        String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    page_number = Column(Integer, nullable=False)
    image_path = Column(String(512), nullable=False)
    page_text = Column(Text, nullable=False)
    meta_data = Column(JSON, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
