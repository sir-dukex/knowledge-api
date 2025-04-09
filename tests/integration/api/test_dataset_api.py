from fastapi.testclient import TestClient

from app.main import app

# 同期的なテストクライアントを生成
client = TestClient(app)


def test_create_dataset():
    test_data = {
        "name": "Dataset To Create",
        "description": "This is a test dataset",
        "meta_data": {"test": True},
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
        "name": "Dataset For List Test",
        "description": "This dataset is for testing list",
        "meta_data": {"info": "list_get_test"},
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


def test_update_dataset():
    # 作成して更新対象のデータセットを用意
    create_payload = {
        "name": "Dataset To Update",
        "description": "Before update",
        "meta_data": {"info": "original"},
    }
    create_resp = client.post("/api/v1/datasets/", json=create_payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    dataset_id = created["id"]

    # 更新用のペイロード（ここでは作成時のスキーマをそのまま利用していますが、更新専用のスキーマを定義するのが望ましい）
    update_payload = {
        "name": "Dataset Updated",
        "description": "After update",
        "meta_data": {"info": "updated"},
    }
    update_resp = client.put(f"/api/v1/datasets/{dataset_id}", json=update_payload)
    assert update_resp.status_code == 200
    updated_data = update_resp.json()
    assert updated_data["id"] == dataset_id
    assert updated_data["name"] == "Dataset Updated"
    assert updated_data["description"] == "After update"
    assert updated_data["meta_data"] == {"info": "updated"}

    # GET で更新結果を確認
    get_resp = client.get(f"/api/v1/datasets/{dataset_id}")
    assert get_resp.status_code == 200
    get_data = get_resp.json()
    assert get_data["name"] == "Dataset Updated"
    assert get_data["description"] == "After update"
    assert get_data["meta_data"] == {"info": "updated"}


def test_delete_dataset():
    # 削除対象のデータセットを作成
    create_payload = {
        "name": "Dataset To Delete",
        "description": "Will be deleted",
        "meta_data": {"info": "delete"},
    }
    create_resp = client.post("/api/v1/datasets/", json=create_payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    dataset_id = created["id"]

    # DELETE エンドポイントの呼び出し
    delete_resp = client.delete(f"/api/v1/datasets/{dataset_id}")
    assert delete_resp.status_code == 204
    assert delete_resp.content == b""  # レスポンスボディが空

    # GET で存在しないことを確認
    get_resp = client.get(f"/api/v1/datasets/{dataset_id}")
    assert get_resp.status_code == 404
    get_data = get_resp.json()
    assert get_data["detail"] == "Dataset not found"
