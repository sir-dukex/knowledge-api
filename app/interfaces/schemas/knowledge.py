from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class KnowledgeBase(BaseModel):
    """
    Knowledge（ページ情報）の共通スキーマ

    Attributes:
        document_id: 紐付くドキュメントID
        page_number: ページ番号
        image_path: ストレージ上の画像パス
        page_text: ページから抽出したテキスト
        meta_data: 追加情報
        is_active: 有効フラグ（True:有効, False:無効）
    """

    document_id: str = Field(..., description="紐付くドキュメントID")
    page_number: int = Field(..., description="ページ番号")
    image_path: str = Field(..., description="ストレージ上の画像パス")
    page_text: str = Field(..., description="ページから抽出したテキスト")
    meta_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="追加情報")
    is_active: bool = Field(True, description="有効フラグ（True:有効, False:無効）")


class KnowledgeCreate(KnowledgeBase):
    """Knowledge作成用スキーマ"""
    pass


class KnowledgeUpdate(BaseModel):
    """
    Knowledge更新用スキーマ

    Attributes:
        page_number: ページ番号
        image_path: ストレージ上の画像パス
        page_text: ページから抽出したテキスト
        meta_data: 追加情報
        is_active: 有効フラグ（True:有効, False:無効）
    """

    page_number: Optional[int] = Field(None, description="ページ番号")
    image_path: Optional[str] = Field(None, description="ストレージ上の画像パス")
    page_text: Optional[str] = Field(None, description="ページから抽出したテキスト")
    meta_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="追加情報")
    is_active: Optional[bool] = Field(None, description="有効フラグ（True:有効, False:無効）")


class KnowledgeResponse(KnowledgeBase):
    """Knowledgeレスポンススキーマ"""

    id: str = Field(..., description="Knowledge ID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")


class KnowledgeListResponse(BaseModel):
    """Knowledge一覧レスポンススキーマ"""

    items: List[KnowledgeResponse]
    total: int
