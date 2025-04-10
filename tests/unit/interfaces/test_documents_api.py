from datetime import datetime
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.domain.entities.document import Document
from app.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture
def dummy_document():
    return Document(
        id="doc-123",
        dataset_id="dataset-123",
        title="Sample Document",
        content="Sample content",
        meta_data={"test": True},
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def test_create_document_api(client, dummy_document):
    """
    Document作成APIのテスト。
    実際のCreateDocumentUseCaseとリポジトリ生成をモック化することで、
    dataset_repositoryの不足エラーなどを回避し、引数の検証を行う。
    """
    with patch(
        "app.interfaces.api.v1.documents.DocumentRepositorySQLAlchemy"
    ) as mock_document_repo, patch(
        "app.interfaces.api.v1.documents.DatasetRepositorySQLAlchemy"
    ) as mock_dataset_repo, patch(
        "app.interfaces.api.v1.documents.CreateDocumentUseCase"
    ) as mock_create_doc:

        # UseCaseのインスタンスを取得し、そのexecuteメソッドの戻り値をモック化
        instance = mock_create_doc.return_value
        instance.execute.return_value = dummy_document

        payload = {
            "dataset_id": "dataset-123",
            "title": "Sample Document",
            "content": "Sample content",
            "meta_data": {"test": True},
        }

        response = client.post("/api/v1/documents/", json=payload)
        assert response.status_code == 201

        result = response.json()
        assert result["id"] == "doc-123"
        assert result["title"] == "Sample Document"

        # CreateDocumentUseCase( document_repository=..., dataset_repository=... ) への引数を確認
        mock_create_doc.assert_called_once_with(
            document_repository=mock_document_repo.return_value,
            dataset_repository=mock_dataset_repo.return_value,
        )
        # execute(...) 呼び出しの引数を確認
        instance.execute.assert_called_once_with(
            dataset_id="dataset-123",
            title="Sample Document",
            content="Sample content",
            meta_data={"test": True},
        )


def test_get_document_api(client, dummy_document):
    with patch(
        "app.interfaces.api.v1.documents.GetDocumentUseCase.execute"
    ) as mock_usecase:
        mock_usecase.return_value = dummy_document
        response = client.get("/api/v1/documents/doc-123")

        assert response.status_code == 200
        result = response.json()
        assert result["id"] == "doc-123"
        mock_usecase.assert_called_once_with("doc-123")


def test_get_document_api_not_found(client):
    with patch(
        "app.interfaces.api.v1.documents.GetDocumentUseCase.execute"
    ) as mock_usecase:
        mock_usecase.side_effect = ValueError("Document not found")
        response = client.get("/api/v1/documents/nonexistent")

        assert response.status_code == 404
        assert response.json()["detail"] == "Document not found"
        mock_usecase.assert_called_once_with("nonexistent")


def test_update_document_api(client, dummy_document):
    with patch(
        "app.interfaces.api.v1.documents.UpdateDocumentUseCase.execute"
    ) as mock_usecase:
        mock_usecase.return_value = dummy_document
        payload = {
            "title": "Updated Document",
            "content": "Updated content",
            "meta_data": {"updated": True},
        }
        response = client.put("/api/v1/documents/doc-123", json=payload)

        assert response.status_code == 200
        result = response.json()
        assert result["id"] == "doc-123"
        mock_usecase.assert_called_once_with(
            document_id="doc-123",
            title="Updated Document",
            content="Updated content",
            meta_data={"updated": True},
        )


def test_delete_document_api(client):
    with patch(
        "app.interfaces.api.v1.documents.DeleteDocumentUseCase.execute"
    ) as mock_usecase:
        mock_usecase.return_value = True
        response = client.delete("/api/v1/documents/doc-123")

        assert response.status_code == 204
        mock_usecase.assert_called_once_with("doc-123")


def test_delete_document_api_not_found(client):
    with patch(
        "app.interfaces.api.v1.documents.DeleteDocumentUseCase.execute"
    ) as mock_usecase:
        mock_usecase.return_value = False
        response = client.delete("/api/v1/documents/nonexistent")

        assert response.status_code == 404
        mock_usecase.assert_called
