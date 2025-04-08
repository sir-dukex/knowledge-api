from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.dataset_repository_impl import DatasetRepositorySQLAlchemy
from app.interfaces.schemas.dataset import DatasetCreate, DatasetResponse, DatasetListResponse
from app.usecases.datasets.create_dataset import CreateDatasetUseCase

router = APIRouter()


@router.post("/", response_model=DatasetResponse, status_code=201)
def create_dataset(
    dataset_create: DatasetCreate,
    session: Annotated[Session, Depends(get_db)]
):
    """新しいデータセットを作成"""
    try:
        # リポジトリの初期化
        dataset_repo = DatasetRepositorySQLAlchemy(session)
        
        # ユースケースの初期化と実行
        usecase = CreateDatasetUseCase(dataset_repo)
        dataset = usecase.execute(
            name=dataset_create.name,
            description=dataset_create.description,
            meta_data=dataset_create.meta_data
        )
        
        # レスポンスの作成
        return DatasetResponse(
            id=dataset.id,
            name=dataset.name,
            description=dataset.description,
            meta_data=dataset.meta_data,
            created_at=dataset.created_at,
            updated_at=dataset.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=DatasetListResponse)
def list_datasets(
    session: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100
):
    """データセット一覧を取得"""
    dataset_repo = DatasetRepositorySQLAlchemy(session)
    datasets = dataset_repo.list_datasets(skip=skip, limit=limit)
    
    return DatasetListResponse(
        items=[
            DatasetResponse(
                id=dataset.id,
                name=dataset.name,
                description=dataset.description,
                meta_data=dataset.meta_data,
                created_at=dataset.created_at,
                updated_at=dataset.updated_at
            )
            for dataset in datasets
        ],
        total=len(datasets)  # 実際の実装では合計カウントを別クエリで取得する
    )


@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(
    dataset_id: str,
    session: Annotated[Session, Depends(get_db)]
):
    """特定のデータセットを取得"""
    dataset_repo = DatasetRepositorySQLAlchemy(session)
    dataset = dataset_repo.get_by_id(dataset_id)
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return DatasetResponse(
        id=dataset.id,
        name=dataset.name,
        description=dataset.description,
        meta_data=dataset.meta_data,
        created_at=dataset.created_at,
        updated_at=dataset.updated_at
    )