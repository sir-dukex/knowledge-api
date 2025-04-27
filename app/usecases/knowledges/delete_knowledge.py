from app.domain.repositories.knowledge_repository import KnowledgeRepository


class DeleteKnowledgeUseCase:
    """
    Knowledge（ページ情報）削除ユースケース
    """

    def __init__(self, knowledge_repository: KnowledgeRepository):
        """
        コンストラクタ

        Args:
            knowledge_repository (KnowledgeRepository): Knowledgeリポジトリ
        """
        self.knowledge_repository = knowledge_repository

    def execute(self, knowledge_id: str) -> bool:
        """
        Knowledge（ページ情報）をIDで削除する

        Args:
            knowledge_id (str): 削除対象のKnowledge ID

        Returns:
            bool: 削除に成功した場合はTrue、存在しなければFalse
        """
        return self.knowledge_repository.delete(knowledge_id)
