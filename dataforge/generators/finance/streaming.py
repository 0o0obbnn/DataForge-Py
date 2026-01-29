"""
实时数据流生成器

支持WebSocket、Kafka、Redis Streams等实时数据流生成
提供事件驱动的金融数据流模拟，适用于实时系统测试和开发
"""

import asyncio
import random  # TODO: Convert to secrets
import secrets
import uuid
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any

from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
)
from ...core.protocols import Validator
from ...core.types import GeneratorType

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   secrets.randbelow(b - a + 1) + a → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   secrets.randbelow(b - a + 1) + a → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   secrets.randbelow(b - a + 1) + a → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   secrets.randbelow(b - a + 1) + a → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


class StreamConfig:
    """流配置"""

    def __init__(
        self,
        symbols: list[str],
        update_interval: float = 1.0,  # 秒
        volatility: float = 0.02,  # 波动率
        batch_size: int = 1,  # 批量大小
        enable_orderbook: bool = True,
        enable_trades: bool = True,
        enable_news: bool = False,
    ):
        self.symbols = symbols
        self.update_interval = update_interval
        self.volatility = volatility
        self.batch_size = batch_size
        self.enable_orderbook = enable_orderbook
        self.enable_trades = enable_trades
        self.enable_news = enable_news


class StreamPriceValidator(Validator):
    """Validator for StreamPriceGenerator parameters."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, GeneratorConfig):
            if not data.parameters.get("symbols"):
                raise ValueError("symbols 不能为空")
            if float(data.parameters.get("update_interval", 1.0)) <= 0:
                raise ValueError("update_interval 必须大于0")
        return True

    @property
    def error_message(self) -> str:
        return "Invalid StreamPriceGenerator configuration"


class StreamPriceGenerator(DataGenerator[dict]):
    """实时价格流生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = StreamPriceValidator()
        self.symbols = self.parameters.get("symbols", ["AAPL", "TSLA", "MSFT"])
        self.update_interval = float(self.parameters.get("update_interval", 1.0))
        self.volatility = float(self.parameters.get("volatility", 0.02))
        self.base_prices = {symbol: random.uniform(50, 500) for symbol in self.symbols}
        self.last_prices = self.base_prices.copy()

    def _setup(self) -> None:
        """初始化价格流生成器"""
        self.symbols = self.parameters.get("symbols", ["AAPL", "TSLA", "MSFT"])
        self.update_interval = float(self.parameters.get("update_interval", 1.0))
        self.volatility = float(self.parameters.get("volatility", 0.02))
        self.base_prices = {symbol: random.uniform(50, 500) for symbol in self.symbols}
        self.last_prices = self.base_prices.copy()

    async def generate_stream(
        self,
    ) -> AsyncGenerator[dict | list[dict[str, Any]], None]:
        """生成实时价格流"""
        while True:
            batch = []
            for _ in range(self.parameters.get("batch_size", 1)):
                symbol = secrets.choice(self.symbols)

                # 计算价格变化
                change_percent = random.gauss(0, self.volatility)
                new_price = self.last_prices[symbol] * (1 + change_percent)
                self.last_prices[symbol] = max(0.01, new_price)

                # 生成交易数据
                volume = secrets.randbelow(99001) + 1000

                price_data = {
                    "type": "PRICE_UPDATE",
                    "symbol": symbol,
                    "price": round(new_price, 2),
                    "change": round(new_price - self.base_prices[symbol], 2),
                    "change_percent": round(change_percent * 100, 2),
                    "volume": volume,
                    "timestamp": datetime.now().isoformat(),
                    "sequence": str(uuid.uuid4()),
                }
                batch.append(price_data)

            yield batch if len(batch) > 1 else batch[0]
            await asyncio.sleep(self.update_interval)

    def generate(self, context: GenerationContext | None = None) -> dict:
        """同步生成单条价格数据"""
        symbol = secrets.choice(self.symbols)
        change_percent = random.gauss(0, self.volatility)
        new_price = self.last_prices[symbol] * (1 + change_percent)
        self.last_prices[symbol] = max(0.01, new_price)

        return {
            "type": "PRICE_UPDATE",
            "symbol": symbol,
            "price": round(new_price, 2),
            "change": round(new_price - self.base_prices[symbol], 2),
            "change_percent": round(change_percent * 100, 2),
            "volume": secrets.randbelow(99001) + 1000,
            "timestamp": datetime.now().isoformat(),
        }

    def generate_single(self, context: GenerationContext | None = None) -> dict:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.FINANCE

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["symbols", "update_interval", "volatility"]

    def validate(self, data: dict) -> bool:
        """验证生成的数据"""
        return True


