"""Make columns Unicode for Japanese support

Revision ID: dab2d82c919c
Revises: 1a2b3c4d5e6f
Create Date: 2025-04-29 20:01:43.011764

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'dab2d82c919c'
down_revision: Union[str, None] = '1a2b3c4d5e6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    既存テーブルの日本語対応カラムをNVARCHAR型へ変更するマイグレーション
    データは保持されます
    """
    # datasets.name, datasets.description
    op.execute("ALTER TABLE datasets ALTER COLUMN name NVARCHAR(255) NOT NULL;")
    op.execute("ALTER TABLE datasets ALTER COLUMN description NVARCHAR(MAX) NULL;")
    # documents.title, documents.content
    op.execute("ALTER TABLE documents ALTER COLUMN title NVARCHAR(255) NOT NULL;")
    op.execute("ALTER TABLE documents ALTER COLUMN content NVARCHAR(MAX) NOT NULL;")
    # knowledges.knowledge_text
    op.execute("ALTER TABLE knowledges ALTER COLUMN knowledge_text NVARCHAR(MAX) NOT NULL;")


def downgrade() -> None:
    """
    ダウングレード時は元の型（VARCHAR/TEXT）に戻します
    """
    op.execute("ALTER TABLE datasets ALTER COLUMN name VARCHAR(255) NOT NULL;")
    op.execute("ALTER TABLE datasets ALTER COLUMN description TEXT NULL;")
    op.execute("ALTER TABLE documents ALTER COLUMN title VARCHAR(255) NOT NULL;")
    op.execute("ALTER TABLE documents ALTER COLUMN content TEXT NOT NULL;")
    op.execute("ALTER TABLE knowledges ALTER COLUMN knowledge_text TEXT NOT NULL;")
