"""
DataForge 核心模块

核心模块包含DataForge的基础组件，负责数据生成的核心逻辑、工厂模式实现和类型系统。

主要组件：
- GeneratorConfig: 生成器配置，定义生成器的参数和行为
- default_factory: 默认工厂实例，用于快速创建各种数据
- default_registry: 默认注册表，管理已注册的生成器
- DataGenerator: 数据生成器基类，定义所有生成器的通用接口
- GeneratorType: 定义生成器类型（基本、复杂、高级）
- Validator: 数据验证器，用于验证生成数据的有效性

使用示例：
```python
# 使用默认工厂创建数据
from dataforge.core import default_factory

# 创建基本数据
string_data = default_factory.create("string")

# 使用配置
config = {"type": "integer", "min": 1, "max": 100}
data = default_factory.create_with_config(config)

# 验证数据
from dataforge.core import Validator
validator = Validator()
result = validator.validate(data, {"type": "integer", "min": 1})
```
"""

from .factory import GeneratorConfig, default_factory, default_registry
from .generator import DataGenerator
from .types import GeneratorType
from .validator import DataValidator as Validator

__all__ = [
    "GeneratorConfig",
    "default_factory",
    "default_registry",
    "DataGenerator",
    "GeneratorType",
    "Validator",
]
