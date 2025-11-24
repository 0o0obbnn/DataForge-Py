"""数字生成器模块"""

import random
from typing import Optional, Union

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorType,
)


class NumberGenerator(DataGenerator):
    """数字生成器"""

    def _setup(self) -> None:
        """初始化设置"""
        pass

    def _generate_raw(
        self, context: Optional[GenerationContext] = None
    ) -> Union[int, float]:
        """生成数字"""
        num_type = self.parameters.get("type", "integer")
        min_val = self.parameters.get("min", 0)
        max_val = self.parameters.get("max", 100)

        if num_type == "float":
            return self._generate_float(min_val, max_val)
        else:
            return self._generate_integer(min_val, max_val)

    def _generate_integer(self, min_val: int, max_val: int) -> int:
        """生成整数"""
        return random.randint(int(min_val), int(max_val))

    def _generate_float(self, min_val: float, max_val: float) -> float:
        """生成浮点数"""
        decimal_places = self.parameters.get("decimal_places", 2)
        value = random.uniform(float(min_val), float(max_val))
        return round(value, decimal_places)

    def validate(self, data: Union[int, float]) -> bool:
        """验证数字"""
        if not isinstance(data, (int, float)):
            return False

        min_val = self.parameters.get("min", float("-inf"))
        max_val = self.parameters.get("max", float("inf"))

        return min_val <= data <= max_val

    def generate_single(
        self, context: Optional[GenerationContext] = None
    ) -> Union[int, float]:
        """生成单个数据项"""
        return self._generate_raw(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.NUMERIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["type", "min", "max", "decimal_places"]


# 注册生成器
register_generator("number")(NumberGenerator)
