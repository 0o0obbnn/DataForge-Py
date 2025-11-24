"""
时区标识生成器模块
支持生成各种时区标识格式
"""

import secrets
from typing import Optional

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
)
from ...core.protocols import Validator
from ...core.types import GeneratorType


class TimezoneValidator(Validator):
    """Validator for timezones."""

    def __init__(self, format: str, timezones: list[str], offsets: list[str]):
        self.format = format
        self.timezones = timezones
        self.offsets = offsets

    def validate(self, data: str) -> bool:
        """验证时区标识格式"""
        if not data or not isinstance(data, str):
            return False

        try:
            if self.format == "iana":
                # 简化的IANA时区验证
                if data in self.timezones or data.endswith(" (DST)"):
                    return True
                # 检查是否包含有效区域前缀
                if any(
                    data.startswith(prefix)
                    for prefix in [
                        "Asia/",
                        "America/",
                        "Europe/",
                        "Pacific/",
                        "Africa/",
                        "Australia/",
                    ]
                ):
                    return True

            elif self.format == "offset":
                # 时区偏移量验证
                if data in self.offsets or data.endswith(" (DST)"):
                    return True
                # 检查UTC/GMT格式
                if data.startswith(("UTC+", "UTC-", "GMT+", "GMT-")):
                    try:
                        offset_part = data[3:] if data.startswith("UTC") else data[3:]
                        if offset_part and (
                            offset_part.isdigit()
                            or (offset_part[0] in "+-" and offset_part[1:].isdigit())
                        ):
                            return True
                    except (ValueError, IndexError):
                        pass

            elif self.format == "abbreviation":
                # 时区缩写验证
                common_abbrevs = [
                    "UTC",
                    "GMT",
                    "CET",
                    "CEST",
                    "EET",
                    "EEST",
                    "WET",
                    "WEST",
                    "EST",
                    "EDT",
                    "CST",
                    "CDT",
                    "MST",
                    "MDT",
                    "PST",
                    "PDT",
                    "JST",
                    "KST",
                    "SGT",
                    "HKT",
                    "IST",
                    "AEST",
                    "AEDT",
                    "NZST",
                    "NZDT",
                ]
                if data in common_abbrevs or data.endswith(" (DST)"):
                    return True

        except (ValueError, AttributeError):
            return False

        return False

    @property
    def error_message(self) -> str:
        return "Invalid timezone format"


