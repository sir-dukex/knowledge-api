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
        session (Session): FastAPI の Depends 経由で注入されるDBセッション

    戻り値:
        DatasetResponse: 作成されたデータセットの詳細情報を含むレスポンスオブジェクト

    例外:
        HTTPException: データセット作成中にエラーが発生した場合、500エラーを返す
    """
    logger.info("Start: Creating new dataset with name=%s", dataset_create.name)
    try:
        # リポジトリの初期化
        dataset_repo = DatasetRepositorySQLAlchemy(session)
        # ユースケースの初期化と実行
        usecase = CreateDatasetUseCase(dataset_repo)
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
    データセットの一覧を取得するエンドポイント

    引数:
        session (Session): FastAPI の Depends 経由で注入されるDBセッション
        skip (int): スキップするレコード数
        limit (int): 取得するレコード数の上限

    戻り値:
        DatasetListResponse: データセット一覧と合計件数を含むレスポンスオブジェクト
    """
    logger.info("Start: Retrieving dataset list. skip=%d, limit=%d", skip, limit)
    dataset_repo = DatasetRepositorySQLAlchemy(session)
    datasets = dataset_repo.list_datasets(skip=skip, limit=limit)
    total = len(datasets)
    logger.info("Success: Retrieved %d datasets", total)
    return DatasetListResponse(
        items=[
            # DatasetResponse で出力
            DatasetResponse(
                id=dataset.id,
                name=dataset.name,
                description=dataset.description,
                meta_data=dataset.meta_data,
                created_at=dataset.created_at,
                updated_at=dataset.updated_at,
            )
            for dataset in datasets
        ],
        total=total,
    )


@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(dataset_id: str, session: Annotated[Session, Depends(get_db)]):
    """
    指定IDのデータセット詳細を取得するエンドポイント

    引数:
        dataset_id (str): 取得対象のデータセットID
        session (Session): FastAPI の Depends 経由で注入されるDBセッション

    戻り値:
        DatasetResponse: 指定されたデータセットの詳細情報を含むレスポンスオブジェクト

    例外:
        HTTPException: 指定されたデータセットが存在しない場合、404エラーを返す
    """
    logger.info("Start: Retrieving dataset with dataset_id=%s", dataset_id)
    dataset_repo = DatasetRepositorySQLAlchemy(session)
    dataset = dataset_repo.get_by_id(dataset_id)
    if not dataset:
        logger.error("Error: Dataset not found with dataset_id=%s", dataset_id)
        raise HTTPException(status_code=404, detail="Dataset not found")
    logger.info("Success: Retrieved dataset with dataset_id=%s", dataset_id)
    return DatasetResponse(
        id=dataset.id,
        name=dataset.name,
        description=dataset.description,
        meta_data=dataset.meta_data,
        created_at=dataset.created_at,
        updated_at=dataset.updated_at,
    )


@router.put("/{dataset_id}", response_model=DatasetResponse)
def update_dataset(
    dataset_id: str,
    dataset_update: DatasetCreate,  # 必要に応じて DatasetUpdate スキーマを新たに定義すべき
    session: Annotated[Session, Depends(get_db)],
):
    """
    指定IDのデータセットを更新するエンドポイント

    引数:
        dataset_id (str): 更新対象のデータセットID
        dataset_update (DatasetCreate): 更新するデータの詳細情報（更新専用スキーマとして定義するのが望ましい）
        session (Session): FastAPI の Depends 経由で注入されるDBセッション

    戻り値:
        DatasetResponse: 更新後のデータセットの詳細情報を含むレスポンスオブジェクト

    例外:
        HTTPException: 更新処理中にエラーが発生した場合
    """
    logger.info("Start: Updating dataset with id=%s", dataset_id)
    dataset_repo = DatasetRepositorySQLAlchemy(session)
    try:
        # 更新するためのドメインエンティティを作成
        # ※本来は更新専用のユースケースがあると望ましいが、ここでは repository.update() を直接呼び出す例です。
        from app.domain.entities.dataset import Dataset

        updated_entity = Dataset(
            id=dataset_id,
            name=dataset_update.name,
            description=dataset_update.description,
            meta_data=dataset_update.meta_data,
            created_at=None,  # 既存の作成日時をそのまま利用するため、更新用には不要（実装によりリポジトリで補完される）
            updated_at=None,
        )
        updated_dataset = dataset_repo.update(updated_entity)
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
        session (Session): FastAPI の Depends 経由で注入されるDBセッション

    戻り値:
        204 No Content（削除成功時）

    例外:
        HTTPException: 対象データセットが存在しない場合
    """
    logger.info("Start: Deleting dataset with id=%s", dataset_id)
    dataset_repo = DatasetRepositorySQLAlchemy(session)
    success = dataset_repo.delete(dataset_id)
    if not success:
        logger.error("Error: Dataset not found for deletion with id=%s", dataset_id)
        raise HTTPException(status_code=404, detail="Dataset not found")
    logger.info("Success: Deleted dataset with id=%s", dataset_id)
    return
