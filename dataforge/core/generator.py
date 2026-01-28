"""
DataForge核心生成器接口和基类
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from .exceptions import (
    DataGenerationError,
    GeneratorConfigError,
)
from .types import GeneratorType

T = TypeVar("T")


@dataclass
class GeneratorConfig:
    """生成器配置类"""

    generator_type: str  # 生成器名称，用于在工厂中查找生成器类
    parameters: dict[str, Any]
    count: int = 1
    validate: bool = True
    unique: bool = False
    related_fields: dict[str, str] | None = None

    def get(self, key: str, default: Any = None) -> Any:
        """获取参数值，兼容字典接口

        此方法使GeneratorConfig对象具有类似字典的get方法，
        确保现有生成器代码无需修改即可正常工作。
        """
        return self.parameters.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """支持字典式访问"""
        return self.parameters[key]

    def __contains__(self, key: str) -> bool:
        """支持in操作符"""
        return key in self.parameters


@dataclass
class GenerationContext:
    """数据生成上下文"""

    config: GeneratorConfig | None = None
    related_data: dict[str, Any] | None = None
    batch_id: str | None = None
    index: int | None = None


class DataGenerator(ABC, Generic[T]):
    """数据生成器抽象基类

    所有数据生成器必须继承此类并实现所有抽象方法和属性。
    """

    def __init__(self, config: GeneratorConfig) -> None:
        if not isinstance(config, GeneratorConfig):
            raise GeneratorConfigError("Invalid generator config type")

        self.config = config
        self.parameters = config.parameters
        try:
            self._setup()
        except Exception as e:
            raise GeneratorConfigError(
                f"Generator setup failed: {str(e)}", config.generator_type
            ) from e

    def _setup(self) -> None:
        """初始化设置，子类可覆盖以设置特定参数"""
        pass

    @abstractmethod
    def generate_single(self, context: GenerationContext | None = None) -> T:
        """生成单个数据项（必须实现）

        Args:
            context: 生成上下文，包含相关数据和配置信息

        Returns:
            T: 生成的数据项

        Raises:
            DataGenerationError: 当数据生成失败时抛出
        """
        pass

    @abstractmethod
    def validate(self, data: T) -> bool:
        """验证生成的数据（必须实现）

        Args:
            data: 待验证的数据

        Returns:
            bool: 数据是否有效
        """
        pass

    @property
    @abstractmethod
    def generator_type(self) -> GeneratorType:
        """返回生成器类型（必须实现）

        Returns:
            GeneratorType: 生成器类型枚举值
        """
        pass

    @property
    @abstractmethod
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表（必须实现）

        Returns:
            list[str]: 参数名称列表
        """
        pass

    def generate(self, context: GenerationContext | None = None) -> T:
        """生成单个数据项（向后兼容方法）

        此方法调用generate_single()以保持向后兼容性。
        新代码应直接使用generate_single()。

        Args:
            context: 生成上下文，包含相关数据和配置信息

        Returns:
            T: 生成的数据项

        Raises:
            DataGenerationError: 当数据生成失败时抛出
        """
        return self.generate_single(context)

    def generate_batch(
        self, count: int, context: GenerationContext | None = None
    ) -> list[T]:
        """生成批量数据

        子类可以重写此方法以实现批量优化。
        默认实现使用循环调用generate_single()。

        Args:
            count: 生成数量
            context: 生成上下文

        Returns:
            list[T]: 生成的数据列表

        Raises:
            DataGenerationError: 当批量生成失败时抛出
        """
        if count <= 0:
            raise DataGenerationError(
                "Count must be positive", self.config.generator_type
            )

        try:
            return [self.generate_single(context) for _ in range(count)]
        except Exception as e:
            raise DataGenerationError(
                f"Batch generation failed: {str(e)}", self.config.generator_type
            ) from e
