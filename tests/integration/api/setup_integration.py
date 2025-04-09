# tests/integration/api/setup_integration.py
import logging
from sqlalchemy import text
from app.infrastructure.database.connection import get_db

logger = logging.getLogger(__name__)

async def setup_datasets_table():
    """統合テスト用にdatasetsテーブルを作成する"""
    # データベースセッションを取得
    db_generator = get_db()
    db = next(db_generator)
    
    try:
        # テーブルが存在するか確認
        check_query = text("SELECT OBJECT_ID('datasets')")
        result = db.execute(check_query)
        table_exists = result.scalar() is not None
        
        if not table_exists:
            # テーブルが存在しない場合は作成
            create_table_query = text("""
            CREATE TABLE datasets (
                id NVARCHAR(36) PRIMARY KEY,
                name NVARCHAR(255) NOT NULL,
                description NVARCHAR(MAX),
                meta_data NVARCHAR(MAX),
                created_at DATETIME,
                updated_at DATETIME
            )
            """)
            db.execute(create_table_query)
            db.commit()
            logger.info("Created datasets table for integration tests")
        else:
            logger.info("datasets table already exists")
    
    except Exception as e:
        logger.error(f"Error setting up datasets table: {str(e)}")
        db.rollback()
        raise
    finally:
        db_generator.close()