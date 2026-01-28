"""
数字生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestNumberGenerator:
    """数字生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个数字"""
        from dataforge.generators.numeric.number import NumberGenerator

        generator_factory.registry.register("number", NumberGenerator)

        config = GeneratorConfig(generator_type="number", parameters={})
        generator = generator_factory.create_generator(config)
        number = generator.generate_single()

        assert isinstance(number, (int, float))
        assert generator.validate(number)

    def test_generate_batch(self, generator_factory):
        """测试批量生成数字"""
        from dataforge.generators.numeric.number import NumberGenerator

        generator_factory.registry.register("number", NumberGenerator)

        config = GeneratorConfig(generator_type="number", parameters={})
        generator = generator_factory.create_generator(config)
        numbers = generator.generate_batch(10)

        assert len(numbers) == 10
        for number in numbers:
            assert isinstance(number, (int, float))

    def test_integer_range(self, generator_factory):
        """测试整数范围"""
        from dataforge.generators.numeric.number import NumberGenerator

        generator_factory.registry.register("number", NumberGenerator)

        config = GeneratorConfig(
            generator_type="number",
            parameters={"type": "integer", "min": 1, "max": 100},
        )
        generator = generator_factory.create_generator(config)
        number = generator.generate_single()

        assert isinstance(number, int)
        assert 1 <= number <= 100

    def test_float_range(self, generator_factory):
        """测试浮点数范围"""
        from dataforge.generators.numeric.number import NumberGenerator

        generator_factory.registry.register("number", NumberGenerator)

        config = GeneratorConfig(
            generator_type="number",
            parameters={"type": "float", "min": 0.0, "max": 1.0},
        )
        generator = generator_factory.create_generator(config)
        number = generator.generate_single()

        assert isinstance(number, float)
        assert 0.0 <= number <= 1.0

    def test_decimal_places(self, generator_factory):
        """测试小数位数"""
        from dataforge.generators.numeric.number import NumberGenerator

        generator_factory.registry.register("number", NumberGenerator)

        config = GeneratorConfig(
            generator_type="number", parameters={"type": "float", "decimal_places": 2}
        )
        generator = generator_factory.create_generator(config)
        number = generator.generate_single()

        if isinstance(number, float):
            # Check decimal places (approximately)
            str_num = str(number)
            if "." in str_num:
                decimal_part = str_num.split(".")[1]
                assert len(decimal_part) <= 4  # Allow some flexibility

    def test_positive_numbers(self, generator_factory):
        """测试正数"""
        from dataforge.generators.numeric.number import NumberGenerator

        generator_factory.registry.register("number", NumberGenerator)

        config = GeneratorConfig(
            generator_type="number", parameters={"min": 1, "max": 1000}
        )
        generator = generator_factory.create_generator(config)
        numbers = generator.generate_batch(20)

        for number in numbers:
            assert number > 0

    def test_negative_numbers(self, generator_factory):
        """测试负数"""
        from dataforge.generators.numeric.number import NumberGenerator

        generator_factory.registry.register("number", NumberGenerator)

        config = GeneratorConfig(
            generator_type="number", parameters={"min": -100, "max": -1}
        )
        generator = generator_factory.create_generator(config)
        numbers = generator.generate_batch(20)

        for number in numbers:
            assert number < 0

    def test_validation(self, generator_factory):
        """测试数字验证"""
        from dataforge.generators.numeric.number import NumberGenerator

        generator_factory.registry.register("number", NumberGenerator)

        config = GeneratorConfig(generator_type="number", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid numbers
        assert generator.validate(42)
        assert generator.validate(3.14)
        assert generator.validate(0)
        assert generator.validate(-5)

        # Invalid numbers
        assert not generator.validate("123")
        assert not generator.validate(None)
        assert not generator.validate("abc")

    def test_distribution(self, generator_factory):
        """测试数字分布"""
        from dataforge.generators.numeric.number import NumberGenerator

        generator_factory.registry.register("number", NumberGenerator)

        config = GeneratorConfig(
            generator_type="number", parameters={"min": 1, "max": 10}
        )
        generator = generator_factory.create_generator(config)
        numbers = generator.generate_batch(100)

        # Should cover the range
        assert min(numbers) >= 1
        assert max(numbers) <= 10
        # Should have variety
        unique_numbers = set(numbers)
        assert len(unique_numbers) > 3

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.numeric.number import NumberGenerator

        generator_factory.registry.register("number", NumberGenerator)

        # Zero range
        config = GeneratorConfig(
            generator_type="number", parameters={"min": 5, "max": 5}
        )
        generator = generator_factory.create_generator(config)
        number = generator.generate_single()
        assert number == 5

        # Large numbers
        config = GeneratorConfig(
            generator_type="number", parameters={"min": 1000000, "max": 9999999}
        )
        generator = generator_factory.create_generator(config)
        number = generator.generate_single()
        assert 1000000 <= number <= 9999999
