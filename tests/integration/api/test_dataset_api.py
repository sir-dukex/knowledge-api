from fastapi.testclient import TestClient
from app.main import app

# 同期的なテストクライアントを生成
client = TestClient(app)

def test_create_dataset():
    test_data = {
        "name": "統合テスト用データセット",
        "description": "APIテスト用",
        "meta_data": {"test": True}
    }
    response = client.post("/api/v1/datasets/", json=test_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == test_data["name"]
    assert response_data["description"] == test_data["description"]
    assert response_data["meta_data"] == test_data["meta_data"]
    assert "id" in response_data

def test_list_datasets_and_get_dataset():
    # まずは新規作成してデータが存在する状態を用意
    test_data = {
        "name": "一覧・個別取得テスト",
        "description": "テストデータ作成",
        "meta_data": {"info": "list_get_test"}
    }
    create_response = client.post("/api/v1/datasets/", json=test_data)
    assert create_response.status_code == 201
    created_dataset = create_response.json()
    dataset_id = created_dataset["id"]

    # 一覧取得のテスト
    list_response = client.get("/api/v1/datasets/")
    assert list_response.status_code == 200
    list_data = list_response.json()
    # 戻り値は DatasetListResponse として items と total を返す
    assert "items" in list_data
    assert "total" in list_data
    # 作成したデータが一覧に含まれているか確認
    matching = [ds for ds in list_data["items"] if ds["id"] == dataset_id]
    assert len(matching) == 1, "一覧に作成したデータが存在するはずです"

    # 個別取得のテスト (正常系)
    get_response = client.get(f"/api/v1/datasets/{dataset_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["id"] == dataset_id
    assert get_data["name"] == test_data["name"]
    assert get_data["description"] == test_data["description"]
    assert get_data["meta_data"] == test_data["meta_data"]

def test_get_dataset_not_found():
    response = client.get("/api/v1/datasets/nonexistent-id")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == "Dataset not found"
