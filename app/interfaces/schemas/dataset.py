from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DatasetCreate(BaseModel):
    """
    データセット作成リクエスト

    Attributes:
        name: データセット名
        description: 説明
        meta_data: メタデータ
        is_active: 有効フラグ（True:有効, False:無効）
    """

    name: str = Field(..., description="データセット名")
    description: str = Field("", description="説明")
    meta_data: Dict[str, Any] = Field(default_factory=dict, description="メタデータ")
    is_active: bool = Field(True, description="有効フラグ（True:有効, False:無効）")


class DatasetUpdate(BaseModel):
    """
    データセット更新リクエスト

    Attributes:
        name: データセット名
        description: 説明
        meta_data: メタデータ
        is_active: 有効フラグ（True:有効, False:無効）
    """

    name: Optional[str] = Field(None, description="データセット名")
    description: Optional[str] = Field(None, description="説明")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="メタデータ")
    is_active: Optional[bool] = Field(None, description="有効フラグ（True:有効, False:無効）")


class DatasetResponse(BaseModel):
    """
    データセットレスポンス

    Attributes:
        id: データセットID
        name: データセット名
        description: 説明
        meta_data: メタデータ
        is_active: 有効フラグ（True:有効, False:無効）
        created_at: 作成日時
        updated_at: 更新日時
    """

    id: str
    name: str
    description: str
    meta_data: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class DatasetListResponse(BaseModel):
    """データセット一覧レスポンス"""

    items: List[DatasetResponse]
    total: int
