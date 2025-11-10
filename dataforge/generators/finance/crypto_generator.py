"""
通用加密货币数据生成器

支持生成加密货币地址、符号、价格、市值等多种数据
"""

import secrets
from typing import Optional, Union, Dict, Any

from ...core.factory import register_generator
from ...core.generator import DataGenerator, GenerationContext
from ...core.types import GeneratorType


@register_generator("crypto", aliases=["cryptocurrency"])
class CryptoGenerator(DataGenerator[Union[str, Dict[str, Any]]]):
    """通用加密货币数据生成器"""

    def _setup(self) -> None:
        """初始化加密货币生成器参数"""
        self.data_type = self.parameters.get("type", "full")  # full, symbol, price, address, etc.
        self.crypto_type = self.parameters.get("crypto_type", "bitcoin")
        self.network = self.parameters.get("network", "mainnet")
        
        # 加密货币符号列表
        self.crypto_symbols = [
            "BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "DOGE", "SOL", 
            "DOT", "MATIC", "LTC", "SHIB", "TRX", "AVAX", "UNI", "LINK",
            "ATOM", "XMR", "ETC", "XLM", "BCH", "ALGO", "VET", "FIL"
        ]
        
        # 加密货币名称
        self.crypto_names = {
            "BTC": "Bitcoin",
            "ETH": "Ethereum",
            "USDT": "Tether",
            "BNB": "Binance Coin",
            "XRP": "Ripple",
            "ADA": "Cardano",
            "DOGE": "Dogecoin",
            "SOL": "Solana",
            "DOT": "Polkadot",
            "MATIC": "Polygon",
            "LTC": "Litecoin",
            "SHIB": "Shiba Inu",
            "TRX": "TRON",
            "AVAX": "Avalanche",
            "UNI": "Uniswap",
            "LINK": "Chainlink",
            "ATOM": "Cosmos",
            "XMR": "Monero",
            "ETC": "Ethereum Classic",
            "XLM": "Stellar",
            "BCH": "Bitcoin Cash",
            "ALGO": "Algorand",
            "VET": "VeChain",
            "FIL": "Filecoin"
        }
        
        # 加密货币类型
        self.crypto_types = ["coin", "token", "stablecoin"]

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> Union[str, Dict[str, Any]]:
        """生成加密货币数据"""
        if self.data_type == "symbol":
            return self._generate_symbol()
        elif self.data_type == "price":
            return self._generate_price()
        elif self.data_type == "bitcoin_address":
            return self._generate_bitcoin_address()
        elif self.data_type == "ethereum_address":
            return self._generate_ethereum_address()
        elif self.data_type == "address":
            return self._generate_address()
        else:
            return self._generate_full_data()

    def _generate_symbol(self) -> str:
        """生成加密货币符号"""
        return secrets.choice(self.crypto_symbols)

    def _generate_price(self) -> float:
        """生成加密货币价格"""
        # 生成随机价格，范围从0.01到100000
        price_range = secrets.choice([
            (0.01, 1.0),      # 小币种
            (1.0, 100.0),     # 中等币种
            (100.0, 10000.0), # 大币种
            (10000.0, 100000.0) # 比特币级别
        ])
        price = secrets.randbelow(int((price_range[1] - price_range[0]) * 100)) / 100 + price_range[0]
        return round(price, 2)

    def _generate_bitcoin_address(self) -> str:
        """生成比特币地址"""
        # P2PKH地址 (以1开头)
        prefix = "1"
        length = secrets.randbelow(10) + 26  # 26-35字符
        chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        address = prefix + "".join(secrets.choice(chars) for _ in range(length - 1))
        return address

    def _generate_ethereum_address(self) -> str:
        """生成以太坊地址"""
        # 以太坊地址格式: 0x + 40位十六进制
        hex_chars = "0123456789abcdef"
        address = "0x" + "".join(secrets.choice(hex_chars) for _ in range(40))
        return address

    def _generate_address(self) -> str:
        """生成通用加密货币地址"""
        # 随机选择一种地址类型
        address_type = secrets.choice(["bitcoin", "ethereum"])
        if address_type == "bitcoin":
            return self._generate_bitcoin_address()
        else:
            return self._generate_ethereum_address()

    def _generate_full_data(self) -> Dict[str, Any]:
        """生成完整的加密货币数据"""
        symbol = self._generate_symbol()
        name = self.crypto_names.get(symbol, symbol)
        price = self._generate_price()
        
        # 生成市值和交易量
        market_cap = round(price * secrets.randbelow(1000000000) + 100000000, 2)
        volume_24h = round(market_cap * (secrets.randbelow(50) + 1) / 100, 2)
        
        # 生成24小时变化
        change_24h = round((secrets.randbelow(2000) - 1000) / 100, 2)  # -10% to +10%
        
        # 生成地址
        if symbol in ["BTC", "BCH", "LTC"]:
            address = self._generate_bitcoin_address()
            network = "Bitcoin"
        else:
            address = self._generate_ethereum_address()
            network = "Ethereum"
        
        # 确定类型
        if symbol in ["USDT", "USDC", "DAI"]:
            crypto_type = "stablecoin"
        elif symbol in ["BTC", "LTC", "BCH", "DOGE", "XMR"]:
            crypto_type = "coin"
        else:
            crypto_type = "token"
        
        return {
            "symbol": symbol,
            "name": name,
            "price": price,
            "market_cap": market_cap,
            "volume_24h": volume_24h,
            "change_24h": change_24h,
            "address": address,
            "network": network,
            "type": crypto_type
        }

    def validate(self, data: Union[str, Dict[str, Any]]) -> bool:
        """验证加密货币数据"""
        if self.data_type == "symbol":
            return isinstance(data, str) and len(data) >= 2 and data.isupper()
        elif self.data_type == "price":
            if isinstance(data, (int, float)):
                return data > 0
            elif isinstance(data, str):
                try:
                    return float(data) > 0
                except ValueError:
                    return False
            return False
        elif self.data_type in ["bitcoin_address", "ethereum_address", "address"]:
            return isinstance(data, str) and len(data) >= 26
        else:
            # 验证完整数据
            if not isinstance(data, dict):
                return False
            required_fields = ["symbol", "name", "price", "address"]
            return all(field in data for field in required_fields)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.FINANCE

    @property
    def supported_parameters(self) -> list[str]:
        return ["type", "crypto_type", "network"]

    def generate_single(self, context: Optional[GenerationContext] = None) -> Union[str, Dict[str, Any]]:
        """生成单个数据项"""
        return self._generate_raw(context)