class StreamOrderbookValidator(Validator):
    """Validator for StreamOrderbookGenerator parameters."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, GeneratorConfig):
            if not data.parameters.get("symbols"):
                raise ValueError("symbols 不能为空")
            if int(data.parameters.get("depth", 5)) <= 0:
                raise ValueError("depth 必须大于0")
        return True

    @property
    def error_message(self) -> str:
        return "Invalid StreamOrderbookGenerator configuration"


class StreamOrderbookGenerator(DataGenerator[dict]):
    """实时订单簿流生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = StreamOrderbookValidator()
        self.symbols = self.parameters.get("symbols", ["AAPL", "TSLA", "MSFT"])
        self.update_interval = float(self.parameters.get("update_interval", 0.5))
        self.depth = int(self.parameters.get("depth", 5))
        self.base_spread = float(self.parameters.get("base_spread", 0.01))

        # 初始化订单簿
        self.orderbooks = {}
        for symbol in self.symbols:
            base_price = random.uniform(50, 500)
            self.orderbooks[symbol] = self._generate_orderbook(base_price)

    def _setup(self) -> None:
        """初始化订单簿流生成器"""
        self.symbols = self.parameters.get("symbols", ["AAPL", "TSLA", "MSFT"])
        self.update_interval = float(self.parameters.get("update_interval", 0.5))
        self.depth = int(self.parameters.get("depth", 5))
        self.base_spread = float(self.parameters.get("base_spread", 0.01))

        # 初始化订单簿
        self.orderbooks = {}
        for symbol in self.symbols:
            base_price = random.uniform(50, 500)
            self.orderbooks[symbol] = self._generate_orderbook(base_price)

    def _generate_orderbook(self, base_price: float) -> dict:
        """生成订单簿"""
        spread = base_price * self.base_spread

        # 买盘
        bids = []
        for i in range(self.depth):
            price = base_price - spread * (i + 1) * random.uniform(0.8, 1.2)
            volume = secrets.randbelow(9901) + 100 // (i + 1)
            bids.append({"price": round(price, 2), "volume": volume})

        # 卖盘
        asks = []
        for i in range(self.depth):
            price = base_price + spread * (i + 1) * random.uniform(0.8, 1.2)
            volume = secrets.randbelow(9901) + 100 // (i + 1)
            asks.append({"price": round(price, 2), "volume": volume})

        return {
            "bids": bids,
            "asks": asks,
            "spread": round(asks[0]["price"] - bids[0]["price"], 2),
        }

    async def generate_stream(self) -> AsyncGenerator[dict, None]:
        """生成实时订单簿流"""
        while True:
            symbol = secrets.choice(self.symbols)

            # 更新订单簿
            current_price = random.uniform(50, 500)
            self.orderbooks[symbol] = self._generate_orderbook(current_price)

            orderbook_data = {
                "type": "ORDERBOOK_UPDATE",
                "symbol": symbol,
                "orderbook": self.orderbooks[symbol],
                "timestamp": datetime.now().isoformat(),
                "sequence": str(uuid.uuid4()),
            }

            yield orderbook_data
            await asyncio.sleep(self.update_interval)

    def generate(self, context: GenerationContext | None = None) -> dict:
        """同步生成订单簿数据"""
        symbol = secrets.choice(self.symbols)
        current_price = random.uniform(50, 500)
        orderbook = self._generate_orderbook(current_price)

        return {
            "type": "ORDERBOOK_UPDATE",
            "symbol": symbol,
            "orderbook": orderbook,
            "timestamp": datetime.now().isoformat(),
        }

    def generate_single(self, context: GenerationContext | None = None) -> dict:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.FINANCE

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["base_spread", "depth", "symbols", "update_interval"]

    def validate(self, data: dict) -> bool:
        """验证生成的数据"""
        return True


class StreamTradeValidator(Validator):
    """Validator for StreamTradeGenerator parameters."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, GeneratorConfig):
            if not data.parameters.get("symbols"):
                raise ValueError("symbols 不能为空")
            if int(data.parameters.get("min_quantity", 100)) <= 0:
                raise ValueError("min_quantity 必须大于0")
        return True

    @property
    def error_message(self) -> str:
        return "Invalid StreamTradeGenerator configuration"


class StreamTradeGenerator(DataGenerator[dict]):
    """实时交易流生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = StreamTradeValidator()
        self.symbols = self.parameters.get("symbols", ["AAPL", "TSLA", "MSFT"])
        self.trade_rate = float(self.parameters.get("trade_rate", 2.0))  # 每秒交易数
        self.min_quantity = int(self.parameters.get("min_quantity", 100))
        self.max_quantity = int(self.parameters.get("max_quantity", 10000))

    def _setup(self) -> None:
        """初始化交易流生成器"""
        self.symbols = self.parameters.get("symbols", ["AAPL", "TSLA", "MSFT"])
        self.trade_rate = float(self.parameters.get("trade_rate", 2.0))  # 每秒交易数
        self.min_quantity = int(self.parameters.get("min_quantity", 100))
        self.max_quantity = int(self.parameters.get("max_quantity", 10000))

    async def generate_stream(self) -> AsyncGenerator[dict, None]:
        """生成实时交易流"""
        while True:
            # 计算本批次交易数量
            trades_per_batch = max(1, int(random.expovariate(1.0 / self.trade_rate)))

            for _ in range(trades_per_batch):
                symbol = secrets.choice(self.symbols)

                # 生成交易数据
                price = random.uniform(50, 500)
                quantity = (
                    secrets.randbelow(self.max_quantity - self.min_quantity + 1)
                    + self.min_quantity
                )
                side = secrets.choice(["BUY", "SELL"])

                trade_data = {
                    "type": "TRADE",
                    "symbol": symbol,
                    "price": round(price, 2),
                    "quantity": quantity,
                    "side": side,
                    "value": round(price * quantity, 2),
                    "timestamp": datetime.now().isoformat(),
                    "trade_id": str(uuid.uuid4()),
                }

                yield trade_data

            await asyncio.sleep(1.0 / self.trade_rate)

    def generate(self, context: GenerationContext | None = None) -> dict:
        """同步生成单条交易数据"""
        symbol = secrets.choice(self.symbols)
        price = random.uniform(50, 500)
        quantity = (
            secrets.randbelow(self.max_quantity - self.min_quantity + 1)
            + self.min_quantity
        )

        return {
            "type": "TRADE",
            "symbol": symbol,
            "price": round(price, 2),
            "quantity": quantity,
            "side": secrets.choice(["BUY", "SELL"]),
            "value": round(price * quantity, 2),
            "timestamp": datetime.now().isoformat(),
        }

    def generate_single(self, context: GenerationContext | None = None) -> dict:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.FINANCE

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["max_quantity", "min_quantity", "symbols", "trade_rate"]

    def validate(self, data: dict) -> bool:
        """验证生成的数据"""
        return True


