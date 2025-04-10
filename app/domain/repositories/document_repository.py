from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.document import Document


class DocumentRepository(ABC):
    """ドキュメントリポジトリの抽象クラス

    このクラスは、ドキュメントの永続化に関するCRUD操作のインターフェースを定義します。
    実際の実装はインフラ層で行い、ドメイン層はこのインターフェースを利用してビジネスロジックを実装します。
    """

    @abstractmethod
    def create(self, document: Document) -> Document:
        """ドキュメントを作成する

        Args:
            document (Document): 作成するドキュメントエンティティ

        Returns:
            Document: 作成されたドキュメントエンティティ
        """
        pass

    @abstractmethod
    def get_by_id(self, document_id: str) -> Optional[Document]:
        """指定されたIDのドキュメントを取得する

        Args:
            document_id (str): 取得対象のドキュメントID

        Returns:
            Optional[Document]: ドキュメントが存在すればエンティティを、存在しなければ None を返します
        """
        pass

    @abstractmethod
    def list_documents(
        self, dataset_id: str, skip: int = 0, limit: int = 100
    ) -> List[Document]:
        """指定されたデータセットに属するドキュメント一覧を取得する

        Args:
            dataset_id (str): ドキュメントが所属するデータセットのID
            skip (int, optional): スキップするレコード数
            limit (int, optional): 取得するレコード数の上限

        Returns:
            List[Document]: ドキュメントエンティティのリスト
        """
        pass

    @abstractmethod
    def update(self, document: Document) -> Document:
        """ドキュメントを更新する

        Args:
            document (Document): 更新対象のドキュメントエンティティ（ID を必ず含む）

        Returns:
            Document: 更新後のドキュメントエンティティ
        """
        pass

    @abstractmethod
    def delete(self, document_id: str) -> bool:
        """指定されたIDのドキュメントを削除する

        Args:
            document_id (str): 削除対象のドキュメントID

        Returns:
            bool: 削除が成功した場合は True、存在しなければ False を返します
        """
        pass
