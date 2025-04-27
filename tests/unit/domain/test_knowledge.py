from datetime import datetime

from app.domain.entities.knowledge import Knowledge


def test_create_knowledge_default():
    """
    Knowledge.create() のデフォルト値（is_active=True）を検証
    """
    knowledge = Knowledge.create(
        document_id="doc-1",
        sequence=1,
        knowledge_text="テストナレッジ",
    )
    assert knowledge.document_id == "doc-1"
    assert knowledge.sequence == 1
    assert knowledge.knowledge_text == "テストナレッジ"
    assert knowledge.meta_data == {}
    assert knowledge.is_active is True
    assert isinstance(knowledge.created_at, datetime)
    assert isinstance(knowledge.updated_at, datetime)


def test_create_knowledge_inactive():
    """
    is_active=FalseでKnowledgeを生成した場合の検証
    """
    knowledge = Knowledge.create(
        document_id="doc-2",
        sequence=2,
        knowledge_text="無効ナレッジ",
        is_active=False,
    )
    assert knowledge.is_active is False
