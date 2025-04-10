from typing import List

from app.domain.entities.document import Document
from app.domain.repositories.document_repository import DocumentRepository


class ListDocumentsUseCase:
    """
    ドキュメント一覧取得ユースケース

    指定されたデータセットに属するドキュメントの一覧を取得します。
    """

    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    def execute(
        self, dataset_id: str, skip: int = 0, limit: int = 100
    ) -> List[Document]:
        """
        ドキュメント一覧を取得する

        Args:
            dataset_id (str): データセットのID
            skip (int, optional): スキップする件数。デフォルトは 0
            limit (int, optional): 取得件数の上限。デフォルトは 100

        Returns:
            List[Document]: 取得したドキュメントエンティティのリスト
        """
        return self.document_repository.list_documents(
            dataset_id, skip=skip, limit=limit
        )
