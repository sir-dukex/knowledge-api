import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, String, Text

from app.infrastructure.database.connection import Base


class DatasetModel(Base):
    """データセットのデータベースモデル"""

    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
