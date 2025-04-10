import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.dataset_repository_impl import (
    DatasetRepositorySQLAlchemy,
)
from app.infrastructure.repositories.document_repository_impl import (
    DocumentRepositorySQLAlchemy,
)
from app.interfaces.schemas.document import (
    DocumentCreate,
    DocumentListResponse,
    DocumentResponse,
    DocumentUpdate,
)
from app.usecases.documents.create_document import CreateDocumentUseCase
from app.usecases.documents.delete_document import DeleteDocumentUseCase
from app.usecases.documents.get_document import GetDocumentUseCase
from app.usecases.documents.list_documents import ListDocumentsUseCase
from app.usecases.documents.update_document import UpdateDocumentUseCase

# モジュール固有のロガー（ログは英語で出力）
logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=DocumentResponse, status_code=201)
def create_document(
    document_create: DocumentCreate, session: Annotated[Session, Depends(get_db)]
):
    """
    新規ドキュメントを作成するエンドポイント
    """
    logger.info("Start: Creating new document with title=%s", document_create.title)
    try:
        doc_repo = DocumentRepositorySQLAlchemy(session)
        dataset_repo = DatasetRepositorySQLAlchemy(session)
        # ★ UseCaseにdataset_repositoryを渡す
        usecase = CreateDocumentUseCase(
            document_repository=doc_repo, dataset_repository=dataset_repo
        )
        document = usecase.execute(
            dataset_id=document_create.dataset_id,
            title=document_create.title,
            content=document_create.content,
            meta_data=document_create.meta_data,
        )
        logger.info("Success: Document created with id=%s", document.id)
        return DocumentResponse(
            id=document.id,
            dataset_id=document.dataset_id,
            title=document.title,
            content=document.content,
            meta_data=document.meta_data,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )
    except Exception as e:
        logger.error("Error: Failed to create document. Error: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=DocumentListResponse)
def list_documents(
    dataset_id: str,
    session: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    """
    指定されたデータセットに属するドキュメント一覧を取得するエンドポイント

    引数:
        dataset_id (str): 対象となるデータセットのID
        session (Session): DB セッション
        skip (int): スキップするレコード数
        limit (int): 取得するレコード数の上限

    戻り値:
        DocumentListResponse: ドキュメント一覧と総件数
    """
    logger.info("Start: Listing documents for dataset_id=%s", dataset_id)
    try:
        repo = DocumentRepositorySQLAlchemy(session)
        usecase = ListDocumentsUseCase(repo)
        documents = usecase.execute(dataset_id=dataset_id, skip=skip, limit=limit)
        total = len(documents)
        logger.info(
            "Success: Retrieved %d documents for dataset_id=%s", total, dataset_id
        )
        return DocumentListResponse(
            items=[
                DocumentResponse(
                    id=document.id,
                    dataset_id=document.dataset_id,
                    title=document.title,
                    content=document.content,
                    meta_data=document.meta_data,
                    created_at=document.created_at,
                    updated_at=document.updated_at,
                )
                for document in documents
            ],
            total=total,
        )
    except Exception as e:
        logger.error("Error: Failed to list documents. Error: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, session: Annotated[Session, Depends(get_db)]):
    """
    指定IDのドキュメント詳細を取得するエンドポイント

    引数:
        document_id (str): 取得対象のドキュメントID
        session (Session): DB セッション

    戻り値:
        DocumentResponse: 取得したドキュメントの詳細
    """
    logger.info("Start: Retrieving document with id=%s", document_id)
    try:
        repo = DocumentRepositorySQLAlchemy(session)
        usecase = GetDocumentUseCase(repo)
        document = usecase.execute(document_id)
        logger.info("Success: Retrieved document with id=%s", document_id)
        return DocumentResponse(
            id=document.id,
            dataset_id=document.dataset_id,
            title=document.title,
            content=document.content,
            meta_data=document.meta_data,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )
    except ValueError as ve:
        logger.error("Error: %s", str(ve))
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error("Error: Failed to retrieve document. Error: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: str,
    document_update: DocumentUpdate,
    session: Annotated[Session, Depends(get_db)],
):
    """
    指定IDのドキュメントを更新するエンドポイント

    引数:
        document_id (str): 更新対象のドキュメントID
        document_update (DocumentCreate): 更新する情報（更新専用スキーマ推奨）
        session (Session): DB セッション

    戻り値:
        DocumentResponse: 更新後のドキュメント詳細
    """
    logger.info("Start: Updating document with id=%s", document_id)
    try:
        repo = DocumentRepositorySQLAlchemy(session)
        usecase = UpdateDocumentUseCase(repo)
        updated_document = usecase.execute(
            document_id=document_id,
            title=document_update.title,
            content=document_update.content,
            meta_data=document_update.meta_data,
        )
        logger.info("Success: Updated document with id=%s", document_id)
        return DocumentResponse(
            id=updated_document.id,
            dataset_id=updated_document.dataset_id,
            title=updated_document.title,
            content=updated_document.content,
            meta_data=updated_document.meta_data,
            created_at=updated_document.created_at,
            updated_at=updated_document.updated_at,
        )
    except Exception as e:
        logger.error(
            "Error: Failed to update document with id=%s, error: %s",
            document_id,
            str(e),
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}", status_code=204)
def delete_document(document_id: str, session: Annotated[Session, Depends(get_db)]):
    """
    指定IDのドキュメントを削除するエンドポイント

    引数:
        document_id (str): 削除対象のドキュメントID
        session (Session): DB セッション

    戻り値:
        204 No Content（削除成功時）
    """
    logger.info("Start: Deleting document with id=%s", document_id)
    try:
        repo = DocumentRepositorySQLAlchemy(session)
        usecase = DeleteDocumentUseCase(repo)
        success = usecase.execute(document_id)
        if not success:
            logger.error(
                "Error: Document not found for deletion with id=%s", document_id
            )
            raise HTTPException(status_code=404, detail="Document not found")
        logger.info("Success: Deleted document with id=%s", document_id)
        return
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(
            "Error: Failed to delete document with id=%s, error: %s",
            document_id,
            str(e),
        )
        raise HTTPException(status_code=500, detail=str(e))
