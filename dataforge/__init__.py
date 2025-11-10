"""
DataForge - 高效、灵活的测试数据生成工具
"""

__version__ = "1.0.0"
__author__ = "DataForge Team"
__email__ = "contact@dataforge.org"
__license__ = "MIT"

from .cli.main import main as cli_main
from .core.factory import default_factory, default_registry, register_generator
from .core.generator import DataGenerator, GenerationContext, GeneratorConfig


# 自动注册内置生成器和启动数据预加载
def _register_builtin_generators() -> None:
    """注册内置生成器"""
    try:
        # 导入各类生成器
        from .generators import (
            basic,
            contact,
            finance,
            identifier,
            network,
            numeric,
            text,
            # datetime模块暂未实现，跳过
        )
    except ImportError as e:
        print(f"警告: 内置生成器注册失败: {e}")
        pass  # 在某些情况下可能无法导入


def _initialize_performance_optimizations() -> None:
    """初始化性能优化功能"""
    try:
        from .core.preloader import start_data_preload

        # 启动数据预加载（异步执行，不会阻塞导入）
        start_data_preload()
    except ImportError:
        pass  # 如果预加载模块不可用，跳过


_register_builtin_generators()
_initialize_performance_optimizations()

__all__ = [
    "DataGenerator",
    "GeneratorConfig",
    "GenerationContext",
    "default_factory",
    "default_registry",
    "register_generator",
    "cli_main",
]
