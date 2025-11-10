"""
股票代码生成器

支持生成沪深A股、港股、美股等市场的股票代码
"""

import random  # TODO: Convert to secrets
import secrets
import re
from ...core.types import (
GeneratorType
)
from typing import Optional

from ...core.factory import register_generator
from ...core.generator import (

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   secrets.randbelow(b - a + 1) + a → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary

    DataGenerator,
    GenerationContext,
)


@register_generator("stock_code", aliases=["stock", "equity"])
class StockCodeGenerator(DataGenerator[str]):
    """股票代码生成器"""

    def _setup(self) -> None:
        """初始化股票代码生成器参数"""
        self.market = self.parameters.get("market", "A_SHARE")  # A_SHARE, HONG_KONG, US
        self.sector = self.parameters.get("sector", None)  # 行业板块
        self.exchange = self.parameters.get("exchange", None)  # 交易所
        self.include_suffix = self.parameters.get(
            "include_suffix", True
        )  # 是否包含后缀
        self.format = self.parameters.get("format", "CODE")  # CODE, FULL, SYMBOL

        # 沪深A股代码规则
        self.a_share_codes = {
            "主板": {"prefix": ["600", "601", "603", "605"], "range": (600000, 609999)},
            "科创板": {"prefix": ["688"], "range": (688000, 688999)},
            "创业板": {"prefix": ["300"], "range": (300000, 309999)},
            "北交所": {"prefix": ["83", "87"], "range": (830000, 839999)},
            "中小板": {"prefix": ["002"], "range": (2000, 2999)},
            "深证主板": {"prefix": ["000"], "range": (1, 999)},
        }

        # 港股代码规则
        self.hk_codes = {
            "主板": {"range": (1, 3999)},
            "创业板": {"range": (8000, 8999)},
            "生物科技": {"range": (18000, 18999)},
            "新经济": {"range": (19000, 19999)},
        }

        # 美股代码规则
        self.us_codes = {
            "NYSE": {"length": [1, 4], "pattern": r"^[A-Z]{1,4}$"},
            "NASDAQ": {"length": [1, 5], "pattern": r"^[A-Z]{1,5}$"},
            "AMEX": {"length": [1, 4], "pattern": r"^[A-Z]{1,4}$"},
        }

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成股票代码"""
        if self.market == "A_SHARE":
            return self._generate_a_share_code()
        elif self.market == "HONG_KONG":
            return self._generate_hk_code()
        elif self.market == "US":
            return self._generate_us_code()
        else:
            return self._generate_a_share_code()  # 默认A股

    def _generate_a_share_code(self) -> str:
        """生成A股代码"""
        sectors = list(self.a_share_codes.keys())
        selected_sector = self.sector or secrets.choice(sectors)

        if selected_sector not in self.a_share_codes:
            selected_sector = secrets.choice(sectors)

        sector_info = self.a_share_codes[selected_sector]
        code_range = sector_info["range"]

        # 生成代码并确保6位
        code_num = secrets.randbelow(code_range[1] - code_range[0] + 1) + code_range[0]
        code = str(code_num).zfill(6)

        # 添加后缀
        if self.include_suffix and self.format == "FULL":
            if selected_sector in ["主板", "科创板"]:
                code += ".SS"  # 上交所
            elif selected_sector in ["创业板", "北交所", "中小板", "深证主板"]:
                code += ".SZ"  # 深交所

        return code

    def _generate_hk_code(self) -> str:
        """生成港股代码"""
        sectors = list(self.hk_codes.keys())
        selected_sector = self.sector or secrets.choice(sectors)

        if selected_sector not in self.hk_codes:
            selected_sector = secrets.choice(sectors)

        sector_info = self.hk_codes[selected_sector]
        code_range = sector_info["range"]

        code = str(secrets.randbelow(code_range[1] - code_range[0] + 1) + code_range[0]).zfill(4)

        if self.include_suffix and self.format == "FULL":
            code += ".HK"

        return code

    def _generate_us_code(self) -> str:
        """生成美股代码"""
        exchanges = list(self.us_codes.keys())
        selected_exchange = self.exchange or secrets.choice(exchanges)

        if selected_exchange not in self.us_codes:
            selected_exchange = secrets.choice(exchanges)

        length_range = self.us_codes[selected_exchange]["length"]
        length = secrets.choice(length_range)

        # 生成大写字母代码
        code = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=length))

        return code

    def validate(self, data: str) -> bool:
        """验证股票代码格式"""
        if not isinstance(data, str):
            return False

        # 移除后缀进行验证
        code = data.split(".")[0]

        if self.market == "A_SHARE":
            return self._validate_a_share_code(code)
        elif self.market == "HONG_KONG":
            return self._validate_hk_code(code)
        elif self.market == "US":
            return self._validate_us_code(code)
        else:
            return self._validate_a_share_code(code)

    def _validate_a_share_code(self, code: str) -> bool:
        """验证A股代码格式"""
        if not code.isdigit() or len(code) != 6:
            return False

        code_int = int(code)
        for _sector, info in self.a_share_codes.items():
            if info["range"][0] <= code_int <= info["range"][1]:
                return True

        return False

    def _validate_hk_code(self, code: str) -> bool:
        """验证港股代码格式"""
        if not code.isdigit():
            return False

        code_int = int(code)
        for _sector, info in self.hk_codes.items():
            if info["range"][0] <= code_int <= info["range"][1]:
                return True

        return False

    def _validate_us_code(self, code: str) -> bool:
        """验证美股代码格式"""
        pattern = r"^[A-Z]{1,5}$"
        return bool(re.match(pattern, code))

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.FINANCE

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "market",
            "sector",
            "exchange",
            "include_suffix",
            "format",
        ]

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项 - TODO: Implement generation logic"""
        return self._generate_raw(context)



@register_generator("stock_code", ["股票代码", "stock", "股票"])
class GenericStockCodeGenerator(StockCodeGenerator):
    """通用股票代码生成器注册版本"""

    pass


