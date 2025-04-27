from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """
    テスト用FastAPIクライアント
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
    return resp.json()


def create_document(client, dataset_id: str) -> dict:
    """
    ドキュメントを作成して結果を返すヘルパー関数
    """
    payload = {
        "dataset_id": dataset_id,
        "title": f"Test Document {uuid4()}",
        "content": "This is a test document content.",
        "meta_data": {"test_key": "test_value"},
    }
    resp = client.post("/api/v1/documents/", json=payload)
    assert resp.status_code == 201
    return resp.json()


def create_knowledge(client, document_id: str, page_number: int = 1, is_active: bool = True) -> dict:
    """
    Knowledge（ページ情報）を作成して結果を返すヘルパー関数
    """
    payload = {
        "document_id": document_id,
        "page_number": page_number,
        "image_path": f"s3://test-bucket/{document_id}/{page_number}.png",
        "page_text": f"Test page text {page_number}",
        "meta_data": {"test_key": "test_value"},
        "is_active": is_active,
    }
    resp = client.post("/api/v1/knowledges/", json=payload)
    assert resp.status_code == 201
    return resp.json()


def test_create_knowledge(client):
    """
    Knowledge（ページ情報）を新規作成する統合テスト
    """
    dataset = create_dataset(client, "KnowledgeCreateCase")
    document = create_document(client, dataset_id=dataset["id"])
    knowledge = create_knowledge(client, document_id=document["id"], page_number=1)
    assert knowledge["document_id"] == document["id"]
    assert knowledge["page_number"] == 1
    assert "Test page text" in knowledge["page_text"]
    assert knowledge["meta_data"]["test_key"] == "test_value"
    assert knowledge["is_active"] is True

    # is_active=Falseで作成
    knowledge2 = create_knowledge(client, document_id=document["id"], page_number=2, is_active=False)
    assert knowledge2["is_active"] is False


def test_get_knowledge(client):
    """
    Knowledgeを作成後、そのKnowledgeをGETで取得するケース
    """
    dataset = create_dataset(client, "KnowledgeGetCase")
    document = create_document(client, dataset_id=dataset["id"])
    knowledge = create_knowledge(client, document_id=document["id"], page_number=2)
    knowledge_id = knowledge["id"]

    resp = client.get(f"/api/v1/knowledges/{knowledge_id}")
    assert resp.status_code == 200
    get_data = resp.json()
    assert get_data["id"] == knowledge_id
    assert get_data["page_number"] == 2
    assert get_data["is_active"] is True


def test_list_knowledges(client):
    """
    Knowledgeを複数作成し、リスト取得するケース
    """
    dataset = create_dataset(client, "KnowledgeListCase")
    document = create_document(client, dataset_id=dataset["id"])
    # 3ページ分作成
    for i in range(1, 4):
        create_knowledge(client, document_id=document["id"], page_number=i, is_active=(i % 2 == 0))

    resp = client.get(f"/api/v1/knowledges/?document_id={document['id']}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3
    page_numbers = [item["page_number"] for item in data["items"]]
    assert set(page_numbers) == {1, 2, 3}
    # is_activeの値も検証
    for i, item in enumerate(sorted(data["items"], key=lambda x: x["page_number"]), 1):
        assert item["is_active"] == (i % 2 == 0)


def test_update_knowledge(client):
    """
    Knowledgeを作成後、PUTで更新するケース
    """
    dataset = create_dataset(client, "KnowledgeUpdateCase")
    document = create_document(client, dataset_id=dataset["id"])
    knowledge = create_knowledge(client, document_id=document["id"], page_number=5)
    knowledge_id = knowledge["id"]

    update_payload = {
        "page_number": 10,
        "image_path": "s3://test-bucket/updated.png",
        "page_text": "Updated page text",
        "meta_data": {"updated": True},
        "is_active": False,
    }
    resp = client.put(f"/api/v1/knowledges/{knowledge_id}", json=update_payload)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["id"] == knowledge_id
    assert updated["page_number"] == 10
    assert updated["image_path"] == "s3://test-bucket/updated.png"
    assert updated["page_text"] == "Updated page text"
    assert updated["meta_data"]["updated"] is True
    assert updated["is_active"] is False


def test_delete_knowledge(client):
    """
    Knowledgeを作成後、DELETEで削除するケース
    """
    dataset = create_dataset(client, "KnowledgeDeleteCase")
    document = create_document(client, dataset_id=dataset["id"])
    knowledge = create_knowledge(client, document_id=document["id"], page_number=7)
    knowledge_id = knowledge["id"]

    resp = client.delete(f"/api/v1/knowledges/{knowledge_id}")
    assert resp.status_code == 204

    # 念のため GET を試して 404 になることを確認
    resp_get = client.get(f"/api/v1/knowledges/{knowledge_id}")
    assert resp_get.status_code == 404
