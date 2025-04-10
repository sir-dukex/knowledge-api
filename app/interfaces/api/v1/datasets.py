# app/interfaces/api/v1/datasets.py
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.dataset_repository_impl import (
    DatasetRepositorySQLAlchemy,
)
from app.interfaces.schemas.dataset import (
    DatasetCreate,
    DatasetListResponse,
    DatasetResponse,
)
from app.usecases.datasets.create_dataset import CreateDatasetUseCase
from app.usecases.datasets.delete_dataset import DeleteDatasetUseCase
from app.usecases.datasets.get_dataset import GetDatasetUseCase
from app.usecases.datasets.list_datasets import ListDatasetsUseCase
from app.usecases.datasets.update_dataset import UpdateDatasetUseCase

# モジュール固有のロガー（ログは英語で出力されます）
logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=DatasetResponse, status_code=201)
def create_dataset(
    dataset_create: DatasetCreate, session: Annotated[Session, Depends(get_db)]
):
    """
    新規データセットを作成するエンドポイント

    引数:
        dataset_create (DatasetCreate): データセットの詳細情報を含むオブジェクト
        session (Session): DBセッション（FastAPI の Depends 経由）

    戻り値:
        DatasetResponse: 作成されたデータセット情報
    """
    logger.info("Start: Creating new dataset with name=%s", dataset_create.name)
    try:
        repo = DatasetRepositorySQLAlchemy(session)
        usecase = CreateDatasetUseCase(repo)
        dataset = usecase.execute(
            name=dataset_create.name,
            description=dataset_create.description,
            meta_data=dataset_create.meta_data,
        )
        logger.info("Success: Dataset created with id=%s", dataset.id)
        return DatasetResponse(
            id=dataset.id,
            name=dataset.name,
            description=dataset.description,
            meta_data=dataset.meta_data,
            created_at=dataset.created_at,
            updated_at=dataset.updated_at,
        )
    except Exception as e:
        logger.error("Error: Failed to create dataset. Error: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=DatasetListResponse)
def list_datasets(
    session: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 100
):
    """
    データセット一覧を取得するエンドポイント

    引数:
        session (Session): DBセッション
        skip (int): スキップする件数
        limit (int): 取得件数の上限

    戻り値:
        DatasetListResponse: 取得したデータセット一覧と総件数
    """
    logger.info("Start: Listing datasets with skip=%d, limit=%d", skip, limit)
    try:
        repo = DatasetRepositorySQLAlchemy(session)
        usecase = ListDatasetsUseCase(repo)
        datasets = usecase.execute(skip=skip, limit=limit)
        total = len(datasets)
        logger.info("Success: Retrieved %d datasets", total)
        return DatasetListResponse(
            items=[
                DatasetResponse(
                    id=ds.id,
                    name=ds.name,
                    description=ds.description,
                    meta_data=ds.meta_data,
                    created_at=ds.created_at,
                    updated_at=ds.updated_at,
                )
                for ds in datasets
            ],
            total=total,
        )
    except Exception as e:
        logger.error("Error: Failed to list datasets. Error: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(dataset_id: str, session: Annotated[Session, Depends(get_db)]):
    """
    指定IDのデータセット詳細を取得するエンドポイント

    引数:
        dataset_id (str): 取得対象のデータセットID
        session (Session): DBセッション（FastAPI の Depends 経由）

    戻り値:
        DatasetResponse: 取得したデータセットの詳細情報を含むレスポンスオブジェクト

    例外:
        HTTPException: 指定されたデータセットが存在しない場合、404 エラーを返す
                   : その他エラー発生時に 500 エラーを返す
    """
    logger.info("Start: Retrieving dataset with id=%s", dataset_id)
    try:
        # リポジトリの初期化
        repo = DatasetRepositorySQLAlchemy(session)
        usecase = GetDatasetUseCase(repo)
        dataset = usecase.execute(dataset_id)
        logger.info("Success: Retrieved dataset with id=%s", dataset_id)
        return DatasetResponse(
            id=dataset.id,
            name=dataset.name,
            description=dataset.description,
            meta_data=dataset.meta_data,
            created_at=dataset.created_at,
            updated_at=dataset.updated_at,
        )
    except ValueError as ve:
        logger.error("Error: %s", str(ve))
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error("Error: Failed to retrieve dataset. Error: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{dataset_id}", response_model=DatasetResponse)
def update_dataset(
    dataset_id: str,
    dataset_update: DatasetCreate,  # 更新専用スキーマがあればそちらを利用
    session: Annotated[Session, Depends(get_db)],
):
    """
    指定IDのデータセットを更新するエンドポイント

    引数:
        dataset_id (str): 更新対象のデータセットID
        dataset_update (DatasetCreate): 更新するデータ（更新専用スキーマ推奨）
        session (Session): DBセッション

    戻り値:
        DatasetResponse: 更新後のデータセット詳細
    """
    logger.info("Start: Updating dataset with id=%s", dataset_id)
    try:
        repo = DatasetRepositorySQLAlchemy(session)
        usecase = UpdateDatasetUseCase(repo)
        updated_dataset = usecase.execute(
            dataset_id=dataset_id,
            name=dataset_update.name,
            description=dataset_update.description,
            meta_data=dataset_update.meta_data,
        )
        logger.info("Success: Updated dataset with id=%s", dataset_id)
        return DatasetResponse(
            id=updated_dataset.id,
            name=updated_dataset.name,
            description=updated_dataset.description,
            meta_data=updated_dataset.meta_data,
            created_at=updated_dataset.created_at,
            updated_at=updated_dataset.updated_at,
        )
    except Exception as e:
        logger.error(
            "Error: Failed to update dataset with id=%s, error: %s", dataset_id, str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{dataset_id}", status_code=204)
def delete_dataset(dataset_id: str, session: Annotated[Session, Depends(get_db)]):
    """
    指定IDのデータセットを削除するエンドポイント

    引数:
        dataset_id (str): 削除対象のデータセットID
        session (Session): DBセッション

    戻り値:
        204 No Content（削除成功時）

    例外:
        HTTPException: 対象データセットが存在しない場合は 404 を返す、その他エラーの場合は 500 を返す
    """
    logger.info("Start: Deleting dataset with id=%s", dataset_id)
    try:
        repo = DatasetRepositorySQLAlchemy(session)
        usecase = DeleteDatasetUseCase(repo)
        success = usecase.execute(dataset_id)
        if not success:
            logger.error("Error: Dataset not found for deletion with id=%s", dataset_id)
            raise HTTPException(status_code=404, detail="Dataset not found")
        logger.info("Success: Deleted dataset with id=%s", dataset_id)
        return
    except Exception as e:
        if isinstance(e, HTTPException):
            # 既に HTTPException の場合はそのまま再送出
            raise e
        logger.error(
            "Error: Failed to delete dataset with id=%s, error: %s", dataset_id, str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))
