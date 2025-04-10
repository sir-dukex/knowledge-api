from datetime import datetime

from app.domain.entities.document import Document
from app.domain.repositories.document_repository import DocumentRepository


class UpdateDocumentUseCase:
    """
    ドキュメント更新ユースケース

    指定されたIDのドキュメントを更新します。
    """

    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def execute(
        self, document_id: str, title: str, content: str, meta_data: dict
    ) -> Document:
        """
        ドキュメントを更新する

        Args:
            document_id (str): 更新対象のドキュメントID
            title (str): 更新するタイトル
            content (str): 更新する本文
            meta_data (dict): 更新するメタ情報

        Returns:
            Document: 更新後のドキュメントエンティティ

        ※ 注意: 既存の dataset_id や created_at はリポジトリ側で保持または補完する設計とします。
        """
        # ここでは created_at は更新せず、updated_at に現在時刻を設定
        updated_document = Document(
            id=document_id,
            dataset_id=None,  # dataset_id の更新が不要なら、repository側で既存情報を使用する前提
            title=title,
            content=content,
            meta_data=meta_data,
            created_at=None,  # 既存の作成日時は repository 側で補完（もしくは既存値をそのまま利用）
            updated_at=datetime.now(),
        )
        return self.document_repository.update(updated_document)
