from app.domain.entities.dataset import Dataset
from app.domain.repositories.dataset_repository import DatasetRepository


class CreateDatasetUseCase:
    """データセット作成のユースケース"""
    
    def __init__(self, dataset_repository: DatasetRepository):
        self.dataset_repository = dataset_repository
    
    def execute(self, name: str, description: str = "", meta_data: dict = None) -> Dataset:
        """
        新しいデータセットを作成する
        
        Args:
            name: データセット名
            description: 説明
            meta_data: メタデータ
            
        Returns:
            作成されたデータセット
        """
        # ドメインエンティティの作成
        dataset = Dataset.create(
            name=name,
            description=description,
            meta_data=meta_data
        )
        
        # リポジトリを使って保存
        created_dataset = self.dataset_repository.create(dataset)
        return created_dataset