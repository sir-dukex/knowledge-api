from app.domain.entities.knowledge import Knowledge
from app.domain.repositories.knowledge_repository import KnowledgeRepository


class UpdateKnowledgeUseCase:
    """
    Knowledge（ページ情報）更新ユースケース
    """

    def __init__(self, knowledge_repository: KnowledgeRepository):
        """
        コンストラクタ

        Args:
            knowledge_repository (KnowledgeRepository): Knowledgeリポジトリ
        """
        self.knowledge_repository = knowledge_repository

    def execute(self, knowledge: Knowledge) -> Knowledge:
        """
        Knowledge（ページ情報）を更新する

        Args:
            knowledge (Knowledge): 更新対象のKnowledgeエンティティ（ID必須）

        Returns:
            Knowledge: 更新後のKnowledgeエンティティ

        Raises:
            ValueError: 指定されたKnowledgeが存在しない場合
        """
        return self.knowledge_repository.update(knowledge)
