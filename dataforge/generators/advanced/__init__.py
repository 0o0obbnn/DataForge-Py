"""
高级生成器模块
"""

try:
    # 导入所有高级生成器以触发注册
    from . import (
        advanced_timestamp,
        datetime,
        enhanced_timestamp,
        json_generator,
        media_files,
        sql_injection,
        trading_calendar,
        user_behavior,
        xml_generator,
        xss_payload,
        yaml_generator,
    )
except ImportError as e:
    print(f"警告: 部分高级生成器导入失败: {e}")

__all__ = [
    "advanced_timestamp",
    "datetime",
    "enhanced_timestamp",
    "json_generator",
    "media_files",
    "sql_injection",
    "trading_calendar",
    "user_behavior",
    "xml_generator",
    "xss_payload",
    "yaml_generator",
]