import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.knowledge_repository_impl import KnowledgeRepositorySQLAlchemy
from app.interfaces.schemas.knowledge import (
    KnowledgeCreate,
    KnowledgeListResponse,
    KnowledgeResponse,
    KnowledgeUpdate,
)
from app.usecases.knowledges.create_knowledge import CreateKnowledgeUseCase
from app.usecases.knowledges.delete_knowledge import DeleteKnowledgeUseCase
from app.usecases.knowledges.get_knowledge import GetKnowledgeUseCase
from app.usecases.knowledges.list_knowledges import ListKnowledgesUseCase
from app.usecases.knowledges.update_knowledge import UpdateKnowledgeUseCase
logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=KnowledgeResponse, status_code=201)
def create_knowledge(
    knowledge_create: KnowledgeCreate, session: Annotated[Session, Depends(get_db)]
):
    """
    新規Knowledge（ページ情報）を作成するエンドポイント
    """
    logger.info("Start: Creating new knowledge for document_id=%s, sequence=%d", knowledge_create.document_id, knowledge_create.sequence)
    try:
        repo = KnowledgeRepositorySQLAlchemy(session)
        usecase = CreateKnowledgeUseCase(repo)
        knowledge = usecase.execute(
            document_id=knowledge_create.document_id,
            sequence=knowledge_create.sequence,
            knowledge_text=knowledge_create.knowledge_text,
            meta_data=knowledge_create.meta_data,
            is_active=knowledge_create.is_active,
        )
        logger.info("Success: Knowledge created with id=%s", knowledge.id)
        return KnowledgeResponse(
            id=knowledge.id,
            document_id=knowledge.document_id,
            sequence=knowledge.sequence,
            knowledge_text=knowledge.knowledge_text,
            meta_data=knowledge.meta_data,
            is_active=knowledge.is_active,
            created_at=knowledge.created_at,
            updated_at=knowledge.updated_at,
        )
    except Exception as e:
        logger.error("Error: Failed to create knowledge. Error: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=KnowledgeListResponse)
def list_knowledges(
    session: Annotated[Session, Depends(get_db)],
    document_id: str = Query(..., description="紐付くドキュメントID"),
    skip: int = 0,
    limit: int = 100,
):
    """
    指定ドキュメントに紐付くKnowledge（ページ情報）一覧を取得するエンドポイント
    """
    logger.info("Start: Listing knowledges for document_id=%s", document_id)
    try:
        repo = KnowledgeRepositorySQLAlchemy(session)
        usecase = ListKnowledgesUseCase(repo)
        knowledges = usecase.execute(document_id=document_id, skip=skip, limit=limit)
        total = len(knowledges)
        logger.info("Success: Retrieved %d knowledges for document_id=%s", total, document_id)
        return KnowledgeListResponse(
            items=[
                KnowledgeResponse(
                    id=k.id,
                    document_id=k.document_id,
                    sequence=k.sequence,
                    knowledge_text=k.knowledge_text,
                    meta_data=k.meta_data,
                    is_active=k.is_active,
                    created_at=k.created_at,
                    updated_at=k.updated_at,
                )
                for k in knowledges
            ],
            total=total,
        )
    except Exception as e:
        logger.error("Error: Failed to list knowledges. Error: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{knowledge_id}", response_model=KnowledgeResponse)
def get_knowledge(knowledge_id: str, session: Annotated[Session, Depends(get_db)]):
    """
    Knowledge（ページ情報）をIDで取得するエンドポイント
    """
    logger.info("Start: Retrieving knowledge with id=%s", knowledge_id)
    try:
        repo = KnowledgeRepositorySQLAlchemy(session)
        usecase = GetKnowledgeUseCase(repo)
        knowledge = usecase.execute(knowledge_id)
    except Exception as e:
        logger.error("Error: Failed to retrieve knowledge. Error: %s", str(e))
        if isinstance(e, ValueError) or "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Knowledge not found")
        raise HTTPException(status_code=500, detail=str(e))
    if not knowledge:
        logger.error("Error: Knowledge not found with id=%s", knowledge_id)
        raise HTTPException(status_code=404, detail="Knowledge not found")
    logger.info("Success: Retrieved knowledge with id=%s", knowledge_id)
    return KnowledgeResponse(
        id=knowledge.id,
        document_id=knowledge.document_id,
        sequence=knowledge.sequence,
        knowledge_text=knowledge.knowledge_text,
        meta_data=knowledge.meta_data,
        is_active=knowledge.is_active,
        created_at=knowledge.created_at,
        updated_at=knowledge.updated_at,
    )


@router.put("/{knowledge_id}", response_model=KnowledgeResponse)
def update_knowledge(
    knowledge_id: str,
    knowledge_update: KnowledgeUpdate,
    session: Annotated[Session, Depends(get_db)],
):
    """
    Knowledge（ページ情報）を更新するエンドポイント
    """
    logger.info("Start: Updating knowledge with id=%s", knowledge_id)
    try:
        repo = KnowledgeRepositorySQLAlchemy(session)
        get_usecase = GetKnowledgeUseCase(repo)
        knowledge = get_usecase.execute(knowledge_id)
        if not knowledge:
            logger.error("Error: Knowledge not found for update with id=%s", knowledge_id)
            raise HTTPException(status_code=404, detail="Knowledge not found")
        # 更新内容を反映
        if knowledge_update.sequence is not None:
            knowledge.sequence = knowledge_update.sequence
        if knowledge_update.knowledge_text is not None:
            knowledge.knowledge_text = knowledge_update.knowledge_text
        if knowledge_update.meta_data is not None:
            knowledge.meta_data = knowledge_update.meta_data
        if knowledge_update.is_active is not None:
            knowledge.is_active = knowledge_update.is_active
        update_usecase = UpdateKnowledgeUseCase(repo)
        updated_knowledge = update_usecase.execute(knowledge)
        logger.info("Success: Updated knowledge with id=%s", knowledge_id)
        return KnowledgeResponse(
            id=updated_knowledge.id,
            document_id=updated_knowledge.document_id,
            sequence=updated_knowledge.sequence,
            knowledge_text=updated_knowledge.knowledge_text,
            meta_data=updated_knowledge.meta_data,
            is_active=updated_knowledge.is_active,
            created_at=updated_knowledge.created_at,
            updated_at=updated_knowledge.updated_at,
        )
    except Exception as e:
        logger.error("Error: Failed to update knowledge with id=%s, error: %s", knowledge_id, str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{knowledge_id}", status_code=204)
def delete_knowledge(knowledge_id: str, session: Annotated[Session, Depends(get_db)]):
    """
    Knowledge（ページ情報）をIDで削除するエンドポイント
    """
    logger.info("Start: Deleting knowledge with id=%s", knowledge_id)
    try:
        repo = KnowledgeRepositorySQLAlchemy(session)
        usecase = DeleteKnowledgeUseCase(repo)
        success = usecase.execute(knowledge_id)
        if not success:
            logger.error("Error: Knowledge not found for deletion with id=%s", knowledge_id)
            raise HTTPException(status_code=404, detail="Knowledge not found")
        logger.info("Success: Deleted knowledge with id=%s", knowledge_id)
        return
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error("Error: Failed to delete knowledge with id=%s, error: %s", knowledge_id, str(e))
        raise HTTPException(status_code=500, detail=str(e))
