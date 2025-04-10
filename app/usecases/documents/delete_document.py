from app.domain.repositories.document_repository import DocumentRepository


class DeleteDocumentUseCase:
    """
    ドキュメント削除ユースケース

    指定されたIDのドキュメントを削除します。
    """

    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def execute(self, document_id: str) -> bool:
        """
        ドキュメントを削除する

        Args:
            document_id (str): 削除対象のドキュメントID

        Returns:
            bool: 削除成功なら True、存在しない場合は False
        """
        return self.document_repository.delete(document_id)
