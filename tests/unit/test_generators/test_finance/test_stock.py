"""
股票代码生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestStockGenerator:
    """股票代码生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个股票代码"""
        from dataforge.generators.finance.stock import StockCodeGenerator
        generator_factory.registry.register("stock", StockCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="stock",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        stock_code = generator.generate_single()
        
        assert isinstance(stock_code, str)
        assert len(stock_code) >= 6
        assert generator.validate(stock_code)

    def test_generate_batch(self, generator_factory):
        """测试批量生成股票代码"""
        from dataforge.generators.finance.stock import StockCodeGenerator
        generator_factory.registry.register("stock", StockCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="stock",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        stock_codes = generator.generate_batch(10)
        
        assert len(stock_codes) == 10
        for code in stock_codes:
            assert isinstance(code, str)
            assert generator.validate(code)

    def test_shanghai_stock(self, generator_factory):
        """测试上海股票代码"""
        from dataforge.generators.finance.stock import StockCodeGenerator
        generator_factory.registry.register("stock", StockCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="stock",
            parameters={"market": "shanghai"}
        )
        generator = generator_factory.create_generator(config)
        stock_code = generator.generate_single()
        
        # Shanghai stocks typically start with 6
        assert isinstance(stock_code, str)
        assert len(stock_code) == 6

    def test_shenzhen_stock(self, generator_factory):
        """测试深圳股票代码"""
        from dataforge.generators.finance.stock import StockCodeGenerator
        generator_factory.registry.register("stock", StockCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="stock",
            parameters={"market": "shenzhen"}
        )
        generator = generator_factory.create_generator(config)
        stock_code = generator.generate_single()
        
        # Shenzhen stocks typically start with 0 or 3
        assert isinstance(stock_code, str)
        assert len(stock_code) == 6

    def test_validation(self, generator_factory):
        """测试股票代码验证"""
        from dataforge.generators.finance.stock import StockCodeGenerator
        generator_factory.registry.register("stock", StockCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="stock",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid stock codes
        assert generator.validate("600000")  # Shanghai
        assert generator.validate("000001")  # Shenzhen
        
        # Invalid stock codes
        assert not generator.validate("12345")  # Too short
        assert not generator.validate("ABCDEF")  # Not numeric
        assert not generator.validate("")

    def test_uniqueness(self, generator_factory):
        """测试股票代码唯一性"""
        from dataforge.generators.finance.stock import StockCodeGenerator
        generator_factory.registry.register("stock", StockCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="stock",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        codes = generator.generate_batch(50)
        
        # Should have variety
        unique_codes = set(codes)
        assert len(unique_codes) > 10

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.finance.stock import StockCodeGenerator
        generator_factory.registry.register("stock", StockCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="stock",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            code = generator.generate_single()
            assert code is not None
            assert code.isdigit()
            assert len(code) == 6
