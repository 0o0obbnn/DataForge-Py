"""
数值生成器模块
"""

from .advanced import (
    CurrencyGenerator,
    IntegerGenerator,
    PercentageGenerator,
    ScientificNumberGenerator,
)
from .advanced import DecimalGenerator as AdvancedDecimalGenerator
from .decimal import DecimalGenerator
from .number import NumberGenerator

# 自动注册所有生成器类
__all__ = [
    "NumberGenerator",
    "DecimalGenerator",
    "AdvancedDecimalGenerator",
    "IntegerGenerator",
    "PercentageGenerator",
    "CurrencyGenerator",
    "ScientificNumberGenerator",
]
