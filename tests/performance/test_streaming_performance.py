#!/usr/bin/env python3
"""
实时数据流生成器测试 (pytest风格)

测试所有实时金融数据流生成器的功能和性能
"""

import pytest
from dataforge.core.factory import GeneratorFactory
from dataforge.core.generator import GeneratorConfig


@pytest.mark.asyncio
async def test_stream_price_generator(generator_factory: GeneratorFactory):
    """测试实时价格流生成器"""
    print("🔄 测试实时价格流生成器...")

    config = GeneratorConfig(
        generator_type="stream_price",
        parameters={
            "symbols": ["AAPL", "TSLA", "MSFT"],
            "update_interval": 0.1,
            "volatility": 0.05,
            "batch_size": 2,
        },
    )
    generator = generator_factory.create_generator(config)

    count = 0
    async for data in generator.generate_stream():
        if isinstance(data, list):
            for item in data:
                assert "type" in item
                assert item["type"] == "PRICE_UPDATE"
                assert "symbol" in item
                assert "price" in item
                assert "volume" in item
                print(
                    f"📊 价格更新: {item['symbol']} ${item['price']} (变化: {item['change_percent']}%)"
                )
        else:
            assert "type" in data
            print(f"📊 价格更新: {data['symbol']} ${data['price']}")

        count += 1
        if count >= 3:
            break

    print("✅ 实时价格流生成器测试通过")

@pytest.mark.asyncio
async def test_stream_orderbook_generator(generator_factory: GeneratorFactory):
    """测试实时订单簿流生成器"""
    print("🔄 测试实时订单簿流生成器...")

    config = GeneratorConfig(
        generator_type="stream_orderbook",
        parameters={"symbols": ["AAPL", "TSLA"], "update_interval": 0.2, "depth": 3},
    )
    generator = generator_factory.create_generator(config)

    count = 0
    async for data in generator.generate_stream():
        assert data["type"] == "ORDERBOOK_UPDATE"
        assert "symbol" in data
        assert "orderbook" in data
        assert "bids" in data["orderbook"]
        assert "asks" in data["orderbook"]

        print(f"📈 订单簿: {data['symbol']}")
        print(f"   买盘: {len(data['orderbook']['bids'])}档")
        print(f"   卖盘: {len(data['orderbook']['asks'])}档")
        print(f"   价差: ${data['orderbook']['spread']}")

        count += 1
        if count >= 2:
            break

    print("✅ 实时订单簿流生成器测试通过")

@pytest.mark.asyncio
async def test_stream_trade_generator(generator_factory: GeneratorFactory):
    """测试实时交易流生成器"""
    print("🔄 测试实时交易流生成器...")

    config = GeneratorConfig(
        generator_type="stream_trade",
        parameters={
            "symbols": ["AAPL", "TSLA", "MSFT"],
            "trade_rate": 1.0,  # 每秒1笔交易
            "min_quantity": 100,
            "max_quantity": 1000,
        },
    )
    generator = generator_factory.create_generator(config)

    count = 0
    async for data in generator.generate_stream():
        assert data["type"] == "TRADE"
        assert "symbol" in data
        assert "price" in data
        assert "quantity" in data
        assert "side" in data

        print(
            f"💰 交易: {data['side']} {data['quantity']}股 {data['symbol']} @ ${data['price']}"
        )

        count += 1
        if count >= 3:
            break

    print("✅ 实时交易流生成器测试通过")

@pytest.mark.asyncio
async def test_stream_news_generator(generator_factory: GeneratorFactory):
    """测试实时新闻流生成器"""
    print("🔄 测试实时新闻流生成器...")

    config = GeneratorConfig(
        generator_type="stream_news",
        parameters={
            "symbols": ["AAPL", "TSLA"],
            "news_rate": 0.5,  # 每分钟0.5条新闻
        },
    )
    generator = generator_factory.create_generator(config)

    count = 0
    async for data in generator.generate_stream():
        assert data["type"] == "NEWS"
        assert "symbol" in data
        assert "headline" in data
        assert "impact" in data

        print(f"📰 新闻: {data['symbol']} - {data['headline']}")
        print(f"   影响: {data['impact']}")

        count += 1
        if count >= 2:
            break

    print("✅ 实时新闻流生成器测试通过")

def test_sync_generators(generator_factory: GeneratorFactory):
    """测试同步生成器功能"""
    print("🔄 测试同步生成器...")

    # 测试同步价格生成
    config = GeneratorConfig(
        generator_type="stream_price", parameters={"symbols": ["TEST"]}
    )
    price_gen = generator_factory.create_generator(config)
    price_data = price_gen.generate()
    assert price_data["type"] == "PRICE_UPDATE"
    print(f"📊 同步价格: {price_data}")

    # 测试同步订单簿生成
    config = GeneratorConfig(
        generator_type="stream_orderbook", parameters={"symbols": ["TEST"]}
    )
    orderbook_gen = generator_factory.create_generator(config)
    orderbook_data = orderbook_gen.generate()
    assert orderbook_data["type"] == "ORDERBOOK_UPDATE"
    print(f"📈 同步订单簿: {orderbook_data}")

    # 测试同步交易生成
    config = GeneratorConfig(
        generator_type="stream_trade", parameters={"symbols": ["TEST"]}
    )
    trade_gen = generator_factory.create_generator(config)
    trade_data = trade_gen.generate()
    assert trade_data["type"] == "TRADE"
    print(f"💰 同步交易: {trade_data}")

    # 测试同步新闻生成
    config = GeneratorConfig(
        generator_type="stream_news", parameters={"symbols": ["TEST"]}
    )
    news_gen = generator_factory.create_generator(config)
    news_data = news_gen.generate()
    assert news_data["type"] == "NEWS"
    print(f"📰 同步新闻: {news_data}")

    print("✅ 同步生成器测试通过")

def test_registration(generator_factory: GeneratorFactory):
    """测试生成器注册"""
    print("🔄 测试生成器注册...")

    stream_generators = [
        "stream_price",
        "stream_orderbook",
        "stream_trade",
        "stream_news",
    ]

    registered = generator_factory.registry.list_generators()

    for gen_name in stream_generators:
        assert gen_name in registered, f"生成器 {gen_name} 未注册"
        print(f"✅ {gen_name} 已注册")

    print("✅ 所有流生成器已正确注册")
