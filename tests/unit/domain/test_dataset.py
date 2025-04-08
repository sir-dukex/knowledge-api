import pytest
from datetime import datetime
from app.domain.entities.dataset import Dataset


class TestDataset:
    def test_create_dataset(self):
        # 準備
        name = "テストデータセット"
        description = "テスト用の説明"
        meta_data = {"key": "value"}
        
        # 実行
        dataset = Dataset.create(name, description, meta_data)
        
        # 検証
        assert dataset.name == name
        assert dataset.description == description
        assert dataset.meta_data == meta_data
        assert isinstance(dataset.created_at, datetime)
        assert isinstance(dataset.updated_at, datetime)
        assert dataset.id is None  # IDは保存時に割り当てられる