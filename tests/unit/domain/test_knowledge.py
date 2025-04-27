from datetime import datetime

from app.domain.entities.knowledge import Knowledge


def test_create_knowledge_default():
    """
    Knowledge.create() のデフォルト値（is_active=True）を検証
    """
    knowledge = Knowledge.create(
        document_id="doc-1",
        page_number=1,
        image_path="s3://bucket/1.png",
        page_text="テストページ",
    )
    assert knowledge.document_id == "doc-1"
    assert knowledge.page_number == 1
    assert knowledge.image_path == "s3://bucket/1.png"
    assert knowledge.page_text == "テストページ"
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
        page_number=2,
        image_path="s3://bucket/2.png",
        page_text="無効ページ",
        is_active=False,
    )
    assert knowledge.is_active is False
