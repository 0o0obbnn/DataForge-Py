"""
生成器工厂和注册表
"""

from typing import Any, Optional

from .exceptions import GeneratorConfigError, GeneratorNotFoundError
from .generator import DataGenerator, GenerationContext, GeneratorConfig
from .relations import DataRelationManager, default_relation_manager


class GeneratorRegistry:
    """生成器注册表"""

    def __init__(self) -> None:
        self._generators: dict[str, type[DataGenerator[Any]]] = {}
        self._aliases: dict[str, str] = {}

    def register(
        self,
        name: str,
        generator_class: type[DataGenerator[Any]],
        aliases: Optional[list[str]] = None,
    ) -> None:
        """注册生成器

        Args:
            name: 生成器名称
            generator_class: 生成器类
            aliases: 别名列表

        Raises:
            GeneratorConfigError: 当注册参数无效时抛出
        """
        if not name or not isinstance(name, str):
            raise GeneratorConfigError("Generator name must be a non-empty string")

        if not issubclass(generator_class, DataGenerator):
            raise GeneratorConfigError(
                f"Generator class must inherit from DataGenerator: {generator_class}"
            )

        self._generators[name] = generator_class

        if aliases:
            for alias in aliases:
                if not isinstance(alias, str):
                    raise GeneratorConfigError(f"Alias must be a string: {alias}")
                self._aliases[alias] = name

    def get_generator_class(self, name: str) -> Optional[type[DataGenerator[Any]]]:
        """获取生成器类

        Args:
            name: 生成器名称或别名

        Returns:
            Optional[Type[DataGenerator[Any]]]: 生成器类，如果未找到则返回None
        """
        if not isinstance(name, str):
            return None

        # 先检查是否为别名
        actual_name = self._aliases.get(name, name)
        return self._generators.get(actual_name)

    def list_generators(self) -> list[str]:
        """列出所有已注册的生成器名称

        Returns:
            list[str]: 生成器名称列表
        """
        return sorted(self._generators.keys())

    def is_registered(self, name: str) -> bool:
        """检查生成器是否已注册

        Args:
            name: 生成器名称或别名

        Returns:
            bool: 是否已注册
        """
        if not isinstance(name, str):
            return False

        actual_name = self._aliases.get(name, name)
        return actual_name in self._generators


class GeneratorFactory:
    """生成器工厂"""

    def __init__(
        self,
        registry: GeneratorRegistry,
        relation_manager: Optional[DataRelationManager] = None,
    ) -> None:
        self.registry = registry
        self.relation_manager = relation_manager or default_relation_manager

    def create_generator(self, config: GeneratorConfig) -> DataGenerator[Any]:
        """创建生成器实例

        Args:
            config: 生成器配置

        Returns:
            DataGenerator[Any]: 生成器实例

        Raises:
            GeneratorNotFoundError: 当生成器类型未找到时抛出
            GeneratorConfigError: 当配置无效时抛出
        """
        if not isinstance(config, GeneratorConfig):
            raise GeneratorConfigError("Invalid generator config type")

        generator_class = self.registry.get_generator_class(config.generator_type)

        if generator_class is None:
            raise GeneratorNotFoundError(config.generator_type)

        try:
            return generator_class(config)
        except Exception as e:
            raise GeneratorConfigError(
                f"Failed to create generator '{config.generator_type}': {str(e)}",
                config.generator_type,
            ) from e

    def create_generators_batch(
        self, configs: list[GeneratorConfig]
    ) -> list[DataGenerator[Any]]:
        """批量创建生成器

        Args:
            configs: 生成器配置列表

        Returns:
            list[DataGenerator[Any]]: 生成器实例列表
        """
        generators: list[DataGenerator[Any]] = []
        for config in configs:
            generator = self.create_generator(config)
            generators.append(generator)
        return generators

    def generate_batch_with_relations(
        self,
        configs: list[GeneratorConfig],
        context: Optional[GenerationContext] = None,
    ) -> dict[str, Any]:
        """批量生成数据并应用关联规则

        Args:
            configs: 生成器配置列表
            context: 生成上下文

        Returns:
            dict[str, Any]: 生成的关联数据

        Raises:
            GeneratorConfigError: 当配置无效时抛出
        """
        if not configs:
            return {}

        if context is None:
            context = GenerationContext()

        try:
            # 1. 获取字段依赖顺序
            field_names = [config.generator_type for config in configs]
            ordered_fields = self.relation_manager.get_relation_dependencies(
                field_names
            )

            # 2. 按顺序生成数据
            result_data: dict[str, Any] = {}
            config_map = {config.generator_type: config for config in configs}

            for field_name in ordered_fields:
                if field_name in config_map:
                    config = config_map[field_name]

                    # 3. 应用关联规则更新配置
                    result_data = self.relation_manager.apply_relations(
                        result_data, [config], context
                    )

                    # 4. 设置上下文关联数据
                    if context.related_data is None:
                        context.related_data = {}
                    context.related_data.update(result_data)

                    # 5. 生成数据
                    generator = self.create_generator(config)
                    generated_value = generator.generate(context)
                    result_data[field_name] = generated_value

                    # 6. 更新上下文关联数据
                    context.related_data[field_name] = generated_value

            return result_data

        except Exception as e:
            raise GeneratorConfigError(
                f"Batch generation with relations failed: {str(e)}"
            ) from e


# 全局注册表实例
default_registry = GeneratorRegistry()
default_factory = GeneratorFactory(default_registry)


def register_generator(name: str, aliases: Optional[list[str]] = None):
    """生成器注册装饰器

    Args:
        name: 生成器名称
        aliases: 别名列表

    Returns:
        装饰器函数
    """

    def decorator(
        generator_class: type[DataGenerator[Any]],
    ) -> type[DataGenerator[Any]]:
        default_registry.register(name, generator_class, aliases)
        # 存储注册信息到类属性中
        generator_class._registered_name = name  # type: ignore
        generator_class._registered_aliases = aliases or []  # type: ignore
        return generator_class

    return decorator