@register_generator("timezone", aliases=["tz", "time_zone"])
class TimezoneGenerator(DataGenerator[str]):
    """时区标识生成器"""

    # 常见时区标识
    TIMEZONES = [
        "UTC",
        "GMT",
        "Asia/Shanghai",
        "Asia/Tokyo",
        "Asia/Seoul",
        "Asia/Singapore",
        "America/New_York",
        "America/Los_Angeles",
        "America/Chicago",
        "Europe/London",
        "Europe/Paris",
        "Europe/Berlin",
        "Europe/Moscow",
        "Australia/Sydney",
        "Australia/Melbourne",
        "Africa/Cairo",
        "Africa/Johannesburg",
        "Pacific/Honolulu",
        "Pacific/Auckland",
    ]

    # 时区偏移量
    OFFSETS = [
        "UTC",
        "GMT",
        "UTC+0",
        "GMT+0",
        "UTC+1",
        "UTC+2",
        "UTC+3",
        "UTC+4",
        "UTC+5",
        "UTC+6",
        "UTC+7",
        "UTC+8",
        "UTC+9",
        "UTC+10",
        "UTC+11",
        "UTC+12",
        "UTC-1",
        "UTC-2",
        "UTC-3",
        "UTC-4",
        "UTC-5",
        "UTC-6",
        "UTC-7",
        "UTC-8",
        "UTC-9",
        "UTC-10",
        "UTC-11",
        "UTC-12",
        "GMT+1",
        "GMT+2",
        "GMT+3",
        "GMT+4",
        "GMT+5",
        "GMT+6",
        "GMT+7",
        "GMT+8",
        "GMT+9",
        "GMT+10",
        "GMT+11",
        "GMT+12",
        "GMT-1",
        "GMT-2",
        "GMT-3",
        "GMT-4",
        "GMT-5",
        "GMT-6",
        "GMT-7",
        "GMT-8",
        "GMT-9",
        "GMT-10",
        "GMT-11",
        "GMT-12",
    ]

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.format = "iana"
        self.region = "global"
        self.include_dst = False
        self.validator = None

    def _setup(self) -> None:
        """配置生成器参数"""
        self.format = self.parameters.get("format", "iana")
        self.region = self.parameters.get("region", "global")
        self.include_dst = self.parameters.get("include_dst", False)
        self.validator = TimezoneValidator(self.format, self.TIMEZONES, self.OFFSETS)

    def _get_regional_timezones(self) -> list:
        """获取区域特定的时区列表"""
        if self.region == "global":
            return self.TIMEZONES

        region_prefixes = {
            "asia": "Asia/",
            "europe": "Europe/",
            "america": "America/",
            "pacific": "Pacific/",
        }

        prefix = region_prefixes.get(self.region, "")
        return [tz for tz in self.TIMEZONES if tz.startswith(prefix)] or self.TIMEZONES

    def generate(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始时区标识"""
        if self.format == "iana":
            return self._generate_iana()
        elif self.format == "offset":
            return self._generate_offset()
        elif self.format == "abbreviation":
            return self._generate_abbreviation()
        else:
            return self._generate_iana()

    def _generate_iana(self) -> str:
        """生成IANA时区标识"""
        # 获取区域特定的时区列表
        regional_timezones = self._get_regional_timezones()
        timezone = secrets.choice(regional_timezones)

        if self.include_dst and (secrets.randbelow(1000000) / 1000000) < 0.3:
            # 模拟夏令时标识（简化处理）
            return f"{timezone} (DST)"

        return timezone

    def _generate_offset(self) -> str:
        """生成时区偏移量标识"""
        offset = secrets.choice(self.OFFSETS)

        if self.include_dst and (secrets.randbelow(1000000) / 1000000) < 0.3:
            # 模拟夏令时偏移（简化处理）
            if offset.startswith("UTC+"):
                return offset.replace("UTC+", "UTC+") + " (DST)"
            elif offset.startswith("UTC-"):
                return offset.replace("UTC-", "UTC-") + " (DST)"
            elif offset.startswith("GMT+"):
                return offset.replace("GMT+", "GMT+") + " (DST)"
            elif offset.startswith("GMT-"):
                return offset.replace("GMT-", "GMT-") + " (DST)"

        return offset

    def _generate_abbreviation(self) -> str:
        """生成时区缩写"""
        # 常见时区缩写
        abbreviations = [
            "UTC",
            "GMT",
            "CET",
            "CEST",
            "EET",
            "EEST",
            "WET",
            "WEST",
            "EST",
            "EDT",
            "CST",
            "CDT",
            "MST",
            "MDT",
            "PST",
            "PDT",
            "JST",
            "KST",
            "CST",
            "SGT",
            "HKT",
            "IST",
            "AEST",
            "AEDT",
            "NZST",
            "NZDT",
        ]

        abbreviation = secrets.choice(abbreviations)

        if self.include_dst and (secrets.randbelow(1000000) / 1000000) < 0.3:
            # 模拟夏令时缩写（简化处理）
            if abbreviation in ["CET", "EET", "WET"]:
                return abbreviation.replace("ET", "EST")
            elif abbreviation in ["EST", "CST", "MST", "PST"]:
                return abbreviation.replace("ST", "DT")

        return abbreviation

    def get_timezone_info(self, value: str) -> dict:
        """获取时区信息"""
        info = {
            "format": self.format,
            "region": self.region,
            "include_dst": self.include_dst,
            "value": value,
        }

        # 简化的时区类型判断
        if value.startswith("Asia/"):
            info["continent"] = "Asia"
        elif value.startswith("Europe/"):
            info["continent"] = "Europe"
        elif value.startswith("America/"):
            info["continent"] = "America"
        elif value.startswith("Pacific/"):
            info["continent"] = "Pacific"
        elif value.startswith("Africa/"):
            info["continent"] = "Africa"
        elif value.startswith("Australia/"):
            info["continent"] = "Australia"

        # 判断是否为夏令时
        if "(DST)" in value:
            info["is_dst"] = True
            info["base_timezone"] = value.replace(" (DST)", "")
        else:
            info["is_dst"] = False

        return info

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.NETWORK

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["format", "include_dst", "region"]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class GenericTimezoneGenerator(TimezoneGenerator):
    """通用时区标识生成器"""

    pass

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        # 尝试调用现有方法
        if hasattr(self, "generate") and callable(self.generate):
            return self.generate(context)
        else:
            # 基本实现
            return "generated_data"

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.NETWORK

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return isinstance(data, str) and bool(data.strip())
