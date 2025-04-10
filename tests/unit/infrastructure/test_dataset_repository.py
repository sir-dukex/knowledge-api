from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.entities.dataset import Dataset
from app.infrastructure.database.connection import Base
from app.infrastructure.repositories.dataset_repository_impl import (
    DatasetRepositorySQLAlchemy,
)


# テスト用のインメモリ SQLite DB を利用したエンジン・セッションを生成するフィクスチャ
@pytest.fixture(scope="function")
def test_session():
    # SQLite の in-memory DB を利用（運用環境と方言は異なりますが、ロジック検証には十分です）
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # __init__.py により、すべてのモデル（DatasetModel など）が Base.metadata に登録されている前提
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_create_dataset(test_session):
    """
    DatasetRepositorySQLAlchemy.create() のテスト
    新規に作成されたデータセットに ID やタイムスタンプが正しく設定されることを検証します。
    """
    repo = DatasetRepositorySQLAlchemy(test_session)
    dataset = Dataset.create(
        name="Test Dataset", description="A test dataset", meta_data={"foo": "bar"}
    )
    result = repo.create(dataset)
    assert result.id is not None
    assert result.name == "Test Dataset"
    assert result.description == "A test dataset"
    assert result.meta_data == {"foo": "bar"}
    assert isinstance(result.created_at, datetime)
    assert isinstance(result.updated_at, datetime)


def test_get_dataset(test_session):
    """
    DatasetRepositorySQLAlchemy.get_by_id() のテスト
    登録済みのデータセットが get_by_id() により正しく取得できることを検証します。
    """
    repo = DatasetRepositorySQLAlchemy(test_session)
    dataset = Dataset.create(
        name="Test Dataset Get", description="Dataset for get test", meta_data={}
    )
    created = repo.create(dataset)
    fetched = repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.name == "Test Dataset Get"


def test_list_datasets(test_session):
    """
    DatasetRepositorySQLAlchemy.list_datasets() のテスト
    同一データセット群を登録後、一覧取得が正しく行われることを検証します。
    """
    repo = DatasetRepositorySQLAlchemy(test_session)
    # 複数のデータセットを作成
    datasets = [
        Dataset.create(
            name=f"Dataset {i}", description=f"Description {i}", meta_data={"index": i}
        )
        for i in range(3)
    ]
    for ds in datasets:
        repo.create(ds)

    result = repo.list_datasets(skip=0, limit=10)
    assert len(result) == 3
    names = {d.name for d in result}
    expected_names = {"Dataset 0", "Dataset 1", "Dataset 2"}
    assert names == expected_names


def test_update_dataset(test_session):
    """
    DatasetRepositorySQLAlchemy.update() のテスト
    作成されたデータセットの内容を更新し、更新後の値と updated_at の更新が反映されることを検証します。
    """
    repo = DatasetRepositorySQLAlchemy(test_session)
    dataset = Dataset.create(
        name="Old Dataset", description="Old description", meta_data={"old": True}
    )
    created = repo.create(dataset)
    # 更新時は created_at は変更せず、updated_at に現在時刻を補完する
    updated_input = Dataset(
        id=created.id,
        name="Updated Dataset",
        description="Updated description",
        meta_data={"new": True},
        created_at=None,  # repository 実装側で元の値を利用する前提
        updated_at=datetime.now(),
    )
    updated = repo.update(updated_input)
    assert updated.id == created.id
    assert updated.name == "Updated Dataset"
    assert updated.description == "Updated description"
    assert updated.meta_data == {"new": True}
    assert updated.updated_at > created.updated_at


def test_delete_dataset(test_session):
    """
    DatasetRepositorySQLAlchemy.delete() のテスト
    データセットを削除した後、get_by_id() で取得できなくなることを検証します。
    """
    repo = DatasetRepositorySQLAlchemy(test_session)
    dataset = Dataset.create(
        name="Dataset To Delete", description="To be deleted", meta_data={}
    )
    created = repo.create(dataset)
    success = repo.delete(created.id)
    assert success is True
    fetched = repo.get_by_id(created.id)
    assert fetched is None
