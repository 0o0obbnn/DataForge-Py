"""基金代码生成器

支持生成公募基金、私募基金等各类基金代码
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
    GeneratorType,
)


class FundCodeGenerator(DataGenerator[str]):
    """基金代码生成器"""

    def _setup(self) -> None:
        """初始化基金代码生成器参数"""
        # 处理fund_type参数，支持equity等别名
        raw_fund_type = self.parameters.get("fund_type", "PUBLIC")
        if raw_fund_type in ["equity", "bond", "hybrid", "index", "money_market"]:
            self.fund_type = "PUBLIC"
            self.fund_category = raw_fund_type
        else:
            self.fund_type = raw_fund_type  # PUBLIC, PRIVATE
            self.fund_category = self.parameters.get("fund_category", None)
        
        self.market = self.parameters.get("market", "CHINA")  # CHINA, HONG_KONG, US
        self.include_suffix = self.parameters.get("include_suffix", True)
        self.format = self.parameters.get("format", "CODE")  # CODE, FULL

        # 中国公募基金代码规则
        self.china_public_funds = {
            "股票型": {"prefix": ["000", "001", "002", "003"], "range": (1, 9999)},
            "混合型": {"prefix": ["110", "160", "260"], "range": (1, 9999)},
            "债券型": {"prefix": ["050", "070", "090"], "range": (1, 9999)},
            "指数型": {
                "prefix": ["150", "160", "510", "512", "513"],
                "range": (1, 9999),
            },
            "QDII": {"prefix": ["050", "070", "080"], "range": (1, 9999)},
            "货币市场": {"prefix": ["000", "003", "004"], "range": (1, 9999)},
            "另类投资": {"prefix": ["160", "161", "162"], "range": (1, 9999)},
        }

        # 私募基金代码规则
        self.china_private_funds = {
            "私募证券": {"prefix": ["SJ"], "pattern": r"^SJ[0-9]{6}$"},
            "私募股权": {"prefix": ["SG"], "pattern": r"^SG[0-9]{6}$"},
            "创业投资": {"prefix": ["CT"], "pattern": r"^CT[0-9]{6}$"},
            "其他私募": {"prefix": ["QT"], "pattern": r"^QT[0-9]{6}$"},
        }

        # 香港基金代码规则
        self.hk_funds = {
            "公募基金": {"prefix": ["0", "1", "2", "3"], "range": (1, 9999)},
            "ETF": {"prefix": ["28", "30", "31"], "range": (1, 9999)},
            "REITs": {"prefix": ["8"], "range": (1, 9999)},
        }

        # 美国基金代码规则
        self.us_funds = {
            "共同基金": {"length": [5], "pattern": r"^[A-Z]{5}$"},
            "ETF": {"length": [3, 4], "pattern": r"^[A-Z]{3,4}$"},
            "REITs": {"length": [3, 4], "pattern": r"^[A-Z]{3,4}$"},
        }

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成基金代码"""
        if self.market == "CHINA":
            if self.fund_type == "PUBLIC":
                return self._generate_china_public_fund()
            else:
                return self._generate_china_private_fund()
        elif self.market == "HONG_KONG":
            return self._generate_hk_fund()
        elif self.market == "US":
            return self._generate_us_fund()
        else:
            return self._generate_china_public_fund()

    def _generate_china_public_fund(self) -> str:
        """生成中国公募基金代码"""
        categories = list(self.china_public_funds.keys())
        selected_category = self.fund_category or secrets.choice(categories)

        if selected_category not in self.china_public_funds:
            selected_category = secrets.choice(categories)

        category_info = self.china_public_funds[selected_category]
        prefix = secrets.choice(category_info["prefix"])

        # 生成6位代码
        suffix = str(secrets.randbelow(9999) + 1).zfill(4)
        code = prefix + suffix

        # 确保6位长度
        if len(code) > 6:
            code = code[:6]
        elif len(code) < 6:
            code = code.ljust(6, "0")

        return code

    def _generate_china_private_fund(self) -> str:
        """生成中国私募基金代码"""
        categories = list(self.china_private_funds.keys())
        selected_category = self.fund_category or secrets.choice(categories)

        if selected_category not in self.china_private_funds:
            selected_category = secrets.choice(categories)

        prefix = secrets.choice(self.china_private_funds[selected_category]["prefix"])
        suffix = str(secrets.randbelow(999999) + 1).zfill(6)

        return prefix + suffix

    def _generate_hk_fund(self) -> str:
        """生成香港基金代码"""
        categories = list(self.hk_funds.keys())
        selected_category = self.fund_category or secrets.choice(categories)

        if selected_category not in self.hk_funds:
            selected_category = secrets.choice(categories)

        category_info = self.hk_funds[selected_category]
        prefix = secrets.choice(category_info["prefix"])
        suffix = str(secrets.randbelow(9999) + 1).zfill(4)

        code = prefix + suffix

        if self.include_suffix and self.format == "FULL":
            code += ".HK"

        return code

    def _generate_us_fund(self) -> str:
        """生成美国基金代码"""
        categories = list(self.us_funds.keys())
        selected_category = self.fund_category or secrets.choice(categories)

        if selected_category not in self.us_funds:
            selected_category = secrets.choice(categories)

        length_range = self.us_funds[selected_category]["length"]
        length = secrets.choice(length_range)

        # 生成大写字母代码
        code = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=length))

        return code

    def validate(self, data: str) -> bool:
        """验证基金代码格式"""
        if not isinstance(data, str):
            return False

        # 移除后缀进行验证
        code = data.split(".")[0]

        if self.market == "CHINA":
            if self.fund_type == "PUBLIC":
                return self._validate_china_public_fund(code)
            else:
                return self._validate_china_private_fund(code)
        elif self.market == "HONG_KONG":
            return self._validate_hk_fund(code)
        elif self.market == "US":
            return self._validate_us_fund(code)
        else:
            return self._validate_china_public_fund(code)

    def _validate_china_public_fund(self, code: str) -> bool:
        """验证中国公募基金代码格式"""
        # 中国公募基金代码为6位数字
        if not code.isdigit() or len(code) != 6:
            return False
        
        # 任何6位数字都是有效的基金代码
        return True

    def _validate_china_private_fund(self, code: str) -> bool:
        """验证中国私募基金代码格式"""
        pattern = r"^[A-Z]{2}[0-9]{6}$"
        return bool(re.match(pattern, code))

    def _validate_hk_fund(self, code: str) -> bool:
        """验证香港基金代码格式"""
        if not code.isdigit():
            return False

        code_int = int(code)
        for _category, info in self.hk_funds.items():
            if info["range"][0] <= code_int <= info["range"][1]:
                return True

        return False

    def _validate_us_fund(self, code: str) -> bool:
        """验证美国基金代码格式"""
        pattern = r"^[A-Z]{3,5}$"
        return bool(re.match(pattern, code))

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.FINANCE

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "fund_type",
            "market",
            "fund_category",
            "include_suffix",
            "format",
        ]

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项 - TODO: Implement generation logic"""
        return self._generate_raw(context)



@register_generator("fund_code", ["基金代码", "fund", "基金"])
class GenericFundCodeGenerator(FundCodeGenerator):
    """通用基金代码生成器注册版本"""

    pass