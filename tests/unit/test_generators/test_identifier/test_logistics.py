"""
物流单号生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestLogisticsGenerator:
    """物流单号生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个物流单号"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(generator_type="logistics", parameters={})
        generator = generator_factory.create_generator(config)
        tracking_number = generator.generate_single()

        assert isinstance(tracking_number, str)
        assert len(tracking_number) >= 10
        assert generator.validate(tracking_number)

    def test_generate_batch(self, generator_factory):
        """测试批量生成物流单号"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(generator_type="logistics", parameters={})
        generator = generator_factory.create_generator(config)
        tracking_numbers = generator.generate_batch(10)

        assert len(tracking_numbers) == 10
        for number in tracking_numbers:
            assert isinstance(number, str)
            assert len(number) >= 10

    def test_sf_express(self, generator_factory):
        """测试顺丰快递单号"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(
            generator_type="logistics", parameters={"carrier": "sf_express"}
        )
        generator = generator_factory.create_generator(config)
        tracking_number = generator.generate_single()

        # SF Express format: 12 digits
        assert isinstance(tracking_number, str)
        assert len(tracking_number) >= 10

    def test_ems(self, generator_factory):
        """测试EMS单号"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(
            generator_type="logistics", parameters={"carrier": "ems"}
        )
        generator = generator_factory.create_generator(config)
        tracking_number = generator.generate_single()

        # EMS format: 13 characters (2 letters + 9 digits + 2 letters)
        assert isinstance(tracking_number, str)

    def test_yto_express(self, generator_factory):
        """测试圆通快递单号"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(
            generator_type="logistics", parameters={"carrier": "yto"}
        )
        generator = generator_factory.create_generator(config)
        tracking_number = generator.generate_single()

        assert isinstance(tracking_number, str)
        assert len(tracking_number) >= 10

    def test_validation(self, generator_factory):
        """测试物流单号验证"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(generator_type="logistics", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid tracking number
        tracking_number = generator.generate_single()
        assert generator.validate(tracking_number)

        # Invalid tracking numbers
        assert not generator.validate("123")  # Too short
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试物流单号唯一性"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(generator_type="logistics", parameters={})
        generator = generator_factory.create_generator(config)
        tracking_numbers = generator.generate_batch(50)

        # All tracking numbers should be unique
        unique_numbers = set(tracking_numbers)
        assert len(unique_numbers) == 50

    def test_format(self, generator_factory):
        """测试单号格式"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(generator_type="logistics", parameters={})
        generator = generator_factory.create_generator(config)
        tracking_number = generator.generate_single()

        # Should be alphanumeric
        assert tracking_number.isalnum()

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(generator_type="logistics", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            number = generator.generate_single()
            assert number is not None
            assert len(number) >= 10
            assert number.isalnum()
