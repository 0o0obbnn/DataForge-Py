"""
数据校验器
"""

import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class DataValidator(ABC):
    """数据校验器抽象基类"""

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """校验数据"""
        pass

    @abstractmethod
    def get_error_message(self, data: Any) -> str:
        """获取错误信息"""
        pass


class RegexValidator(DataValidator):
    """正则表达式校验器"""

    def __init__(self, pattern: str, error_message: str = "Data format is invalid"):
        self.pattern = re.compile(pattern)
        self.error_message = error_message

    def validate(self, data: Any) -> bool:
        if not isinstance(data, str):
            return False
        return bool(self.pattern.match(data))

    def get_error_message(self, data: Any) -> str:
        return self.error_message


class LengthValidator(DataValidator):
    """长度校验器"""

    def __init__(
        self, min_length: int | None = None, max_length: int | None = None
    ):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, data: Any) -> bool:
        if hasattr(data, "__len__"):
            length = len(data)
            if self.min_length is not None and length < self.min_length:
                return False
            if self.max_length is not None and length > self.max_length:
                return False
            return True
        return False

    def get_error_message(self, data: Any) -> str:
        length = len(data) if hasattr(data, "__len__") else 0
        if self.min_length and self.max_length:
            return f"Length {length} is not between {self.min_length} and {self.max_length}"
        elif self.min_length:
            return f"Length {length} is less than minimum {self.min_length}"
        elif self.max_length:
            return f"Length {length} is greater than maximum {self.max_length}"
        return "Invalid length"


class RangeValidator(DataValidator):
    """数值范围校验器"""

    def __init__(
        self, min_value: float | None = None, max_value: float | None = None
    ):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, data: Any) -> bool:
        try:
            value = float(data)
            if self.min_value is not None and value < self.min_value:
                return False
            if self.max_value is not None and value > self.max_value:
                return False
            return True
        except (ValueError, TypeError):
            return False

    def get_error_message(self, data: Any) -> str:
        if self.min_value and self.max_value:
            return f"Value {data} is not between {self.min_value} and {self.max_value}"
        elif self.min_value:
            return f"Value {data} is less than minimum {self.min_value}"
        elif self.max_value:
            return f"Value {data} is greater than maximum {self.max_value}"
        return "Invalid value range"


class CompositeValidator(DataValidator):
    """复合校验器"""

    def __init__(self, validators: list[DataValidator], require_all: bool = True):
        self.validators = validators
        self.require_all = require_all

    def validate(self, data: Any) -> bool:
        if self.require_all:
            return all(validator.validate(data) for validator in self.validators)
        else:
            return any(validator.validate(data) for validator in self.validators)

    def get_error_message(self, data: Any) -> str:
        errors = []
        for validator in self.validators:
            if not validator.validate(data):
                errors.append(validator.get_error_message(data))
        return "; ".join(errors)


class CustomValidator(DataValidator):
    """自定义函数校验器"""

    def __init__(
        self,
        validate_func: Callable[[Any], bool],
        error_message: str = "Validation failed",
    ):
        self.validate_func = validate_func
        self.error_message = error_message

    def validate(self, data: Any) -> bool:
        return self.validate_func(data)

    def get_error_message(self, data: Any) -> str:
        return self.error_message


# 常用校验器实例
PHONE_VALIDATOR = RegexValidator(
    r"^1[3-9]\d{9}$", "Invalid Chinese mobile phone number"
)
EMAIL_VALIDATOR = RegexValidator(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", "Invalid email format"
)
IDCARD_VALIDATOR = RegexValidator(r"^\d{17}[\dXx]$", "Invalid Chinese ID card format")
