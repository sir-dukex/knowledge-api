from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DatasetCreate(BaseModel):
    """データセット作成リクエスト"""

    name: str = Field(..., description="データセット名")
    description: str = Field("", description="説明")
    meta_data: Dict[str, Any] = Field(default_factory=dict, description="メタデータ")


class DatasetResponse(BaseModel):
    """データセットレスポンス"""

    id: str
    name: str
    description: str
    meta_data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class DatasetListResponse(BaseModel):
    """データセット一覧レスポンス"""

    items: List[DatasetResponse]
    total: int
