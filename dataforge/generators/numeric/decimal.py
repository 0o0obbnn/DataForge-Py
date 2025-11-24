"""小数生成器模块"""

import random
from typing import Optional, Union

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorType,
)


class DecimalGenerator(DataGenerator):
    """小数生成器"""

    def _setup(self) -> None:
        """初始化设置"""
        pass

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> float:
        """生成小数"""
        min_val = self.parameters.get("min", 0.0)
        max_val = self.parameters.get("max", 1.0)
        decimal_places = self.parameters.get("decimal_places", 2)

        value = random.uniform(float(min_val), float(max_val))
        return round(value, decimal_places)

    def validate(self, data: Union[int, float]) -> bool:
        """验证小数"""
        if not isinstance(data, (int, float)):
            return False

        min_val = self.parameters.get("min", float("-inf"))
        max_val = self.parameters.get("max", float("inf"))

        return min_val <= data <= max_val

    def generate_single(self, context: Optional[GenerationContext] = None) -> float:
        """生成单个数据项"""
        return self._generate_raw(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.NUMERIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["min", "max", "decimal_places"]


# 注册生成器
register_generator("decimal")(DecimalGenerator)
