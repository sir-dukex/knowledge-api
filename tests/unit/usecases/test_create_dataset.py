import pytest
from datetime import datetime
from unittest.mock import Mock
from app.domain.entities.dataset import Dataset
from app.usecases.datasets.create_dataset import CreateDatasetUseCase


class TestCreateDatasetUseCase:
    def test_execute(self):
        # モックの準備
        mock_repo = Mock()
        mock_repo.create.return_value = Dataset(
            id="test-id",
            name="テストデータセット",
            description="説明",
            meta_data={"key": "value"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # ユースケースの初期化
        usecase = CreateDatasetUseCase(mock_repo)
        
        # 実行
        result = usecase.execute(
            name="テストデータセット",
            description="説明",
            meta_data={"key": "value"}
        )
        
        # 検証
        assert result.id == "test-id"
        assert result.name == "テストデータセット"
        mock_repo.create.assert_called_once()
        # 渡されたデータセットの検証
        dataset_arg = mock_repo.create.call_args[0][0]
        assert dataset_arg.name == "テストデータセット"
        assert dataset_arg.description == "説明"