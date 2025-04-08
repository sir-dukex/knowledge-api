import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.dataset import Dataset
from app.domain.repositories.dataset_repository import DatasetRepository
from app.infrastructure.database.models.dataset import DatasetModel


class DatasetRepositorySQLAlchemy(DatasetRepository):
    """SQLAlchemyを使ったデータセットリポジトリの実装"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, dataset: Dataset) -> Dataset:
        """データセットを作成"""
        # エンティティをDBモデルに変換
        db_dataset = DatasetModel(
            id=str(uuid.uuid4()) if not dataset.id else dataset.id,
            name=dataset.name,
            description=dataset.description,
            meta_data=dataset.meta_data,
            created_at=dataset.created_at,
            updated_at=dataset.updated_at
        )
        
        # DBに保存
        self.session.add(db_dataset)
        self.session.commit()
        self.session.refresh(db_dataset)
        
        # DBモデルをエンティティに変換して返却
        return Dataset(
            id=db_dataset.id,
            name=db_dataset.name,
            description=db_dataset.description,
            meta_data=db_dataset.meta_data,
            created_at=db_dataset.created_at,
            updated_at=db_dataset.updated_at
        )
    
    def get_by_id(self, dataset_id: str) -> Optional[Dataset]:
        """IDでデータセットを取得"""
        stmt = select(DatasetModel).where(DatasetModel.id == dataset_id)
        db_dataset = self.session.execute(stmt).scalar_one_or_none()
        
        if not db_dataset:
            return None
        
        return Dataset(
            id=db_dataset.id,
            name=db_dataset.name,
            description=db_dataset.description,
            meta_data=db_dataset.meta_data,
            created_at=db_dataset.created_at,
            updated_at=db_dataset.updated_at
        )
    
    def list_datasets(self, skip: int = 0, limit: int = 100) -> List[Dataset]:
        """データセット一覧を取得"""
        stmt = select(DatasetModel).offset(skip).limit(limit)
        db_datasets = self.session.execute(stmt).scalars().all()
        
        return [
            Dataset(
                id=db_dataset.id,
                name=db_dataset.name,
                description=db_dataset.description,
                meta_data=db_dataset.meta_data,
                created_at=db_dataset.created_at,
                updated_at=db_dataset.updated_at
            )
            for db_dataset in db_datasets
        ]
    
    def update(self, dataset: Dataset) -> Dataset:
        """データセットを更新"""
        stmt = select(DatasetModel).where(DatasetModel.id == dataset.id)
        db_dataset = self.session.execute(stmt).scalar_one_or_none()
        
        if not db_dataset:
            raise ValueError(f"Dataset with id {dataset.id} not found")
        
        db_dataset.name = dataset.name
        db_dataset.description = dataset.description
        db_dataset.meta_data = dataset.meta_data
        db_dataset.updated_at = dataset.updated_at
        
        self.session.commit()
        self.session.refresh(db_dataset)
        
        return Dataset(
            id=db_dataset.id,
            name=db_dataset.name,
            description=db_dataset.description,
            meta_data=db_dataset.meta_data,
            created_at=db_dataset.created_at,
            updated_at=db_dataset.updated_at
        )
    
    def delete(self, dataset_id: str) -> bool:
        """データセットを削除"""
        stmt = select(DatasetModel).where(DatasetModel.id == dataset_id)
        db_dataset = self.session.execute(stmt).scalar_one_or_none()
        
        if not db_dataset:
            return False
        
        self.session.delete(db_dataset)
        self.session.commit()
        
        return True