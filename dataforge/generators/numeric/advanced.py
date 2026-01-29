"""高级数值生成器
支持整数、小数、百分比、币种金额等多种数值类型
"""

import random
import secrets
from decimal import ROUND_HALF_UP, Decimal

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorType,
)

from ...resources.finance_data_loader import load_finance_data_config


class IntegerGenerator(DataGenerator[int]):
    """专用整数生成器"""

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.NUMERIC

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "min_value",
            "max_value",
            "step",
            "include_negative",
            "include_zero",
            "format_string",
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.min_value = self.parameters.get("min_value", 0)
        self.max_value = self.parameters.get("max_value", 100)
        self.step = self.parameters.get("step", 1)
        self.include_negative = self.parameters.get("include_negative", True)
        self.include_zero = self.parameters.get("include_zero", True)
        self.format_string = self.parameters.get("format_string", None)

    def _generate_raw(self, context: GenerationContext | None = None) -> int:
        """生成整数"""
        # 确保step为正数
        step = max(1, abs(self.step))

        # 计算可能的值范围
        min_val = int(self.min_value)
        max_val = int(self.max_value)

        # 生成范围内的随机整数
        if min_val > max_val:
            min_val, max_val = max_val, min_val

        # 考虑步长
        if step > 1:
            possible_values = list(range(min_val, max_val + 1, step))
            if not possible_values:
                possible_values = [min_val]
            value = random.choice(possible_values)
        else:
            value = secrets.randbelow(max_val - min_val + 1) + min_val

        return value

    def generate_single(self, context: GenerationContext | None = None) -> int:
        """生成单个数据项"""
        return self._generate_raw(context)

    def validate(self, data: int) -> bool:
        """验证生成的数据"""
        if not isinstance(data, int):
            return False
        return self.min_value <= data <= self.max_value


class DecimalGenerator(DataGenerator[Decimal]):
    """小数生成器 - 支持精度控制"""

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.NUMERIC

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "min_value",
            "max_value",
            "precision",
            "scale",
            "include_negative",
            "include_zero",
            "rounding_mode",
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.min_value = Decimal(str(self.parameters.get("min_value", 0.0)))
        self.max_value = Decimal(str(self.parameters.get("max_value", 100.0)))
        self.precision = self.parameters.get("precision", 10)
        self.scale = self.parameters.get("scale", 2)
        self.include_negative = self.parameters.get("include_negative", True)
        self.include_zero = self.parameters.get("include_zero", True)
        self.rounding_mode = self.parameters.get("rounding_mode", ROUND_HALF_UP)

    def _generate_raw(self, context: GenerationContext | None = None) -> Decimal:
        """生成小数"""
        # 确保范围正确
        min_val = min(self.min_value, self.max_value)
        max_val = max(self.min_value, self.max_value)

        # 生成随机小数
        value = Decimal(random.uniform(float(min_val), float(max_val)))
        return value.quantize(
            Decimal("0." + "0" * self.scale), rounding=self.rounding_mode
        )

    def generate_single(self, context: GenerationContext | None = None) -> Decimal:
        """生成单个数据项"""
        return self._generate_raw(context)

    def validate(self, data: Decimal) -> bool:
        """验证生成的数据"""
        if not isinstance(data, Decimal):
            return False
        return self.min_value <= data <= self.max_value


class PercentageGenerator(DataGenerator[float | str]):
    """百分比生成器"""

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.NUMERIC

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "min_value",
            "max_value",
            "precision",
            "include_symbol",
            "format_string",
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.min_value = self.parameters.get("min_value", 0.0)
        self.max_value = self.parameters.get("max_value", 100.0)
        self.precision = self.parameters.get("precision", 2)
        self.include_symbol = self.parameters.get("include_symbol", False)
        self.format_string = self.parameters.get("format_string", None)

    def _generate_raw(self, context: GenerationContext | None = None) -> float:
        """生成百分比"""
        # 确保范围在0-100之间
        min_val = max(0.0, min(100.0, float(self.min_value)))
        max_val = max(0.0, min(100.0, float(self.max_value)))

        if min_val > max_val:
            min_val, max_val = max_val, min_val

        # 生成随机百分比
        value = random.uniform(min_val, max_val)
        return round(value, self.precision)

    def generate(self, context: GenerationContext | None = None) -> float | str:
        """生成百分比"""
        value = self._generate_raw(context)
        if self.include_symbol:
            return f"{value}%"
        else:
            return value

    def generate_single(self, context: GenerationContext | None = None) -> float | str:
        """生成单个数据项"""
        return self.generate(context)

    def validate(self, data: float | str) -> bool:
        """验证生成的数据"""
        # 如果是字符串且包含%符号，提取数值部分验证
        if isinstance(data, str) and data.endswith("%"):
            try:
                value = float(data[:-1])
                return 0.0 <= value <= 100.0
            except ValueError:
                return False
        elif isinstance(data, (int, float)):
            return 0.0 <= data <= 100.0
        return False


class CurrencyGenerator(DataGenerator[str]):
    """币种金额生成器 - 支持多币种、格式化"""

    def _setup(self) -> None:
        self.currency = self.parameters.get("currency", "CNY")
        self.min_value = self.parameters.get("min_value", 0.01)
        self.max_value = self.parameters.get("max_value", 10000.0)
        self.precision = self.parameters.get("precision", 2)
        # 加载金融配置（仅用于货币符号映射）
        locale = self.parameters.get("locale", "zh_CN")
        self._finance_config = load_finance_data_config(locale=locale)

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        # 生成随机金额
        amount = round(random.uniform(self.min_value, self.max_value), self.precision)

        currency_symbols = self._finance_config.get("currency_symbols", {})
        symbol = currency_symbols.get(self.currency, self.currency)
        return f"{symbol}{amount:,.{self.precision}f}"

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        return isinstance(data, str) and len(data) > 0

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.NUMERIC

    @property
    def supported_parameters(self) -> list[str]:
        return ["currency", "min_value", "max_value", "precision", "locale"]


class ScientificNumberGenerator(DataGenerator[str]):
    """科学计数法生成器"""

    def _setup(self) -> None:
        self.min_value = self.parameters.get("min_value", 1e-6)
        self.max_value = self.parameters.get("max_value", 1e6)
        self.precision = self.parameters.get("precision", 2)

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        import random

        value = random.uniform(self.min_value, self.max_value)
        return f"{value:.{self.precision}e}"

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        return isinstance(data, str) and ("e" in data or "E" in data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.NUMERIC

    @property
    def supported_parameters(self) -> list[str]:
        return ["min_value", "max_value", "precision"]


# 注册生成器
register_generator("integer", ["整数"])(IntegerGenerator)
register_generator("decimal", ["小数"])(DecimalGenerator)
register_generator("percentage", ["百分比"])(PercentageGenerator)
register_generator("currency", ["货币"])(CurrencyGenerator)
register_generator("scientific", ["科学计数"])(ScientificNumberGenerator)
