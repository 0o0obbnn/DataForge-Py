from __future__ import annotations

import re
import secrets
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

from ...core.factory import register_generator
from ...core.generator import DataGenerator, GenerationContext, GeneratorConfig
from ...core.protocols import Validator
from ...core.types import GeneratorType
from ...resources.name_config_loader import load_name_en_config


@dataclass
class PassportInfo:
    """护照信息数据模型"""

    passport_number: str
    passport_type: str
    country_code: str
    issue_date: str
    expiry_date: str
    holder_name: str


class PassportValidator(Validator):
    """Validator for passport numbers."""

    def validate(self, data: Any) -> bool:
        """验证生成的护照数据"""
        if not isinstance(data, dict):
            return False

        passport_number = data.get("passport_number")
        if not isinstance(passport_number, str) or not re.match(
            r"^[A-Z][0-9]{7,9}$", passport_number
        ):
            return False

        # 如果只有passport_number，只验证号码格式
        if len(data) == 1:
            return True

        country_code = data.get("country_code")
        if country_code is not None:
            if (
                not isinstance(country_code, str)
                or len(country_code) != 3
                or not country_code.isalpha()
            ):
                return False

        return True

    @property
    def error_message(self) -> str:
        return "Invalid passport format"


@dataclass
class PassportGeneratorConfig(GeneratorConfig):
    passport_type: str = "E"
    country_code: str = "CHN"
    include_dates: bool = True
    include_name: bool = True


class PassportGenerator(DataGenerator[dict[str, Any]]):
    """护照号码生成器

    功能特性：
    - 生成符合ICAO标准的护照号码
    - 支持中国护照(E开头)、外交护照(D开头)、公务护照(S开头)
    - 支持普通护照(G开头)和特区护照(H开头)
    - 包含有效期和签发日期计算
    """

    def __init__(self, config: PassportGeneratorConfig):
        super().__init__(config)
        self.config = config
        self.validator = PassportValidator()

        self.passport_types = {
            "E": "普通护照",
            "D": "外交护照",
            "S": "公务护照",
            "G": "普通护照",
            "H": "特区护照",
            "P": "普通护照",
        }
        self.chinese_surnames = [
            "张",
            "王",
            "李",
            "赵",
            "刘",
            "陈",
            "杨",
            "黄",
            "周",
            "吴",
            "徐",
            "孙",
            "胡",
            "朱",
            "高",
            "林",
            "何",
            "郭",
            "马",
            "罗",
        ]
        self.chinese_names = [
            "伟",
            "芳",
            "娜",
            "秀英",
            "敏",
            "静",
            "丽",
            "强",
            "磊",
            "军",
            "洋",
            "勇",
            "艳",
            "杰",
            "娟",
            "涛",
            "明",
            "超",
            "秀兰",
            "霞",
        ]

    def _generate_passport_number(self, passport_type: str) -> str:
        """生成符合规则的护照号码"""
        if passport_type.upper() not in self.passport_types:
            passport_type = "E"
        digits = "".join(str(secrets.randbelow(10)) for _ in range(8))
        return f"{passport_type.upper()}{digits}"

    def _generate_dates(self) -> tuple[str, str]:
        """生成签发日期和有效期"""
        issue_date = date.today() - timedelta(days=secrets.randbelow(365 * 5 + 1))
        expiry_date = issue_date + timedelta(days=365 * 10)
        return issue_date.strftime("%Y-%m-%d"), expiry_date.strftime("%Y-%m-%d")

    def _generate_chinese_name(self) -> str:
        """生成中文姓名"""
        surname = secrets.choice(self.chinese_surnames)
        name_part = secrets.choice(self.chinese_names)
        if (secrets.randbelow(1000000) / 1000000) > 0.5:
            name_part += secrets.choice(self.chinese_names)
        return f"{surname}{name_part}"

    def _generate_english_name(self) -> str:
        """生成英文姓名"""
        cfg = load_name_en_config()
        first_names = cfg.get("first_names_male", []) + cfg.get(
            "first_names_female", []
        )
        last_names = cfg.get("last_names", [])

        first = secrets.choice(first_names or ["John", "Jane"])
        last = secrets.choice(last_names or ["Smith"])
        return f"{first} {last}"

    def generate_single(
        self, context: GenerationContext | None = None
    ) -> str | dict[str, Any]:
        """生成单个护照数据

        默认返回护照号码字符串，除非明确设置string_only=False
        """
        # 如果没有明确设置string_only，默认为True（返回字符串）
        if "string_only" not in self.parameters:
            self.parameters["string_only"] = True

        passport_type = self.parameters.get("passport_type", "E").upper()
        country_code = self.parameters.get("country_code", "CHN").upper()

        passport_number = self._generate_passport_number(passport_type)

        # 如果只需要字符串，直接返回
        if self.parameters.get("string_only", False):
            return passport_number

        if country_code == "CHN":
            holder_name = self._generate_chinese_name()
        else:
            holder_name = self._generate_english_name()

        result: dict[str, Any] = {
            "passport_number": passport_number,
            "passport_type": passport_type,
            "passport_type_name": self.passport_types.get(passport_type, "未知类型"),
            "country_code": country_code,
        }

        if self.parameters.get("include_dates", True):
            issue_date, expiry_date = self._generate_dates()
            result.update(
                {
                    "issue_date": issue_date,
                    "expiry_date": expiry_date,
                    "valid_days": 365 * 10,
                }
            )

        if self.parameters.get("include_name", False):
            result["holder_name"] = holder_name

        return result

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证生成的护照数据

        Args:
            data: 护照号码字符串或包含完整信息的字典
        """
        # 类型检查
        if not isinstance(data, (str, dict)):
            return False

        # 如果是字符串，转换为dict格式进行验证
        if isinstance(data, str):
            data = {"passport_number": data}

        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["passport_type", "country_code", "include_dates", "include_name"]


@register_generator("generic_passport", aliases=["passport", "护照"])
class GenericPassportGenerator(DataGenerator[str]):
    """通用护照号码生成器(仅生成号码字符串)"""

    _passport_generator: PassportGenerator = field(init=False)

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        # 使用内部的PassportGenerator来生成核心数据
        passport_config = PassportGeneratorConfig(
            generator_type="passport_internal",
            parameters=self.parameters,
            passport_type=self.parameters.get("passport_type", "E"),
            country_code=self.parameters.get("country_code", "CHN"),
            include_dates=False,
            include_name=False,
        )
        self._passport_generator = PassportGenerator(passport_config)

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个护照号码字符串"""
        passport_type = self._passport_generator.config.passport_type
        return self._passport_generator._generate_passport_number(passport_type)

    def validate(self, data: str) -> bool:
        """验证护照号码字符串的格式"""
        return isinstance(data, str) and bool(re.match(r"^[A-Z][0-9]{7,9}$", data))

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["passport_type", "country_code"]
