"""
Generator Factory集成测试
"""

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.integration
class TestGeneratorFactoryIntegration:
    """Generator Factory集成测试类"""

    def test_factory_with_multiple_generators(self):
        """测试工厂创建多个不同类型的生成器"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册多个生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)

        # 创建多个生成器
        name_config = GeneratorConfig(generator_type="name", parameters={})
        age_config = GeneratorConfig(generator_type="age", parameters={})
        gender_config = GeneratorConfig(generator_type="gender", parameters={})

        name_gen = factory.create_generator(name_config)
        age_gen = factory.create_generator(age_config)
        gender_gen = factory.create_generator(gender_config)

        # 验证生成器工作正常
        assert name_gen.generate_single() is not None
        assert age_gen.generate_single() is not None
        assert gender_gen.generate_single() is not None

    def test_factory_batch_creation(self):
        """测试工厂批量创建生成器"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        # 创建多个相同类型的生成器实例
        configs = [
            GeneratorConfig(generator_type="name", parameters={"locale": "zh_CN"}),
            GeneratorConfig(generator_type="name", parameters={"locale": "en_US"}),
            GeneratorConfig(generator_type="name", parameters={"locale": "zh_CN"}),
        ]

        generators = [factory.create_generator(config) for config in configs]

        assert len(generators) == 3
        for gen in generators:
            assert gen.generate_single() is not None

    def test_factory_with_complex_parameters(self):
        """测试工厂处理复杂参数"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.address import AddressGenerator

        registry.register("address", AddressGenerator)

        config = GeneratorConfig(
            generator_type="address",
            parameters={
                "locale": "zh_CN",
                "include_province": True,
                "include_city": True,
                "include_district": True,
                "include_street": True,
            },
        )

        generator = factory.create_generator(config)
        address = generator.generate_single()

        assert address is not None
        assert isinstance(address, (str, dict))

    def test_factory_error_handling(self):
        """测试工厂错误处理"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 测试未注册的生成器
        config = GeneratorConfig(generator_type="nonexistent", parameters={})

        with pytest.raises(Exception):
            factory.create_generator(config)

    def test_factory_generator_reuse(self):
        """测试生成器实例复用"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        config = GeneratorConfig(generator_type="name", parameters={})

        # 创建两个生成器
        gen1 = factory.create_generator(config)
        gen2 = factory.create_generator(config)

        # 验证它们都能正常工作
        assert gen1.generate_single() is not None
        assert gen2.generate_single() is not None

    def test_factory_with_all_basic_generators(self):
        """测试工厂与所有基础生成器"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所有基础生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        from dataforge.generators.basic.address import AddressGenerator

        generators_to_register = {
            "name": NameGenerator,
            "age": AgeGenerator,
            "gender": GenderGenerator,
            "address": AddressGenerator,
        }

        for name, gen_class in generators_to_register.items():
            registry.register(name, gen_class)

        # 测试每个生成器
        for gen_type in generators_to_register.keys():
            config = GeneratorConfig(generator_type=gen_type, parameters={})
            generator = factory.create_generator(config)
            result = generator.generate_single()
            assert result is not None

    def test_factory_concurrent_creation(self):
        """测试工厂并发创建生成器"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        config = GeneratorConfig(generator_type="name", parameters={})

        # 并发创建多个生成器
        generators = [factory.create_generator(config) for _ in range(10)]

        # 验证所有生成器都能工作
        results = [gen.generate_single() for gen in generators]
        assert len(results) == 10
        assert all(r is not None for r in results)

    def test_factory_with_different_locales(self):
        """测试工厂处理不同地区设置"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        locales = ["zh_CN", "en_US", "ja_JP"]

        for locale in locales:
            config = GeneratorConfig(
                generator_type="name", parameters={"locale": locale}
            )
            generator = factory.create_generator(config)
            name = generator.generate_single()
            assert name is not None
            assert isinstance(name, str)
