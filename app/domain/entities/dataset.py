from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Dataset:
    """データセットのドメインエンティティ"""

    id: Optional[str] = None
    name: str = ""
    description: str = ""
    meta_data: Dict[str, Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create(
        cls, name: str, description: str = "", meta_data: Dict[str, Any] = None
    ) -> "Dataset":
        """新しいデータセットを作成"""
        return cls(
            name=name,
            description=description,
            meta_data=meta_data or {},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
