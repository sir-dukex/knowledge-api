from app.domain.entities.document import Document
from app.domain.repositories.document_repository import DocumentRepository


class GetDocumentUseCase:
    """
    ドキュメント取得ユースケース

    指定されたIDのドキュメントを取得し、存在しなければ ValueError を発生させます。
    """

    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def execute(self, document_id: str) -> Document:
        document = self.document_repository.get_by_id(document_id)
        if not document:
            raise ValueError("Document not found")
        return document
