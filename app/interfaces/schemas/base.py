"""
共通スキーマ基底クラス

- 全てのスキーマはこのCustomBaseModelを継承すること
- レスポンス時はキャメルケースで出力される
"""

from pydantic import BaseModel


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
    """

    model_config = {
        "alias_generator": snake_to_camel,
        "populate_by_name": True,
        "from_attributes": True,
    }
