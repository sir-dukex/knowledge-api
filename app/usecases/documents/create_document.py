from app.domain.entities.dataset import Dataset  # 既存の Dataset エンティティ
from app.domain.entities.document import Document
from app.domain.repositories.dataset_repository import DatasetRepository
from app.domain.repositories.document_repository import DocumentRepository


class CreateDocumentUseCase:
    """
    ドキュメント作成ユースケース
    """

    def __init__(
        self,
        document_repository: DocumentRepository,
        dataset_repository: DatasetRepository,  # dataset repository も受け取る
    ):
        self.document_repository = document_repository
        self.dataset_repository = dataset_repository

    def execute(
        self, dataset_id: str, title: str, content: str, meta_data: dict = None, is_active: bool = True
    ) -> Document:
        """
        新規ドキュメントを作成する。
        dataset_id が存在しない場合は、document の title と同じ Dataset を自動生成します。

        Args:
            dataset_id (str): Document 作成時に指定された Dataset ID（オプショナル）
            title (str): ドキュメントのタイトル
            content (str): ドキュメントの本文
            meta_data (dict, optional): 追加のメタ情報
            is_active (bool): 有効フラグ（True:有効, False:無効）

        Returns:
            Document: 作成されたドキュメントエンティティ
        """
        # dataset_id が指定されているか、または存在しているか確認
        dataset = None
        if dataset_id:
            dataset = self.dataset_repository.get_by_id(dataset_id)

        # 存在しない場合は document の title を利用して Dataset を自動生成
        if not dataset:
            from app.usecases.datasets.create_dataset import (
                CreateDatasetUseCase as CreateDatasetUC,
            )

            # Dataset 作成用ユースケース（既存の実装）を利用し、新たな Dataset を作成する
            create_dataset_uc = CreateDatasetUC(self.dataset_repository)
            dataset = create_dataset_uc.execute(
                name=title,  # document title と同じ名前
                description="Auto-created from document creation",
                meta_data={},
                is_active=True,
            )
            dataset_id = dataset.id

        # Document を作成する
        document = Document.create(
            dataset_id=dataset_id,
            title=title,
            content=content,
            meta_data=meta_data,
            is_active=is_active,
        )
        return self.document_repository.create(document)
