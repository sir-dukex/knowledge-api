from typing import List
from app.domain.entities.knowledge import Knowledge
from app.domain.repositories.knowledge_repository import KnowledgeRepository


class ListKnowledgesUseCase:
    """
    Knowledge（ページ情報）一覧取得ユースケース
    """

    def __init__(self, knowledge_repository: KnowledgeRepository):
        """
        コンストラクタ

        Args:
            knowledge_repository (KnowledgeRepository): Knowledgeリポジトリ
        """
        self.knowledge_repository = knowledge_repository

    def execute(self, document_id: str, skip: int = 0, limit: int = 100) -> List[Knowledge]:
        """
        指定ドキュメントに紐付くKnowledge（ページ情報）一覧を取得する

        Args:
            document_id (str): 紐付くドキュメントID
            skip (int, optional): スキップするレコード数
            limit (int, optional): 取得するレコード数の上限

        Returns:
            List[Knowledge]: Knowledgeエンティティのリスト
        """
        return self.knowledge_repository.list_knowledges(document_id, skip, limit)
