"""
流式金融数据生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
@pytest.mark.skip(reason="StreamingFinanceGenerator not implemented - advanced feature")
class TestStreamingFinanceGenerator:
    """流式金融数据生成器测试类"""

    def test_generate_stream_price(self, generator_factory):
        """测试生成流式价格数据"""
        from dataforge.generators.finance.streaming import StreamPriceGenerator

        generator_factory.registry.register("stream_price", StreamPriceGenerator)

        config = GeneratorConfig(generator_type="stream_price", parameters={})
        generator = generator_factory.create_generator(config)
        price_data = generator.generate_single()

        assert price_data is not None
        assert generator.validate(price_data)

    def test_generate_stream_orderbook(self, generator_factory):
        """测试生成流式订单簿数据"""
        from dataforge.generators.finance.streaming import StreamOrderbookGenerator

        generator_factory.registry.register(
            "stream_orderbook", StreamOrderbookGenerator
        )

        config = GeneratorConfig(generator_type="stream_orderbook", parameters={})
        generator = generator_factory.create_generator(config)
        orderbook = generator.generate_single()

        assert orderbook is not None
        assert generator.validate(orderbook)

    def test_generate_stream_trade(self, generator_factory):
        """测试生成流式交易数据"""
        from dataforge.generators.finance.streaming import StreamTradeGenerator

        generator_factory.registry.register("stream_trade", StreamTradeGenerator)

        config = GeneratorConfig(generator_type="stream_trade", parameters={})
        generator = generator_factory.create_generator(config)
        trade = generator.generate_single()

        assert trade is not None
        assert generator.validate(trade)

    def test_generate_stream_news(self, generator_factory):
        """测试生成流式新闻数据"""
        from dataforge.generators.finance.streaming import StreamNewsGenerator

        generator_factory.registry.register("stream_news", StreamNewsGenerator)

        config = GeneratorConfig(generator_type="stream_news", parameters={})
        generator = generator_factory.create_generator(config)
        news = generator.generate_single()

        assert news is not None
        assert generator.validate(news)

    def test_batch_generation(self, generator_factory):
        """测试批量生成流式数据"""
        from dataforge.generators.finance.streaming import StreamPriceGenerator

        generator_factory.registry.register("stream_price", StreamPriceGenerator)

        config = GeneratorConfig(generator_type="stream_price", parameters={})
        generator = generator_factory.create_generator(config)
        prices = generator.generate_batch(10)

        assert len(prices) == 10
        for price in prices:
            assert price is not None

    def test_price_with_symbol(self, generator_factory):
        """测试指定股票代码的价格"""
        from dataforge.generators.finance.streaming import StreamPriceGenerator

        generator_factory.registry.register("stream_price", StreamPriceGenerator)

        config = GeneratorConfig(
            generator_type="stream_price", parameters={"symbol": "AAPL"}
        )
        generator = generator_factory.create_generator(config)
        price_data = generator.generate_single()

        assert price_data is not None

    def test_validation(self, generator_factory):
        """测试流式数据验证"""
        from dataforge.generators.finance.streaming import StreamPriceGenerator

        generator_factory.registry.register("stream_price", StreamPriceGenerator)

        config = GeneratorConfig(generator_type="stream_price", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid data
        price_data = generator.generate_single()
        assert generator.validate(price_data)

        # Invalid data
        assert not generator.validate(None)
        assert not generator.validate("")

    def test_time_series(self, generator_factory):
        """测试时间序列数据"""
        from dataforge.generators.finance.streaming import StreamPriceGenerator

        generator_factory.registry.register("stream_price", StreamPriceGenerator)

        config = GeneratorConfig(
            generator_type="stream_price", parameters={"include_timestamp": True}
        )
        generator = generator_factory.create_generator(config)
        prices = generator.generate_batch(5)

        # Should have timestamps
        assert len(prices) == 5

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.finance.streaming import StreamPriceGenerator

        generator_factory.registry.register("stream_price", StreamPriceGenerator)

        config = GeneratorConfig(generator_type="stream_price", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            price_data = generator.generate_single()
            assert price_data is not None
