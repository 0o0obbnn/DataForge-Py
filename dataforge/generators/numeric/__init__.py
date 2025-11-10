"""
数值生成器模块
"""

from .advanced import (
    CurrencyGenerator,
    DecimalGenerator as AdvancedDecimalGenerator,
    IntegerGenerator,
    PercentageGenerator,
    ScientificNumberGenerator,
)
from .number import NumberGenerator
from .decimal import DecimalGenerator

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
