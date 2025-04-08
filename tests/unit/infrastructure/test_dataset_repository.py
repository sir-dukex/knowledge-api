import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.dataset import Dataset
from app.infrastructure.repositories.dataset_repository_impl import DatasetRepositorySQLAlchemy
from app.infrastructure.database.models.dataset import DatasetModel


class TestDatasetRepositorySQLAlchemy:
    @pytest.mark.asyncio
    async def test_create(self):
        # モックセッションの準備
        mock_session = AsyncMock(spec=AsyncSession)
        
        # テスト対象のリポジトリ
        repository = DatasetRepositorySQLAlchemy(mock_session)
        
        # テストデータ
        test_dataset = Dataset.create(
            name="テストデータセット",
            description="説明",
            meta_data={"key": "value"}
        )
        
        # 実行
        result = repository.create(test_dataset)
        
        # 検証
        assert mock_session.add.called
        assert mock_session.commit.called
        assert mock_session.refresh.called
        assert result.name == test_dataset.name