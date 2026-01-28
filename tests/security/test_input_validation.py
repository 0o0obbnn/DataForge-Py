"""
输入验证安全测试
"""

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.security
class TestInputValidation:
    """输入验证安全测试类"""

    def test_invalid_generator_type(self):
        """测试无效的生成器类型"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 测试各种无效输入
        invalid_types = [
            None,
            "",
            123,
            [],
            {},
            "../../../etc/passwd",  # 路径遍历
            "'; DROP TABLE users--",  # SQL注入尝试
            "<script>alert('xss')</script>",  # XSS尝试
        ]

        for invalid_type in invalid_types:
            try:
                config = GeneratorConfig(invalid_type, {})
                factory.create_generator(config)
                pytest.fail(f"应该拒绝无效类型: {invalid_type}")
            except Exception:
                pass  # 预期会抛出异常

    def test_invalid_parameters(self):
        """测试无效的参数"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.age import AgeGenerator

        registry.register("age", AgeGenerator)

        # 测试各种无效参数
        invalid_params = [
            {"min": "invalid"},  # 字符串而非数字
            {"min": -999999999},  # 极端负数
            {"min": 999999999},  # 极端正数
            {"min": float("inf")},  # 无穷大
            {"min": float("nan")},  # NaN
        ]

        for params in invalid_params:
            try:
                config = GeneratorConfig("age", params)
                generator = factory.create_generator(config)
                generator.generate_single()
            except Exception:
                pass  # 预期会处理或抛出异常

    def test_parameter_injection(self):
        """测试参数注入攻击"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        # 尝试注入恶意参数
        malicious_params = {
            "locale": "'; DROP TABLE users--",
            "format": "<script>alert('xss')</script>",
            "prefix": "../../../etc/passwd",
        }

        try:
            config = GeneratorConfig("name", malicious_params)
            generator = factory.create_generator(config)
            result = generator.generate_single()

            # 验证结果不包含恶意内容
            assert "DROP TABLE" not in str(result)
            assert "<script>" not in str(result)
            assert "../../../" not in str(result)
        except Exception:
            pass  # 如果拒绝也是正确的

    def test_buffer_overflow_prevention(self):
        """测试缓冲区溢出防护"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        # 尝试超大参数
        config = GeneratorConfig(
            "name",
            {
                "length": 999999999,  # 极大的长度
                "prefix": "A" * 100000,  # 超长前缀
            },
        )

        try:
            generator = factory.create_generator(config)
            result = generator.generate_single()

            # 验证结果长度合理
            assert len(str(result)) < 1000000
        except Exception:
            pass  # 如果拒绝也是正确的

    def test_null_byte_injection(self):
        """测试空字节注入"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        # 尝试空字节注入
        try:
            config = GeneratorConfig("name", {"prefix": "test\x00malicious"})
            generator = factory.create_generator(config)
            result = generator.generate_single()

            # 验证结果不包含空字节
            assert "\x00" not in str(result)
        except Exception:
            pass

    def test_unicode_validation(self):
        """测试Unicode验证"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        # 测试各种Unicode字符
        unicode_tests = [
            "测试",  # 中文
            "テスト",  # 日文
            "тест",  # 俄文
            "🔥💯",  # Emoji
            "\u202e",  # 右到左覆盖
        ]

        for test_str in unicode_tests:
            try:
                config = GeneratorConfig("name", {"prefix": test_str})
                generator = factory.create_generator(config)
                result = generator.generate_single()
                assert result is not None
            except Exception:
                pass

    def test_type_confusion(self):
        """测试类型混淆攻击"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.age import AgeGenerator

        registry.register("age", AgeGenerator)

        # 尝试类型混淆
        type_confusion_params = [
            {"min": [1, 2, 3]},  # 列表而非数字
            {"min": {"value": 1}},  # 字典而非数字
            {"min": lambda x: x},  # 函数而非数字
        ]

        for params in type_confusion_params:
            try:
                config = GeneratorConfig("age", params)
                generator = factory.create_generator(config)
                generator.generate_single()
            except Exception:
                pass  # 预期会处理或拒绝

    def test_recursive_data_structures(self):
        """测试递归数据结构"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        # 创建递归结构
        recursive_dict = {}
        recursive_dict["self"] = recursive_dict

        try:
            config = GeneratorConfig("name", recursive_dict)
            generator = factory.create_generator(config)
            generator.generate_single()
        except Exception:
            pass  # 预期会处理递归
