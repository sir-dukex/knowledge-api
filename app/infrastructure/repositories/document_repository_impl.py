import logging
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.document import Document
from app.domain.repositories.document_repository import DocumentRepository
from app.infrastructure.database.models.document import DocumentModel

# モジュール固有のロガー（ログは英語で出力）
logger = logging.getLogger(__name__)


class DocumentRepositorySQLAlchemy(DocumentRepository):
    """
    SQLAlchemy を利用した DocumentRepository の実装
    """

    def __init__(self, session: Session):
        """
        コンストラクタ

        Args:
            session (Session): 同期的な DB セッション
        """
        self.session = session

    def create(self, document: Document) -> Document:
        """
        ドキュメントを作成する

        Args:
            document (Document): 作成するドキュメントのエンティティ

        Returns:
            Document: 作成されたドキュメントエンティティ
        """
        logger.info("Start: Creating document with title=%s", document.title)
        # エンティティを DB モデルに変換
        db_document = DocumentModel(
            id=str(uuid.uuid4()) if not document.id else document.id,
            dataset_id=document.dataset_id,
            title=document.title,
            content=document.content,
            meta_data=document.meta_data,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )
        self.session.add(db_document)
        self.session.commit()
        self.session.refresh(db_document)
        logger.info("Success: Document created with id=%s", db_document.id)
        return Document(
            id=db_document.id,
            dataset_id=db_document.dataset_id,
            title=db_document.title,
            content=db_document.content,
            meta_data=db_document.meta_data,
            created_at=db_document.created_at,
            updated_at=db_document.updated_at,
        )

    def get_by_id(self, document_id: str) -> Optional[Document]:
        """
        指定されたIDのドキュメントを取得する

        Args:
            document_id (str): 取得対象のドキュメントID

        Returns:
            Optional[Document]: 存在すればドキュメントエンティティ、存在しなければ None
        """
        logger.info("Start: Retrieving document with id=%s", document_id)
        stmt = select(DocumentModel).where(DocumentModel.id == document_id)
        db_document = self.session.execute(stmt).scalar_one_or_none()
        if not db_document:
            logger.error("Error: Document not found with id=%s", document_id)
            return None
        logger.info("Success: Retrieved document with id=%s", document_id)
        return Document(
            id=db_document.id,
            dataset_id=db_document.dataset_id,
            title=db_document.title,
            content=db_document.content,
            meta_data=db_document.meta_data,
            created_at=db_document.created_at,
            updated_at=db_document.updated_at,
        )

    def list_documents(
        self, dataset_id: str, skip: int = 0, limit: int = 100
    ) -> List[Document]:
        """
        指定されたデータセットに属するドキュメント一覧を取得する

        Args:
            dataset_id (str): ドキュメントが属するデータセットのID
            skip (int): スキップするレコード数
            limit (int): 取得するレコード数の上限

        Returns:
            List[Document]: 取得したドキュメントエンティティのリスト
        """
        logger.info(
            "Start: Listing documents for dataset_id=%s, skip=%d, limit=%d",
            dataset_id,
            skip,
            limit,
        )
        stmt = (
            select(DocumentModel)
            .where(DocumentModel.dataset_id == dataset_id)
            .order_by(DocumentModel.created_at)
            .offset(skip)
            .limit(limit)
        )
        result = self.session.execute(stmt)
        db_documents = result.scalars().all()
        logger.info("Success: Retrieved %d documents", len(db_documents))
        return [
            Document(
                id=db_doc.id,
                dataset_id=db_doc.dataset_id,
                title=db_doc.title,
                content=db_doc.content,
                meta_data=db_doc.meta_data,
                created_at=db_doc.created_at,
                updated_at=db_doc.updated_at,
            )
            for db_doc in db_documents
        ]

    def update(self, document: Document) -> Document:
        """
        ドキュメントを更新する

        Args:
            document (Document): 更新対象のドキュメントエンティティ（ID 必須）

        Returns:
            Document: 更新後のドキュメントエンティティ

        Raises:
            ValueError: 指定されたドキュメントが存在しない場合
        """
        logger.info("Start: Updating document with id=%s", document.id)
        stmt = select(DocumentModel).where(DocumentModel.id == document.id)
        db_document = self.session.execute(stmt).scalar_one_or_none()
        if not db_document:
            logger.error("Error: Document not found for update with id=%s", document.id)
            raise ValueError(f"Document with id {document.id} not found")
        db_document.title = document.title
        db_document.content = document.content
        db_document.meta_data = document.meta_data
        # updated_at が None の場合、現在時刻で補完
        db_document.updated_at = (
            document.updated_at if document.updated_at is not None else datetime.now()
        )
        self.session.commit()
        self.session.refresh(db_document)
        logger.info("Success: Updated document with id=%s", document.id)
        return Document(
            id=db_document.id,
            dataset_id=db_document.dataset_id,
            title=db_document.title,
            content=db_document.content,
            meta_data=db_document.meta_data,
            created_at=db_document.created_at,
            updated_at=db_document.updated_at,
        )

    def delete(self, document_id: str) -> bool:
        """
        指定されたIDのドキュメントを削除する

        Args:
            document_id (str): 削除対象のドキュメントID

        Returns:
            bool: 削除に成功した場合は True、存在しなければ False
        """
        logger.info("Start: Deleting document with id=%s", document_id)
        stmt = select(DocumentModel).where(DocumentModel.id == document_id)
        db_document = self.session.execute(stmt).scalar_one_or_none()
        if not db_document:
            logger.error(
                "Error: Document not found for deletion with id=%s", document_id
            )
            return False
        self.session.delete(db_document)
        self.session.commit()
        logger.info("Success: Deleted document with id=%s", document_id)
        return True
