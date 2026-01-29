"""
银行卡号生成器
"""

import re
import secrets

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
)
from ...core.luhn import calculate_luhn_check_digit, validate_luhn
from ...core.protocols import Validator
from ...core.types import GeneratorType

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


class BankCardValidator(Validator):
    """Validator for bank card numbers."""

    def __init__(self, bank_bins: dict, card_type_prefixes: dict):
        self.bank_bins = bank_bins
        self.card_type_prefixes = card_type_prefixes

    def validate(self, data: str, strict: bool = False) -> bool:
        """校验银行卡号

        Args:
            data: 银行卡号
            strict: 是否进行严格校验（包括BIN）
        """
        if not isinstance(data, str):
            return False

        # 移除格式字符（空白字符和连字符）
        clean_number = re.sub(r"[\s-]", "", data)

        # 检查是否为纯数字
        if not clean_number.isdigit():
            return False

        # 检查长度
        if len(clean_number) not in [13, 15, 16, 19]:
            return False

        # Luhn校验（所有模式都需要）
        if not self._validate_luhn(clean_number):
            return False

        # 严格模式下检查BIN号
        if strict:
            return self._is_valid_bin(clean_number)

        return True

    def _is_valid_bin(self, card_number: str) -> bool:
        """检查BIN号是否有效"""
        # 检查是否以有效的BIN号开头
        for bins in self.bank_bins.values():
            for bin_prefix in bins:
                if card_number.startswith(bin_prefix):
                    return True

        # 检查卡类型前缀
        for prefixes in self.card_type_prefixes.values():
            for prefix in prefixes:
                if card_number.startswith(prefix):
                    return True

        return False

    def _validate_luhn(self, card_number: str) -> bool:
        """验证Luhn算法"""
        return validate_luhn(card_number)

    @property
    def error_message(self) -> str:
        return "Invalid bank card number"


