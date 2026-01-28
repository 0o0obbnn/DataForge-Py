"""
LEI码生成器 (Legal Entity Identifier)
"""

import random  # Keep for random.choices
import secrets

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
)
from ...core.protocols import Validator
from ...core.types import GeneratorType


class LEIValidator(Validator):
    """Validator for LEI codes."""

    def __init__(self, lei_chars: str):
        self.lei_chars = lei_chars

    def validate(self, data: str) -> bool:
        """校验LEI码"""
        if not isinstance(data, str) or len(data) != 20:
            return False

        # 检查字符格式
        # 前18位应该是数字和字母（不包含0、1、I、O）
        for i, char in enumerate(data[:18]):
            if i < 6:  # 前6位（LOU ID + 保留位）应该是数字
                if not char.isdigit():
                    return False
            else:  # 后12位（实体代码）应该是允许的字符
                if char not in self.lei_chars:
                    return False

        # 最后2位应该是数字
        if not data[18:20].isdigit():
            return False

        # 校验位验证
        code_without_check = data[:18]
        expected_check = self._calculate_check_digits(code_without_check)
        return data[18:20] == expected_check

    def _calculate_check_digits(self, code_18: str) -> str:
        """计算LEI码校验位 (ISO 17442标准 - MOD 97算法)"""
        if len(code_18) != 18:
            raise ValueError("代码长度必须为18位")

        # 将字母转换为数字
        numeric_string = ""
        for char in code_18:
            if char.isdigit():
                numeric_string += char
            else:
                # A=10, B=11, ..., Z=35
                numeric_string += str(ord(char) - ord("A") + 10)

        # 添加两个0用于校验计算
        numeric_string += "00"

        # 使用MOD 97算法计算校验位
        remainder = int(numeric_string) % 97
        check_digits = 98 - remainder

        return f"{check_digits:02d}"

    @property
    def error_message(self) -> str:
        return "Invalid LEI code format"


class LEIGenerator(DataGenerator[str]):
    """LEI码生成器 (ISO 17442标准)"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.valid = self.parameters.get("valid", True)  # 是否保证生成有效LEI码

        # LEI码字符集（不包含0、1、I、O）
        self.lei_chars = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
        self.validator = LEIValidator(self.lei_chars)

        # 常用LOU ID（Local Operating Unit）
        self.lou_ids = [
            "5493",  # GLEIF
            "9845",  # 中国LOU
            "2138",  # 美国LOU
            "2549",  # 英国LOU
            "3912",  # 德国LOU
            "7245",  # 日本LOU
            "8156",  # 法国LOU
            "6734",  # 澳大利亚LOU
            "4821",  # 加拿大LOU
            "5067",  # 新加坡LOU
        ]

        # 保留位（通常为00）
        self.reserved_digits = "00"

    def _setup(self) -> None:
        self.valid = self.parameters.get("valid", True)  # 是否保证生成有效LEI码

    def generate(self, context: GenerationContext | None = None) -> str:
        """生成原始LEI码"""
        # 1. LOU ID (4位)
        lou_id = secrets.choice(self.lou_ids)

        # 2. 保留位 (2位)
        reserved = self.reserved_digits

        # 3. 实体特定代码 (12位)
        entity_code = "".join(random.choices(self.lei_chars, k=12))

        # 4. 校验位 (2位)
        code_without_check = lou_id + reserved + entity_code

        if self.valid:
            check_digits = self._calculate_check_digits(code_without_check)
        else:
            # 生成错误的校验位
            check_digits = "".join(random.choices("0123456789", k=2))
            # 确保不是正确的校验位
            correct_check = self._calculate_check_digits(code_without_check)
            while check_digits == correct_check:
                check_digits = "".join(random.choices("0123456789", k=2))

        return code_without_check + check_digits

    def _calculate_check_digits(self, code_18: str) -> str:
        """计算LEI码校验位 (ISO 17442标准 - MOD 97算法)"""
        if len(code_18) != 18:
            raise ValueError("代码长度必须为18位")

        # 将字母转换为数字
        numeric_string = ""
        for char in code_18:
            if char.isdigit():
                numeric_string += char
            else:
                # A=10, B=11, ..., Z=35
                numeric_string += str(ord(char) - ord("A") + 10)

        # 添加两个0用于校验计算
        numeric_string += "00"

        # 使用MOD 97算法计算校验位
        remainder = int(numeric_string) % 97
        check_digits = 98 - remainder

        return f"{check_digits:02d}"

    def get_lei_info(self, lei: str) -> dict:
        """解析LEI码信息"""
        if not self.validator.validate(lei):
            return {"valid": False, "error": "无效的LEI码"}

        result = {
            "valid": True,
            "lei": lei,
            "lou_id": lei[:4],
            "reserved_digits": lei[4:6],
            "entity_code": lei[6:18],
            "check_digits": lei[18:20],
            "formatted": f"{lei[:4]}-{lei[4:6]}-{lei[6:18]}-{lei[18:20]}",
        }

        # 根据LOU ID推测发行机构
        lou_mapping = {
            "5493": "GLEIF",
            "9845": "中国LOU",
            "2138": "美国LOU",
            "2549": "英国LOU",
            "3912": "德国LOU",
            "7245": "日本LOU",
            "8156": "法国LOU",
            "6734": "澳大利亚LOU",
            "4821": "加拿大LOU",
            "5067": "新加坡LOU",
        }

        result["lou_name"] = lou_mapping.get(lei[:4], "未知LOU")

        return result

    def format_lei(self, lei: str) -> str:
        """格式化LEI码（添加连字符）"""
        if len(lei) == 20:
            return f"{lei[:4]}-{lei[4:6]}-{lei[6:18]}-{lei[18:20]}"
        return lei

    def generate_with_info(self, context: GenerationContext | None = None) -> dict:
        """生成LEI码并返回详细信息"""
        lei = self.generate(context)
        return self.get_lei_info(lei)

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


@register_generator("lei_code", aliases=["lei", "LEI"])
class LEICodeGenerator(LEIGenerator):
    """LEI码生成器注册版本"""

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
        return isinstance(data, str) and bool(data.strip())
