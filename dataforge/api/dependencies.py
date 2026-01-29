"""
依赖注入提供者

FastAPI的Depends函数，用于注入注册表、关系管理器和生成器工厂
"""

from fastapi import Depends

from ..core.factory import (
    GeneratorFactory,
    GeneratorRegistry,
    default_registry,
)
from ..core.relations import (
    DataRelationManager,
    default_relation_manager,
)


def get_registry() -> GeneratorRegistry:
    """
    获取生成器注册表

    返回全局默认注册表实例
    注意：注册表在导入时通过装饰器填充，这里仍使用全局实例
    更高级的模式可能涉及应用启动事件来构建注册表
    """
    return default_registry


def get_relation_manager() -> DataRelationManager:
    """
    获取数据关系管理器

    返回全局默认关系管理器实例
    """
    return default_relation_manager


def get_generator_factory(
    registry: GeneratorRegistry = Depends(get_registry),
    relation_manager: DataRelationManager = Depends(get_relation_manager),
) -> GeneratorFactory:
    """
    获取生成器工厂

    Args:
        registry: 生成器注册表（通过Depends注入）
        relation_manager: 数据关系管理器（通过Depends注入）

    Returns:
        GeneratorFactory实例
    """
    return GeneratorFactory(registry, relation_manager)
