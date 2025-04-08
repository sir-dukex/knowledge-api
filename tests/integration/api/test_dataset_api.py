import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_dataset():
    # テストクライアントの準備
    async with AsyncClient(app=app, base_url="http://test") as client:
        # テストデータ
        test_data = {
            "name": "統合テスト用データセット",
            "description": "APIテスト用",
            "meta_data": {"test": True}
        }
        
        # APIエンドポイントを呼び出し
        response = client.post("/api/v1/datasets/", json=test_data)
        
        # 検証
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["name"] == test_data["name"]
        assert response_data["description"] == test_data["description"]
        assert response_data["meta_data"] == test_data["meta_data"]
        assert "id" in response_data