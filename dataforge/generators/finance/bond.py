"""债券代码生成器

支持生成国债、企业债、可转债等各类债券代码
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


class BondCodeGenerator(DataGenerator[str]):
    """债券代码生成器"""

    def _setup(self) -> None:
        """初始化债券代码生成器参数"""
        self.bond_type = self.parameters.get(
            "bond_type", "TREASURY"
        )  # TREASURY, CORPORATE, CONVERTIBLE
        self.market = self.parameters.get("market", "CHINA")  # CHINA, HONG_KONG, US
        self.include_suffix = self.parameters.get("include_suffix", True)
        self.format = self.parameters.get("format", "CODE")  # CODE, FULL

        # 中国债券代码规则
        self.china_bonds = {
            "国债": {
                "记账式国债": {"prefix": ["019", "010"], "range": (101, 999)},
                "储蓄国债": {"prefix": ["101", "102"], "range": (101, 999)},
                "特别国债": {"prefix": ["107"], "range": (701, 799)},
            },
            "企业债": {
                "一般企业债": {"prefix": ["122", "127"], "range": (1001, 9999)},
                "公司债": {"prefix": ["112", "113"], "range": (1001, 9999)},
                "中期票据": {"prefix": ["138", "108"], "range": (1001, 9999)},
            },
            "可转债": {
                "上证": {"prefix": ["110", "113"], "range": (101, 999)},
                "深证": {"prefix": ["125", "126", "127", "128"], "range": (101, 999)},
                "科创板": {"prefix": ["118"], "range": (101, 999)},
                "创业板": {"prefix": ["123"], "range": (101, 999)},
            },
            "地方政府债": {
                "一般债": {"prefix": ["130", "131"], "range": (1001, 9999)},
                "专项债": {"prefix": ["132", "133"], "range": (1001, 9999)},
            },
        }

        # 香港债券代码规则
        self.hk_bonds = {
            "政府债券": {"prefix": ["420", "421"], "range": (1001, 9999)},
            "企业债券": {"prefix": ["500", "501", "502"], "range": (1001, 9999)},
            "可转债": {"prefix": ["600", "601"], "range": (1001, 9999)},
        }

        # 美国债券代码规则
        self.us_bonds = {
            "TREASURY": {
                "pattern": r"^[A-Z]{2,3}[0-9]{2}$",
                "examples": ["US10Y", "US5Y", "US2Y"],
            },
            "CORPORATE": {
                "pattern": r"^[A-Z]{1,5}[0-9]{2}$",
                "examples": ["AAPL25", "MSFT30"],
            },
            "MUNICIPAL": {
                "pattern": r"^[A-Z]{2,4}[0-9]{2}$",
                "examples": ["CA25", "NY30"],
            },
        }

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成债券代码"""
        if self.market == "CHINA":
            return self._generate_china_bond()
        elif self.market == "HONG_KONG":
            return self._generate_hk_bond()
        elif self.market == "US":
            return self._generate_us_bond()
        else:
            return self._generate_china_bond()

    def _generate_china_bond(self) -> str:
        """生成中国债券代码"""
        bond_categories = list(self.china_bonds.keys())

        # 根据债券类型选择类别
        if self.bond_type == "TREASURY":
            selected_category = "国债"
        elif self.bond_type == "CORPORATE":
            selected_category = "企业债"
        elif self.bond_type == "CONVERTIBLE":
            selected_category = "可转债"
        else:
            selected_category = secrets.choice(bond_categories)

        if selected_category not in self.china_bonds:
            selected_category = secrets.choice(bond_categories)

        category_types = list(self.china_bonds[selected_category].keys())
        selected_type = secrets.choice(category_types)
        type_info = self.china_bonds[selected_category][selected_type]

        prefix = secrets.choice(type_info["prefix"])
        suffix = str(
            secrets.randbelow(type_info["range"][1] - type_info["range"][0] + 1) + type_info["range"][0]
        ).zfill(3)

        code = prefix + suffix

        # 添加交易所后缀
        if self.include_suffix and self.format == "FULL":
            if prefix.startswith("1") or prefix.startswith("2"):
                code += ".SS"  # 上交所
            elif prefix.startswith("0") or prefix.startswith("3"):
                code += ".SZ"  # 深交所

        return code

    def _generate_hk_bond(self) -> str:
        """生成香港债券代码"""
        # 根据债券类型选择类别
        if self.bond_type == "TREASURY":
            selected_category = "政府债券"
        elif self.bond_type == "CORPORATE":
            selected_category = "企业债券"
        elif self.bond_type == "CONVERTIBLE":
            selected_category = "可转债"
        else:
            selected_category = secrets.choice(list(self.hk_bonds.keys()))

        if selected_category not in self.hk_bonds:
            selected_category = secrets.choice(list(self.hk_bonds.keys()))

        category_info = self.hk_bonds[selected_category]
        prefix = secrets.choice(category_info["prefix"])
        suffix = str(
            secrets.randbelow(category_info["range"][1] - category_info["range"][0] + 1) + category_info["range"][0]
        ).zfill(4)

        code = prefix + suffix

        if self.include_suffix and self.format == "FULL":
            code += ".HK"

        return code

    def _generate_us_bond(self) -> str:
        """生成美国债券代码"""
        # 根据债券类型选择格式
        if self.bond_type == "TREASURY":
            # 美国国债代码格式：US + 期限 + Y
            tenors = ["2Y", "5Y", "10Y", "30Y"]
            tenor = secrets.choice(tenors)
            return f"US{tenor}"
        elif self.bond_type == "CORPORATE":
            # 企业债券代码格式：公司代码 + 到期年
            companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
            company = secrets.choice(companies)
            year = secrets.randbelow(11) + 25
            return f"{company}{year}"
        elif self.bond_type == "MUNICIPAL":
            # 市政债券代码格式：州代码 + 到期年
            states = ["CA", "NY", "TX", "FL", "IL"]
            state = secrets.choice(states)
            year = secrets.randbelow(11) + 25
            return f"{state}{year}"
        else:
            return self._generate_us_bond()

    def validate(self, data: str) -> bool:
        """验证债券代码格式"""
        if not isinstance(data, str):
            return False

        # 移除后缀进行验证
        code = data.split(".")[0]

        if self.market == "CHINA":
            return self._validate_china_bond(code)
        elif self.market == "HONG_KONG":
            return self._validate_hk_bond(code)
        elif self.market == "US":
            return self._validate_us_bond(code)
        else:
            return self._validate_china_bond(code)

    def _validate_china_bond(self, code: str) -> bool:
        """验证中国债券代码格式"""
        if not code.isdigit() or len(code) != 6:
            return False

        # 检查前缀匹配
        for _category, types in self.china_bonds.items():
            for _bond_type, info in types.items():
                for prefix in info["prefix"]:
                    if code.startswith(prefix):
                        return True

        return False

    def _validate_hk_bond(self, code: str) -> bool:
        """验证香港债券代码格式"""
        if not code.isdigit() or len(code) != 7:
            return False

        # 检查前缀匹配
        for _category, info in self.hk_bonds.items():
            for prefix in info["prefix"]:
                if code.startswith(prefix):
                    return True

        return False

    def _validate_us_bond(self, code: str) -> bool:
        """验证美国债券代码格式"""

        if self.bond_type == "TREASURY":
            pattern = r"^US[0-9]+Y$"
        elif self.bond_type == "CORPORATE":
            pattern = r"^[A-Z]{1,5}[0-9]{2}$"
        elif self.bond_type == "MUNICIPAL":
            pattern = r"^[A-Z]{2}[0-9]{2}$"
        else:
            pattern = r"^[A-Z]{2,5}[0-9]{2}$"

        return bool(re.match(pattern, code))

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.FINANCE

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "bond_type",
            "market",
            "include_suffix",
            "format",
        ]

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项 - TODO: Implement generation logic"""
        return self._generate_raw(context)



@register_generator("bond_code", ["债券代码", "bond", "债券"])
class GenericBondCodeGenerator(BondCodeGenerator):
    """通用债券代码生成器注册版本"""

    pass