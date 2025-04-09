import uuid
import logging
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.dataset import Dataset
from app.domain.repositories.dataset_repository import DatasetRepository
from app.infrastructure.database.models.dataset import DatasetModel

# モジュール固有のロガーを定義（ログは英語で出力されます）
logger = logging.getLogger(__name__)

class DatasetRepositorySQLAlchemy(DatasetRepository):
    """SQLAlchemyを用いたデータセットリポジトリの実装"""

    def __init__(self, session: Session):
        """
        コンストラクタ

        引数:
            session (Session): 同期的なDBセッション
        """
        self.session = session

    def create(self, dataset: Dataset) -> Dataset:
        """
        データセットを作成する

        引数:
            dataset (Dataset): 作成するデータセットのエンティティ

        戻り値:
            Dataset: 作成されたデータセットエンティティ

        ※ ログは英語で出力されます。
        """
        logger.info("Start: Creating dataset with name=%s", dataset.name)
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
        logger.info("Success: Created dataset with id=%s", db_dataset.id)

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
        """
        IDでデータセットを取得する

        引数:
            dataset_id (str): 取得対象のデータセットID

        戻り値:
            Optional[Dataset]: 存在すればデータセットエンティティ、存在しなければ None
        """
        logger.info("Start: Retrieving dataset with id=%s", dataset_id)
        stmt = select(DatasetModel).where(DatasetModel.id == dataset_id)
        db_dataset = self.session.execute(stmt).scalar_one_or_none()

        if not db_dataset:
            logger.error("Error: Dataset not found with id=%s", dataset_id)
            return None

        logger.info("Success: Retrieved dataset with id=%s", dataset_id)
        return Dataset(
            id=db_dataset.id,
            name=db_dataset.name,
            description=db_dataset.description,
            meta_data=db_dataset.meta_data,
            created_at=db_dataset.created_at,
            updated_at=db_dataset.updated_at
        )

    def list_datasets(self, skip: int = 0, limit: int = 100) -> List[Dataset]:
        """
        データセット一覧を取得する

        引数:
            skip (int): スキップするレコード数
            limit (int): 取得するレコード数の上限

        戻り値:
            List[Dataset]: データセットエンティティのリスト

        注意:
            MSSQLではOFFSETやLIMIT句を使用する場合、ORDER BY句が必須です。
        """
        logger.info("Start: Listing datasets with skip=%d, limit=%d", skip, limit)
        # ORDER BY句を追加してMSSQLの要求に対応（例: 作成日時でソート）
        stmt = select(DatasetModel).order_by(DatasetModel.created_at).offset(skip).limit(limit)
        result = self.session.execute(stmt)
        db_datasets = result.scalars().all()
        logger.info("Success: Retrieved %d datasets", len(db_datasets))

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
        """
        データセットを更新する

        引数:
            dataset (Dataset): 更新対象のデータセットエンティティ

        戻り値:
            Dataset: 更新後のデータセットエンティティ

        例外:
            ValueError: 指定したIDのデータセットが存在しない場合
        """
        logger.info("Start: Updating dataset with id=%s", dataset.id)
        stmt = select(DatasetModel).where(DatasetModel.id == dataset.id)
        db_dataset = self.session.execute(stmt).scalar_one_or_none()

        if not db_dataset:
            logger.error("Error: Dataset not found for update with id=%s", dataset.id)
            raise ValueError(f"Dataset with id {dataset.id} not found")

        # データ更新処理
        db_dataset.name = dataset.name
        db_dataset.description = dataset.description
        db_dataset.meta_data = dataset.meta_data
        db_dataset.updated_at = dataset.updated_at

        self.session.commit()
        self.session.refresh(db_dataset)
        logger.info("Success: Updated dataset with id=%s", dataset.id)

        return Dataset(
            id=db_dataset.id,
            name=db_dataset.name,
            description=db_dataset.description,
            meta_data=db_dataset.meta_data,
            created_at=db_dataset.created_at,
            updated_at=db_dataset.updated_at
        )

    def delete(self, dataset_id: str) -> bool:
        """
        指定したIDのデータセットを削除する

        引数:
            dataset_id (str): 削除対象のデータセットID

        戻り値:
            bool: 削除が成功した場合は True、存在しない場合は False
        """
        logger.info("Start: Deleting dataset with id=%s", dataset_id)
        stmt = select(DatasetModel).where(DatasetModel.id == dataset_id)
        db_dataset = self.session.execute(stmt).scalar_one_or_none()

        if not db_dataset:
            logger.error("Error: Dataset not found for deletion with id=%s", dataset_id)
            return False

        self.session.delete(db_dataset)
        self.session.commit()
        logger.info("Success: Deleted dataset with id=%s", dataset_id)
        return True

