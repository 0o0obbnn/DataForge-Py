"""
加密货币地址生成器

支持生成比特币、以太坊、莱特币等主流加密货币地址
"""

import secrets
from typing import Any, Optional, Union

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
)
from ...core.types import GeneratorType


@register_generator("crypto_address", aliases=["crypto", "cryptocurrency"])
class CryptoAddressGenerator(DataGenerator[str]):
    """加密货币地址生成器"""

    def _setup(self) -> None:
        """初始化加密货币地址生成器参数"""
        self.crypto_type = self.parameters.get(
            "crypto_type", "BITCOIN"
        )  # BITCOIN, ETHEREUM, LITECOIN, etc.
        self.network = self.parameters.get("network", "MAINNET")  # MAINNET, TESTNET
        self.address_type = self.parameters.get(
            "address_type", "P2PKH"
        )  # P2PKH, P2SH, BECH32
        self.include_prefix = self.parameters.get("include_prefix", False)
        self.format = self.parameters.get("format", "ADDRESS")  # ADDRESS, FULL

        # 加密货币地址规则
        self.crypto_configs = {
            "BITCOIN": {
                "mainnet": {
                    "P2PKH": {"prefix": "1", "length": [26, 35], "base58": True},
                    "P2SH": {"prefix": "3", "length": [26, 35], "base58": True},
                    "BECH32": {"prefix": "bc1", "length": [42, 62], "bech32": True},
                },
                "testnet": {
                    "P2PKH": {"prefix": "m", "length": [26, 35], "base58": True},
                    "P2SH": {"prefix": "2", "length": [26, 35], "base58": True},
                    "BECH32": {"prefix": "tb1", "length": [42, 62], "bech32": True},
                },
            },
            "ETHEREUM": {
                "mainnet": {
                    "P2PKH": {"prefix": "0x", "length": 42, "hex": True},
                },
                "testnet": {
                    "P2PKH": {"prefix": "0x", "length": 42, "hex": True},
                },
            },
            "LITECOIN": {
                "mainnet": {
                    "P2PKH": {"prefix": "L", "length": [26, 35], "base58": True},
                    "P2SH": {"prefix": "M", "length": [26, 35], "base58": True},
                    "BECH32": {"prefix": "ltc1", "length": [42, 62], "bech32": True},
                },
                "testnet": {
                    "P2PKH": {"prefix": "m", "length": [26, 35], "base58": True},
                    "P2SH": {"prefix": "Q", "length": [26, 35], "base58": True},
                    "BECH32": {"prefix": "tltc1", "length": [42, 62], "bech32": True},
                },
            },
            "BITCOINCASH": {
                "mainnet": {
                    "P2PKH": {"prefix": "1", "length": [26, 35], "base58": True},
                    "P2SH": {"prefix": "3", "length": [26, 35], "base58": True},
                    "CASHADDR": {
                        "prefix": "bitcoincash:q",
                        "length": [42, 62],
                        "cashaddr": True,
                    },
                },
                "testnet": {
                    "P2PKH": {"prefix": "m", "length": [26, 35], "base58": True},
                    "P2SH": {"prefix": "2", "length": [26, 35], "base58": True},
                    "CASHADDR": {
                        "prefix": "bchtest:q",
                        "length": [42, 62],
                        "cashaddr": True,
                    },
                },
            },
            "DOGECOIN": {
                "mainnet": {
                    "P2PKH": {"prefix": "D", "length": [26, 35], "base58": True},
                    "P2SH": {"prefix": "A", "length": [26, 35], "base58": True},
                },
                "testnet": {
                    "P2PKH": {"prefix": "n", "length": [26, 35], "base58": True},
                    "P2SH": {"prefix": "2", "length": [26, 35], "base58": True},
                },
            },
            "CARDANO": {
                "mainnet": {
                    "P2PKH": {"prefix": "addr1", "length": [59, 103], "bech32": True},
                },
                "testnet": {
                    "P2PKH": {
                        "prefix": "addr_test1",
                        "length": [59, 103],
                        "bech32": True,
                    },
                },
            },
            "POLKADOT": {
                "mainnet": {
                    "P2PKH": {"prefix": "1", "length": [47, 48], "base58": True},
                },
                "testnet": {
                    "P2PKH": {"prefix": "5", "length": [47, 48], "base58": True},
                },
            },
        }

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成加密货币地址"""
        if self.crypto_type not in self.crypto_configs:
            self.crypto_type = "BITCOIN"

        crypto_config = self.crypto_configs[self.crypto_type]

        if self.network not in crypto_config:
            self.network = "mainnet"

        network_config = crypto_config[self.network]

        if self.address_type not in network_config:
            self.address_type = list(network_config.keys())[0]

        address_config = network_config[self.address_type]

        return self._generate_address_by_type(address_config)

    def _generate_address_by_type(self, config: dict) -> str:
        """根据地址类型生成地址"""
        if "bech32" in config and config["bech32"]:
            return self._generate_bech32_address(config)
        elif "base58" in config and config["base58"]:
            return self._generate_base58_address(config)
        elif "hex" in config and config["hex"]:
            return self._generate_hex_address(config)
        elif "cashaddr" in config and config["cashaddr"]:
            return self._generate_cashaddr_address(config)
        else:
            return self._generate_base58_address(config)

    def _generate_bech32_address(self, config: dict) -> str:
        """生成Bech32格式地址"""
        prefix = config["prefix"]
        length = config["length"]

        if isinstance(length, list):
            actual_length = secrets.choice(range(length[0], length[1] + 1))
        else:
            actual_length = length

        # 生成随机数据
        random_data = self._generate_random_data(actual_length - len(prefix))

        return prefix + random_data

    def _generate_base58_address(self, config: dict) -> str:
        """生成Base58格式地址"""
        prefix = config["prefix"]
        length = config["length"]

        if isinstance(length, list):
            actual_length = secrets.choice(range(length[0], length[1] + 1))
        else:
            actual_length = length

        # 生成随机数据
        remaining_length = actual_length - len(prefix)
        random_data = self._generate_base58_data(remaining_length)

        return prefix + random_data

    def _generate_hex_address(self, config: dict) -> str:
        """生成Hex格式地址"""
        prefix = config["prefix"]

        # 生成40位十六进制地址
        address_data = "".join([secrets.choice("0123456789abcdef") for _ in range(40)])

        return prefix + address_data

    def _generate_cashaddr_address(self, config: dict) -> str:
        """生成CashAddr格式地址"""
        prefix = config["prefix"]
        length = config["length"]

        if isinstance(length, list):
            actual_length = secrets.choice(range(length[0], length[1] + 1))
        else:
            actual_length = length

        # 生成随机数据
        random_data = self._generate_base58_data(actual_length - len(prefix))

        return prefix + random_data

    def _generate_random_data(self, length: int) -> str:
        """生成随机数据"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        return "".join([secrets.choice(chars) for _ in range(length)])

    def _generate_base58_data(self, length: int) -> str:
        """生成Base58格式数据"""
        chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        return "".join([secrets.choice(chars) for _ in range(length)])

    def validate(self, data: str) -> bool:
        """验证加密货币地址格式"""
        if not isinstance(data, str):
            return False

        if self.crypto_type not in self.crypto_configs:
            return False

        crypto_config = self.crypto_configs[self.crypto_type]

        if self.network not in crypto_config:
            return False

        network_config = crypto_config[self.network]

        if self.address_type not in network_config:
            return False

        address_config = network_config[self.address_type]

        return self._validate_address_format(data, address_config)

    def _validate_address_format(self, address: str, config: dict) -> bool:
        """验证地址格式"""
        prefix = config["prefix"]
        length = config["length"]

        # 检查前缀
        if not address.startswith(prefix):
            return False

        # 检查长度
        if isinstance(length, list):
            if not (length[0] <= len(address) <= length[1]):
                return False
        else:
            if len(address) != length:
                return False

        # 检查字符集
        if "bech32" in config and config["bech32"]:
            return self._validate_bech32_chars(address[len(prefix) :])
        elif "base58" in config and config["base58"]:
            return self._validate_base58_chars(address[len(prefix) :])
        elif "hex" in config and config["hex"]:
            return self._validate_hex_chars(address[len(prefix) :])
        elif "cashaddr" in config and config["cashaddr"]:
            return self._validate_base58_chars(address[len(prefix) :])
        else:
            return True

    def _validate_bech32_chars(self, data: str) -> bool:
        """验证Bech32字符集"""
        valid_chars = set("abcdefghijklmnopqrstuvwxyz0123456789")
        return all(c in valid_chars for c in data)

    def _validate_base58_chars(self, data: str) -> bool:
        """验证Base58字符集"""
        valid_chars = set("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
        return all(c in valid_chars for c in data)

    def _validate_hex_chars(self, data: str) -> bool:
        """验证Hex字符集"""
        valid_chars = set("0123456789abcdefABCDEF")
        return all(c in valid_chars for c in data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.FINANCE

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "crypto_type",
            "network",
            "address_type",
            "include_prefix",
            "format",
        ]

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项 - TODO: Implement generation logic"""
        return self._generate_raw(context)


@register_generator("crypto_address", ["加密货币地址", "crypto", "钱包地址"])
class GenericCryptoAddressGenerator(CryptoAddressGenerator):
    """通用加密货币地址生成器注册版本"""

    pass


# 通用加密货币生成器已在文件开头定义
# 这里的重复定义应该被移除或合并
class CryptoGenerator(DataGenerator[Union[str, dict[str, Any]]]):
    """通用加密货币数据生成器"""

    def _setup(self) -> None:
        """初始化加密货币生成器参数"""
        self.data_type = self.parameters.get(
            "type", "full"
        )  # full, symbol, price, address, etc.
        self.crypto_type = self.parameters.get("crypto_type", "bitcoin")
        self.network = self.parameters.get("network", "mainnet")

        # 加密货币符号列表
        self.crypto_symbols = [
            "BTC",
            "ETH",
            "USDT",
            "BNB",
            "XRP",
            "ADA",
            "DOGE",
            "SOL",
            "DOT",
            "MATIC",
            "LTC",
            "SHIB",
            "TRX",
            "AVAX",
            "UNI",
            "LINK",
            "ATOM",
            "XMR",
            "ETC",
            "XLM",
            "BCH",
            "ALGO",
            "VET",
            "FIL",
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
            "FIL": "Filecoin",
        }

        # 加密货币类型
        self.crypto_types = ["coin", "token", "stablecoin"]

    def _generate_raw(
        self, context: Optional[GenerationContext] = None
    ) -> Union[str, dict[str, Any]]:
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
        price_range = secrets.choice(
            [
                (0.01, 1.0),  # 小币种
                (1.0, 100.0),  # 中等币种
                (100.0, 10000.0),  # 大币种
                (10000.0, 100000.0),  # 比特币级别
            ]
        )
        price = (
            secrets.randbelow(int((price_range[1] - price_range[0]) * 100)) / 100
            + price_range[0]
        )
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

    def _generate_full_data(self) -> dict[str, Any]:
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
            "type": crypto_type,
        }

    def validate(self, data: Union[str, dict[str, Any]]) -> bool:
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

    def generate_single(
        self, context: Optional[GenerationContext] = None
    ) -> Union[str, dict[str, Any]]:
        """生成单个数据项"""
        return self._generate_raw(context)
