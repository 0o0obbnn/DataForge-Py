"""
基金代码生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestFundGenerator:
    """基金代码生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个基金代码"""
        from dataforge.generators.finance.fund import FundCodeGenerator

        generator_factory.registry.register("fund", FundCodeGenerator)

        config = GeneratorConfig(generator_type="fund", parameters={})
        generator = generator_factory.create_generator(config)
        fund_code = generator.generate_single()

        assert isinstance(fund_code, str)
        assert len(fund_code) == 6
        assert fund_code.isdigit()
        assert generator.validate(fund_code)

    def test_generate_batch(self, generator_factory):
        """测试批量生成基金代码"""
        from dataforge.generators.finance.fund import FundCodeGenerator

        generator_factory.registry.register("fund", FundCodeGenerator)

        config = GeneratorConfig(generator_type="fund", parameters={})
        generator = generator_factory.create_generator(config)
        fund_codes = generator.generate_batch(10)

        assert len(fund_codes) == 10
        for code in fund_codes:
            assert isinstance(code, str)
            assert len(code) == 6
            assert code.isdigit()

    def test_fund_type(self, generator_factory):
        """测试基金类型"""
        from dataforge.generators.finance.fund import FundCodeGenerator

        generator_factory.registry.register("fund", FundCodeGenerator)

        config = GeneratorConfig(
            generator_type="fund", parameters={"fund_type": "equity"}
        )
        generator = generator_factory.create_generator(config)
        fund_code = generator.generate_single()

        assert isinstance(fund_code, str)
        assert len(fund_code) == 6

    def test_market(self, generator_factory):
        """测试市场类型"""
        from dataforge.generators.finance.fund import FundCodeGenerator

        generator_factory.registry.register("fund", FundCodeGenerator)

        config = GeneratorConfig(
            generator_type="fund", parameters={"market": "domestic"}
        )
        generator = generator_factory.create_generator(config)
        fund_code = generator.generate_single()

        assert isinstance(fund_code, str)
        assert fund_code.isdigit()

    def test_validation(self, generator_factory):
        """测试基金代码验证"""
        from dataforge.generators.finance.fund import FundCodeGenerator

        generator_factory.registry.register("fund", FundCodeGenerator)

        config = GeneratorConfig(generator_type="fund", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid fund codes
        assert generator.validate("000001")
        assert generator.validate("519888")

        # Invalid fund codes
        assert not generator.validate("12345")  # Too short
        assert not generator.validate("ABCDEF")  # Not numeric
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试基金代码唯一性"""
        from dataforge.generators.finance.fund import FundCodeGenerator

        generator_factory.registry.register("fund", FundCodeGenerator)

        config = GeneratorConfig(generator_type="fund", parameters={})
        generator = generator_factory.create_generator(config)
        codes = generator.generate_batch(50)

        # Should have variety
        unique_codes = set(codes)
        assert len(unique_codes) > 30

    def test_format(self, generator_factory):
        """测试代码格式"""
        from dataforge.generators.finance.fund import FundCodeGenerator

        generator_factory.registry.register("fund", FundCodeGenerator)

        config = GeneratorConfig(generator_type="fund", parameters={})
        generator = generator_factory.create_generator(config)
        fund_code = generator.generate_single()

        # Chinese fund code: 6 digits
        assert len(fund_code) == 6
        assert fund_code.isdigit()
        assert fund_code[0] in "0123456789"

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.finance.fund import FundCodeGenerator

        generator_factory.registry.register("fund", FundCodeGenerator)

        config = GeneratorConfig(generator_type="fund", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            code = generator.generate_single()
            assert code is not None
            assert len(code) == 6
            assert code.isdigit()
