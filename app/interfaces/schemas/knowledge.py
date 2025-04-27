from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import Field
from app.interfaces.schemas.base import CustomBaseModel


class KnowledgeBase(CustomBaseModel):
    """
    Knowledge（ナレッジ情報）の共通スキーマ

    Attributes:
        document_id: 紐付くドキュメントID
        sequence: ナレッジの順番（0始まりのインデックス）
        knowledge_text: ナレッジ本文
        meta_data: 追加情報
        is_active: 有効フラグ（True:有効, False:無効）
    """

    document_id: str = Field(..., description="紐付くドキュメントID")
    sequence: int = Field(..., description="ナレッジの順番（0始まりのインデックス）")
    knowledge_text: str = Field(..., description="ナレッジ本文")
    meta_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="追加情報")
    is_active: bool = Field(True, description="有効フラグ（True:有効, False:無効）")


class KnowledgeCreate(KnowledgeBase):
    """Knowledge作成用スキーマ"""
    pass


class KnowledgeUpdate(CustomBaseModel):
    """
    Knowledge更新用スキーマ

    Attributes:
        sequence: ナレッジの順番（0始まりのインデックス）
        knowledge_text: ナレッジ本文
        meta_data: 追加情報
        is_active: 有効フラグ（True:有効, False:無効）
    """

    sequence: Optional[int] = Field(None, description="ナレッジの順番（0始まりのインデックス）")
    knowledge_text: Optional[str] = Field(None, description="ナレッジ本文")
    meta_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="追加情報")
    is_active: Optional[bool] = Field(None, description="有効フラグ（True:有効, False:無効）")


class KnowledgeResponse(KnowledgeBase):
    """Knowledgeレスポンススキーマ"""

    id: str = Field(..., description="Knowledge ID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")


class KnowledgeListResponse(CustomBaseModel):
    """Knowledge一覧レスポンススキーマ"""

    items: List[KnowledgeResponse]
    total: int
