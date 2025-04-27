from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.dataset import Dataset


class DatasetRepository(ABC):
    """データセットリポジトリのインターフェース"""

    @abstractmethod
    def create(self, dataset: Dataset) -> Dataset:
        """データセットを作成"""
        pass

    @abstractmethod
    def get_by_id(self, dataset_id: str) -> Optional[Dataset]:
        """IDでデータセットを取得"""
        pass

    @abstractmethod
    def list_datasets(self, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None) -> List[Dataset]:
        """
        データセット一覧を取得

        Args:
            skip (int): スキップ件数
            limit (int): 最大取得件数
            is_active (Optional[bool]): 有効フラグでのフィルタ（Noneの場合は全件）

        Returns:
            List[Dataset]: データセットのリスト
        """
        pass

    @abstractmethod
    def update(self, dataset: Dataset) -> Dataset:
        """データセットを更新"""
        pass

    @abstractmethod
    def delete(self, dataset_id: str) -> bool:
        """データセットを削除"""
        pass
