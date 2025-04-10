from datetime import datetime
from unittest.mock import Mock

import pytest

from app.domain.entities.document import Document
from app.usecases.documents.create_document import CreateDocumentUseCase
from app.usecases.documents.delete_document import DeleteDocumentUseCase
from app.usecases.documents.get_document import GetDocumentUseCase
from app.usecases.documents.list_documents import ListDocumentsUseCase
from app.usecases.documents.update_document import UpdateDocumentUseCase


class TestCreateDocumentUseCase:
    def test_execute_creates_document(self):
        # モックの準備
        mock_repo = Mock()
        # dataset_repository も同じモックで簡略化
        dummy_doc = Document(
            id="doc-123",
            dataset_id="dataset-abc",
            title="Sample Document",
            content="This is a sample document.",
            meta_data={"key": "value"},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        # repository.create() の戻り値を設定
        mock_repo.create.return_value = dummy_doc

        # ユースケースのインスタンスを、document_repository と dataset_repository に同じモックを渡す
        usecase = CreateDocumentUseCase(
            document_repository=mock_repo, dataset_repository=mock_repo
        )
        # dataset_id を指定している場合は、存在確認ロジックがあるとしても、
        # モックにより dummy_doc が返る想定でテストを進めます。
        result = usecase.execute(
            dataset_id="dataset-abc",
            title="Sample Document",
            content="This is a sample document.",
            meta_data={"key": "value"},
        )
        mock_repo.create.assert_called_once()
        assert result.id == "doc-123"
        assert result.title == "Sample Document"
        assert result.dataset_id == "dataset-abc"


class TestUpdateDocumentUseCase:
    def test_execute_updates_document(self):
        mock_repo = Mock()
        updated_doc = Document(
            id="doc-456",
            dataset_id="dataset-abc",
            title="Updated Title",
            content="Updated content",
            meta_data={"key": "updated"},
            created_at=datetime.now(),  # 既存の作成日時（このテストでは詳細に比較しなくてもOK）
            updated_at=datetime.now(),
        )
        mock_repo.update.return_value = updated_doc

        usecase = UpdateDocumentUseCase(mock_repo)
        result = usecase.execute(
            document_id="doc-456",
            title="Updated Title",
            content="Updated content",
            meta_data={"key": "updated"},
        )
        mock_repo.update.assert_called_once()
        assert result.id == "doc-456"
        assert result.title == "Updated Title"
        assert result.content == "Updated content"


class TestDeleteDocumentUseCase:
    def test_execute_success(self):
        mock_repo = Mock()
        mock_repo.delete.return_value = True
        usecase = DeleteDocumentUseCase(mock_repo)

        result = usecase.execute("doc-789")
        mock_repo.delete.assert_called_once_with("doc-789")
        assert result is True

    def test_execute_failure(self):
        mock_repo = Mock()
        mock_repo.delete.return_value = False
        usecase = DeleteDocumentUseCase(mock_repo)

        result = usecase.execute("nonexistent-doc")
        mock_repo.delete.assert_called_once_with("nonexistent-doc")
        assert result is False


class TestListDocumentsUseCase:
    def test_execute_returns_documents(self):
        mock_repo = Mock()
        doc1 = Document(
            id="doc-1",
            dataset_id="dataset-xyz",
            title="Doc 1",
            content="Content 1",
            meta_data={},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        doc2 = Document(
            id="doc-2",
            dataset_id="dataset-xyz",
            title="Doc 2",
            content="Content 2",
            meta_data={},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repo.list_documents.return_value = [doc1, doc2]
        usecase = ListDocumentsUseCase(mock_repo)
        result = usecase.execute(dataset_id="dataset-xyz", skip=0, limit=10)
        mock_repo.list_documents.assert_called_once_with(
            "dataset-xyz", skip=0, limit=10
        )
        assert len(result) == 2
        ids = [doc.id for doc in result]
        assert "doc-1" in ids and "doc-2" in ids


class TestGetDocumentUseCase:
    def test_execute_success(self):
        mock_repo = Mock()
        dummy_doc = Document(
            id="doc-001",
            dataset_id="dataset-abc",
            title="Existing Document",
            content="Some content",
            meta_data={"test": True},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_repo.get_by_id.return_value = dummy_doc
        usecase = GetDocumentUseCase(mock_repo)
        result = usecase.execute("doc-001")
        mock_repo.get_by_id.assert_called_once_with("doc-001")
        assert result.id == "doc-001"
        assert result.title == "Existing Document"

    def test_execute_not_found(self):
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = None
        usecase = GetDocumentUseCase(mock_repo)
        with pytest.raises(ValueError, match="Document not found"):
            usecase.execute("nonexistent-doc")
