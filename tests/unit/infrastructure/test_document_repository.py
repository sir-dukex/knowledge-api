import uuid
from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.entities.document import Document
from app.infrastructure.database.connection import Base
from app.infrastructure.repositories.document_repository_impl import (
    DocumentRepositorySQLAlchemy,
)


# テスト用のインメモリ SQLite エンジン・セッションを生成するフィクスチャ
@pytest.fixture(scope="function")
def test_session():
    # SQLite の in-memory DB を利用
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_create_document(test_session):
    """
    DocumentRepositorySQLAlchemy.create() のテスト
    新規ドキュメント作成時に、IDおよびタイムスタンプが正しく設定されることを検証します。
    """
    repo = DocumentRepositorySQLAlchemy(test_session)
    doc = Document.create(
        dataset_id="test-dataset-1",
        title="Test Document",
        content="This is a test document.",
        meta_data={"key": "value"},
    )
    result = repo.create(doc)
    # 登録後に ID, created_at, updated_at が設定される
    assert result.id is not None
    assert result.dataset_id == "test-dataset-1"
    assert result.title == "Test Document"
    assert result.content == "This is a test document."
    assert result.meta_data == {"key": "value"}
    assert isinstance(result.created_at, datetime)
    assert isinstance(result.updated_at, datetime)


def test_get_document(test_session):
    """
    DocumentRepositorySQLAlchemy.get_by_id() のテスト
    作成したドキュメントが get_by_id() によって正しく取得できることを検証します。
    """
    repo = DocumentRepositorySQLAlchemy(test_session)
    doc = Document.create(
        dataset_id="test-dataset-1",
        title="Test Document",
        content="Document content.",
        meta_data={"a": 1},
    )
    created = repo.create(doc)
    fetched = repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.title == "Test Document"
    assert fetched.content == "Document content."
    assert fetched.meta_data == {"a": 1}


def test_list_documents(test_session):
    """
    DocumentRepositorySQLAlchemy.list_documents() のテスト
    同一 dataset_id に属する複数のドキュメントを作成し、一覧取得できるか検証します。
    """
    repo = DocumentRepositorySQLAlchemy(test_session)
    docs = [
        Document.create(
            dataset_id="test-dataset-list",
            title=f"Doc {i}",
            content=f"Content {i}",
            meta_data={"num": i},
        )
        for i in range(3)
    ]
    for doc in docs:
        repo.create(doc)

    result = repo.list_documents(dataset_id="test-dataset-list", skip=0, limit=10)
    assert len(result) == 3
    titles = {d.title for d in result}
    expected_titles = {"Doc 0", "Doc 1", "Doc 2"}
    assert titles == expected_titles


def test_update_document(test_session):
    """
    DocumentRepositorySQLAlchemy.update() のテスト
    作成後、ドキュメントの情報を更新し、更新された内容および updated_at が反映されることを検証します。
    """
    repo = DocumentRepositorySQLAlchemy(test_session)
    doc = Document.create(
        dataset_id="test-dataset-update",
        title="Old Title",
        content="Old Content",
        meta_data={"old": True},
    )
    created = repo.create(doc)
    # 更新用入力：更新後の情報を含むエンティティを作成（created_at は repository 側で補完）
    updated_input = Document(
        id=created.id,
        dataset_id=created.dataset_id,
        title="New Title",
        content="New Content",
        meta_data={"new": True},
        created_at=None,
        updated_at=datetime.now(),
    )
    updated = repo.update(updated_input)
    assert updated.id == created.id
    assert updated.title == "New Title"
    assert updated.content == "New Content"
    assert updated.meta_data == {"new": True}
    assert updated.updated_at > created.updated_at


def test_delete_document(test_session):
    """
    DocumentRepositorySQLAlchemy.delete() のテスト
    作成したドキュメントを削除し、その後 get_by_id() で取得できなくなることを検証します。
    """
    repo = DocumentRepositorySQLAlchemy(test_session)
    doc = Document.create(
        dataset_id="test-dataset-delete",
        title="Delete Document",
        content="Content to delete",
        meta_data={},
    )
    created = repo.create(doc)
    success = repo.delete(created.id)
    assert success is True
    fetched = repo.get_by_id(created.id)
    assert fetched is None
