"""
数据生成上下文管理模块

提供数据关联性和生成器间依赖管理功能
"""

import builtins
import logging
import threading
from collections import defaultdict
from typing import Any, Optional

from .generator import GenerationContext

logger = logging.getLogger(__name__)


class ExtendedGenerationContext(GenerationContext):
    """
    扩展的数据生成上下文管理器

    用于在生成过程中传递和存储已生成的数据，
    支持生成器间的数据依赖和上下文共享
    """

    def __init__(self):
        super().__init__()
        self._data: dict[str, Any] = {}
        self._metadata: dict[str, dict[str, Any]] = {}
        self._dependencies: dict[str, set[str]] = defaultdict(set)
        self._lock = threading.RLock()
        self._generation_order: list[str] = []

    def set(
        self, key: str, value: Any, metadata: Optional[dict[str, Any]] = None
    ) -> None:
        """设置上下文数据"""
        with self._lock:
            self._data[key] = value
            if metadata:
                self._metadata[key] = metadata
            logger.debug(f"Context set: {key} = {type(value).__name__}")

    def get(self, key: str, default: Any = None) -> Any:
        """获取上下文数据"""
        with self._lock:
            return self._data.get(key, default)

    def has(self, key: str) -> bool:
        """检查键是否存在"""
        with self._lock:
            return key in self._data

    def remove(self, key: str) -> bool:
        """移除上下文数据"""
        with self._lock:
            if key in self._data:
                del self._data[key]
                if key in self._metadata:
                    del self._metadata[key]
                return True
            return False

    def add_dependency(self, generator: str, depends_on: str) -> None:
        """添加生成器依赖关系"""
        with self._lock:
            self._dependencies[generator].add(depends_on)
            logger.debug(f"Dependency added: {generator} -> {depends_on}")

    def get_dependencies(self, generator: str) -> builtins.set[str]:
        """获取生成器的依赖项"""
        with self._lock:
            return self._dependencies.get(generator, set()).copy()

    def get_all_dependencies(self) -> dict[str, builtins.set[str]]:
        """获取所有依赖关系"""
        with self._lock:
            return {k: v.copy() for k, v in self._dependencies.items()}

    def clear(self) -> None:
        """清空上下文数据"""
        with self._lock:
            self._data.clear()
            self._metadata.clear()
            self._dependencies.clear()
            self._generation_order.clear()
            logger.debug("Context cleared")

    def snapshot(self) -> dict[str, Any]:
        """创建上下文快照"""
        with self._lock:
            return {
                "data": self._data.copy(),
                "metadata": self._metadata.copy(),
                "dependencies": dict(self._dependencies),
                "generation_order": self._generation_order.copy(),
            }

    def restore(self, snapshot: dict[str, Any]) -> None:
        """从快照恢复上下文"""
        with self._lock:
            self._data = snapshot["data"].copy()
            self._metadata = snapshot["metadata"].copy()
            self._dependencies = defaultdict(set)
            for k, v in snapshot["dependencies"].items():
                self._dependencies[k] = set(v)
            self._generation_order = snapshot["generation_order"].copy()
            logger.debug("Context restored from snapshot")

    def add_generation_order(self, generator_name: str) -> None:
        """记录生成顺序"""
        with self._lock:
            if generator_name not in self._generation_order:
                self._generation_order.append(generator_name)

    def get_generation_order(self) -> list[str]:
        """获取生成顺序"""
        with self._lock:
            return self._generation_order.copy()

    def get_metadata(self, key: str) -> Optional[dict[str, Any]]:
        """获取数据的元数据"""
        with self._lock:
            return self._metadata.get(key)

    def keys(self) -> list[str]:
        """获取所有键"""
        with self._lock:
            return list(self._data.keys())

    def items(self) -> list[tuple[str, Any]]:
        """获取所有键值对"""
        with self._lock:
            return list(self._data.items())


class DependencyResolver:
    """
    生成器依赖解析器

    负责解析生成器间的依赖关系，确保正确的生成顺序
    """

    @staticmethod
    def topological_sort(dependencies: dict[str, set[str]]) -> list[str]:
        """
        使用拓扑排序确定生成器的执行顺序

        Args:
            dependencies: 生成器依赖关系字典

        Returns:
            排序后的生成器名称列表

        Raises:
            ValueError: 如果存在循环依赖
        """
        # 初始化结果列表和访问状态
        result = []
        visited = set()
        temp = set()

        def visit(node: str):
            if node in temp:
                raise ValueError(f"检测到循环依赖: {node}")
            if node not in visited:
                temp.add(node)
                if node in dependencies:
                    for neighbor in dependencies[node]:
                        visit(neighbor)
                temp.remove(node)
                visited.add(node)
                result.append(node)

        # 遍历所有节点
        for node in dependencies:
            if node not in visited:
                visit(node)

        return result

    @staticmethod
    def validate_dependencies(dependencies: dict[str, set[str]]) -> bool:
        """验证依赖关系是否有效"""
        try:
            DependencyResolver.topological_sort(dependencies)
            return True
        except ValueError:
            return False

    def _get_all_dependencies(self, generator_name: str) -> builtins.set[str]:
        """
        获取指定生成器的所有（传递闭包）依赖。
        注意：
            - 当前类未持有全局依赖图，也未在方法签名中传入依赖关系，因此无法在此处解析实际依赖。
            - 为保持类型安全并修复 Pylance 对未知属性的报错，此实现返回空集合。
            - 若未来需要启用该功能，应在 DependencyResolver 中引入依赖图（例如通过参数传入或实例属性注入），
              然后在此方法中执行递归解析并返回闭包依赖集合。
        """
        return set()

    def _find_missing_dependencies(
        self, required_generators: set[str], available_generators: set[str]
    ) -> dict[str, set[str]]:
        """找出缺失的依赖项"""
        missing = {}
        for generator_name in required_generators:
            if generator_name not in available_generators:
                missing_generators = self._get_all_dependencies(generator_name)
                missing[generator_name] = missing_generators - available_generators
        return missing


class ContextAwareGenerator:
    """
    上下文感知生成器基类

    为需要依赖上下文的生成器提供基础支持
    """

    def __init__(self, context: Optional[ExtendedGenerationContext] = None):
        self.context = context or ExtendedGenerationContext()
        self._dependencies: set[str] = set()

    def add_dependency(self, *generators: str) -> None:
        """添加依赖的生成器"""
        self._dependencies.update(generators)

    def get_dependencies(self) -> set[str]:
        """获取所有依赖的生成器"""
        return self._dependencies.copy()

    def validate_dependencies(self, available_generators: set[str]) -> bool:
        """验证依赖是否满足"""
        return self._dependencies.issubset(available_generators)

    def get_missing_dependencies(self, available_generators: set[str]) -> set[str]:
        """获取缺失的依赖"""
        return self._dependencies - available_generators

    def ensure_dependencies(self) -> None:
        """确保所有依赖项都已生成"""
        missing = []
        for dep in self._dependencies:
            if not self.context.has(dep):
                missing.append(dep)

        if missing:
            raise ValueError(f"缺少依赖的生成器: {missing}")

    def get_context_value(self, key: str, default: Any = None) -> Any:
        """从上下文中获取值"""
        return self.context.get(key, default)

    def set_context_value(
        self, key: str, value: Any, metadata: Optional[dict[str, Any]] = None
    ) -> None:
        """向上下文中设置值"""
        self.context.set(key, value, metadata)
        self.context.add_generation_order(self.__class__.__name__)
