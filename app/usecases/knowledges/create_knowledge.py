from app.domain.entities.knowledge import Knowledge
from app.domain.repositories.knowledge_repository import KnowledgeRepository


class CreateKnowledgeUseCase:
    """
    Knowledge（ページ情報）作成ユースケース
    """

    def __init__(self, knowledge_repository: KnowledgeRepository):
        """
        コンストラクタ

        Args:
            knowledge_repository (KnowledgeRepository): Knowledgeリポジトリ
        """
        self.knowledge_repository = knowledge_repository

    def execute(
        self,
        document_id: str,
        sequence: int,
        knowledge_text: str,
        meta_data: dict = None,
        is_active: bool = True,
    ) -> Knowledge:
        """
        新規Knowledge（ナレッジ情報）を作成する

        Args:
            document_id (str): 紐付くドキュメントID
            sequence (int): ナレッジの順番（0始まりのインデックス）
            knowledge_text (str): ナレッジ本文
            meta_data (dict, optional): 追加情報
            is_active (bool): 有効フラグ（True:有効, False:無効）

        Returns:
            Knowledge: 作成されたKnowledgeエンティティ
        """
        knowledge = Knowledge.create(
            document_id=document_id,
            sequence=sequence,
            knowledge_text=knowledge_text,
            meta_data=meta_data,
            is_active=is_active,
        )
        return self.knowledge_repository.create(knowledge)
