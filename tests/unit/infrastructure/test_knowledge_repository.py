import uuid
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.entities.knowledge import Knowledge
from app.domain.entities.document import Document
from app.infrastructure.database.connection import Base
from app.infrastructure.repositories.knowledge_repository_impl import (
    KnowledgeRepositorySQLAlchemy,
)
from app.infrastructure.repositories.document_repository_impl import (
    DocumentRepositorySQLAlchemy,
)


@pytest.fixture(scope="function")
def test_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_document_for_knowledge(session):
    repo = DocumentRepositorySQLAlchemy(session)
    doc = Document.create(
        dataset_id="test-dataset-knowledge",
        title="Doc for Knowledge",
        content="Doc content",
        meta_data={},
    )
    return repo.create(doc)


def test_create_knowledge(test_session):
    repo = KnowledgeRepositorySQLAlchemy(test_session)
    doc = create_document_for_knowledge(test_session)
    # is_active True
    knowledge = Knowledge.create(
        document_id=doc.id,
        page_number=1,
        image_path="s3://bucket/doc/1.png",
        page_text="Page 1 text",
        meta_data={"k": 1},
    )
    result = repo.create(knowledge)
    assert result.id is not None
    assert result.document_id == doc.id
    assert result.page_number == 1
    assert result.image_path == "s3://bucket/doc/1.png"
    assert result.page_text == "Page 1 text"
    assert result.meta_data == {"k": 1}
    assert result.is_active is True
    assert isinstance(result.created_at, datetime)
    assert isinstance(result.updated_at, datetime)
    # is_active False
    knowledge2 = Knowledge.create(
        document_id=doc.id,
        page_number=2,
        image_path="s3://bucket/doc/2.png",
        page_text="Inactive",
        meta_data={},
        is_active=False,
    )
    result2 = repo.create(knowledge2)
    assert result2.is_active is False


def test_get_knowledge(test_session):
    repo = KnowledgeRepositorySQLAlchemy(test_session)
    doc = create_document_for_knowledge(test_session)
    knowledge = Knowledge.create(
        document_id=doc.id,
        page_number=2,
        image_path="s3://bucket/doc/2.png",
        page_text="Page 2 text",
        meta_data={"k": 2},
        is_active=False,
    )
    created = repo.create(knowledge)
    fetched = repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.page_number == 2
    assert fetched.page_text == "Page 2 text"
    assert fetched.meta_data == {"k": 2}
    assert fetched.is_active is False


def test_list_knowledges(test_session):
    repo = KnowledgeRepositorySQLAlchemy(test_session)
    doc = create_document_for_knowledge(test_session)
    knowledges = [
        Knowledge.create(
            document_id=doc.id,
            page_number=i,
            image_path=f"s3://bucket/doc/{i}.png",
            page_text=f"Page {i} text",
            meta_data={"k": i},
            is_active=(i % 2 == 0),
        )
        for i in range(1, 4)
    ]
    for k in knowledges:
        repo.create(k)

    result = repo.list_knowledges(document_id=doc.id, skip=0, limit=10)
    assert len(result) == 3
    page_numbers = {k.page_number for k in result}
    assert page_numbers == {1, 2, 3}
    # is_activeの値も検証
    for i, k in enumerate(sorted(result, key=lambda x: x.page_number), 1):
        assert k.is_active == (i % 2 == 0)


def test_update_knowledge(test_session):
    repo = KnowledgeRepositorySQLAlchemy(test_session)
    doc = create_document_for_knowledge(test_session)
    knowledge = Knowledge.create(
        document_id=doc.id,
        page_number=5,
        image_path="s3://bucket/doc/5.png",
        page_text="Old text",
        meta_data={"old": True},
    )
    created = repo.create(knowledge)
    updated_input = Knowledge(
        id=created.id,
        document_id=created.document_id,
        page_number=10,
        image_path="s3://bucket/doc/updated.png",
        page_text="Updated text",
        meta_data={"new": True},
        is_active=False,
        created_at=None,
        updated_at=datetime.now(),
    )
    updated = repo.update(updated_input)
    assert updated.id == created.id
    assert updated.page_number == 10
    assert updated.image_path == "s3://bucket/doc/updated.png"
    assert updated.page_text == "Updated text"
    assert updated.meta_data == {"new": True}
    assert updated.is_active is False
    assert updated.updated_at > created.updated_at


def test_delete_knowledge(test_session):
    repo = KnowledgeRepositorySQLAlchemy(test_session)
    doc = create_document_for_knowledge(test_session)
    knowledge = Knowledge.create(
        document_id=doc.id,
        page_number=7,
        image_path="s3://bucket/doc/7.png",
        page_text="To delete",
        meta_data={},
    )
    created = repo.create(knowledge)
    success = repo.delete(created.id)
    assert success is True
    fetched = repo.get_by_id(created.id)
    assert fetched is None