@register_generator("bankcard", aliases=["bank_card", "银行卡"])
class BankCardGenerator(DataGenerator[str]):
    """银行卡号生成器"""

    validator: BankCardValidator

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.card_type = self.parameters.get("card_type", None)
        self.bank_code = self.parameters.get("bank_code", None)
        self.format_with_spaces = self.parameters.get("format_with_spaces", False)
        self.format_with_dashes = self.parameters.get("format_with_dashes", False)

        # 银行卡BIN号映射（部分主要银行）
        self.bank_bins = {
            "ICBC": ["622202", "622208", "621226"],  # 工商银行
            "CCB": ["622700", "436742", "621700"],  # 建设银行
            "ABC": ["622848", "622845", "621336"],  # 农业银行
            "BOC": ["621661", "456351", "601382"],  # 中国银行
            "BOCOM": ["622260", "601428", "405512"],  # 交通银行
            "CMB": ["622588", "439225", "621483"],  # 招商银行
            "CMBC": ["622622", "421349", "621691"],  # 民生银行
            "CEB": ["622658", "622663", "621492"],  # 光大银行
            "CITIC": ["622690", "622689", "621771"],  # 中信银行
            "SPDB": ["622521", "622522", "621352"],  # 浦发银行
            "PAB": ["622525", "622526", "621626"],  # 平安银行
            "GDB": ["622556", "622559", "621462"],  # 广发银行
            "HXB": ["622630", "622631", "621222"],  # 华夏银行
            "PSBC": ["622188", "621098", "621797"],  # 邮储银行
        }

        # 卡类型对应的BIN号前缀
        self.card_type_prefixes = {
            "VISA": ["4"],
            "MASTERCARD": ["5"],
            "AMEX": ["34", "37"],
            "UNIONPAY": ["62", "88"],
            "DISCOVER": ["6011"],
        }
        self.validator = BankCardValidator(self.bank_bins, self.card_type_prefixes)

    def _setup(self) -> None:
        """初始化设置"""
        self.card_type = self.parameters.get("card_type", None)
        self.bank_code = self.parameters.get("bank_code", None)
        self.format_with_spaces = self.parameters.get("format_with_spaces", False)
        self.format_with_dashes = self.parameters.get("format_with_dashes", False)

    def generate(self, context: GenerationContext | None = None) -> str:
        """生成原始银行卡号"""
        # 获取BIN号
        bin_prefix = self._get_bin_prefix()

        # 计算剩余位数
        total_length = 16  # 标准银行卡号长度
        if bin_prefix.startswith("6") or bin_prefix.startswith("5"):
            total_length = 16
        elif bin_prefix.startswith("3"):
            total_length = 15  # 美国运通卡

        remaining_length = total_length - len(bin_prefix)

        # 生成随机数字
        random_digits = "".join(
            [str(secrets.randbelow(10)) for _ in range(remaining_length - 1)]
        )

        # 生成基础卡号（不含校验位）
        base_number = bin_prefix + random_digits

        # 计算并添加Luhn校验位
        check_digit = self._calculate_luhn_check_digit(base_number)
        card_number = base_number + str(check_digit)

        # 格式化输出
        return self._format_card_number(card_number)

    def _get_bin_prefix(self) -> str:
        """获取BIN号前缀"""
        if self.bank_code and self.bank_code in self.bank_bins:
            return secrets.choice(self.bank_bins[self.bank_code])

        if self.card_type and self.card_type.upper() in self.card_type_prefixes:
            prefixes = self.card_type_prefixes[self.card_type.upper()]
            return secrets.choice(prefixes)

        # 随机选择银行
        all_bins = []
        for bins in self.bank_bins.values():
            all_bins.extend(bins)

        if all_bins:
            return secrets.choice(all_bins)

        # 默认使用银联BIN号
        return "6222"

    def _calculate_luhn_checksum(self, number: str) -> int:
        """计算Luhn校验和"""

        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(number)
        odd_digits = digits[-1::-2]  # 从右数第1,3,5...位
        even_digits = digits[-2::-2]  # 从右数第2,4,6...位

        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))

        return checksum % 10

    def _calculate_luhn_check_digit(self, number: str) -> int:
        """计算Luhn校验位"""
        return calculate_luhn_check_digit(number)

    def _format_card_number(self, card_number: str) -> str:
        """格式化卡号"""
        if self.format_with_spaces:
            # 每4位添加空格
            return " ".join(
                [card_number[i : i + 4] for i in range(0, len(card_number), 4)]
            )
        elif self.format_with_dashes:
            # 每4位添加连字符
            return "-".join(
                [card_number[i : i + 4] for i in range(0, len(card_number), 4)]
            )
        else:
            return card_number

    def get_bank_info(self, card_number: str) -> dict:
        """获取银行卡信息"""
        clean_number = re.sub(r"[\s-]", "", card_number)

        bank_info = {
            "card_number": clean_number,
            "card_type": "未知",
            "bank_name": "未知",
            "is_valid": self.validator.validate(card_number),
        }

        if not bank_info["is_valid"]:
            return bank_info

        # 判断卡类型
        for card_type, prefixes in self.card_type_prefixes.items():
            for prefix in prefixes:
                if clean_number.startswith(prefix):
                    bank_info["card_type"] = card_type
                    break

        # 判断银行
        for bank_name, bins in self.bank_bins.items():
            for bin_prefix in bins:
                if clean_number.startswith(bin_prefix):
                    bank_info["bank_name"] = bank_name
                    break

        return bank_info

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
        return ["bank_code", "card_type", "format_with_dashes", "format_with_spaces"]

    def validate(self, data: str) -> bool:
        """验证生成的数据

        默认使用严格模式验证（包括Luhn校验）
        """
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            # 默认使用严格模式
            return self.validator.validate(data, strict=True)
        return True

    def _luhn_validate(self, card_number: str) -> bool:
        """Luhn算法验证（用于测试兼容性）"""
        if hasattr(self, "validator") and hasattr(self.validator, "_validate_luhn"):
            return self.validator._validate_luhn(card_number)
        return False


@register_generator("generic_bankcard", aliases=["通用银行卡", "银行卡通用"])
class GenericBankCardGenerator(BankCardGenerator):
    """通用银行卡号生成器注册版本"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        # TODO: 根据实际参数更新此列表
        return []

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return isinstance(data, str) and bool(data.strip())
