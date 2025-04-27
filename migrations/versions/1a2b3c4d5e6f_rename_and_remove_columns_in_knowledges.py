"""rename and remove columns in knowledges table

Revision ID: 1a2b3c4d5e6f
Revises: 3c777ad8ef0c
Create Date: 2025-04-27 21:57:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a2b3c4d5e6f'
down_revision = '3c777ad8ef0c'
branch_labels = None
depends_on = None


def upgrade():
    """knowledgesテーブルのカラム名変更・削除マイグレーション"""
    # page_number → sequence
    op.alter_column('knowledges', 'page_number', new_column_name='sequence')
    # page_text → knowledge_text
    op.alter_column('knowledges', 'page_text', new_column_name='knowledge_text')
    # image_path削除
    op.drop_column('knowledges', 'image_path')


def downgrade():
    """knowledgesテーブルのカラム名・削除の巻き戻し"""
    # sequence → page_number
    op.alter_column('knowledges', 'sequence', new_column_name='page_number')
    # knowledge_text → page_text
    op.alter_column('knowledges', 'knowledge_text', new_column_name='page_text')
    # image_path復活
    op.add_column('knowledges', sa.Column('image_path', sa.String(length=512), nullable=False))
