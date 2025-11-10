"""通用参数验证工具"""

from typing import Any, Optional, Tuple
from datetime import datetime, date

from .exceptions import GeneratorConfigError


class ParameterValidator:
    """参数验证器基类"""

    @staticmethod
    def validate_positive_int(
        value: Any,
        param_name: str,
        min_value: int = 1
    ) -> int:
        """验证正整数参数

        Args:
            value: 参数值
            param_name: 参数名称
            min_value: 最小值

        Returns:
            int: 验证后的整数值

        Raises:
            GeneratorConfigError: 参数无效时抛出
        """
        try:
            int_value = int(value)
            if int_value < min_value:
                raise GeneratorConfigError(
                    f"{param_name} must be >= {min_value}, got {int_value}"
                )
            return int_value
        except (ValueError, TypeError):
            raise GeneratorConfigError(
                f"{param_name} must be an integer, got {type(value).__name__}"
            )

    @staticmethod
    def validate_date_range(
        start_date: str,
        end_date: str,
        param_name: str = "date_range"
    ) -> Tuple[date, date]:
        """验证日期范围

        Args:
            start_date: 开始日期字符串 (YYYY-MM-DD)
            end_date: 结束日期字符串 (YYYY-MM-DD)
            param_name: 参数名称

        Returns:
            Tuple[date, date]: 验证后的日期范围

        Raises:
            GeneratorConfigError: 日期格式无效或范围不合理时抛出
        """
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()

            if start >= end:
                raise GeneratorConfigError(
                    f"{param_name}: start_date must be before end_date"
                )

            return start, end

        except ValueError as e:
            raise GeneratorConfigError(
                f"{param_name}: Invalid date format. Use YYYY-MM-DD. Error: {e}"
            )

    @staticmethod
    def validate_choice(
        value: str,
        choices: list[str],
        param_name: str,
        case_sensitive: bool = False
    ) -> str:
        """验证选项参数

        Args:
            value: 参数值
            choices: 有效选项列表
            param_name: 参数名称
            case_sensitive: 是否大小写敏感

        Returns:
            str: 验证后的值（可能已转换大小写）

        Raises:
            GeneratorConfigError: 值不在有效选项中时抛出
        """
        if not case_sensitive:
            value = value.upper()
            choices = [c.upper() for c in choices]

        if value not in choices:
            raise GeneratorConfigError(
                f"{param_name} must be one of {choices}, got '{value}'"
            )

        return value

    @staticmethod
    def validate_range(
        value: float,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        param_name: str = "value"
    ) -> float:
        """验证数值范围

        Args:
            value: 参数值
            min_value: 最小值（可选）
            max_value: 最大值（可选）
            param_name: 参数名称

        Returns:
            float: 验证后的值

        Raises:
            GeneratorConfigError: 值超出范围时抛出
        """
        if min_value is not None and value < min_value:
            raise GeneratorConfigError(
                f"{param_name} must be >= {min_value}, got {value}"
            )

        if max_value is not None and value > max_value:
            raise GeneratorConfigError(
                f"{param_name} must be <= {max_value}, got {value}"
            )

        return value