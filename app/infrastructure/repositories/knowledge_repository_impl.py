import logging
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.knowledge import Knowledge
from app.domain.repositories.knowledge_repository import KnowledgeRepository
from app.infrastructure.database.models.knowledge import KnowledgeModel

# モジュール固有のロガー（ログは英語で出力）
logger = logging.getLogger(__name__)


class KnowledgeRepositorySQLAlchemy(KnowledgeRepository):
    """
    SQLAlchemy を利用した KnowledgeRepository の実装
    """

    def __init__(self, session: Session):
        """
        コンストラクタ

        Args:
            session (Session): 同期的な DB セッション
        """
        self.session = session

    def create(self, knowledge: Knowledge) -> Knowledge:
        """
        Knowledge（ページ情報）を作成する

        Args:
            knowledge (Knowledge): 作成するKnowledgeエンティティ

        Returns:
            Knowledge: 作成されたKnowledgeエンティティ
        """
        logger.info("Start: Creating knowledge for document_id=%s, sequence=%d", knowledge.document_id, knowledge.sequence)
        db_knowledge = KnowledgeModel(
            id=str(uuid.uuid4()) if not knowledge.id else knowledge.id,
            document_id=knowledge.document_id,
            sequence=knowledge.sequence,
            knowledge_text=knowledge.knowledge_text,
            meta_data=knowledge.meta_data,
            is_active=knowledge.is_active,
            created_at=knowledge.created_at,
            updated_at=knowledge.updated_at,
        )
        self.session.add(db_knowledge)
        self.session.commit()
        self.session.refresh(db_knowledge)
        logger.info("Success: Knowledge created with id=%s", db_knowledge.id)
        return Knowledge(
            id=db_knowledge.id,
            document_id=db_knowledge.document_id,
            sequence=db_knowledge.sequence,
            knowledge_text=db_knowledge.knowledge_text,
            meta_data=db_knowledge.meta_data,
            is_active=db_knowledge.is_active,
            created_at=db_knowledge.created_at,
            updated_at=db_knowledge.updated_at,
        )

    def get_by_id(self, knowledge_id: str) -> Optional[Knowledge]:
        """
        指定されたIDのKnowledgeを取得する

        Args:
            knowledge_id (str): 取得対象のKnowledge ID

        Returns:
            Optional[Knowledge]: 存在すればKnowledgeエンティティ、存在しなければ None
        """
        logger.info("Start: Retrieving knowledge with id=%s", knowledge_id)
        stmt = select(KnowledgeModel).where(KnowledgeModel.id == knowledge_id)
        db_knowledge = self.session.execute(stmt).scalar_one_or_none()
        if not db_knowledge:
            logger.error("Error: Knowledge not found with id=%s", knowledge_id)
            return None
        logger.info("Success: Retrieved knowledge with id=%s", knowledge_id)
        return Knowledge(
            id=db_knowledge.id,
            document_id=db_knowledge.document_id,
            sequence=db_knowledge.sequence,
            knowledge_text=db_knowledge.knowledge_text,
            meta_data=db_knowledge.meta_data,
            is_active=db_knowledge.is_active,
            created_at=db_knowledge.created_at,
            updated_at=db_knowledge.updated_at,
        )

    def list_knowledges(
        self, document_id: str, skip: int = 0, limit: int = 100
    ) -> List[Knowledge]:
        """
        指定されたドキュメントに属するKnowledge一覧を取得する

        Args:
            document_id (str): Knowledgeが属するドキュメントのID
            skip (int): スキップするレコード数
            limit (int): 取得するレコード数の上限

        Returns:
            List[Knowledge]: 取得したKnowledgeエンティティのリスト
        """
        logger.info(
            "Start: Listing knowledges for document_id=%s, skip=%d, limit=%d",
            document_id,
            skip,
            limit,
        )
        stmt = (
            select(KnowledgeModel)
            .where(KnowledgeModel.document_id == document_id)
            .order_by(KnowledgeModel.sequence)
            .offset(skip)
            .limit(limit)
        )
        result = self.session.execute(stmt)
        db_knowledges = result.scalars().all()
        logger.info("Success: Retrieved %d knowledges", len(db_knowledges))
        return [
            Knowledge(
                id=db_knowledge.id,
                document_id=db_knowledge.document_id,
                sequence=db_knowledge.sequence,
                knowledge_text=db_knowledge.knowledge_text,
                meta_data=db_knowledge.meta_data,
                is_active=db_knowledge.is_active,
                created_at=db_knowledge.created_at,
                updated_at=db_knowledge.updated_at,
            )
            for db_knowledge in db_knowledges
        ]

    def update(self, knowledge: Knowledge) -> Knowledge:
        """
        Knowledgeを更新する

        Args:
            knowledge (Knowledge): 更新対象のKnowledgeエンティティ（ID 必須）

        Returns:
            Knowledge: 更新後のKnowledgeエンティティ

        Raises:
            ValueError: 指定されたKnowledgeが存在しない場合
        """
        logger.info("Start: Updating knowledge with id=%s", knowledge.id)
        stmt = select(KnowledgeModel).where(KnowledgeModel.id == knowledge.id)
        db_knowledge = self.session.execute(stmt).scalar_one_or_none()
        if not db_knowledge:
            logger.error("Error: Knowledge not found for update with id=%s", knowledge.id)
            raise ValueError(f"Knowledge with id {knowledge.id} not found")
        db_knowledge.sequence = knowledge.sequence
        db_knowledge.knowledge_text = knowledge.knowledge_text
        db_knowledge.meta_data = knowledge.meta_data
        db_knowledge.is_active = knowledge.is_active
        db_knowledge.updated_at = (
            knowledge.updated_at if knowledge.updated_at is not None else datetime.now()
        )
        self.session.commit()
        self.session.refresh(db_knowledge)
        logger.info("Success: Updated knowledge with id=%s", knowledge.id)
        return Knowledge(
            id=db_knowledge.id,
            document_id=db_knowledge.document_id,
            sequence=db_knowledge.sequence,
            knowledge_text=db_knowledge.knowledge_text,
            meta_data=db_knowledge.meta_data,
            is_active=db_knowledge.is_active,
            created_at=db_knowledge.created_at,
            updated_at=db_knowledge.updated_at,
        )

    def delete(self, knowledge_id: str) -> bool:
        """
        指定されたIDのKnowledgeを削除する

        Args:
            knowledge_id (str): 削除対象のKnowledge ID

        Returns:
            bool: 削除に成功した場合は True、存在しなければ False
        """
        logger.info("Start: Deleting knowledge with id=%s", knowledge_id)
        stmt = select(KnowledgeModel).where(KnowledgeModel.id == knowledge_id)
        db_knowledge = self.session.execute(stmt).scalar_one_or_none()
        if not db_knowledge:
            logger.error(
                "Error: Knowledge not found for deletion with id=%s", knowledge_id
            )
            return False
        self.session.delete(db_knowledge)
        self.session.commit()
        logger.info("Success: Deleted knowledge with id=%s", knowledge_id)
        return True
