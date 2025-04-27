from datetime import datetime, timedelta

from app.domain.entities.document import Document


def test_create_document_default_metadata():
    """
    Document.create() でメタデータを省略した場合、meta_data が空の辞書となり、
    created_at と updated_at に現在時刻が設定されることを検証します。
    """
    doc = Document.create(
        dataset_id="dataset-123", title="Test Title", content="Test content"
    )
    assert doc.dataset_id == "dataset-123"
    assert doc.title == "Test Title"
    assert doc.content == "Test content"
    # created_at, updated_at が datetime 型であることの確認
    assert isinstance(doc.created_at, datetime)
    assert isinstance(doc.updated_at, datetime)
    # meta_data の初期値が {} であることを検証
    assert doc.meta_data == {}
    # is_activeのデフォルトはTrue
    assert doc.is_active is True


def test_create_document_with_metadata():
    """
    Document.create() に meta_data を指定した場合、入力した値が反映されることを検証します。
    """
    meta = {"author": "Tester", "views": 100}
    doc = Document.create(
        dataset_id="dataset-456",
        title="Another Title",
        content="Some content",
        meta_data=meta,
    )
    assert doc.dataset_id == "dataset-456"
    assert doc.title == "Another Title"
    assert doc.content == "Some content"
    assert doc.meta_data == meta
    assert doc.is_active is True


def test_document_timestamp_order():
    """
    作成時に生成される created_at と updated_at の差がごくわずかであることを検証します。
    """
    doc = Document.create(
        dataset_id="dataset-789", title="Check Timestamp", content="Test content"
    )
    # 生成直後はほぼ同一時刻になっているはず
    delta = doc.updated_at - doc.created_at
    # 差が1秒未満であればOK（環境によって微妙なずれが出る可能性があるため）
    assert delta < timedelta(seconds=1)

def test_create_document_inactive():
    """
    is_active=Falseで生成した場合の検証
    """
    doc = Document.create(
        dataset_id="dataset-999", title="Inactive", content="Inactive content", is_active=False
    )
    assert doc.is_active is False
