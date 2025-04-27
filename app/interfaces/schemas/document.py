from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    """
    ドキュメント作成用の入力スキーマ

    dataset_id, title, content は必須項目。
    meta_data は任意で、付随情報を JSON 形式で指定できます。
    is_active は有効フラグ（デフォルト: True）
    """

    dataset_id: str = Field(..., description="所属データセットID")
    title: str = Field(..., description="ドキュメントのタイトル")
    content: str = Field(..., description="ドキュメントの本文や内容")
    meta_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="メタデータ")
    is_active: bool = Field(True, description="有効フラグ（True:有効, False:無効）")


class DocumentUpdate(BaseModel):
    """
    ドキュメント更新用の入力スキーマ

    dataset_id は作成時にのみ設定されるため、更新時には不要としています。
    title, content, meta_data, is_active は任意項目で、必要に応じて変更可能です。
    変更が不要な項目は指定しなくても問題ありません。
    """

    title: Optional[str] = Field(None, description="ドキュメントのタイトル")
    content: Optional[str] = Field(None, description="ドキュメントの本文や内容")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="メタデータ")
    is_active: Optional[bool] = Field(None, description="有効フラグ（True:有効, False:無効）")


class DocumentResponse(BaseModel):
    """
    ドキュメント出力用のレスポンススキーマ

    SQLAlchemy モデルとの相互変換のために orm_mode を True に設定。

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

    id: str
    dataset_id: str
    title: str
    content: str
    meta_data: Optional[Dict[str, Any]]
    is_active: bool
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
