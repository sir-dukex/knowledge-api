from typing import List

from app.domain.entities.dataset import Dataset
from app.domain.repositories.dataset_repository import DatasetRepository


class ListDatasetsUseCase:
    """
    データセット一覧取得ユースケース

    指定された条件に従ってデータセットの一覧を取得します。
    """

    def __init__(self, dataset_repository: DatasetRepository):
        self.dataset_repository = dataset_repository

    def execute(self, skip: int = 0, limit: int = 100) -> List[Dataset]:
        """
        データセット一覧を取得する

        Args:
            skip (int, optional): スキップするレコード数。デフォルトは0。
            limit (int, optional): 取得するレコード数の上限。デフォルトは100。

        Returns:
            List[Dataset]: 取得されたデータセットエンティティのリスト
        """
        return self.dataset_repository.list_datasets(skip=skip, limit=limit)
