from datetime import datetime
from unittest.mock import Mock

import pytest

from app.domain.entities.dataset import Dataset

# CreateDatasetUseCase のテスト
from app.usecases.datasets.create_dataset import CreateDatasetUseCase
from app.usecases.datasets.delete_dataset import DeleteDatasetUseCase
from app.usecases.datasets.get_dataset import GetDatasetUseCase
from app.usecases.datasets.list_datasets import ListDatasetsUseCase
from app.usecases.datasets.update_dataset import UpdateDatasetUseCase


class TestCreateDatasetUseCase:
    def test_execute_creates_dataset(self):
        # モック repository の準備
        mock_repo = Mock()
        dummy_dataset = Dataset(
            id="dataset-123",
            name="Test Dataset",
            description="This is a test dataset.",
            meta_data={"foo": "bar"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repo.create.return_value = dummy_dataset

        usecase = CreateDatasetUseCase(mock_repo)
        # 実行時、入力値から Dataset.create() を内部で呼び出し、repository.create() に渡す実装を前提とする
        result = usecase.execute(
            name="Test Dataset",
            description="This is a test dataset.",
            meta_data={"foo": "bar"},
        )
        mock_repo.create.assert_called_once()
        assert result.id == "dataset-123"
        assert result.name == "Test Dataset"


class TestUpdateDatasetUseCase:
    def test_execute_updates_dataset(self):
        # モック repository の準備
        mock_repo = Mock()
        updated_dataset = Dataset(
            id="dataset-456",
            name="Updated Dataset",
            description="Updated description",
            meta_data={"key": "updated"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repo.update.return_value = updated_dataset

        usecase = UpdateDatasetUseCase(mock_repo)
        result = usecase.execute(
            dataset_id="dataset-456",
            name="Updated Dataset",
            description="Updated description",
            meta_data={"key": "updated"},
        )
        mock_repo.update.assert_called_once()
        assert result.id == "dataset-456"
        assert result.name == "Updated Dataset"
        assert result.description == "Updated description"


class TestDeleteDatasetUseCase:
    def test_execute_success(self):
        mock_repo = Mock()
        mock_repo.delete.return_value = True
        usecase = DeleteDatasetUseCase(mock_repo)
        result = usecase.execute("dataset-789")
        mock_repo.delete.assert_called_once_with("dataset-789")
        assert result is True

    def test_execute_failure(self):
        mock_repo = Mock()
        mock_repo.delete.return_value = False
        usecase = DeleteDatasetUseCase(mock_repo)
        result = usecase.execute("nonexistent-dataset")
        mock_repo.delete.assert_called_once_with("nonexistent-dataset")
        assert result is False


class TestListDatasetsUseCase:
    def test_execute_returns_datasets(self):
        mock_repo = Mock()
        # 複数件のダミー Dataset を作成
        ds1 = Dataset(
            id="ds-1",
            name="Dataset 1",
            description="Desc 1",
            meta_data={"num": 1},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        ds2 = Dataset(
            id="ds-2",
            name="Dataset 2",
            description="Desc 2",
            meta_data={"num": 2},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repo.list_datasets.return_value = [ds1, ds2]

        usecase = ListDatasetsUseCase(mock_repo)
        result = usecase.execute(skip=0, limit=10)
        mock_repo.list_datasets.assert_called_once_with(skip=0, limit=10)
        assert len(result) == 2
        ids = [d.id for d in result]
        assert "ds-1" in ids and "ds-2" in ids


class TestGetDatasetUseCase:
    def test_execute_success(self):
        mock_repo = Mock()
        dummy_dataset = Dataset(
            id="ds-001",
            name="Existing Dataset",
            description="Existing description",
            meta_data={"test": True},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = dummy_dataset
        usecase = GetDatasetUseCase(mock_repo)
        result = usecase.execute("ds-001")
        mock_repo.get_by_id.assert_called_once_with("ds-001")
        assert result.id == "ds-001"
        assert result.name == "Existing Dataset"

    def test_execute_not_found(self):
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        usecase = GetDatasetUseCase(mock_repo)
        with pytest.raises(ValueError, match="Dataset not found"):
            usecase.execute("nonexistent-ds")
