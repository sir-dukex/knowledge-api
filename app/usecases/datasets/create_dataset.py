from app.domain.entities.dataset import Dataset
from app.domain.repositories.dataset_repository import DatasetRepository


class CreateDatasetUseCase:
    """データセット作成のユースケース"""

    def __init__(self, dataset_repository: DatasetRepository):
        self.dataset_repository = dataset_repository

    def execute(
        self, name: str, description: str = "", meta_data: dict = None, is_active: bool = True
    ) -> Dataset:
        """
        新しいデータセットを作成する

        Args:
            name: データセット名
            description: 説明
            meta_data: メタデータ
            is_active: 有効フラグ（True:有効, False:無効）

        Returns:
            作成されたデータセット
        """
        # ドメインエンティティの作成
        dataset = Dataset.create(
            name=name, description=description, meta_data=meta_data, is_active=is_active
        )

        # リポジトリを使って保存
        created_dataset = self.dataset_repository.create(dataset)
        return created_dataset