class StreamNewsValidator(Validator):
    """Validator for StreamNewsGenerator parameters."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, GeneratorConfig):
            if not data.parameters.get("symbols"):
                raise ValueError("symbols 不能为空")
        return True

    @property
    def error_message(self) -> str:
        return "Invalid StreamNewsGenerator configuration"


class StreamNewsGenerator(DataGenerator[dict]):
    """实时新闻流生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = StreamNewsValidator()
        self.symbols = self.parameters.get("symbols", ["AAPL", "TSLA", "MSFT"])
        self.news_rate = float(self.parameters.get("news_rate", 0.1))  # 每分钟新闻数

        self.templates = [
            "{symbol} 宣布新的季度财报，营收超出预期 {percent}%",
            "{symbol} 获得重要合同，预计带来 {value} 亿美元收入",
            "分析师上调 {symbol} 目标价至 ${price}",
            "{symbol} 宣布股票回购计划，规模达 {value} 亿美元",
            "{symbol} 新产品发布获得市场积极反响",
        ]

    def _setup(self) -> None:
        """初始化新闻流生成器"""
        self.symbols = self.parameters.get("symbols", ["AAPL", "TSLA", "MSFT"])
        self.news_rate = float(self.parameters.get("news_rate", 0.1))  # 每分钟新闻数

        self.templates = [
            "{symbol} 宣布新的季度财报，营收超出预期 {percent}%",
            "{symbol} 获得重要合同，预计带来 {value} 亿美元收入",
            "分析师上调 {symbol} 目标价至 ${price}",
            "{symbol} 宣布股票回购计划，规模达 {value} 亿美元",
            "{symbol} 新产品发布获得市场积极反响",
        ]

    async def generate_stream(self) -> AsyncGenerator[dict, None]:
        """生成实时新闻流"""
        while True:
            # 计算新闻间隔
            interval = random.expovariate(self.news_rate / 60.0)  # 转换为秒

            symbol = secrets.choice(self.symbols)
            template = secrets.choice(self.templates)

            # 填充模板
            content = template.format(
                symbol=symbol,
                percent=secrets.randbelow(46) + 5,
                value=secrets.randbelow(100) + 1,
                price=secrets.randbelow(901) + 100,
            )

            news_data = {
                "type": "NEWS",
                "symbol": symbol,
                "headline": content,
                "impact": secrets.choice(["POSITIVE", "NEGATIVE", "NEUTRAL"]),
                "urgency": secrets.choice(["LOW", "MEDIUM", "HIGH"]),
                "timestamp": datetime.now().isoformat(),
                "news_id": str(uuid.uuid4()),
            }

            yield news_data
            await asyncio.sleep(interval)

    def generate(self, context: GenerationContext | None = None) -> dict:
        """同步生成新闻数据"""
        symbol = secrets.choice(self.symbols)
        template = secrets.choice(self.templates)

        return {
            "type": "NEWS",
            "symbol": symbol,
            "headline": template.format(
                symbol=symbol,
                percent=secrets.randbelow(46) + 5,
                value=secrets.randbelow(100) + 1,
                price=secrets.randbelow(901) + 100,
            ),
            "impact": secrets.choice(["POSITIVE", "NEGATIVE", "NEUTRAL"]),
            "timestamp": datetime.now().isoformat(),
        }

    def generate_single(self, context: GenerationContext | None = None) -> dict:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.FINANCE

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["news_rate", "symbols"]

    def validate(self, data: dict) -> bool:
        """验证生成的数据"""
        return True
