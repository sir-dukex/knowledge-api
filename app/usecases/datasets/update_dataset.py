from datetime import datetime

from app.domain.entities.dataset import Dataset
from app.domain.repositories.dataset_repository import DatasetRepository


class UpdateDatasetUseCase:
    """
    データセット更新ユースケース

    指定されたIDのデータセットの更新を行います。
    """

    def __init__(self, dataset_repository: DatasetRepository):
        self.dataset_repository = dataset_repository

    def execute(
        self, dataset_id: str, name: str, description: str, meta_data: dict
    ) -> Dataset:
        """
        データセットを更新する

        Args:
            dataset_id (str): 更新対象のデータセットID
            name (str): 更新する新しい名前
            description (str): 更新する説明
            meta_data (dict): 更新するメタデータ

        Returns:
            Dataset: 更新後のデータセットエンティティ
        """
        # 更新用エンティティを作成します。
        # created_at は既存の値を保持するため、更新時は repository 側で補完する想定です。
        updated_dataset = Dataset(
            id=dataset_id,
            name=name,
            description=description,
            meta_data=meta_data,
            created_at=None,  # repository 実装側で既存の created_at を反映
            updated_at=datetime.now(),
        )
        return self.dataset_repository.update(updated_dataset)
