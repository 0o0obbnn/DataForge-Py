"""
婚姻状况生成器

提供中国及国际通用的婚姻状况数据生成，支持年龄关联规则。
"""

import random
from typing import Any, Optional, Union

try:
    from typing import override
except ImportError:
    from typing_extensions import override

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
    GeneratorType,
)


@register_generator("marital_status")
class MaritalStatusGenerator(DataGenerator[str]):
    """婚姻状况生成器基类"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.region: str = self.parameters.get("region", "china")
        self.include_age_factor: bool = self.parameters.get("include_age_factor", True)
        self._setup()

    @override
    def _setup(self) -> None:
        """初始化设置"""
        pass

    @property
    @override
    def generator_type(self) -> GeneratorType:
        """获取生成器类型"""
        return GeneratorType.BASIC

    @property
    @override
    def supported_parameters(self) -> list[str]:
        """获取支持的参数列表"""
        return ["region", "include_age_factor"]

    def _get_marital_status_options(self) -> list[str]:
        """获取婚姻状况选项"""
        if self.region == "china":
            return [
                "未婚",
                "已婚",
                "离异",
                "丧偶",
                "再婚",
            ]
        else:  # international
            return [
                "single",
                "married",
                "divorced",
                "widowed",
                "separated",
            ]

    def _age_based_weights(self, age: Optional[int] = None) -> list[float]:
        """基于年龄的婚姻状况权重"""
        if age is None or not self.include_age_factor:
            # 默认权重分布
            return [0.35, 0.45, 0.12, 0.05, 0.03]

        if age < 20:
            return [0.85, 0.10, 0.03, 0.01, 0.01]  # 年轻人未婚率高
        elif age < 30:
            return [0.45, 0.48, 0.05, 0.01, 0.01]  # 适婚年龄
        elif age < 40:
            return [0.15, 0.70, 0.10, 0.03, 0.02]  # 中年已婚为主
        elif age < 50:
            return [0.08, 0.75, 0.12, 0.03, 0.02]  # 中年稳定期
        else:  # 50+
            return [0.05, 0.65, 0.15, 0.10, 0.05]  # 老年丧偶率增加

    @override
    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始婚姻状况字符串"""
        options = self._get_marital_status_options()

        # 从context获取年龄信息
        age: Optional[int] = None
        if context and context.related_data:
            if "age" in context.related_data:
                age = context.related_data["age"]
            elif "birth_year" in context.related_data:
                from datetime import datetime
                current_year = datetime.now().year
                age = current_year - context.related_data["birth_year"]

        weights = self._age_based_weights(age)
        return random.choices(options, weights=weights)[0]

    def get_marital_status_options(self) -> list[str]:
        """获取婚姻状况选项（公共方法）"""
        return self._get_marital_status_options()

    def get_age_based_weights(self, age: Optional[int] = None) -> list[float]:
        """获取基于年龄的权重（公共方法）"""
        return self._age_based_weights(age)

    def generate(self, context: Optional[Union[GenerationContext, dict[str, Any]]] = None) -> str:
        """生成单个数据项（重载以支持字典类型的context）"""
        if isinstance(context, dict):
            # 为了兼容测试，将字典包装成GenerationContext
            from dataforge.core.generator import GenerationContext
            wrapped_context = GenerationContext(related_data=context)
            return self.generate_single(wrapped_context)
        return self.generate_single(context)

    @override
    def validate(self, data: str) -> bool:
        """验证婚姻状况格式"""
        valid_options = self._get_marital_status_options()
        return isinstance(data, str) and bool(data.strip()) and data.strip() in valid_options
