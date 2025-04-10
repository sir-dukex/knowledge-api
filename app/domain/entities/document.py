from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Document:
    """ドキュメントのドメインエンティティ

    datasets → documents の階層におけるドキュメント情報を管理する。
    dataset_id を持つことで、どのデータセットに属するかを紐付ける。
    """

    id: Optional[str] = None
    dataset_id: Optional[str] = None
    title: str = ""
    content: str = ""
    meta_data: Dict[str, Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls, dataset_id: str, title: str, content: str, meta_data: Dict[str, Any] = None
    ) -> "Document":
        """新しいドキュメントを作成する

        Args:
            dataset_id (str): このドキュメントが属するデータセットのID
            title (str): ドキュメントのタイトル
            content (str): ドキュメントの本文や内容
            meta_data (Dict[str, Any], optional): その他の付随情報。デフォルトは空の辞書

        Returns:
            Document: 作成されたドキュメントエンティティ
        """
        return cls(
            dataset_id=dataset_id,
            title=title,
            content=content,
            meta_data=meta_data or {},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
