"""
物流单号生成器

生成各大快递公司的物流单号
支持顺丰、京东、中通、圆通、申通、韵达等主流快递公司
"""

import random  # TODO: Convert to secrets
import re
import secrets
from dataclasses import dataclass
from typing import Optional, Union

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
)
from ...core.protocols import Validator
from ...core.types import GeneratorType

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


@dataclass
class TrackingInfo:
    """物流单号信息数据模型"""

    tracking_number: str
    carrier: str
    service_type: str
    origin_city: str
    destination_city: str


class LogisticsValidator(Validator):
    """Validator for logistics numbers."""

    def __init__(self, carrier_config: dict):
        self.carrier_config = carrier_config

    def validate(self, data: dict[str, Union[str, int]]) -> bool:
        """验证生成的物流单号数据"""
        if "tracking_number" not in data:
            return False

        tracking_number = data["tracking_number"]
        carrier = data.get("carrier", "SF")

        # 确保 tracking_number 是字符串类型
        if not isinstance(tracking_number, str):
            return False

        # 验证快递公司
        if carrier not in self.carrier_config:
            return False

        # 验证单号格式
        config = self.carrier_config[carrier]
        if not re.match(config["pattern"], tracking_number):
            return False

        return True

    @property
    def error_message(self) -> str:
        return "Invalid logistics number format"


class LogisticsGenerator(DataGenerator[dict[str, Union[str, int]]]):
    """物流单号生成器

    功能特性：
    - 支持顺丰、京东、中通、圆通、申通、韵达等主流快递公司
    - 生成符合各公司规则的物流单号
    - 包含发件城市、收件城市等附加信息
    """

    def _setup(self) -> None:
        """初始化物流生成器配置"""
        self.carrier = self.parameters.get("carrier", "SF").upper()
        self.service_type = self.parameters.get("service_type", "STANDARD").upper()
        self.include_cities = self.parameters.get("include_cities", True)
        self.include_date = self.parameters.get("include_date", False)

        # 快递公司配置
        self.carrier_config = {
            "SF": {
                "name": "顺丰速运",
                "prefix": ["SF", "CX", "SF1"],
                "length": 12,
                "pattern": r"^SF\d{10,12}$|^CX\d{10,12}$",
            },
            "JD": {
                "name": "京东物流",
                "prefix": ["JD", "JDV", "JDX"],
                "length": 15,
                "pattern": r"^JD\d{13,15}$|^JDV\d{10,12}$",
            },
            "ZTO": {
                "name": "中通快递",
                "prefix": ["ZT", "753", "778"],
                "length": 12,
                "pattern": r"^ZT\d{10,12}$|^\d{12,15}$",
            },
            "YTO": {
                "name": "圆通速递",
                "prefix": ["YT", "DD", "V"],
                "length": 10,
                "pattern": r"^YT\d{8,10}$|^DD\d{8,10}$|^V\d{8,10}$",
            },
            "STO": {
                "name": "申通快递",
                "prefix": ["ST", "77", "88"],
                "length": 12,
                "pattern": r"^ST\d{10,12}$|^\d{12,15}$",
            },
            "YUNDA": {
                "name": "韵达快递",
                "prefix": ["YD", "120", "310"],
                "length": 13,
                "pattern": r"^YD\d{11,13}$|^\d{13,15}$",
            },
            "EMS": {
                "name": "邮政EMS",
                "prefix": ["EM", "EA", "EB"],
                "length": 13,
                "pattern": r"^EM\d{11,13}$|^EA\d{11,13}$",
            },
            "HTKY": {
                "name": "百世快递",
                "prefix": ["HT", "BH", "BS"],
                "length": 12,
                "pattern": r"^HT\d{10,12}$|^BH\d{10,12}$",
            },
        }
        self.validator = LogisticsValidator(self.carrier_config)

        # 主要城市列表
        self.cities = [
            "北京",
            "上海",
            "广州",
            "深圳",
            "杭州",
            "南京",
            "苏州",
            "天津",
            "武汉",
            "成都",
            "重庆",
            "西安",
            "长沙",
            "青岛",
            "济南",
            "大连",
            "沈阳",
            "哈尔滨",
            "长春",
            "郑州",
            "石家庄",
            "太原",
            "昆明",
            "贵阳",
            "南宁",
            "福州",
            "厦门",
            "南昌",
            "合肥",
            "海口",
        ]

    def _generate_tracking_number(self, carrier: str) -> str:
        """生成符合快递公司规则的物流单号"""
        if carrier not in self.carrier_config:
            carrier = "SF"

        config = self.carrier_config[carrier]
        prefix = secrets.choice(config["prefix"])

        # 计算数字部分长度，确保总长度符合要求
        prefix_length = len(prefix)
        target_length = config["length"]
        digits_length = target_length - prefix_length

        # 生成数字部分
        digits = "".join(str(secrets.randbelow(10)) for _ in range(digits_length))
        tracking_number = f"{prefix}{digits}"

        return tracking_number

    def _generate_service_info(self, carrier: str, service_type: str) -> dict[str, str]:
        """生成服务信息"""
        service_mapping = {
            "STANDARD": "标准快递",
            "EXPRESS": "特快专递",
            "ECONOMY": "经济快递",
            "OVERNIGHT": "次日达",
            "SAMEDAY": "当日达",
        }

        return {
            "service_type": service_type,
            "service_name": service_mapping.get(service_type, "标准服务"),
        }

    def _generate_date_info(self) -> dict[str, str]:
        """生成日期信息"""
        import datetime

        # 生成发货日期（过去30天内）
        today = datetime.date.today()
        random_days = secrets.randbelow(31)
        ship_date = today - datetime.timedelta(days=random_days)

        # 预计送达日期（发货后1-7天）
        delivery_days = secrets.randbelow(7) + 1
        expected_delivery = ship_date + datetime.timedelta(days=delivery_days)

        return {
            "ship_date": ship_date.strftime("%Y-%m-%d"),
            "expected_delivery": expected_delivery.strftime("%Y-%m-%d"),
            "delivery_days": str(delivery_days),
        }

    def generate(
        self, context: Optional[GenerationContext] = None
    ) -> dict[str, Union[str, int]]:
        """生成物流单号数据

        Returns:
            包含完整信息的字典
        """
        # 生成物流单号
        tracking_number = self._generate_tracking_number(self.carrier)

        # 获取快递公司信息
        carrier_info = self.carrier_config.get(self.carrier, self.carrier_config["SF"])

        # 生成服务信息
        service_info = self._generate_service_info(self.carrier, self.service_type)

        # 随机选择发件和收件城市
        origin_city, destination_city = random.sample(self.cities, 2)

        result = {
            "tracking_number": tracking_number,
            "carrier": self.carrier,
            "carrier_name": carrier_info["name"],
            "service_type": service_info["service_type"],
            "service_name": service_info["service_name"],
        }

        if self.include_cities:
            result.update(
                {
                    "origin_city": origin_city,
                    "destination_city": destination_city,
                }
            )

        if self.include_date:
            date_info = self._generate_date_info()
            result.update(date_info)

        return result

    def generate_single(
        self, context: Optional[GenerationContext] = None
    ) -> dict[str, Union[str, int]]:
        """生成单个数据项

        返回包含完整物流信息的字典
        """
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["carrier", "include_cities", "include_date", "service_type"]

    def validate(self, data: dict[str, Union[str, int]]) -> bool:
        """验证生成的数据

        Args:
            data: 包含完整信息的字典
        """
        # 类型检查
        if not isinstance(data, dict):
            return False

        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


