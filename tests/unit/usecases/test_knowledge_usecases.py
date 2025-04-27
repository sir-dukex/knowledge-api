from datetime import datetime
from unittest.mock import Mock

import pytest

from app.domain.entities.knowledge import Knowledge
from app.usecases.knowledges.create_knowledge import CreateKnowledgeUseCase
from app.usecases.knowledges.delete_knowledge import DeleteKnowledgeUseCase
from app.usecases.knowledges.get_knowledge import GetKnowledgeUseCase
from app.usecases.knowledges.list_knowledges import ListKnowledgesUseCase
from app.usecases.knowledges.update_knowledge import UpdateKnowledgeUseCase


class TestCreateKnowledgeUseCase:
    def test_execute_creates_knowledge(self):
        mock_repo = Mock()
        dummy_knowledge = Knowledge(
            id="k-123",
            document_id="doc-abc",
            sequence=1,
            knowledge_text="Test knowledge text",
            meta_data={"key": "value"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repo.create.return_value = dummy_knowledge

        usecase = CreateKnowledgeUseCase(mock_repo)
        result = usecase.execute(
            document_id="doc-abc",
            sequence=1,
            knowledge_text="Test knowledge text",
            meta_data={"key": "value"},
        )
        mock_repo.create.assert_called_once()
        assert result.id == "k-123"
        assert result.document_id == "doc-abc"
        assert result.sequence == 1


class TestUpdateKnowledgeUseCase:
    def test_execute_updates_knowledge(self):
        mock_repo = Mock()
        updated_knowledge = Knowledge(
            id="k-456",
            document_id="doc-abc",
            sequence=2,
            knowledge_text="Updated text",
            meta_data={"key": "updated"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repo.update.return_value = updated_knowledge

        usecase = UpdateKnowledgeUseCase(mock_repo)
        result = usecase.execute(updated_knowledge)
        mock_repo.update.assert_called_once()
        assert result.id == "k-456"
        assert result.sequence == 2
        assert result.knowledge_text == "Updated text"


class TestDeleteKnowledgeUseCase:
    def test_execute_success(self):
        mock_repo = Mock()
        mock_repo.delete.return_value = True
        usecase = DeleteKnowledgeUseCase(mock_repo)

        result = usecase.execute("k-789")
        mock_repo.delete.assert_called_once_with("k-789")
        assert result is True

    def test_execute_failure(self):
        mock_repo = Mock()
        mock_repo.delete.return_value = False
        usecase = DeleteKnowledgeUseCase(mock_repo)

        result = usecase.execute("nonexistent-k")
        mock_repo.delete.assert_called_once_with("nonexistent-k")
        assert result is False


class TestListKnowledgesUseCase:
    def test_execute_returns_knowledges(self):
        mock_repo = Mock()
        k1 = Knowledge(
            id="k-1",
            document_id="doc-xyz",
            sequence=1,
            knowledge_text="Knowledge 1",
            meta_data={},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        k2 = Knowledge(
            id="k-2",
            document_id="doc-xyz",
            sequence=2,
            knowledge_text="Knowledge 2",
            meta_data={},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repo.list_knowledges.return_value = [k1, k2]
        usecase = ListKnowledgesUseCase(mock_repo)
        result = usecase.execute(document_id="doc-xyz", skip=0, limit=10)
        mock_repo.list_knowledges.assert_called_once_with("doc-xyz", 0, 10)
        assert len(result) == 2
        ids = [k.id for k in result]
        assert "k-1" in ids and "k-2" in ids


class TestGetKnowledgeUseCase:
    def test_execute_success(self):
        mock_repo = Mock()
        dummy_knowledge = Knowledge(
            id="k-001",
            document_id="doc-abc",
            sequence=1,
            knowledge_text="Some text",
            meta_data={"test": True},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = dummy_knowledge
        usecase = GetKnowledgeUseCase(mock_repo)
        result = usecase.execute("k-001")
        mock_repo.get_by_id.assert_called_once_with("k-001")
        assert result.id == "k-001"
        assert result.knowledge_text == "Some text"

    def test_execute_not_found(self):
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        usecase = GetKnowledgeUseCase(mock_repo)
        result = usecase.execute("nonexistent-k")
        mock_repo.get_by_id.assert_called_once_with("nonexistent-k")
        assert result is None
