"""
DataForge 简化API门面

提供类似 Faker 的链式调用方式，简化常见使用场景。

使用示例：
    from dataforge import gen

    # 生成单个数据
    name = gen.name()
    phone = gen.phone(operator='MOBILE')

    # 批量生成
    names = gen.name(count=10)
    idcards = gen.idcard(region='北京', gender='MALE', count=5)
"""

from collections.abc import Callable
from typing import Any

from .exceptions import GeneratorNotFoundError
from .factory import GeneratorFactory, default_registry
from .generator import GeneratorConfig


class DataForge:
    """
    DataForge 简化API门面类

    通过动态属性访问的方式提供简洁的数据生成接口。
    每个属性对应一个已注册的生成器类型。

    特性：
    - 简洁的链式调用：gen.name(), gen.phone()
    - 灵活的参数传递：gen.idcard(region='北京', gender='MALE')
    - 智能批量生成：count=1返回单值，count>1返回列表
    - 友好的错误提示：生成器不存在时给出建议

    示例：
        >>> gen = DataForge()
        >>> # 生成单个姓名
        >>> name = gen.name()
        >>> # 生成10个手机号
        >>> phones = gen.phone(count=10, operator='MOBILE')
        >>> # 生成5个北京身份证号
        >>> idcards = gen.idcard(count=5, region='北京')
    """

    def __init__(self, factory: GeneratorFactory | None = None):
        """
        初始化 DataForge 实例

        Args:
            factory: 生成器工厂实例，默认使用全局工厂
        """
        self._factory = factory or GeneratorFactory(default_registry)
        self._registry = self._factory.registry

    def __getattr__(self, name: str) -> Callable[..., Any]:
        """
        动态代理生成器方法

        当访问不存在的属性时，动态创建对应的生成器调用函数。

        Args:
            name: 生成器类型名称（如 'name', 'phone', 'idcard'）

        Returns:
            生成器调用函数

        Raises:
            AttributeError: 当生成器类型不存在时抛出，并提供相似建议
        """
        # 检查生成器是否存在
        if not self._registry.is_registered(name):
            # 提供友好的错误提示和相似建议
            available_generators = self._registry.list_generators()
            similar = self._find_similar_generators(name, available_generators)

            error_msg = f"生成器 '{name}' 不存在"
            if similar:
                suggestions = ", ".join(f"'{g}'" for g in similar[:3])
                error_msg += f"\n\n💡 你是不是想用这些？{suggestions}"
            else:
                error_msg += f"\n\n📝 可用的生成器有 {len(available_generators)} 个"
                error_msg += "\n   使用 gen.list_generators() 查看所有生成器"

            raise AttributeError(error_msg)

        # 返回生成器调用函数
        def _generate(**kwargs: Any) -> Any | list[Any]:
            """
            执行数据生成

            Args:
                **kwargs: 生成器参数
                    - count: 生成数量（默认1）
                    - 其他参数会传递给具体的生成器

            Returns:
                生成的数据（单个值或列表）
            """
            # 提取 count 参数
            count = kwargs.pop("count", 1)

            # 验证 count 参数
            if not isinstance(count, int) or count < 1:
                raise ValueError(f"count 参数必须是大于0的整数，当前值: {count}")

            # 创建生成器配置
            config = GeneratorConfig(
                generator_type=name, parameters=kwargs, count=count
            )

            try:
                # 创建生成器实例
                generator = self._factory.create_generator(config)

                # 生成数据
                if count == 1:
                    # 单个数据直接返回
                    return generator.generate_single()
                else:
                    # 批量数据返回列表
                    return generator.generate_batch(count)

            except GeneratorNotFoundError:
                # 这个异常不应该出现，因为我们已经检查过了
                raise AttributeError(f"生成器 '{name}' 未正确注册")

            except Exception as e:
                # 包装其他异常，提供更友好的错误信息
                raise RuntimeError(
                    f"生成数据时发生错误 (生成器: '{name}', 参数: {kwargs})\n"
                    f"错误详情: {str(e)}"
                ) from e

        return _generate

    def _find_similar_generators(
        self, name: str, available: list[str], max_results: int = 5
    ) -> list[str]:
        """
        查找相似的生成器名称（简单的字符串匹配）

        Args:
            name: 用户输入的名称
            available: 可用生成器列表
            max_results: 最多返回结果数

        Returns:
            相似的生成器名称列表
        """
        name_lower = name.lower()

        # 1. 完全包含匹配
        contains_matches = [
            g for g in available if name_lower in g.lower() or g.lower() in name_lower
        ]

        # 2. 前缀匹配
        prefix_matches = [
            g
            for g in available
            if g.lower().startswith(name_lower) or name_lower.startswith(g.lower())
        ]

        # 合并结果并去重
        similar = []
        seen = set()

        for g in prefix_matches + contains_matches:
            if g not in seen:
                similar.append(g)
                seen.add(g)
            if len(similar) >= max_results:
                break

        return similar

    def list_generators(self) -> list[str]:
        """
        列出所有已注册的生成器

        Returns:
            生成器名称列表（按字母顺序排序）
        """
        return self._registry.list_generators()

    def is_available(self, name: str) -> bool:
        """
        检查指定的生成器是否可用

        Args:
            name: 生成器名称

        Returns:
            是否可用
        """
        return self._registry.is_registered(name)

    def help(self, name: str | None = None) -> str:
        """
        获取帮助信息

        Args:
            name: 生成器名称（可选）

        Returns:
            帮助文本
        """
        if name is None:
            # 返回总体帮助
            generators = self.list_generators()
            help_text = f"""
DataForge 简化 API 使用指南
============================

当前已注册 {len(generators)} 个生成器

基本用法：
    from dataforge import gen

    # 生成单个数据
    name = gen.name()

    # 生成多个数据
    names = gen.name(count=10)

    # 带参数生成
    phone = gen.phone(operator='MOBILE')
    idcard = gen.idcard(region='北京', gender='MALE')

常用生成器：
    - gen.name()           # 姓名
    - gen.phone()          # 手机号
    - gen.idcard()         # 身份证
    - gen.email()          # 邮箱
    - gen.address()        # 地址
    - gen.company_name()   # 公司名称
    - gen.bankcard()       # 银行卡号
    - gen.age()            # 年龄
    - gen.gender()         # 性别

查看所有生成器：
    gen.list_generators()

检查生成器是否可用：
    gen.is_available('name')
"""
            return help_text.strip()
        else:
            # 返回特定生成器的帮助
            if not self.is_available(name):
                return f"生成器 '{name}' 不存在。使用 gen.list_generators() 查看所有可用生成器。"

            return f"生成器: {name}\n使用方式: gen.{name}(count=1, **parameters)"

    def __repr__(self) -> str:
        """返回对象的字符串表示"""
        count = len(self.list_generators())
        return f"<DataForge: {count} generators available>"

    def __str__(self) -> str:
        """返回用户友好的字符串表示"""
        return self.help()


# 创建全局单例实例
gen = DataForge()


# 为了方便导入，也提供一个函数形式的快捷方式
def create_gen(factory: GeneratorFactory | None = None) -> DataForge:
    """
    创建一个新的 DataForge 实例

    Args:
        factory: 自定义的生成器工厂

    Returns:
        DataForge 实例
    """
    return DataForge(factory)


__all__ = ["DataForge", "gen", "create_gen"]
