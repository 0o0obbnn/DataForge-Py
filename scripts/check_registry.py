#!/usr/bin/env python3
"""
生成器注册和验证模块

负责管理所有数据生成器的注册、验证和生命周期管理
"""

import logging
from typing import Any, Optional

from dataforge.core.context import GenerationContext
from dataforge.generators.base import BaseGenerator

logger = logging.getLogger(__name__)


class GeneratorRegistry:
    """
    生成器注册中心

    负责管理所有可用的数据生成器，包括注册、验证、获取和实例化
    """

    def __init__(self):
        self._generators: dict[str, type[BaseGenerator]] = {}
        self._metadata: dict[str, dict[str, Any]] = {}
        self._aliases: dict[str, str] = {}

    def register(
        self,
        name: str,
        generator_class: type[BaseGenerator],
        metadata: Optional[dict[str, Any]] = None,
        aliases: Optional[list[str]] = None,
    ) -> None:
        """
        注册一个新的生成器

        Args:
            name: 生成器名称
            generator_class: 生成器类
            metadata: 生成器元数据
            aliases: 生成器别名列表
        """
        if not issubclass(generator_class, BaseGenerator):
            raise TypeError(f"生成器类必须继承自 BaseGenerator: {generator_class}")

        self._generators[name] = generator_class
        self._metadata[name] = metadata or {}

        # 注册别名
        if aliases:
            for alias in aliases:
                self._aliases[alias] = name

        logger.info(f"生成器已注册: {name}")

    def get(self, name: str) -> Optional[type[BaseGenerator]]:
        """
        获取生成器类

        Args:
            name: 生成器名称或别名

        Returns:
            生成器类，如果未找到则返回 None
        """
        # 检查别名
        actual_name = self._aliases.get(name, name)
        return self._generators.get(actual_name)

    def create(
        self, name: str, context: Optional[GenerationContext] = None, **kwargs
    ) -> Optional[BaseGenerator]:
        """
        创建生成器实例

        Args:
            name: 生成器名称或别名
            context: 生成上下文
            **kwargs: 传递给生成器构造函数的参数

        Returns:
            生成器实例，如果未找到则返回 None
        """
        generator_class = self.get(name)
        if generator_class:
            return generator_class(context=context, **kwargs)
        return None

    def list_all(self) -> list[str]:
        """获取所有注册的生成器名称"""
        return list(self._generators.keys())

    def list_aliases(self) -> dict[str, str]:
        """获取所有别名映射"""
        return self._aliases.copy()

    def get_metadata(self, name: str) -> Optional[dict[str, Any]]:
        """获取生成器元数据"""
        actual_name = self._aliases.get(name, name)
        return self._metadata.get(actual_name)

    def is_registered(self, name: str) -> bool:
        """检查生成器是否已注册"""
        actual_name = self._aliases.get(name, name)
        return actual_name in self._generators

    def unregister(self, name: str) -> bool:
        """
        取消注册生成器

        Args:
            name: 生成器名称

        Returns:
            如果成功取消注册返回 True，否则返回 False
        """
        if name in self._generators:
            del self._generators[name]
            del self._metadata[name]

            # 移除相关别名
            aliases_to_remove = [k for k, v in self._aliases.items() if v == name]
            for alias in aliases_to_remove:
                del self._aliases[alias]

            logger.info(f"生成器已取消注册: {name}")
            return True
        return False

    def clear(self) -> None:
        """清空所有注册信息"""
        self._generators.clear()
        self._metadata.clear()
        self._aliases.clear()
        logger.info("所有生成器已清空")

    def validate_dependencies(self, generator_names: list[str]) -> dict[str, Any]:
        """
        验证生成器依赖关系

        Args:
            generator_names: 要验证的生成器名称列表

        Returns:
            验证结果字典，包含是否有效、缺失的依赖等信息
        """
        missing_deps = {}
        available = set(self._generators.keys())

        for name in generator_names:
            generator_class = self.get(name)
            if generator_class and hasattr(generator_class, "get_dependencies"):
                deps = generator_class.get_dependencies()
                missing = deps - available
                if missing:
                    missing_deps[name] = list(missing)

        return {
            "valid": len(missing_deps) == 0,
            "missing_dependencies": missing_deps,
            "available_generators": list(available),
        }

    def get_generator_info(self, name: str) -> Optional[dict[str, Any]]:
        """
        获取生成器详细信息

        Args:
            name: 生成器名称或别名

        Returns:
            包含生成器信息的字典，如果未找到则返回 None
        """
        generator_class = self.get(name)
        if not generator_class:
            return None

        actual_name = self._aliases.get(name, name)
        metadata = self._metadata.get(actual_name, {})

        info = {
            "name": actual_name,
            "class": generator_class.__name__,
            "module": generator_class.__module__,
            "metadata": metadata,
            "aliases": [k for k, v in self._aliases.items() if v == actual_name],
        }

        # 添加依赖信息
        if hasattr(generator_class, "get_dependencies"):
            info["dependencies"] = list(generator_class.get_dependencies())

        return info

    def search(self, query: str) -> list[str]:
        """
        搜索生成器

        Args:
            query: 搜索关键词

        Returns:
            匹配的生成器名称列表
        """
        query = query.lower()
        matches = []

        for name in self._generators.keys():
            if query in name.lower():
                matches.append(name)

        # 搜索别名
        for alias, actual_name in self._aliases.items():
            if query in alias.lower() and actual_name not in matches:
                matches.append(actual_name)

        return matches


# 全局注册中心实例
_registry = GeneratorRegistry()


def register_generator(
    name: str,
    generator_class: type[BaseGenerator],
    metadata: Optional[dict[str, Any]] = None,
    aliases: Optional[list[str]] = None,
) -> None:
    """
    注册生成器（全局函数）

    Args:
        name: 生成器名称
        generator_class: 生成器类
        metadata: 生成器元数据
        aliases: 生成器别名列表
    """
    _registry.register(name, generator_class, metadata, aliases)


def get_generator(name: str) -> Optional[type[BaseGenerator]]:
    """获取生成器类（全局函数）"""
    return _registry.get(name)


def create_generator(
    name: str, context: Optional[GenerationContext] = None, **kwargs
) -> Optional[BaseGenerator]:
    """创建生成器实例（全局函数）"""
    return _registry.create(name, context, **kwargs)


def list_generators() -> list[str]:
    """获取所有注册的生成器名称（全局函数）"""
    return _registry.list_all()


def get_registry() -> GeneratorRegistry:
    """获取全局注册中心实例"""
    return _registry
