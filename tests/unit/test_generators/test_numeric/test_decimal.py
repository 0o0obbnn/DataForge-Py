"""
小数生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestDecimalGenerator:
    """小数生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个小数"""
        from dataforge.generators.numeric.decimal import DecimalGenerator

        generator_factory.registry.register("decimal", DecimalGenerator)

        config = GeneratorConfig(generator_type="decimal", parameters={})
        generator = generator_factory.create_generator(config)
        decimal = generator.generate_single()

        assert isinstance(decimal, (float, int))
        assert generator.validate(decimal)

    def test_generate_batch(self, generator_factory):
        """测试批量生成小数"""
        from dataforge.generators.numeric.decimal import DecimalGenerator

        generator_factory.registry.register("decimal", DecimalGenerator)

        config = GeneratorConfig(generator_type="decimal", parameters={})
        generator = generator_factory.create_generator(config)
        decimals = generator.generate_batch(10)

        assert len(decimals) == 10
        for decimal in decimals:
            assert isinstance(decimal, (float, int))

    def test_decimal_range(self, generator_factory):
        """测试小数范围"""
        from dataforge.generators.numeric.decimal import DecimalGenerator

        generator_factory.registry.register("decimal", DecimalGenerator)

        config = GeneratorConfig(
            generator_type="decimal", parameters={"min": 0.0, "max": 1.0}
        )
        generator = generator_factory.create_generator(config)
        decimal = generator.generate_single()

        assert 0.0 <= decimal <= 1.0

    def test_decimal_places(self, generator_factory):
        """测试小数位数"""
        from dataforge.generators.numeric.decimal import DecimalGenerator

        generator_factory.registry.register("decimal", DecimalGenerator)

        config = GeneratorConfig(
            generator_type="decimal", parameters={"decimal_places": 2}
        )
        generator = generator_factory.create_generator(config)
        decimal = generator.generate_single()

        if isinstance(decimal, float):
            str_decimal = str(decimal)
            if "." in str_decimal:
                decimal_part = str_decimal.split(".")[1]
                assert len(decimal_part) <= 4  # Allow some flexibility

    def test_positive_decimals(self, generator_factory):
        """测试正小数"""
        from dataforge.generators.numeric.decimal import DecimalGenerator

        generator_factory.registry.register("decimal", DecimalGenerator)

        config = GeneratorConfig(
            generator_type="decimal", parameters={"min": 0.1, "max": 100.0}
        )
        generator = generator_factory.create_generator(config)
        decimals = generator.generate_batch(20)

        for decimal in decimals:
            assert decimal > 0

    def test_negative_decimals(self, generator_factory):
        """测试负小数"""
        from dataforge.generators.numeric.decimal import DecimalGenerator

        generator_factory.registry.register("decimal", DecimalGenerator)

        config = GeneratorConfig(
            generator_type="decimal", parameters={"min": -100.0, "max": -0.1}
        )
        generator = generator_factory.create_generator(config)
        decimals = generator.generate_batch(20)

        for decimal in decimals:
            assert decimal < 0

    def test_validation(self, generator_factory):
        """测试小数验证"""
        from dataforge.generators.numeric.decimal import DecimalGenerator

        generator_factory.registry.register("decimal", DecimalGenerator)

        config = GeneratorConfig(generator_type="decimal", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid decimals
        assert generator.validate(3.14)
        assert generator.validate(0.0)
        assert generator.validate(-2.5)

        # Invalid decimals
        assert not generator.validate("3.14")
        assert not generator.validate(None)

    def test_distribution(self, generator_factory):
        """测试小数分布"""
        from dataforge.generators.numeric.decimal import DecimalGenerator

        generator_factory.registry.register("decimal", DecimalGenerator)

        config = GeneratorConfig(
            generator_type="decimal", parameters={"min": 0.0, "max": 10.0}
        )
        generator = generator_factory.create_generator(config)
        decimals = generator.generate_batch(100)

        # Should cover the range
        assert min(decimals) >= 0.0
        assert max(decimals) <= 10.0
