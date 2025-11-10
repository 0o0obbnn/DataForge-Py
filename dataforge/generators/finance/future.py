"""期货合约代码生成器

支持生成商品期货、金融期货等各类期货合约代码
"""

import random  # TODO: Convert to secrets
import secrets
import re
from datetime import datetime, timedelta
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


class FutureCodeGenerator(DataGenerator[str]):
    """期货合约代码生成器"""

    def _setup(self) -> None:
        """初始化期货合约代码生成器参数"""
        self.future_type = self.parameters.get(
            "future_type", "COMMODITY"
        )  # COMMODITY, FINANCIAL
        self.market = self.parameters.get("market", "CHINA")  # CHINA, US
        self.commodity = self.parameters.get("commodity", None)  # 商品类型
        self.expiry_month = self.parameters.get("expiry_month", None)  # 到期月份
        self.expiry_year = self.parameters.get("expiry_year", None)  # 到期年份
        self.format = self.parameters.get("format", "CODE")  # CODE, FULL

        # 中国商品期货合约代码规则
        self.china_commodity_futures = {
            "金属类": {
                "铜": {"code": "CU", "exchange": "SHFE"},
                "铝": {"code": "AL", "exchange": "SHFE"},
                "锌": {"code": "ZN", "exchange": "SHFE"},
                "铅": {"code": "PB", "exchange": "SHFE"},
                "镍": {"code": "NI", "exchange": "SHFE"},
                "锡": {"code": "SN", "exchange": "SHFE"},
                "黄金": {"code": "AU", "exchange": "SHFE"},
                "白银": {"code": "AG", "exchange": "SHFE"},
                "螺纹钢": {"code": "RB", "exchange": "SHFE"},
                "热轧卷板": {"code": "HC", "exchange": "SHFE"},
            },
            "能源化工类": {
                "原油": {"code": "SC", "exchange": "INE"},
                "燃料油": {"code": "FU", "exchange": "SHFE"},
                "沥青": {"code": "BU", "exchange": "SHFE"},
                "PTA": {"code": "TA", "exchange": "ZCE"},
                "甲醇": {"code": "MA", "exchange": "ZCE"},
                "聚乙烯": {"code": "L", "exchange": "DCE"},
                "聚丙烯": {"code": "PP", "exchange": "DCE"},
                "聚氯乙烯": {"code": "V", "exchange": "DCE"},
                "天然橡胶": {"code": "RU", "exchange": "SHFE"},
            },
            "农产品类": {
                "豆粕": {"code": "M", "exchange": "DCE"},
                "豆油": {"code": "Y", "exchange": "DCE"},
                "棕榈油": {"code": "P", "exchange": "DCE"},
                "玉米": {"code": "C", "exchange": "DCE"},
                "白糖": {"code": "SR", "exchange": "ZCE"},
                "棉花": {"code": "CF", "exchange": "ZCE"},
                "鸡蛋": {"code": "JD", "exchange": "DCE"},
                "苹果": {"code": "AP", "exchange": "ZCE"},
            },
        }

        # 中国金融期货合约代码规则
        self.china_financial_futures = {
            "股指期货": {
                "沪深300": {"code": "IF", "exchange": "CFFEX"},
                "上证50": {"code": "IH", "exchange": "CFFEX"},
                "中证500": {"code": "IC", "exchange": "CFFEX"},
                "中证1000": {"code": "IM", "exchange": "CFFEX"},
            },
            "国债期货": {
                "2年期": {"code": "TS", "exchange": "CFFEX"},
                "5年期": {"code": "TF", "exchange": "CFFEX"},
                "10年期": {"code": "T", "exchange": "CFFEX"},
                "30年期": {"code": "TL", "exchange": "CFFEX"},
            },
        }

        # 美国期货合约代码规则
        self.us_futures = {
            "金属类": {
                "黄金": {"code": "GC", "exchange": "COMEX"},
                "白银": {"code": "SI", "exchange": "COMEX"},
                "铜": {"code": "HG", "exchange": "COMEX"},
                "铂金": {"code": "PL", "exchange": "NYMEX"},
                "钯金": {"code": "PA", "exchange": "NYMEX"},
            },
            "能源类": {
                "原油": {"code": "CL", "exchange": "NYMEX"},
                "天然气": {"code": "NG", "exchange": "NYMEX"},
                "取暖油": {"code": "HO", "exchange": "NYMEX"},
                "汽油": {"code": "RB", "exchange": "NYMEX"},
            },
            "农产品类": {
                "玉米": {"code": "C", "exchange": "CBOT"},
                "大豆": {"code": "S", "exchange": "CBOT"},
                "小麦": {"code": "W", "exchange": "CBOT"},
                "棉花": {"code": "CT", "exchange": "ICE"},
                "糖": {"code": "SB", "exchange": "ICE"},
                "咖啡": {"code": "KC", "exchange": "ICE"},
            },
            "金融类": {
                "标普500": {"code": "ES", "exchange": "CME"},
                "纳斯达克": {"code": "NQ", "exchange": "CME"},
                "道琼斯": {"code": "YM", "exchange": "CBOT"},
                "美元指数": {"code": "DX", "exchange": "ICE"},
                "10年期国债": {"code": "ZN", "exchange": "CBOT"},
            },
        }

        # 期货月份代码
        self.month_codes = {
            1: "F",
            2: "G",
            3: "H",
            4: "J",
            5: "K",
            6: "M",
            7: "N",
            8: "Q",
            9: "U",
            10: "V",
            11: "X",
            12: "Z",
        }

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成期货合约代码"""
        if self.market == "CHINA":
            if self.future_type == "COMMODITY":
                return self._generate_china_commodity_future()
            else:
                return self._generate_china_financial_future()
        elif self.market == "US":
            return self._generate_us_future()
        else:
            return self._generate_china_commodity_future()

    def _generate_china_commodity_future(self) -> str:
        """生成中国商品期货合约代码"""
        # 选择商品类别
        categories = list(self.china_commodity_futures.keys())
        selected_category = secrets.choice(categories)

        # 选择具体商品
        commodities = list(self.china_commodity_futures[selected_category].keys())
        selected_commodity = self.commodity or secrets.choice(commodities)

        if selected_commodity not in self.china_commodity_futures[selected_category]:
            selected_commodity = secrets.choice(commodities)

        commodity_info = self.china_commodity_futures[selected_category][
            selected_commodity
        ]
        code = commodity_info["code"]
        exchange = commodity_info["exchange"]

        # 生成到期月份和年份
        expiry_month, expiry_year = self._get_expiry_date()

        # 中国期货格式：代码 + 年份后两位 + 月份
        contract_code = f"{code}{expiry_year}{expiry_month:02d}"

        if self.format == "FULL":
            return f"{contract_code}.{exchange}"

        return contract_code

    def _generate_china_financial_future(self) -> str:
        """生成中国金融期货合约代码"""
        # 选择期货类型
        categories = list(self.china_financial_futures.keys())
        selected_category = secrets.choice(categories)

        # 选择具体合约
        contracts = list(self.china_financial_futures[selected_category].keys())
        selected_contract = secrets.choice(contracts)

        contract_info = self.china_financial_futures[selected_category][
            selected_contract
        ]
        code = contract_info["code"]
        exchange = contract_info["exchange"]

        # 生成到期月份和年份
        expiry_month, expiry_year = self._get_expiry_date()

        # 中国金融期货格式：代码 + 年份后两位 + 月份
        contract_code = f"{code}{expiry_year}{expiry_month:02d}"

        if self.format == "FULL":
            return f"{contract_code}.{exchange}"

        return contract_code

    def _generate_us_future(self) -> str:
        """生成美国期货合约代码"""
        # 选择期货类别
        categories = list(self.us_futures.keys())
        selected_category = secrets.choice(categories)

        # 选择具体商品
        commodities = list(self.us_futures[selected_category].keys())
        selected_commodity = self.commodity or secrets.choice(commodities)

        if selected_commodity not in self.us_futures[selected_category]:
            selected_commodity = secrets.choice(commodities)

        commodity_info = self.us_futures[selected_category][selected_commodity]
        code = commodity_info["code"]
        exchange = commodity_info["exchange"]

        # 生成到期月份和年份
        expiry_month, expiry_year = self._get_expiry_date()

        # 美国期货格式：代码 + 月份字母 + 年份后两位
        month_letter = self.month_codes[expiry_month]
        contract_code = f"{code}{month_letter}{expiry_year}"

        if self.format == "FULL":
            return f"{contract_code}.{exchange}"

        return contract_code

    def _get_expiry_date(self) -> tuple[int, int]:
        """获取期货合约到期月份和年份"""
        if self.expiry_month and self.expiry_year:
            return self.expiry_month, self.expiry_year % 100

        # 默认生成未来1-12个月的合约
        today = datetime.now()
        months_ahead = secrets.randbelow(12) + 1
        expiry_date = today + timedelta(days=months_ahead * 30)

        return expiry_date.month, expiry_date.year % 100

    def validate(self, data: str) -> bool:
        """验证期货合约代码格式"""
        if not isinstance(data, str):
            return False

        # 移除交易所后缀
        code = data.split(".")[0]

        if self.market == "CHINA":
            return self._validate_china_future(code)
        elif self.market == "US":
            return self._validate_us_future(code)
        else:
            return self._validate_china_future(code)

    def _validate_china_future(self, code: str) -> bool:
        """验证中国期货合约代码格式"""

        # 中国期货格式：商品代码(1-3字母) + 年份后两位 + 月份(2位)
        pattern = r"^[A-Z]{1,3}[0-9]{2}(0[1-9]|1[0-2])$"
        return bool(re.match(pattern, code))

    def _validate_us_future(self, code: str) -> bool:
        """验证美国期货合约代码格式"""

        # 美国期货格式：商品代码(1-3字母) + 月份字母 + 年份后两位
        month_letters = "FGHJKMNQUVXZ"
        pattern = rf"^[A-Z]{{1,3}}[{month_letters}][0-9]{{2}}$"
        return bool(re.match(pattern, code))

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.FINANCE

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "future_type",
            "market",
            "commodity",
            "expiry_month",
            "expiry_year",
            "format",
        ]

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项 - TODO: Implement generation logic"""
        return self._generate_raw(context)



@register_generator("future_code", ["期货合约", "future", "期货"])
class GenericFutureCodeGenerator(FutureCodeGenerator):
    """通用期货合约代码生成器注册版本"""

    pass