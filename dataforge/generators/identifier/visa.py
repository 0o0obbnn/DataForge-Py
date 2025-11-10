from ...core.types import GeneratorType

"""
签证号生成器

生成符合各国签证标准的签证号码
支持中国签证、美国签证、申根签证等多种类型
"""

import random  # TODO: Convert to secrets
import secrets
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Union

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
)
from ...core.protocols import Validator

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary



@dataclass
class VisaInfo:
    """签证信息数据模型"""
    visa_number: str
    visa_type: str
    country: str
    issue_date: str
    expiry_date: str
    duration_days: int
    entries: str  # 入境次数：单次/多次
    passport_number: str
    holder_name: str


class VisaValidator(Validator):
    """Validator for visa information."""

    def __init__(self, country_formats):
        self.country_formats = country_formats

    def validate(self, data: dict[str, str]) -> bool:
        """验证生成的签证信息"""
        # 如果只有visa_number，只验证号码格式
        if len(data) == 1 and "visa_number" in data:
            visa_number = data["visa_number"]
            # 基本格式检查：至少8位，包含字母或数字
            if not isinstance(visa_number, str) or len(visa_number) < 8:
                return False
            return bool(re.match(r'^[A-Z0-9]{8,}$', visa_number))
        
        # 完整验证
        required_fields = ["visa_number", "visa_type", "country", "issue_date", "expiry_date"]

        for field in required_fields:
            if field not in data:
                return False

        # 验证签证号码格式
        country = data.get("country", "CN")
        if country in self.country_formats:
            pattern = self.country_formats[country]["pattern"]
            if not re.match(pattern, data["visa_number"]):
                return False

        # 验证日期格式
        try:
            issue_date = datetime.strptime(data["issue_date"], "%Y-%m-%d")
            expiry_date = datetime.strptime(data["expiry_date"], "%Y-%m-%d")

            if expiry_date <= issue_date:
                return False

        except ValueError:
            return False

        return True

    @property
    def error_message(self) -> str:
        return "Invalid visa information format"


