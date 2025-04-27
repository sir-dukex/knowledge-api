from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Dataset:
    """
    データセットのドメインエンティティ

    Attributes:
        id: データセットID
        name: データセット名
        description: データセットの説明
        meta_data: メタデータ
        is_active: 有効フラグ（True:有効, False:無効）
        created_at: 作成日時
        updated_at: 更新日時
    """

    id: Optional[str] = None
    name: str = ""
    description: str = ""
    meta_data: Dict[str, Any] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls, name: str, description: str = "", meta_data: Dict[str, Any] = None, is_active: bool = True
    ) -> "Dataset":
        """
        新しいデータセットを作成

        Args:
            name: データセット名
            description: データセットの説明
            meta_data: メタデータ
            is_active: 有効フラグ（デフォルト: True）

        Returns:
            Dataset: 新規作成されたデータセットエンティティ
        """
        return cls(
            name=name,
            description=description,
            meta_data=meta_data or {},
            is_active=is_active,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
