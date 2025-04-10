from app.domain.entities.dataset import Dataset
from app.domain.repositories.dataset_repository import DatasetRepository


class GetDatasetUseCase:
    """
    データセット取得ユースケース

    指定されたIDのデータセットを取得し、存在しない場合は例外を発生させます。
    """

    def __init__(self, dataset_repository: DatasetRepository):
        self.dataset_repository = dataset_repository

    def execute(self, dataset_id: str) -> Dataset:
        """
        指定されたIDのデータセットを取得する

        Args:
            dataset_id (str): 取得対象のデータセットID

        Returns:
            Dataset: 取得したデータセットのエンティティ

        Raises:
            ValueError: データセットが存在しない場合
        """
        dataset = self.dataset_repository.get_by_id(dataset_id)
        if dataset is None:
            raise ValueError("Dataset not found")
        return dataset
