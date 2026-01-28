"""
固定电话生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
@pytest.mark.skip(reason="LandlineGenerator not implemented yet")
class TestLandlineGenerator:
    """固定电话生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个固定电话"""
        from dataforge.generators.contact.landline import LandlineGenerator

        generator_factory.registry.register("landline", LandlineGenerator)

        config = GeneratorConfig(generator_type="landline", parameters={})
        generator = generator_factory.create_generator(config)
        landline = generator.generate_single()

        assert isinstance(landline, str)
        assert generator.validate(landline)

    def test_generate_batch(self, generator_factory):
        """测试批量生成固定电话"""
        from dataforge.generators.contact.landline import LandlineGenerator

        generator_factory.registry.register("landline", LandlineGenerator)

        config = GeneratorConfig(generator_type="landline", parameters={})
        generator = generator_factory.create_generator(config)
        landlines = generator.generate_batch(10)

        assert len(landlines) == 10
        for landline in landlines:
            assert isinstance(landline, str)
            assert generator.validate(landline)

    def test_beijing_landline(self, generator_factory):
        """测试北京固定电话"""
        from dataforge.generators.contact.landline import LandlineGenerator

        generator_factory.registry.register("landline", LandlineGenerator)

        config = GeneratorConfig(
            generator_type="landline", parameters={"city": "beijing"}
        )
        generator = generator_factory.create_generator(config)
        landline = generator.generate_single()

        # Beijing area code is 010
        assert "010" in landline or landline.startswith("010")

    def test_shanghai_landline(self, generator_factory):
        """测试上海固定电话"""
        from dataforge.generators.contact.landline import LandlineGenerator

        generator_factory.registry.register("landline", LandlineGenerator)

        config = GeneratorConfig(
            generator_type="landline", parameters={"city": "shanghai"}
        )
        generator = generator_factory.create_generator(config)
        landline = generator.generate_single()

        # Shanghai area code is 021
        assert "021" in landline or landline.startswith("021")

    def test_with_area_code(self, generator_factory):
        """测试带区号的固定电话"""
        from dataforge.generators.contact.landline import LandlineGenerator

        generator_factory.registry.register("landline", LandlineGenerator)

        config = GeneratorConfig(
            generator_type="landline", parameters={"include_area_code": True}
        )
        generator = generator_factory.create_generator(config)
        landline = generator.generate_single()

        # Should have area code (3-4 digits)
        assert isinstance(landline, str)
        assert len(landline.replace("-", "").replace(" ", "")) >= 10

    def test_format_with_hyphen(self, generator_factory):
        """测试带连字符格式"""
        from dataforge.generators.contact.landline import LandlineGenerator

        generator_factory.registry.register("landline", LandlineGenerator)

        config = GeneratorConfig(
            generator_type="landline", parameters={"format": "hyphen"}
        )
        generator = generator_factory.create_generator(config)
        landline = generator.generate_single()

        # May contain hyphens
        assert isinstance(landline, str)

    def test_validation(self, generator_factory):
        """测试固定电话验证"""
        from dataforge.generators.contact.landline import LandlineGenerator

        generator_factory.registry.register("landline", LandlineGenerator)

        config = GeneratorConfig(generator_type="landline", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid landlines
        assert generator.validate("010-12345678")
        assert generator.validate("021-87654321")

        # Invalid landlines
        assert not generator.validate("123")
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试固定电话唯一性"""
        from dataforge.generators.contact.landline import LandlineGenerator

        generator_factory.registry.register("landline", LandlineGenerator)

        config = GeneratorConfig(generator_type="landline", parameters={})
        generator = generator_factory.create_generator(config)
        landlines = generator.generate_batch(50)

        # Should have variety
        unique_landlines = set(landlines)
        assert len(unique_landlines) > 30

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.contact.landline import LandlineGenerator

        generator_factory.registry.register("landline", LandlineGenerator)

        config = GeneratorConfig(generator_type="landline", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            landline = generator.generate_single()
            assert landline is not None
            assert isinstance(landline, str)
            assert len(landline) >= 8
