"""
统一社会信用代码生成器
"""

import random  # Keep for random.choices
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


class USCCValidator(Validator):
    """Validator for Chinese Unified Social Credit Code."""

    def __init__(self):
        self.check_code_chars = "0123456789ABCDEFGHJKLMNPQRTUWXY"
        self.weight_factors = [
            1,
            3,
            9,
            27,
            19,
            26,
            16,
            17,
            20,
            29,
            25,
            13,
            8,
            24,
            10,
            30,
            28,
        ]
        self.registration_departments = {
            "1": "机构编制",
            "5": "民政",
            "9": "工商",
            "Y": "其他",
        }
        self.organization_types = {
            "1": "企业",
            "2": "个体工商户",
            "3": "农民专业合作社",
            "9": "其他",
        }

    def validate(self, data: str) -> bool:
        """校验统一社会信用代码"""
        if not isinstance(data, str) or len(data) != 18:
            return False

        # 检查字符是否都在允许的字符集中
        for char in data:
            if char not in self.check_code_chars:
                return False

        # 检查登记管理部门码
        if data[0] not in self.registration_departments:
            return False

        # 检查机构类别码
        if data[1] not in self.organization_types:
            return False

        # 检查行政区划码（前6位数字）
        region_code = data[2:8]
        if not region_code.isdigit():
            return False

        # 校验码验证
        code_without_check = data[:17]
        expected_check = self._calculate_check_code(code_without_check)
        return data[17] == expected_check

    def _calculate_check_code(self, code_17: str) -> str:
        """计算校验码 (GB32100-2015标准)"""
        if len(code_17) != 17:
            raise ValueError("代码长度必须为17位")

        # 将字符转换为数值
        total = 0
        for i, char in enumerate(code_17):
            try:
                char_value = self.check_code_chars.index(char)
            except ValueError as err:
                # Should be caught by the main validate method, but as a safeguard:
                raise ValueError(f"Invalid character '{char}' in USCC code.") from err

            total += char_value * self.weight_factors[i]

        # 计算校验码
        remainder = total % 31
        check_index = (31 - remainder) % 31
        return self.check_code_chars[check_index]

    @property
    def error_message(self) -> str:
        return "Invalid USCC format"


class USCCGenerator(DataGenerator[str]):
    """统一社会信用代码生成器 (GB32100-2015标准)"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.region = self.parameters.get("region", None)  # 行政区划码
        self.valid = self.parameters.get("valid", True)  # 是否保证生成有效代码
        self.validator = USCCValidator()

        # For generation, we use the validator's configs
        self.registration_departments = self.validator.registration_departments
        self.organization_types = self.validator.organization_types
        self.check_code_chars = self.validator.check_code_chars

        # 常用行政区划码（部分）
        self.regions = {
            "110000": "北京市",
            "120000": "天津市",
            "130000": "河北省",
            "140000": "山西省",
            "150000": "内蒙古自治区",
            "210000": "辽宁省",
            "220000": "吉林省",
            "230000": "黑龙江省",
            "310000": "上海市",
            "320000": "江苏省",
            "330000": "浙江省",
            "340000": "安徽省",
            "350000": "福建省",
            "360000": "江西省",
            "370000": "山东省",
            "410000": "河南省",
            "420000": "湖北省",
            "430000": "湖南省",
            "440000": "广东省",
            "450000": "广西壮族自治区",
            "460000": "海南省",
            "500000": "重庆市",
            "510000": "四川省",
            "520000": "贵州省",
            "530000": "云南省",
            "540000": "西藏自治区",
            "610000": "陕西省",
            "620000": "甘肃省",
            "630000": "青海省",
            "640000": "宁夏回族自治区",
            "650000": "新疆维吾尔自治区",
        }

    def _setup(self) -> None:
        self.region = self.parameters.get("region", None)
        self.valid = self.parameters.get("valid", True)

    def generate(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始统一社会信用代码"""
        # 1. 登记管理部门码 (1位)
        dept_code = secrets.choice(list(self.registration_departments.keys()))

        # 2. 机构类别码 (1位)
        org_type = secrets.choice(list(self.organization_types.keys()))

        # 3. 行政区划码 (6位)
        if self.region and self.region in self.regions:
            region_code = self.region
        else:
            region_code = secrets.choice(list(self.regions.keys()))

        # 4. 主体标识码 (9位) - 随机生成
        entity_id = self._generate_entity_id()

        # 5. 校验码 (1位)
        code_without_check = dept_code + org_type + region_code + entity_id

        if self.valid:
            check_code = self.validator._calculate_check_code(code_without_check)
        else:
            # 生成错误的校验码
            correct_check = self.validator._calculate_check_code(code_without_check)
            possible_wrong_codes = [c for c in self.check_code_chars if c != correct_check]
            check_code = secrets.choice(possible_wrong_codes)

        return code_without_check + check_code

    def _generate_entity_id(self) -> str:
        """生成主体标识码 (9位)"""
        # 使用数字和字母（除I、O、S、V、Z）
        return "".join(random.choices(self.check_code_chars, k=9))

    def get_uscc_info(self, uscc: str) -> dict:
        """解析统一社会信用代码信息"""
        if not self.validator.validate(uscc):
            return {"valid": False, "error": self.validator.error_message}

        result = {
            "valid": True,
            "uscc": uscc,
            "registration_dept_code": uscc[0],
            "registration_dept_name": self.registration_departments.get(uscc[0], "未知"),
            "organization_type_code": uscc[1],
            "organization_type_name": self.organization_types.get(uscc[1], "未知"),
            "region_code": uscc[2:8],
            "region_name": self.regions.get(uscc[2:8], "未知地区"),
            "entity_id": uscc[8:17],
            "check_code": uscc[17],
        }

        return result

    def generate_with_info(self, context: Optional[GenerationContext] = None) -> dict:
        """生成统一社会信用代码并返回详细信息"""
        uscc = self.generate(context)
        return self.get_uscc_info(uscc)

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
        return ["region", "valid"]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, 'validator') and hasattr(self.validator, 'validate'):
            return self.validator.validate(data)
        return True



@register_generator("chinese_uscc", aliases=["统一社会信用代码", "uscc"])
class ChineseUSCCGenerator(USCCGenerator):
    """中国统一社会信用代码生成器注册版本"""

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
        # TODO: 根据实际参数更新此列表
        return []

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        return super().validate(data)
