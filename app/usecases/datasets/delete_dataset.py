from app.domain.repositories.dataset_repository import DatasetRepository


class DeleteDatasetUseCase:
    """
    データセット削除ユースケース

    指定されたIDのデータセットを削除します。
    """

    def __init__(self, dataset_repository: DatasetRepository):
        self.dataset_repository = dataset_repository

    def execute(self, dataset_id: str) -> bool:
        """
        指定されたデータセットを削除する

        Args:
            dataset_id (str): 削除対象のデータセットID

        Returns:
            bool: 削除に成功した場合は True、失敗（存在しない場合など）なら False
        """
        return self.dataset_repository.delete(dataset_id)
