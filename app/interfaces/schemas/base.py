"""
共通スキーマ基底クラス

- 全てのスキーマはこのCustomBaseModelを継承すること
- レスポンス時はキャメルケースで出力される
"""

from pydantic import BaseModel, field_serializer
from datetime import datetime
import logging
import zoneinfo

# ロガーの取得
logger = logging.getLogger("app.interfaces.schemas.base")

def snake_to_camel(string: str) -> str:
    """
    スネークケースをキャメルケースに変換するユーティリティ関数

    Args:
        string (str): スネークケースの文字列

    Returns:
        str: キャメルケースの文字列
    """
    parts = string.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


class CustomBaseModel(BaseModel):
    """
    全スキーマ共通の基底クラス

    - レスポンス時はキャメルケースで出力される
    - datetime型フィールドはJST（Asia/Tokyo）で返却される

    Note:
        datetime型フィールドは自動的にUTC→JST変換されます。
    """

    model_config = {
        "alias_generator": snake_to_camel,
        "populate_by_name": True,
        "from_attributes": True,
    }

    @field_serializer(datetime, mode="plain", check_fields=False)
    def serialize_datetime_to_jst(self, value: datetime):
        """
        datetime型フィールドをJST（Asia/Tokyo）に変換してISOフォーマットで返却する

        Args:
            value (datetime): UTCのdatetime

        Returns:
            str: JSTのISOフォーマット文字列
        """
        if value is None:
            return None
        if value.tzinfo is None:
            # naiveな場合はUTCとして扱う
            value = value.replace(tzinfo=zoneinfo.ZoneInfo("UTC"))
        jst_value = value.astimezone(zoneinfo.ZoneInfo("Asia/Tokyo"))
        logger.debug(f"Serialize datetime: {value.isoformat()} (UTC) -> {jst_value.isoformat()} (JST)")
        return jst_value.isoformat()
