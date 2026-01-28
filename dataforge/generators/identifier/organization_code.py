"""
组织机构代码生成器 (历史数据支持)
"""

import secrets

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
)
from ...core.protocols import Validator
from ...core.types import GeneratorType


class OrganizationCodeValidator(Validator):
    """Validator for Chinese organization codes."""

    def __init__(
        self, code_chars: str, weight_factors: list[int], check_codes: dict[int, str]
    ):
        self.code_chars = code_chars
        self.weight_factors = weight_factors
        self.check_codes = check_codes

    def validate(self, data: str) -> bool:
        """校验组织机构代码"""
        if not isinstance(data, str):
            return False

        # 去除可能的分隔符
        clean_code = data.replace("-", "").replace(" ", "")

        # 检查长度
        if len(clean_code) != 9:
            return False

        # 分离主体代码和校验位
        main_code = clean_code[:8]
        check_digit = clean_code[8]

        # 检查字符是否合法
        for char in main_code:
            if char not in self.code_chars:
                return False

        if check_digit not in "0123456789X":
            return False

        # 计算校验位
        expected_check = self._calculate_check_digit(main_code)
        return check_digit.upper() == expected_check.upper()

    def _calculate_check_digit(self, main_code: str) -> str:
        """计算校验位 (GB 11714-1997标准)"""
        if len(main_code) != 8:
            raise ValueError("主体代码长度必须为8位")

        # 计算加权和
        total = 0
        for i, char in enumerate(main_code):
            # 将字符转换为数值
            if char.isdigit():
                char_value = int(char)
            else:
                # 字母转换：A=10, B=11, ..., Z=35
                char_value = ord(char.upper()) - ord("A") + 10

            total += char_value * self.weight_factors[i]

        # 计算校验位
        remainder = total % 11
        return self.check_codes[remainder]

    @property
    def error_message(self) -> str:
        return "Invalid Chinese organization code format"


class OrganizationCodeGenerator(DataGenerator[str]):
    """组织机构代码生成器 (GB 11714-1997标准)"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.valid = self.parameters.get("valid", True)  # 是否保证生成有效代码

        # 校验码权重因子 (GB 11714-1997)
        self.weight_factors = [3, 7, 9, 10, 5, 8, 4, 2]

        # 校验码映射表
        self.check_codes = {
            0: "1",
            1: "2",
            2: "3",
            3: "4",
            4: "5",
            5: "6",
            6: "7",
            7: "8",
            8: "9",
            9: "X",
            10: "0",
        }

        # 代码字符集（数字和字母）
        self.code_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.validator = OrganizationCodeValidator(
            self.code_chars, self.weight_factors, self.check_codes
        )

    def _setup(self) -> None:
        self.valid = self.parameters.get("valid", True)  # 是否保证生成有效代码

    def generate(self, context: GenerationContext | None = None) -> str:
        """生成原始组织机构代码"""
        # 生成8位主体代码
        main_code = self._generate_main_code()

        # 计算校验位
        if self.valid:
            check_digit = self._calculate_check_digit(main_code)
        else:
            # 生成错误的校验位
            wrong_checks = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "X"]
            correct_check = self._calculate_check_digit(main_code)
            wrong_checks.remove(correct_check)
            check_digit = secrets.choice(wrong_checks)

        return main_code + "-" + check_digit

    def _generate_main_code(self) -> str:
        """生成8位主体代码"""
        # 根据GB 11714-1997标准，组织机构代码的前8位通常都是数字
        # 生成8位数字主体代码
        return "".join(secrets.choice("0123456789") for _ in range(8))

    def _calculate_check_digit(self, main_code: str) -> str:
        """计算校验位 (GB 11714-1997标准)"""
        if len(main_code) != 8:
            raise ValueError("主体代码长度必须为8位")

        # 计算加权和
        total = 0
        for i, char in enumerate(main_code):
            # 将字符转换为数值
            if char.isdigit():
                char_value = int(char)
            else:
                # 字母转换：A=10, B=11, ..., Z=35
                char_value = ord(char.upper()) - ord("A") + 10

            total += char_value * self.weight_factors[i]

        # 计算校验位
        remainder = total % 11
        return self.check_codes[remainder]

    def get_org_code_info(self, org_code: str) -> dict:
        """解析组织机构代码信息"""
        # 清理输入
        clean_code = org_code.replace("-", "").replace(" ", "")

        if not self.validator.validate(org_code):
            return {"valid": False, "error": "无效的组织机构代码"}

        result = {
            "valid": True,
            "original": org_code,
            "clean_code": clean_code,
            "formatted_code": f"{clean_code[:8]}-{clean_code[8]}",
            "main_code": clean_code[:8],
            "check_digit": clean_code[8],
            "region_or_industry_code": clean_code[:2],
            "sequence_code": clean_code[2:8],
        }

        return result

    def format_code(self, code: str) -> str:
        """格式化组织机构代码（添加连字符）"""
        clean_code = code.replace("-", "").replace(" ", "")
        if len(clean_code) == 9:
            return f"{clean_code[:8]}-{clean_code[8]}"
        return code

    def generate_with_info(self, context: GenerationContext | None = None) -> dict:
        """生成组织机构代码并返回详细信息"""
        org_code = self.generate(context)
        return self.get_org_code_info(org_code)

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["valid"]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


@register_generator("chinese_organization_code", aliases=["组织机构代码", "org_code"])
class ChineseOrganizationCodeGenerator(OrganizationCodeGenerator):
    """中国组织机构代码生成器注册版本"""

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["valid"]
