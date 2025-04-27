from datetime import datetime

import pytest

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
        assert dataset.is_active is True  # デフォルトはTrue
        assert isinstance(dataset.created_at, datetime)
        assert isinstance(dataset.updated_at, datetime)
        assert dataset.id is None  # IDは保存時に割り当てられる

    def test_create_dataset_inactive(self):
        # is_active=Falseで生成
        name = "無効データセット"
        description = "無効説明"
        meta_data = {"key": "value2"}
        dataset = Dataset.create(name, description, meta_data, is_active=False)
        assert dataset.is_active is False
