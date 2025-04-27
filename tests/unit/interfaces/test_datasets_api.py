from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.domain.entities.dataset import Dataset


# クライアントのフィクスチャ。FastAPI の TestClient を返します。
@pytest.fixture(scope="module")
def client():
    from app.main import app

    return TestClient(app)


# CreateDatasetUseCase のパッチフィクスチャ（POST用）
@pytest.fixture
def patch_create_dataset_usecase():
    with patch(
        "app.interfaces.api.v1.datasets.CreateDatasetUseCase"
    ) as mock_usecase_class:
        yield mock_usecase_class


# DatasetRepositorySQLAlchemy のパッチフィクスチャ（GET, PUT, DELETE 用）
@pytest.fixture
def patch_dataset_repository():
    with patch(
        "app.interfaces.api.v1.datasets.DatasetRepositorySQLAlchemy"
    ) as mock_repo_class:
        yield mock_repo_class


def test_create_dataset_api_interface(client, patch_create_dataset_usecase):
    """
    CreateDatasetUseCase をモックして、API /api/v1/datasets/ の POST エンドポイントの
    正常な動作を検証するテスト
    """
    # Arrange: ダミーの Dataset エンティティを作成
    dummy_dataset = Dataset(
        id="dummy-id",
        name="Test Dataset",
        description="Test description",
        meta_data={"key": "value"},
        created_at=datetime(2025, 4, 10, 0, 0),
        updated_at=datetime(2025, 4, 10, 0, 0),
    )
    # CreateDatasetUseCase のインスタンスのモック設定
    mock_usecase_instance = MagicMock()
    mock_usecase_instance.execute.return_value = dummy_dataset
    patch_create_dataset_usecase.return_value = mock_usecase_instance

    test_payload = {
        "name": "Test Dataset",
        "description": "Test description",
        "meta_data": {"key": "value"},
    }

    # Act
    response = client.post("/api/v1/datasets/", json=test_payload)

    # Assert
    assert (
        response.status_code == 201
    ), f"Response status code was {response.status_code}"
    data = response.json()
    assert data["id"] == "dummy-id"
    assert data["name"] == "Test Dataset"
    assert data["description"] == "Test description"
    assert data["metaData"] == {"key": "value"}


def test_get_dataset_api_interface(client, patch_dataset_repository):
    """
    DatasetRepositorySQLAlchemy の get_by_id をモックして、GET /api/v1/datasets/{dataset_id} のエンドポイントの
    正常な動作を検証するテスト
    """
    # Arrange
    dummy_dataset = Dataset(
        id="dummy-id",
        name="Test Dataset",
        description="Test description",
        meta_data={"key": "value"},
        created_at=datetime(2025, 4, 10, 0, 0),
        updated_at=datetime(2025, 4, 10, 0, 0),
    )
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_by_id.return_value = dummy_dataset
    patch_dataset_repository.return_value = mock_repo_instance

    # Act
    response = client.get("/api/v1/datasets/dummy-id")

    # Assert
    assert (
        response.status_code == 200
    ), f"Response status code was {response.status_code}"
    data = response.json()
    assert data["id"] == "dummy-id"
    assert data["name"] == "Test Dataset"
    assert data["description"] == "Test description"
    assert data["metaData"] == {"key": "value"}


def test_get_dataset_not_found_api_interface(client, patch_dataset_repository):
    """
    DatasetRepositorySQLAlchemy の get_by_id をモックして、対象のデータセットが存在しない場合の
    GET /api/v1/datasets/{dataset_id} の挙動（404）を検証するテスト
    """
    # Arrange
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_by_id.return_value = None
    patch_dataset_repository.return_value = mock_repo_instance

    # Act
    response = client.get("/api/v1/datasets/nonexistent-id")

    # Assert
    assert (
        response.status_code == 404
    ), f"Response status code was {response.status_code}"
    data = response.json()
    assert data["detail"] == "Dataset not found"


def test_update_dataset_api_interface(client, patch_dataset_repository):
    """
    DatasetRepositorySQLAlchemy の update をモックして、PUT /api/v1/datasets/{dataset_id} の
    正常な動作を検証するテスト
    """
    # Arrange
    dummy_updated = Dataset(
        id="dummy-id",
        name="Updated Dataset",
        description="Updated description",
        meta_data={"key": "updated_value"},
        created_at=datetime(2025, 4, 10, 0, 0),
        updated_at=datetime(2025, 4, 10, 12, 0),
    )
    mock_repo_instance = MagicMock()
    mock_repo_instance.update.return_value = dummy_updated
    patch_dataset_repository.return_value = mock_repo_instance

    payload = {
        "name": "Updated Dataset",
        "description": "Updated description",
        "meta_data": {"key": "updated_value"},
    }

    # Act
    response = client.put("/api/v1/datasets/dummy-id", json=payload)

    # Assert
    assert (
        response.status_code == 200
    ), f"Response status code was {response.status_code}"
    data = response.json()
    assert data["id"] == "dummy-id"
    assert data["name"] == "Updated Dataset"
    assert data["description"] == "Updated description"
    assert data["metaData"] == {"key": "updated_value"}


def test_delete_dataset_api_interface_success(client, patch_dataset_repository):
    """
    DatasetRepositorySQLAlchemy の delete をモックして、DELETE /api/v1/datasets/{dataset_id} の
    正常な動作（削除成功時）を検証するテスト
    """
    # Arrange
    mock_repo_instance = MagicMock()
    # 削除成功時は True を返す
    mock_repo_instance.delete.return_value = True
    patch_dataset_repository.return_value = mock_repo_instance

    # Act
    response = client.delete("/api/v1/datasets/dummy-id")

    # Assert: 204 No Content を返す
    assert (
        response.status_code == 204
    ), f"Response status code was {response.status_code}"
    assert response.content == b""  # レスポンスボディは空


def test_delete_dataset_api_interface_not_found(client, patch_dataset_repository):
    """
    DatasetRepositorySQLAlchemy の delete をモックして、対象データセットが存在しない場合の
    DELETE /api/v1/datasets/{dataset_id} の挙動（404）を検証するテスト
    """
    # Arrange
    mock_repo_instance = MagicMock()
    # 存在しない場合は False を返す
    mock_repo_instance.delete.return_value = False
    patch_dataset_repository.return_value = mock_repo_instance

    # Act
    response = client.delete("/api/v1/datasets/nonexistent-id")

    # Assert
    assert (
        response.status_code == 404
    ), f"Response status code was {response.status_code}"
    data = response.json()
    assert data["detail"] == "Dataset not found"
