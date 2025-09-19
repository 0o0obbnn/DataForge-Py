"""
核心类型定义模块

定义系统中使用的枚举类型和基础类型
"""

from enum import Enum
from typing import Any, Union


class GeneratorType(Enum):
    """生成器类型枚举"""

    BASIC = "basic"
    AUTH = "auth"
    CONTACT = "contact"
    DATETIME = "datetime"
    FINANCE = "finance"
    IDENTIFIER = "identifier"
    NETWORK = "network"
    NUMERIC = "numeric"
    TEXT = "text"


class DataType(Enum):
    """数据类型枚举"""

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"
    URL = "url"
    EMAIL = "email"
    IP = "ip"
    PHONE = "phone"


class ValidationLevel(Enum):
    """验证级别枚举"""

    STRICT = "strict"
    NORMAL = "normal"
    LOOSE = "loose"


class GenerationMode(Enum):
    """生成模式枚举"""

    RANDOM = "random"
    SEQUENTIAL = "sequential"
    PATTERN = "pattern"
    CONTEXTUAL = "contextual"


# 基础类型别名
Parameters = dict[str, Any]
ValidationResult = dict[str, Union[bool, str, list[str]]]
GeneratorConfig = dict[str, Any]
DataSchema = dict[str, Any]