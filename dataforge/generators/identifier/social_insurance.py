from ...core.types import GeneratorType

"""社保/医保号生成器"""

import random  # TODO: Convert to secrets
import secrets
from typing import Optional

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



class SocialInsuranceNumberValidator(Validator):
    """Validator for social insurance numbers."""

    def __init__(self):
        self.weights = [3, 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        self.check_map = {
            0: "1",
            1: "0",
            2: "X",
            3: "9",
            4: "8",
            5: "7",
            6: "6",
            7: "5",
            8: "4",
            9: "3",
            10: "2",
        }

    def validate(self, data: str) -> bool:
        """校验社保/医保号"""
        if not isinstance(data, str):
            return False

        # 清理格式字符
        clean_data = data.replace("-", "").replace(" ", "")

        # 检查长度
        if len(clean_data) != 15:
            return False

        # 检查是否全为数字（除校验位可能是X）
        if not clean_data[:14].isdigit():
            return False

        # 检查校验位
        expected_check = self._generate_check_digit(clean_data[:14])
        actual_check = clean_data[14:]

        return expected_check == actual_check

    def _generate_check_digit(self, number: str) -> str:
        """生成校验位（模11算法）"""
        if len(number) != 14:  # 6位区划 + 8位顺序号
            # 如果长度不足，填充到14位
            number = number.ljust(14, "0")

        total = 0
        for i, digit in enumerate(number):
            if i < len(self.weights):
                total += int(digit) * self.weights[i]

        remainder = total % 11

        return self.check_map.get(remainder, "X")

    @property
    def error_message(self) -> str:
        return "Invalid social insurance number format"


class SocialInsuranceNumberGenerator(DataGenerator[str]):
    """社保号生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.region_code = self.parameters.get("region_code", None)  # 行政区划代码
        self.insurance_type = self.parameters.get(
            "type", "SOCIAL"
        )  # 保险类型: SOCIAL, MEDICAL
        self.valid = self.parameters.get("valid", True)  # 是否生成有效号码
        self.format_style = self.parameters.get(
            "format", "STANDARD"
        )  # 格式: STANDARD, NO_SEPARATOR
        self.validator = SocialInsuranceNumberValidator()

        # 默认行政区划代码（示例）
        self.default_regions = [
            "110000",  # 北京市
            "310000",  # 上海市
            "440100",  # 广州市
            "440300",  # 深圳市
            "330100",  # 杭州市
            "320100",  # 南京市
        ]

    def _setup(self) -> None:
        self.region_code = self.parameters.get("region_code", None)  # 行政区划代码
        self.insurance_type = self.parameters.get(
            "type", "SOCIAL"
        )  # 保险类型: SOCIAL, MEDICAL
        self.valid = self.parameters.get("valid", True)  # 是否生成有效号码
        self.format_style = self.parameters.get(
            "format", "STANDARD"
        )  # 格式: STANDARD, NO_SEPARATOR
        self.country = self.parameters.get("country", "china").lower()  # 国家: china, usa

    def generate(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始社保/医保号"""
        # 根据国家生成不同格式
        if self.country == "usa":
            return self._generate_us_ssn()
        
        # 默认生成中国社保号
        if not self.valid:
            return self._generate_invalid_number()

        # 1. 选择行政区划代码
        region = self._select_region_code()

        # 2. 生成顺序号（8位数字）
        sequence = "".join([str(secrets.randbelow(10)) for _ in range(8)])

        # 3. 生成校验位
        check_digit = self.validator._generate_check_digit(region + sequence)

        social_insurance_number = region + sequence + check_digit

        # 格式化输出
        return self._format_number(social_insurance_number)

    def _generate_us_ssn(self) -> str:
        """生成美国社会安全号码 (SSN)
        
        格式: XXX-XX-XXXX
        - 前3位: Area Number (001-899, 不包括666)
        - 中2位: Group Number (01-99)
        - 后4位: Serial Number (0001-9999)
        """
        # 生成Area Number (001-899, 排除666)
        area = secrets.randbelow(899) + 1
        while area == 666:
            area = secrets.randbelow(899) + 1
        
        # 生成Group Number (01-99)
        group = secrets.randbelow(99) + 1
        
        # 生成Serial Number (0001-9999)
        serial = secrets.randbelow(9999) + 1
        
        # 格式化
        if self.format_style.upper() == "NO_SEPARATOR":
            return f"{area:03d}{group:02d}{serial:04d}"
        else:
            return f"{area:03d}-{group:02d}-{serial:04d}"
    
    def _select_region_code(self) -> str:
        """选择行政区划代码"""
        if self.region_code:
            return str(self.region_code).zfill(6)
        return secrets.choice(self.default_regions)

    def _format_number(self, number: str) -> str:
        """格式化社保/医保号"""
        if self.format_style.upper() == "NO_SEPARATOR":
            return number

        # 标准格式：6-8-1（区划-顺序号-校验位）
        if len(number) == 15:
            return f"{number[:6]}-{number[6:14]}-{number[14:]}"
        return number

    def _generate_invalid_number(self) -> str:
        """生成无效社保/医保号"""
        invalid_type = secrets.choice(
            ["wrong_length", "wrong_region", "wrong_check_digit", "wrong_format"]
        )

        if invalid_type == "wrong_length":
            # 错误长度
            wrong_length = secrets.choice([10, 12, 13, 16])
            return "".join([str(secrets.randbelow(10)) for _ in range(wrong_length)])
        elif invalid_type == "wrong_region":
            # 错误行政区划代码
            region = "".join([str(secrets.randbelow(10)) for _ in range(6)])
            sequence = "".join([str(secrets.randbelow(10)) for _ in range(8)])
            return region + sequence + str(secrets.randbelow(10))
        elif invalid_type == "wrong_check_digit":
            # 错误校验位
            region = self._select_region_code()
            sequence = "".join([str(secrets.randbelow(10)) for _ in range(8)])
            # 故意生成错误的校验位
            wrong_check = str(secrets.randbelow(10))
            return region + sequence + wrong_check
        else:  # wrong_format
            # 包含字母或特殊字符
            return "".join([secrets.choice("0123456789ABCDEF-() ") for _ in range(15)])

    def extract_region_info(self, number: str) -> dict[str, str]:
        """从社保号中提取地区信息"""
        if not self.validator.validate(number):
            return {
                "region_code": "UNKNOWN",
                "region_name": "未知地区",
                "insurance_type": "INVALID",
            }

        clean_number = number.replace("-", "").replace(" ", "")
        region_code = clean_number[:6]

        # 简单的地区代码映射（示例）
        region_map = {
            "110000": "北京市",
            "310000": "上海市",
            "440100": "广州市",
            "440300": "深圳市",
            "330100": "杭州市",
            "320100": "南京市",
        }

        region_name = region_map.get(region_code, "未知地区")

        return {
            "region_code": region_code,
            "region_name": region_name,
            "insurance_type": self.insurance_type,
        }

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["format", "region_code", "type", "valid"]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, 'validator') and hasattr(self.validator, 'validate'):
            return self.validator.validate(data)
        return True



@register_generator("chinese_social_insurance", aliases=["社保号", "医保号", "social_insurance"])
class ChineseSocialInsuranceGenerator(SocialInsuranceNumberGenerator):
    """中国社保/医保号生成器注册版本"""

    pass


# 添加别名以支持测试导入
SocialInsuranceGenerator = SocialInsuranceNumberGenerator
