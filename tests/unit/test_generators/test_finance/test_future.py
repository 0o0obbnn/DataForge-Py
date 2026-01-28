"""
期货代码生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
@pytest.mark.skip(reason="FutureCodeGenerator not implemented - advanced feature")
class TestFutureGenerator:
    """期货代码生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个期货代码"""
        from dataforge.generators.finance.future import FutureCodeGenerator

        generator_factory.registry.register("future", FutureCodeGenerator)

        config = GeneratorConfig(generator_type="future", parameters={})
        generator = generator_factory.create_generator(config)
        future_code = generator.generate_single()

        assert isinstance(future_code, str)
        assert len(future_code) >= 4
        assert generator.validate(future_code)

    def test_generate_batch(self, generator_factory):
        """测试批量生成期货代码"""
        from dataforge.generators.finance.future import FutureCodeGenerator

        generator_factory.registry.register("future", FutureCodeGenerator)

        config = GeneratorConfig(generator_type="future", parameters={})
        generator = generator_factory.create_generator(config)
        future_codes = generator.generate_batch(10)

        assert len(future_codes) == 10
        for code in future_codes:
            assert isinstance(code, str)
            assert len(code) >= 4

    def test_commodity_future(self, generator_factory):
        """测试商品期货代码"""
        from dataforge.generators.finance.future import FutureCodeGenerator

        generator_factory.registry.register("future", FutureCodeGenerator)

        config = GeneratorConfig(
            generator_type="future", parameters={"type": "commodity"}
        )
        generator = generator_factory.create_generator(config)
        future_code = generator.generate_single()

        assert isinstance(future_code, str)

    def test_financial_future(self, generator_factory):
        """测试金融期货代码"""
        from dataforge.generators.finance.future import FutureCodeGenerator

        generator_factory.registry.register("future", FutureCodeGenerator)

        config = GeneratorConfig(
            generator_type="future", parameters={"type": "financial"}
        )
        generator = generator_factory.create_generator(config)
        future_code = generator.generate_single()

        assert isinstance(future_code, str)

    def test_with_month(self, generator_factory):
        """测试带月份的期货代码"""
        from dataforge.generators.finance.future import FutureCodeGenerator

        generator_factory.registry.register("future", FutureCodeGenerator)

        config = GeneratorConfig(
            generator_type="future", parameters={"include_month": True}
        )
        generator = generator_factory.create_generator(config)
        future_code = generator.generate_single()

        # Future code with month: AB2401 (symbol + year + month)
        assert isinstance(future_code, str)
        assert len(future_code) >= 4

    def test_validation(self, generator_factory):
        """测试期货代码验证"""
        from dataforge.generators.finance.future import FutureCodeGenerator

        generator_factory.registry.register("future", FutureCodeGenerator)

        config = GeneratorConfig(generator_type="future", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid future code
        future_code = generator.generate_single()
        assert generator.validate(future_code)

        # Invalid future codes
        assert not generator.validate("AB")  # Too short
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试期货代码唯一性"""
        from dataforge.generators.finance.future import FutureCodeGenerator

        generator_factory.registry.register("future", FutureCodeGenerator)

        config = GeneratorConfig(generator_type="future", parameters={})
        generator = generator_factory.create_generator(config)
        codes = generator.generate_batch(50)

        # Should have variety
        unique_codes = set(codes)
        assert len(unique_codes) > 20

    def test_format(self, generator_factory):
        """测试代码格式"""
        from dataforge.generators.finance.future import FutureCodeGenerator

        generator_factory.registry.register("future", FutureCodeGenerator)

        config = GeneratorConfig(generator_type="future", parameters={})
        generator = generator_factory.create_generator(config)
        future_code = generator.generate_single()

        # Future code format: letters + digits
        assert isinstance(future_code, str)
        assert future_code.isalnum()

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.finance.future import FutureCodeGenerator

        generator_factory.registry.register("future", FutureCodeGenerator)

        config = GeneratorConfig(generator_type="future", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            code = generator.generate_single()
            assert code is not None
            assert len(code) >= 4
            assert code.isalnum()
