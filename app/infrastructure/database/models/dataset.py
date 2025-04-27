import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, String, Text, Boolean

from app.infrastructure.database.connection import Base



class DatasetModel(Base):
    """
    データセットのデータベースモデル

    Attributes:
        id: データセットID
        name: データセット名
        description: データセットの説明
        meta_data: メタデータ
        is_active: 有効フラグ（True:有効, False:無効）
        created_at: 作成日時
        updated_at: 更新日時
    """

    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    meta_data = Column(JSON, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
