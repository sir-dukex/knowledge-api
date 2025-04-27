from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.knowledge import Knowledge


class KnowledgeRepository(ABC):
    """Knowledge（ページネーション情報）リポジトリの抽象クラス

    このクラスは、Knowledgeの永続化に関するCRUD操作のインターフェースを定義します。
    実際の実装はインフラ層で行い、ドメイン層はこのインターフェースを利用してビジネスロジックを実装します。
    """

    @abstractmethod
    def create(self, knowledge: Knowledge) -> Knowledge:
        """Knowledge（ページ情報）を作成する

        Args:
            knowledge (Knowledge): 作成するKnowledgeエンティティ

        Returns:
            Knowledge: 作成されたKnowledgeエンティティ
        """
        pass

    @abstractmethod
    def get_by_id(self, knowledge_id: str) -> Optional[Knowledge]:
        """指定されたIDのKnowledgeを取得する

        Args:
            knowledge_id (str): 取得対象のKnowledge ID

        Returns:
            Optional[Knowledge]: Knowledgeが存在すればエンティティを、存在しなければ None を返します
        """
        pass

    @abstractmethod
    def list_knowledges(
        self, document_id: str, skip: int = 0, limit: int = 100
    ) -> List[Knowledge]:
        """指定されたドキュメントに属するKnowledge一覧を取得する

        Args:
            document_id (str): Knowledgeが所属するドキュメントのID
            skip (int, optional): スキップするレコード数
            limit (int, optional): 取得するレコード数の上限

        Returns:
            List[Knowledge]: Knowledgeエンティティのリスト
        """
        pass

    @abstractmethod
    def update(self, knowledge: Knowledge) -> Knowledge:
        """Knowledgeを更新する

        Args:
            knowledge (Knowledge): 更新対象のKnowledgeエンティティ（ID を必ず含む）

        Returns:
            Knowledge: 更新後のKnowledgeエンティティ
        """
        pass

    @abstractmethod
    def delete(self, knowledge_id: str) -> bool:
        """指定されたIDのKnowledgeを削除する

        Args:
            knowledge_id (str): 削除対象のKnowledge ID

        Returns:
            bool: 削除が成功した場合は True、存在しなければ False を返します
        """
        pass
