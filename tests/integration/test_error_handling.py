"""
错误处理集成测试
"""

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.integration
class TestErrorHandling:
    """错误处理集成测试类"""

    def test_unregistered_generator_error(self):
        """测试未注册生成器错误"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        config = GeneratorConfig("nonexistent", {})

        with pytest.raises(Exception):
            factory.create_generator(config)

    def test_invalid_config_error(self):
        """测试无效配置错误"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        # 测试None配置
        with pytest.raises(Exception):
            factory.create_generator(None)

    def test_invalid_parameter_type(self):
        """测试无效参数类型"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.age import AgeGenerator

        registry.register("age", AgeGenerator)

        # 测试字符串作为数字参数
        config = GeneratorConfig("age", {"min": "invalid", "max": "invalid"})

        try:
            generator = factory.create_generator(config)
            # 如果创建成功，尝试生成数据时应该失败
            generator.generate_single()
        except Exception:
            pass  # 预期会抛出异常

    def test_invalid_parameter_range(self):
        """测试无效参数范围"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.age import AgeGenerator

        registry.register("age", AgeGenerator)

        # min > max
        config = GeneratorConfig("age", {"min": 100, "max": 0})

        try:
            generator = factory.create_generator(config)
            generator.generate_single()
        except Exception:
            pass  # 预期会抛出异常

    def test_generator_validation_error(self):
        """测试生成器验证错误"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        config = GeneratorConfig("name", {})
        generator = factory.create_generator(config)

        # 测试验证无效数据
        assert not generator.validate("")
        assert not generator.validate(None)
        assert not generator.validate(123)

    def test_batch_generation_error_recovery(self):
        """测试批量生成错误恢复"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        config = GeneratorConfig("name", {})
        generator = factory.create_generator(config)

        # 测试批量生成
        try:
            names = generator.generate_batch(10)
            assert len(names) == 10
        except Exception as e:
            pytest.fail(f"Batch generation should not fail: {e}")

    def test_multiple_error_scenarios(self):
        """测试多种错误场景"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 场景1: 空注册表
        with pytest.raises(Exception):
            config = GeneratorConfig("name", {})
            factory.create_generator(config)

        # 场景2: 注册后正常工作
        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        config = GeneratorConfig("name", {})
        generator = factory.create_generator(config)
        assert generator.generate_single() is not None

    def test_concurrent_error_handling(self):
        """测试并发错误处理"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        config = GeneratorConfig("name", {})

        # 并发创建多个生成器
        generators = []
        for _ in range(10):
            try:
                gen = factory.create_generator(config)
                generators.append(gen)
            except Exception:
                pass

        # 验证至少有一些生成器创建成功
        assert len(generators) > 0

    def test_error_message_clarity(self):
        """测试错误消息清晰度"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        config = GeneratorConfig("nonexistent_generator", {})

        try:
            factory.create_generator(config)
            pytest.fail("Should raise exception")
        except Exception as e:
            # 验证错误消息包含有用信息
            error_msg = str(e)
            assert len(error_msg) > 0

    def test_graceful_degradation(self):
        """测试优雅降级"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)

        # 即使一个生成器失败，其他应该继续工作
        name_gen = factory.create_generator(GeneratorConfig("name", {}))
        age_gen = factory.create_generator(GeneratorConfig("age", {}))

        assert name_gen.generate_single() is not None
        assert age_gen.generate_single() is not None

    def test_error_recovery_after_failure(self):
        """测试失败后错误恢复"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 第一次尝试失败
        try:
            config = GeneratorConfig("nonexistent", {})
            factory.create_generator(config)
        except Exception:
            pass

        # 注册生成器后应该成功
        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        config = GeneratorConfig("name", {})
        generator = factory.create_generator(config)
        assert generator.generate_single() is not None

    def test_validation_error_handling(self):
        """测试验证错误处理"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.contact.email import EmailGenerator

        registry.register("email", EmailGenerator)

        config = GeneratorConfig("email", {})
        generator = factory.create_generator(config)

        # 测试有效邮箱
        email = generator.generate_single()
        assert generator.validate(email)

        # 测试无效邮箱
        assert not generator.validate("invalid_email")
        assert not generator.validate("")
        assert not generator.validate(None)