class VisaGenerator(DataGenerator[dict[str, str]]):
    """签证号生成器

    功能特性：
    - 支持多种签证类型：旅游、商务、学生、工作等
    - 支持中国、美国、申根等主要国家签证格式
    - 生成符合各国签证标准的号码和有效期
    - 包含完整的签证信息
    """

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.visa_type = self.parameters.get("visa_type", "tourist").lower()
        self.country = self.parameters.get("country", "CN").upper()
        self.duration_days = self.parameters.get("duration_days", 30)
        self.entries = self.parameters.get("entries", "single").lower()
        self.include_passport = self.parameters.get("include_passport", True)

        # 国家签证格式配置
        self.country_formats = {
            "CN": {  # 中国签证
                "prefix": "",
                "length": 9,
                "pattern": r"^\d{9}$",
                "format": "数字9位",
                "issue_authority": "中国出入境管理局"
            },
            "US": {  # 美国签证
                "prefix": "",
                "length": 8,
                "pattern": r"^[A-Z0-9]{8}$",
                "format": "字母数字8位",
                "issue_authority": "美国国务院"
            },
            "UK": {  # 英国签证
                "prefix": "",
                "length": 9,
                "pattern": r"^[A-Z0-9]{9}$",
                "format": "字母数字9位",
                "issue_authority": "英国内政部"
            },
            "DE": {  # 德国签证（申根）
                "prefix": "",
                "length": 12,
                "pattern": r"^[A-Z0-9]{12}$",
                "format": "字母数字12位",
                "issue_authority": "德国联邦外交部"
            },
            "FR": {  # 法国签证（申根）
                "prefix": "",
                "length": 12,
                "pattern": r"^[A-Z0-9]{12}$",
                "format": "字母数字12位",
                "issue_authority": "法国外交部"
            },
            "CA": {  # 加拿大签证
                "prefix": "",
                "length": 10,
                "pattern": r"^[A-Z0-9]{10}$",
                "format": "字母数字10位",
                "issue_authority": "加拿大移民部"
            },
            "AU": {  # 澳大利亚签证
                "prefix": "",
                "length": 11,
                "pattern": r"^[A-Z0-9]{11}$",
                "format": "字母数字11位",
                "issue_authority": "澳大利亚内政部"
            },
            "JP": {  # 日本签证
                "prefix": "",
                "length": 9,
                "pattern": r"^\d{9}$",
                "format": "数字9位",
                "issue_authority": "日本外务省"
            }
        }
        self.validator = VisaValidator(self.country_formats)

        # 签证类型映射
        self.visa_types = {
            "tourist": "旅游签证",
            "business": "商务签证",
            "student": "学生签证",
            "work": "工作签证",
            "transit": "过境签证",
            "family": "探亲签证",
            "medical": "医疗签证"
        }

        # 常见中文姓名
        self.chinese_first_names = [
            "张伟", "王芳", "李娜", "刘洋", "陈静", "杨明", "黄丽", "赵强", "吴敏", "周杰",
            "徐婷", "孙浩", "朱琳", "高鹏", "林燕", "何斌", "郭静", "马涛", "罗丹", "梁超"
        ]

        # 常见英文姓名
        self.english_names = [
            "John Smith", "Emma Johnson", "Michael Brown", "Sarah Davis", "David Wilson",
            "Lisa Anderson", "James Taylor", "Jennifer Martinez", "Robert Thomas", "Maria Garcia",
            "William Lee", "Jessica White", "Daniel Clark", "Amanda Rodriguez", "Christopher Lewis"
        ]

    def _setup(self) -> None:
        """初始化签证生成器参数"""
        self.visa_type = self.parameters.get("visa_type", "tourist").lower()
        self.country = self.parameters.get("country", "CN").upper()
        self.duration_days = self.parameters.get("duration_days", 30)
        self.entries = self.parameters.get("entries", "single").lower()
        self.include_passport = self.parameters.get("include_passport", True)

    def _generate_visa_number(self, country: str) -> str:
        """生成符合指定国家格式的签证号码"""
        if country not in self.country_formats:
            country = "CN"

        format_config = self.country_formats[country]
        length = format_config["length"]

        if country == "CN":
            # 中国签证：纯数字9位
            return ''.join([str(secrets.randbelow(10)) for _ in range(length)])
        elif country == "US":
            # 美国签证：字母数字8位
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            return ''.join([secrets.choice(chars) for _ in range(length)])
        elif country in ["DE", "FR"]:  # 申根签证
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            return ''.join([secrets.choice(chars) for _ in range(length)])
        elif country in ["UK", "CA", "AU", "JP"]:
            # 其他格式
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            return ''.join([secrets.choice(chars) for _ in range(length)])
        else:
            # 默认格式
            chars = "0123456789"
            return ''.join([secrets.choice(chars) for _ in range(length)])

    def _generate_passport_number(self) -> str:
        """生成护照号码"""
        # 中国护照格式：E+8位数字
        return f"E{secrets.randbelow(90000000) + 10000000}"

    def _generate_holder_name(self, country: str) -> str:
        """生成持有人姓名"""
        if country == "CN":
            return secrets.choice(self.chinese_first_names)
        else:
            return secrets.choice(self.english_names)

    def _generate_issue_date(self) -> str:
        """生成签发日期"""
        # 生成过去1年内的随机日期
        days_ago = secrets.randbelow(365) + 1
        issue_date = datetime.now() - timedelta(days=days_ago)
        return issue_date.strftime("%Y-%m-%d")

    def _generate_expiry_date(self, issue_date: str, duration_days: int) -> str:
        """根据签发日期和停留天数计算有效期"""
        issue_dt = datetime.strptime(issue_date, "%Y-%m-%d")

        # 根据签证类型和国家调整有效期
        if self.country in ["US", "UK", "CA", "AU"]:
            # 这些国家通常给较长的有效期
            if self.visa_type == "tourist":
                validity_days = max(duration_days * 2, 180)  # 至少6个月
            elif self.visa_type == "business":
                validity_days = max(duration_days * 3, 365)  # 至少1年
            elif self.visa_type == "student":
                validity_days = max(duration_days * 4, 730)  # 至少2年
            else:
                validity_days = max(duration_days * 2, 180)
        else:
            # 其他国家按停留天数计算
            validity_days = duration_days + 30  # 额外30天缓冲

        expiry_date = issue_dt + timedelta(days=validity_days)
        return expiry_date.strftime("%Y-%m-%d")

    def _generate_entries(self) -> str:
        """生成入境次数"""
        if self.entries == "multiple":
            return "多次入境"
        else:
            return "单次入境"

    def generate(self, context: Optional[GenerationContext] = None) -> Union[str, dict[str, str]]:
        """生成签证信息
        
        Returns:
            如果string_only=True，返回签证号码字符串
            否则返回包含完整信息的字典
        """
        # 验证国家代码
        if self.country not in self.country_formats:
            self.country = "CN"

        # 验证停留天数
        valid_durations = [30, 60, 90, 180, 365]
        if self.duration_days not in valid_durations:
            self.duration_days = min(valid_durations, key=lambda x: abs(x - self.duration_days))

        # 生成签证号码
        visa_number = self._generate_visa_number(self.country)

        # 如果只需要字符串，直接返回
        if self.parameters.get('string_only', False):
            return visa_number

        # 生成签发日期和有效期
        issue_date = self._generate_issue_date()
        expiry_date = self._generate_expiry_date(issue_date, self.duration_days)

        # 生成持有人信息
        holder_name = self._generate_holder_name(self.country)
        passport_number = self._generate_passport_number() if self.include_passport else ""

        result = {
            "visa_number": visa_number,
            "visa_type": self.visa_types[self.visa_type],
            "country": self.country,
            "issue_date": issue_date,
            "expiry_date": expiry_date,
            "duration_days": str(self.duration_days),
            "entries": self._generate_entries(),
            "issue_authority": self.country_formats[self.country]["issue_authority"],
            "holder_name": holder_name,
        }

        if self.include_passport:
            result["passport_number"] = passport_number

        return result

    def generate_single(self, context: Optional[GenerationContext] = None) -> Union[str, dict[str, str]]:
        """生成单个数据项
        
        默认返回签证号码字符串，除非明确设置string_only=False
        """
        # 如果没有明确设置string_only，默认为True（返回字符串）
        if 'string_only' not in self.parameters:
            self.parameters['string_only'] = True
        
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["country", "duration_days", "entries", "include_passport", "visa_type"]

    def validate(self, data: Union[str, dict[str, str]]) -> bool:
        """验证生成的数据
        
        Args:
            data: 签证号码字符串或包含完整信息的字典
        """
        # 类型检查
        if not isinstance(data, (str, dict)):
            return False
            
        # 如果是字符串，转换为dict格式进行验证
        if isinstance(data, str):
            data = {"visa_number": data}
        
        if hasattr(self, 'validator') and hasattr(self.validator, 'validate'):
            return self.validator.validate(data)
        return True



@register_generator("generic_visa", aliases=["visa", "签证"])
class GenericVisaGenerator(VisaGenerator):
    """通用签证号生成器注册版本"""
    pass
