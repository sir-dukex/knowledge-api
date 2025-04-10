from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class DocumentCreate(BaseModel):
    """
    ドキュメント作成用の入力スキーマ

    dataset_id, title, content は必須項目。
    meta_data は任意で、付随情報を JSON 形式で指定できます。
    """

    dataset_id: str
    title: str
    content: str
    meta_data: Optional[Dict[str, Any]] = {}


class DocumentUpdate(BaseModel):
    """
    ドキュメント更新用の入力スキーマ

    dataset_id は作成時にのみ設定されるため、更新時には不要としています。
    title, content, meta_data は任意項目で、必要に応じて変更可能です。
    変更が不要な項目は指定しなくても問題ありません。
    """

    title: Optional[str] = None
    content: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None


class DocumentResponse(BaseModel):
    """
    ドキュメント出力用のレスポンススキーマ

    SQLAlchemy モデルとの相互変換のために orm_mode を True に設定。
    """

    id: str
    dataset_id: str
    title: str
    content: str
    meta_data: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class DocumentListResponse(BaseModel):
    """
    複数のドキュメント取得用レスポンススキーマ

    items は DocumentResponse 型のリスト、total には全件数を保持します。
    """

    items: List[DocumentResponse]
    total: int
