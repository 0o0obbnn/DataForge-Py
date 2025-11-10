"""
配置管理集成测试
"""

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.integration
class TestConfigManagement:
    """配置管理集成测试类"""

    def test_config_with_default_parameters(self):
        """测试默认参数配置"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        # 使用默认参数
        config = GeneratorConfig(generator_type="name", parameters={})
        generator = factory.create_generator(config)
        
        name = generator.generate_single()
        assert name is not None
        assert isinstance(name, str)

    def test_config_with_custom_parameters(self):
        """测试自定义参数配置"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.age import AgeGenerator
        registry.register("age", AgeGenerator)
        
        # 使用自定义参数
        config = GeneratorConfig(
            generator_type="age",
            parameters={"min": 18, "max": 65}
        )
        generator = factory.create_generator(config)
        
        age = generator.generate_single()
        assert 18 <= age <= 65

    def test_config_parameter_validation(self):
        """测试配置参数验证"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.age import AgeGenerator
        registry.register("age", AgeGenerator)
        
        # 测试有效参数
        valid_config = GeneratorConfig(
            generator_type="age",
            parameters={"min": 0, "max": 100}
        )
        generator = factory.create_generator(valid_config)
        assert generator is not None

    def test_config_locale_settings(self):
        """测试地区设置配置"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        locales = ["zh_CN", "en_US", "ja_JP"]
        
        for locale in locales:
            config = GeneratorConfig(
                generator_type="name",
                parameters={"locale": locale}
            )
            generator = factory.create_generator(config)
            name = generator.generate_single()
            assert name is not None

    def test_config_batch_size(self):
        """测试批量大小配置"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        config = GeneratorConfig(generator_type="name", parameters={})
        generator = factory.create_generator(config)
        
        # 测试不同批量大小
        batch_sizes = [1, 10, 50, 100]
        for size in batch_sizes:
            names = generator.generate_batch(size)
            assert len(names) == size

    def test_config_format_options(self):
        """测试格式选项配置"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.address import AddressGenerator
        registry.register("address", AddressGenerator)
        
        # 测试不同格式选项
        config = GeneratorConfig(
            generator_type="address",
            parameters={
                "include_province": True,
                "include_city": True,
                "include_district": True
            }
        )
        generator = factory.create_generator(config)
        address = generator.generate_single()
        assert address is not None

    def test_config_multiple_generators(self):
        """测试多生成器配置"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        
        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        
        # 创建多个配置
        configs = {
            "name": GeneratorConfig("name", {"locale": "zh_CN"}),
            "age": GeneratorConfig("age", {"min": 18, "max": 65}),
            "gender": GeneratorConfig("gender", {}),
        }
        
        # 创建生成器
        generators = {
            key: factory.create_generator(config)
            for key, config in configs.items()
        }
        
        # 验证所有生成器
        assert all(gen.generate_single() is not None for gen in generators.values())

    def test_config_override(self):
        """测试配置覆盖"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.age import AgeGenerator
        registry.register("age", AgeGenerator)
        
        # 第一个配置
        config1 = GeneratorConfig("age", {"min": 0, "max": 18})
        gen1 = factory.create_generator(config1)
        age1 = gen1.generate_single()
        assert 0 <= age1 <= 18
        
        # 第二个配置（覆盖）
        config2 = GeneratorConfig("age", {"min": 65, "max": 100})
        gen2 = factory.create_generator(config2)
        age2 = gen2.generate_single()
        assert 65 <= age2 <= 100

    def test_config_persistence(self):
        """测试配置持久性"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        config = GeneratorConfig("name", {"locale": "zh_CN"})
        generator = factory.create_generator(config)
        
        # 多次生成，验证配置保持一致
        names = [generator.generate_single() for _ in range(10)]
        assert len(names) == 10
        assert all(isinstance(n, str) for n in names)

    def test_config_complex_parameters(self):
        """测试复杂参数配置"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.address import AddressGenerator
        registry.register("address", AddressGenerator)
        
        # 复杂参数配置
        config = GeneratorConfig(
            generator_type="address",
            parameters={
                "locale": "zh_CN",
                "include_province": True,
                "include_city": True,
                "include_district": True,
                "include_street": True,
                "include_building": False,
                "format": "full"
            }
        )
        
        generator = factory.create_generator(config)
        address = generator.generate_single()
        assert address is not None
