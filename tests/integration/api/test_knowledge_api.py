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


def create_knowledge(client, document_id: str, sequence: int = 1, is_active: bool = True) -> dict:
    """
    Knowledge（ナレッジ情報）を作成して結果を返すヘルパー関数
    """
    payload = {
        "document_id": document_id,
        "sequence": sequence,
        "knowledge_text": f"Test knowledge text {sequence}",
        "meta_data": {"test_key": "test_value"},
        "is_active": is_active,
    }
    resp = client.post("/api/v1/knowledges/", json=payload)
    assert resp.status_code == 201
    return resp.json()


def test_create_knowledge(client):
    """
    Knowledge（ナレッジ情報）を新規作成する統合テスト
    """
    dataset = create_dataset(client, "KnowledgeCreateCase")
    document = create_document(client, dataset_id=dataset["id"])
    knowledge = create_knowledge(client, document_id=document["id"], sequence=1)
    assert knowledge["documentId"] == document["id"]
    assert knowledge["sequence"] == 1
    assert "Test knowledge text" in knowledge["knowledgeText"]
    assert knowledge["metaData"]["test_key"] == "test_value"
    assert knowledge["isActive"] is True

    # isActive=Falseで作成
    knowledge2 = create_knowledge(client, document_id=document["id"], sequence=2, is_active=False)
    assert knowledge2["isActive"] is False


def test_get_knowledge(client):
    """
    Knowledgeを作成後、そのKnowledgeをGETで取得するケース
    """
    dataset = create_dataset(client, "KnowledgeGetCase")
    document = create_document(client, dataset_id=dataset["id"])
    knowledge = create_knowledge(client, document_id=document["id"], sequence=2)
    knowledge_id = knowledge["id"]

    resp = client.get(f"/api/v1/knowledges/{knowledge_id}")
    assert resp.status_code == 200
    get_data = resp.json()
    assert get_data["id"] == knowledge_id
    assert get_data["sequence"] == 2
    assert get_data["isActive"] is True


def test_list_knowledges(client):
    """
    Knowledgeを複数作成し、リスト取得するケース
    """
    dataset = create_dataset(client, "KnowledgeListCase")
    document = create_document(client, dataset_id=dataset["id"])
    # 3つ分作成
    for i in range(1, 4):
        create_knowledge(client, document_id=document["id"], sequence=i, is_active=(i % 2 == 0))

    resp = client.get(f"/api/v1/knowledges/?document_id={document['id']}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3
    sequences = [item["sequence"] for item in data["items"]]
    assert set(sequences) == {1, 2, 3}
    # is_activeの値も検証
    for i, item in enumerate(sorted(data["items"], key=lambda x: x["sequence"]), 1):
        assert item["isActive"] == (i % 2 == 0)


def test_update_knowledge(client):
    """
    Knowledgeを作成後、PUTで更新するケース
    """
    dataset = create_dataset(client, "KnowledgeUpdateCase")
    document = create_document(client, dataset_id=dataset["id"])
    knowledge = create_knowledge(client, document_id=document["id"], sequence=5)
    knowledge_id = knowledge["id"]

    update_payload = {
        "sequence": 10,
        "knowledge_text": "Updated knowledge text",
        "meta_data": {"updated": True},
        "is_active": False,
    }
    resp = client.put(f"/api/v1/knowledges/{knowledge_id}", json=update_payload)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["id"] == knowledge_id
    assert updated["sequence"] == 10
    assert updated["knowledgeText"] == "Updated knowledge text"
    assert updated["metaData"]["updated"] is True
    assert updated["isActive"] is False


def test_delete_knowledge(client):
    """
    Knowledgeを作成後、DELETEで削除するケース
    """
    dataset = create_dataset(client, "KnowledgeDeleteCase")
    document = create_document(client, dataset_id=dataset["id"])
    knowledge = create_knowledge(client, document_id=document["id"], sequence=7)
    knowledge_id = knowledge["id"]

    resp = client.delete(f"/api/v1/knowledges/{knowledge_id}")
    assert resp.status_code == 204

    # 念のため GET を試して 404 になることを確認
    resp_get = client.get(f"/api/v1/knowledges/{knowledge_id}")
    assert resp_get.status_code == 404
