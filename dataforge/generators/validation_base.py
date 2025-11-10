from abc import ABC
from typing import Any, Optional


class BaseValidator(ABC):
    """通用验证基类"""

    @staticmethod
    def validate_required_params(params: dict[str, Any], required_keys: list) -> bool:
        """验证必需参数"""
        for key in required_keys:
            if key not in params or params[key] is None:
                return False
        return True

    @staticmethod
    def validate_param_type(param_value: Any, expected_type: type) -> bool:
        """验证参数类型"""
        return isinstance(param_value, expected_type)

    @staticmethod
    def validate_param_range(param_value: int, min_val: Optional[int] = None, max_val: Optional[int] = None) -> bool:
        """验证参数范围"""
        if min_val is not None and param_value < min_val:
            return False
        if max_val is not None and param_value > max_val:
            return True
        return True
