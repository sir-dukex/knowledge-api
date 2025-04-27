from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Knowledge:
    """
    Knowledge（ページネーション情報）のドメインエンティティ

    1つのドキュメントに複数のKnowledge（ページ情報）が紐付く。
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

    id: Optional[str] = None
    document_id: Optional[str] = None
    page_number: int = 0
    image_path: str = ""
    page_text: str = ""
    meta_data: Dict[str, Any] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        document_id: str,
        page_number: int,
        image_path: str,
        page_text: str,
        meta_data: Dict[str, Any] = None,
        is_active: bool = True,
    ) -> "Knowledge":
        """
        新しいKnowledge（ページ情報）を作成する

        Args:
            document_id (str): 紐付くドキュメントID
            page_number (int): ページ番号
            image_path (str): S3上の画像パス
            page_text (str): ページから抽出したテキスト
            meta_data (Dict[str, Any], optional): 追加情報
            is_active (bool, optional): 有効フラグ（デフォルト: True）

        Returns:
            Knowledge: 作成されたKnowledgeエンティティ
        """
        return cls(
            document_id=document_id,
            page_number=page_number,
            image_path=image_path,
            page_text=page_text,
            meta_data=meta_data or {},
            is_active=is_active,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
