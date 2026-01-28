"""DataForge - 高效、灵活的测试数据生成工具

DataForge是一个功能丰富的Python库，用于高效生成、转换和处理各种类型的数据。
它支持从简单的数据类型到复杂的结构化数据的生成，并提供多种配置选项。

主要功能：
- 支持多种基础数据类型生成
- 提供复杂数据结构生成能力
- 内置性能优化机制
- 支持自定义生成器扩展
- 命令行工具支持

使用示例：
```python
# 💡 简化 API（推荐新手使用）
from dataforge import gen

# 生成单个数据
name = gen.name()
phone = gen.phone(operator='MOBILE')

# 批量生成数据
names = gen.name(count=10)
idcards = gen.idcard(region='北京', gender='MALE', count=5)

# 🔧 高级 API（适用于复杂场景）
from dataforge import default_factory, GeneratorConfig

# 使用配置创建生成器
config = GeneratorConfig(
    generator_type='idcard',
    parameters={'region': '北京', 'gender': 'MALE'}
)
generator = default_factory.create_generator(config)
data = generator.generate_batch(10)

# 自定义生成器注册
from dataforge import register_generator

@register_generator("custom")
class CustomGenerator:
    def generate_single(self):
        return {"custom_field": "generated_value"}
```

版本: 1.0.0
作者: DataForge Team
邮箱: contact@dataforge.org
许可证: MIT
"""

__version__ = "1.0.0"
__author__ = "DataForge Team"
__email__ = "contact@dataforge.org"
__license__ = "MIT"

from .cli.main import main as cli_main
from .core.facade import DataForge, create_gen, gen
from .core.factory import default_factory, default_registry, register_generator
from .core.generator import DataGenerator, GenerationContext, GeneratorConfig


# 自动注册内置生成器和启动数据预加载
def _register_builtin_generators() -> None:
    """注册内置生成器"""
    try:
        # 导入各类生成器
        from .generators import (  # datetime模块暂未实现，跳过
            basic,
            contact,
            finance,
            identifier,
            network,
            numeric,
            text,
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
    # 简化 API（推荐）
    "gen",
    "DataForge",
    "create_gen",
    # 高级 API
    "DataGenerator",
    "GeneratorConfig",
    "GenerationContext",
    "default_factory",
    "default_registry",
    "register_generator",
    # CLI
    "cli_main",
]
