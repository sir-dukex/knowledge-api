from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Knowledge:
    """
    Knowledge（ナレッジ情報）のドメインエンティティ

    1つのドキュメントに複数のKnowledge（ナレッジ要素）が紐付く。
    各Knowledgeは順番、テキスト等を保持する。

    Attributes:
        id: Knowledge ID
        document_id: 紐付くドキュメントID
        sequence: ナレッジの順番（0始まりのインデックス）
        knowledge_text: ナレッジ本文
        meta_data: メタデータ
        is_active: 有効フラグ（True:有効, False:無効）
        created_at: 作成日時
        updated_at: 更新日時
    """

    id: Optional[str] = None
    document_id: Optional[str] = None
    sequence: int = 0
    knowledge_text: str = ""
    meta_data: Dict[str, Any] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        document_id: str,
        sequence: int,
        knowledge_text: str,
        meta_data: Dict[str, Any] = None,
        is_active: bool = True,
    ) -> "Knowledge":
        """
        新しいKnowledge（ナレッジ情報）を作成する

        Args:
            document_id (str): 紐付くドキュメントID
            sequence (int): ナレッジの順番（0始まりのインデックス）
            knowledge_text (str): ナレッジ本文
            meta_data (Dict[str, Any], optional): 追加情報
            is_active (bool, optional): 有効フラグ（デフォルト: True）

        Returns:
            Knowledge: 作成されたKnowledgeエンティティ
        """
        return cls(
            document_id=document_id,
            sequence=sequence,
            knowledge_text=knowledge_text,
            meta_data=meta_data or {},
            is_active=is_active,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
