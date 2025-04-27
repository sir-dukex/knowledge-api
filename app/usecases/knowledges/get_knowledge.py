from typing import Optional
from app.domain.entities.knowledge import Knowledge
from app.domain.repositories.knowledge_repository import KnowledgeRepository


class GetKnowledgeUseCase:
    """
    Knowledge（ページ情報）取得ユースケース
    """

    def __init__(self, knowledge_repository: KnowledgeRepository):
        """
        コンストラクタ

        Args:
            knowledge_repository (KnowledgeRepository): Knowledgeリポジトリ
        """
        self.knowledge_repository = knowledge_repository

    def execute(self, knowledge_id: str) -> Optional[Knowledge]:
        """
        Knowledge（ページ情報）をIDで取得する

        Args:
            knowledge_id (str): 取得対象のKnowledge ID

        Returns:
            Optional[Knowledge]: Knowledgeエンティティ（存在しなければNone）
        """
        return self.knowledge_repository.get_by_id(knowledge_id)
