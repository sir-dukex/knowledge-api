from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """
    テスト用FastAPIクライアント
    docker-compose 等を通じて実際のSQL Serverが起動している前提
    """
    return TestClient(app)


def create_dataset(client, name: str) -> dict:
    """
    データセットを作成して結果を返すヘルパー関数
    """
    payload = {
        "name": name,
        "description": f"Integration test dataset for {name}",
        "meta_data": {},
    }
    resp = client.post("/api/v1/datasets/", json=payload)
    assert resp.status_code == 201
    return resp.json()  # { "id": "...", "name": "...", ... }


def create_document(client, dataset_id: str = None, is_active: bool = True) -> dict:
    """
    ドキュメントを作成して結果を返すヘルパー関数

    dataset_id が指定されていなければ None を渡すことで
    DocumentCreateUseCase 内で自動的に Dataset を作成する。
    is_activeは明示的に指定可能
    """
    payload = {
        # 存在しない or None でもキーは送ってみる
        "dataset_id": dataset_id if dataset_id else "",
        "title": f"Test Document {uuid4()}",
        "content": "This is a test document content.",
        "meta_data": {"test_key": "test_value"},
        "is_active": is_active,
    }
    resp = client.post("/api/v1/documents/", json=payload)
    assert resp.status_code == 201
    return resp.json()  # { "id": "...", "dataset_id": "...", "title": "...", ... }


def test_create_document_with_existing_dataset(client):
    """
    すでに存在するDatasetに紐づくドキュメントを作成するケースの統合テスト
    """
    # 1) まずデータセットを作成
    dataset_resp = create_dataset(client, "ExistingDatasetCase")
    dataset_id = dataset_resp["id"]

    # 2) そのdatasetに紐づくDocumentを作成
    doc_resp = create_document(client, dataset_id=dataset_id)
    assert doc_resp["datasetId"] == dataset_id
    assert "Test Document" in doc_resp["title"]
    assert doc_resp["metaData"]["test_key"] == "test_value"
    assert doc_resp["isActive"] is True

    # isActive=Falseで作成
    doc_resp2 = create_document(client, dataset_id=dataset_id, is_active=False)
    assert doc_resp2["isActive"] is False


def test_create_document_with_no_dataset(client):
    """
    存在しないDatasetを指定、またはdataset_idを空で渡した場合に
    Document作成時にDatasetが自動生成されるケースの統合テスト
    """
    # dataset_idを渡さない（None / ""）ことで、自動生成を試す
    doc_resp = create_document(client, dataset_id=None)

    # Documentが正常に返ってきたのでステータスコード201は通過済み
    # dataset_id が自動生成されていることを確認
    auto_dataset_id = doc_resp["datasetId"]
    assert auto_dataset_id is not None and auto_dataset_id != ""

    # 念のため、Documentの内容も確認
    assert "Test Document" in doc_resp["title"]
    assert doc_resp["metaData"]["test_key"] == "test_value"
    assert doc_resp["isActive"] is True

    # isActive=Falseで作成
    doc_resp2 = create_document(client, dataset_id=None, is_active=False)
    assert doc_resp2["isActive"] is False


def test_get_document(client):
    """
    Documentを作成後、そのDocumentをGETで取得するケース
    """
    # まずDataset & Documentを作る
    dataset_resp = create_dataset(client, "GetDocumentCase")
    doc_resp = create_document(client, dataset_id=dataset_resp["id"])
    doc_id = doc_resp["id"]

    # GET /api/v1/documents/{document_id}
    resp = client.get(f"/api/v1/documents/{doc_id}")
    assert resp.status_code == 200
    get_data = resp.json()
    assert get_data["id"] == doc_id
    assert get_data["title"] == doc_resp["title"]
    assert get_data["isActive"] is True


def test_update_document(client):
    """
    Documentを作成後、PUT で更新するケース
    """
    dataset_resp = create_dataset(client, "UpdateDocumentCase")
    doc_resp = create_document(client, dataset_id=dataset_resp["id"])
    doc_id = doc_resp["id"]

    update_payload = {
        "title": "Updated Title",
        "content": "Updated content",
        "meta_data": {"updated": True},
        "is_active": False,
    }
    resp = client.put(f"/api/v1/documents/{doc_id}", json=update_payload)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["id"] == doc_id
    assert updated["title"] == "Updated Title"
    assert updated["content"] == "Updated content"
    assert updated["metaData"]["updated"] is True
    assert updated["isActive"] is False


def test_delete_document(client):
    """
    Documentを作成後、DELETE で削除するケース
    """
    dataset_resp = create_dataset(client, "DeleteDocumentCase")
    doc_resp = create_document(client, dataset_id=dataset_resp["id"])
    doc_id = doc_resp["id"]

    # DELETE /api/v1/documents/{document_id}
    resp = client.delete(f"/api/v1/documents/{doc_id}")
    assert resp.status_code == 204

    # 念のため GET を試して 404 になることを確認
    resp_get = client.get(f"/api/v1/documents/{doc_id}")
    assert resp_get.status_code == 404