@register_generator("generic_tracking_number", aliases=["tracking_number", "物流单号"])
class GenericTrackingNumberGenerator(LogisticsGenerator):
    """通用物流单号生成器注册版本"""

    def generate_single(
        self, context: Optional[GenerationContext] = None
    ) -> dict[str, Union[str, int]]:
        """生成单个数据项"""
        return self.generate(context)

    def validate(self, data: dict[str, Union[str, int]]) -> bool:
        """验证生成的数据"""
        validator = LogisticsValidator(self.carrier_config)
        return validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["carrier", "service_type", "include_cities", "include_date"]


@register_generator("generic_waybill", aliases=["waybill", "运单"])
class GenericWaybillGenerator(LogisticsGenerator):
    """通用运单号生成器注册版本"""

    def _setup(self) -> None:
        """重写运单号配置"""
        super()._setup()

        # 运单号通常更长，修复正则表达式以匹配所有前缀
        self.carrier_config.update(
            {
                "SF": {
                    "name": "顺丰货运",
                    "prefix": ["SF", "SFH", "SFW"],
                    "length": 15,
                    # 修复正则：匹配所有前缀，数字长度动态调整
                    "pattern": r"^(SF|SFH|SFW)\d{12,15}$",
                },
                "JD": {
                    "name": "京东货运",
                    "prefix": ["JDW", "JDH"],
                    "length": 18,
                    # 修复正则：匹配所有前缀，确保总长度符合要求
                    "pattern": r"^(JDW|JDH)\d{14,16}$",
                },
            }
        )

    def generate_single(
        self, context: Optional[GenerationContext] = None
    ) -> dict[str, Union[str, int]]:
        """生成单个数据项"""
        return self.generate(context)

    def validate(self, data: dict[str, Union[str, int]]) -> bool:
        """验证生成的数据"""
        validator = LogisticsValidator(self.carrier_config)
        return validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["carrier", "service_type", "include_cities", "include_date"]
