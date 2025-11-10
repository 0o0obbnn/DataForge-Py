"""
签证号生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestVisaGenerator:
    """签证号生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个签证号"""
        from dataforge.generators.identifier.visa import VisaGenerator
        generator_factory.registry.register("visa", VisaGenerator)
        
        config = GeneratorConfig(
            generator_type="visa",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        visa = generator.generate_single()
        
        assert isinstance(visa, str)
        assert len(visa) >= 8
        assert generator.validate(visa)

    def test_generate_batch(self, generator_factory):
        """测试批量生成签证号"""
        from dataforge.generators.identifier.visa import VisaGenerator
        generator_factory.registry.register("visa", VisaGenerator)
        
        config = GeneratorConfig(
            generator_type="visa",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        visas = generator.generate_batch(10)
        
        assert len(visas) == 10
        for visa in visas:
            assert isinstance(visa, str)
            assert len(visa) >= 8

    def test_us_visa(self, generator_factory):
        """测试美国签证号"""
        from dataforge.generators.identifier.visa import VisaGenerator
        generator_factory.registry.register("visa", VisaGenerator)
        
        config = GeneratorConfig(
            generator_type="visa",
            parameters={"country": "usa"}
        )
        generator = generator_factory.create_generator(config)
        visa = generator.generate_single()
        
        # US visa number format
        assert isinstance(visa, str)
        assert len(visa) >= 8

    def test_schengen_visa(self, generator_factory):
        """测试申根签证号"""
        from dataforge.generators.identifier.visa import VisaGenerator
        generator_factory.registry.register("visa", VisaGenerator)
        
        config = GeneratorConfig(
            generator_type="visa",
            parameters={"country": "schengen"}
        )
        generator = generator_factory.create_generator(config)
        visa = generator.generate_single()
        
        assert isinstance(visa, str)

    def test_visa_type(self, generator_factory):
        """测试签证类型"""
        from dataforge.generators.identifier.visa import VisaGenerator
        generator_factory.registry.register("visa", VisaGenerator)
        
        config = GeneratorConfig(
            generator_type="visa",
            parameters={"visa_type": "tourist"}
        )
        generator = generator_factory.create_generator(config)
        visa = generator.generate_single()
        
        assert isinstance(visa, str)

    def test_validation(self, generator_factory):
        """测试签证号验证"""
        from dataforge.generators.identifier.visa import VisaGenerator
        generator_factory.registry.register("visa", VisaGenerator)
        
        config = GeneratorConfig(
            generator_type="visa",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid visa
        visa = generator.generate_single()
        assert generator.validate(visa)
        
        # Invalid visas
        assert not generator.validate("123")  # Too short
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试签证号唯一性"""
        from dataforge.generators.identifier.visa import VisaGenerator
        generator_factory.registry.register("visa", VisaGenerator)
        
        config = GeneratorConfig(
            generator_type="visa",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        visas = generator.generate_batch(50)
        
        # All visas should be unique
        unique_visas = set(visas)
        assert len(unique_visas) == 50

    def test_format(self, generator_factory):
        """测试签证号格式"""
        from dataforge.generators.identifier.visa import VisaGenerator
        generator_factory.registry.register("visa", VisaGenerator)
        
        config = GeneratorConfig(
            generator_type="visa",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        visa = generator.generate_single()
        
        # Should be alphanumeric
        assert visa.replace('-', '').isalnum()

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.identifier.visa import VisaGenerator
        generator_factory.registry.register("visa", VisaGenerator)
        
        config = GeneratorConfig(
            generator_type="visa",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            visa = generator.generate_single()
            assert visa is not None
            assert len(visa) >= 8
