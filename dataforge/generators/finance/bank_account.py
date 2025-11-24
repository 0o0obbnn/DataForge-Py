"""银行账号生成器

支持生成符合各银行规则的银行账号
"""

import secrets
from typing import Optional

from ...core.factory import register_generator
from ...core.generator import (  # WARNING: This file uses random.randint/randrange/normalvariate that needs manual review; Conversion patterns:; secrets.randbelow(b - a + 1) + a → secrets.randbelow(b - a + 1) + a; random.randrange(n) → secrets.randbelow(n); For statistical distributions, consider if CSPRNG is necessary
    DataGenerator,
    GenerationContext,
)
from ...core.types import GeneratorType


@register_generator("bank_account", aliases=["account", "bank_account_number"])
class BankAccountGenerator(DataGenerator[str]):
    """银行账号生成器"""

    def _setup(self) -> None:
        """初始化银行账号生成器参数"""
        # 初始化银行映射表
        self._init_bank_mappings()

        # 银行名称映射，支持中英文别名
        self.bank_name = self._normalize_bank_name(
            self.parameters.get("bank", "工商银行")
        )
        self.account_type = self.parameters.get(
            "account_type", "SAVINGS"
        )  # SAVINGS, CHECKING, CREDIT
        self.include_bank_name = self.parameters.get("include_bank_name", False)
        self.format = self.parameters.get("format", "ACCOUNT")  # ACCOUNT, FULL

    def _init_bank_mappings(self) -> None:
        """初始化银行映射表"""
        # 中国主要银行及账号规则
        self.china_banks = {
            "工商银行": {"prefix": "6222", "account_length": 19},
            "农业银行": {"prefix": "6228", "account_length": 19},
            "中国银行": {"prefix": "6216", "account_length": 19},
            "建设银行": {"prefix": "6227", "account_length": 19},
            "交通银行": {"prefix": "6222", "account_length": 19},
            "招商银行": {"prefix": "6225", "account_length": 16},
            "浦发银行": {"prefix": "6225", "account_length": 16},
            "中信银行": {"prefix": "6226", "account_length": 16},
            "光大银行": {"prefix": "6226", "account_length": 16},
            "民生银行": {"prefix": "6226", "account_length": 16},
            "平安银行": {"prefix": "6225", "account_length": 16},
            "兴业银行": {"prefix": "6229", "account_length": 16},
            "广发银行": {"prefix": "6225", "account_length": 16},
        }

        # 美国主要银行及账号规则
        self.us_banks = {
            "JPMorgan Chase": {
                "routing_number": "021000021",
                "account_length": [10, 12, 17],
            },
            "Bank of America": {
                "routing_number": "026009593",
                "account_length": [10, 12],
            },
            "Wells Fargo": {"routing_number": "121000248", "account_length": [10, 13]},
            "Citibank": {"routing_number": "021000089", "account_length": [10, 16]},
            "Goldman Sachs": {"routing_number": "026014601", "account_length": [8, 12]},
            "Morgan Stanley": {
                "routing_number": "021272655",
                "account_length": [9, 12],
            },
            "U.S. Bank": {"routing_number": "091000022", "account_length": [8, 17]},
            "PNC Bank": {"routing_number": "043000096", "account_length": [10, 12, 17]},
        }

        # 银行名称映射表，支持中英文别名
        self.bank_name_mapping = {
            # 中国主要银行映射
            "icbc": "工商银行",
            "工商银行": "工商银行",
            "中国工商银行": "工商银行",
            "abc": "农业银行",
            "农业银行": "农业银行",
            "中国农业银行": "农业银行",
            "boc": "中国银行",
            "中国银行": "中国银行",
            "ccb": "建设银行",
            "建设银行": "建设银行",
            "中国建设银行": "建设银行",
            "bcm": "交通银行",
            "交通银行": "交通银行",
            "cmb": "招商银行",
            "招商银行": "招商银行",
            "spdb": "浦发银行",
            "浦发银行": "浦发银行",
            "citic": "中信银行",
            "中信银行": "中信银行",
            "ceb": "光大银行",
            "光大银行": "光大银行",
            "cmbc": "民生银行",
            "民生银行": "民生银行",
            "pingan": "平安银行",
            "平安银行": "平安银行",
            "cib": "兴业银行",
            "兴业银行": "兴业银行",
            "cgb": "广发银行",
            "广发银行": "广发银行",
            # 美国主要银行映射
            "jpmorgan": "JPMorgan Chase",
            "chase": "JPMorgan Chase",
            "JPMorgan Chase": "JPMorgan Chase",
            "boa": "Bank of America",
            "bank_of_america": "Bank of America",
            "Bank of America": "Bank of America",
            "wells_fargo": "Wells Fargo",
            "Wells Fargo": "Wells Fargo",
            "citi": "Citibank",
            "citibank": "Citibank",
            "Citibank": "Citibank",
            "goldman": "Goldman Sachs",
            "goldman_sachs": "Goldman Sachs",
            "Goldman Sachs": "Goldman Sachs",
            "morgan_stanley": "Morgan Stanley",
            "Morgan Stanley": "Morgan Stanley",
        }

        # 设置银行名称
        self.bank_name = self._normalize_bank_name(
            self.parameters.get("bank", "工商银行")
        )
        self.account_type = self.parameters.get(
            "account_type", "SAVINGS"
        )  # SAVINGS, CHECKING, CREDIT
        self.include_bank_name = self.parameters.get("include_bank_name", False)
        self.format = self.parameters.get("format", "ACCOUNT")  # ACCOUNT, FULL

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成银行账号"""
        if self.bank_name in self.china_banks:
            return self._generate_china_bank_account()
        elif self.bank_name in self.us_banks:
            return self._generate_us_bank_account()
        else:
            return self._generate_china_bank_account()

    def _generate_china_bank_account(self) -> str:
        """生成中国银行账号"""
        bank_info = self.china_banks[self.bank_name]
        account_length = bank_info["account_length"]
        prefix = bank_info["prefix"]

        # 生成银行卡号
        if self.account_type in ["SAVINGS", "CHECKING"]:
            # 银行卡号格式：前缀 + 随机数字 + 校验位
            remaining_length = account_length - len(prefix) - 1
            middle_digits = "".join(
                [str(secrets.randbelow(9 + 1)) for _ in range(remaining_length)]
            )
            card_number = prefix + middle_digits

            # 计算Luhn校验位
            check_digit = self._calculate_luhn_check_digit(card_number)
            card_number += str(check_digit)

            if self.format == "FULL":
                return f"{self.bank_name}:{card_number}"
            else:
                return card_number
        else:
            # 信用卡账号
            credit_prefix = "4" if secrets.choice([True, False]) else "5"
            remaining_length = 16 - len(credit_prefix) - 1
            middle_digits = "".join(
                [str(secrets.randbelow(9 + 1)) for _ in range(remaining_length)]
            )
            card_number = credit_prefix + middle_digits

            check_digit = self._calculate_luhn_check_digit(card_number)
            card_number += str(check_digit)

            return card_number

    def _generate_us_bank_account(self) -> str:
        """生成美国银行账号"""
        bank_info = self.us_banks[self.bank_name]
        routing_number = bank_info["routing_number"]
        account_lengths = bank_info["account_length"]
        account_length = secrets.choice(account_lengths)

        # 生成账号
        account_number = "".join(
            [str(secrets.randbelow(9 + 1)) for _ in range(account_length)]
        )

        if self.format == "FULL":
            return f"{self.bank_name}:{routing_number}:{account_number}"
        else:
            return account_number

    def _normalize_bank_name(self, bank_input: str) -> str:
        """标准化银行名称

        支持中英文别名、大小写不敏感
        """
        if not bank_input:
            return "工商银行"

        # 转换为小写并去除空格
        normalized = str(bank_input).lower().strip().replace(" ", "")

        # 查找映射
        if normalized in self.bank_name_mapping:
            return self.bank_name_mapping[normalized]

        # 如果直接匹配失败，尝试模糊匹配
        for key, value in self.bank_name_mapping.items():
            if normalized in key.lower().replace(" ", ""):
                return value

        # 默认返回工商银行
        return "工商银行"

    def _calculate_luhn_check_digit(self, card_number: str) -> int:
        """计算Luhn校验位"""

        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return (10 - (checksum % 10)) % 10

    def _validate_luhn(self, card_number: str) -> bool:
        """验证Luhn算法"""
        return self._calculate_luhn_check_digit(card_number[:-1]) == int(
            card_number[-1]
        )

    def validate(self, data: str) -> bool:
        """验证银行账号格式"""
        if not isinstance(data, str):
            return False

        # 移除银行名称前缀
        if ":" in data:
            data = data.split(":")[-1]

        if self.bank_name in self.china_banks:
            return self._validate_china_bank_account(data)
        elif self.bank_name in self.us_banks:
            return self._validate_us_bank_account(data)
        else:
            return self._validate_china_bank_account(data)

    def _validate_china_bank_account(self, account: str) -> bool:
        """验证中国银行账号格式"""
        if not account.isdigit():
            return False

        # 检查长度
        bank_info = self.china_banks[self.bank_name]
        expected_length = bank_info["account_length"]

        if len(account) != expected_length:
            return False

        # 验证Luhn校验位
        return self._validate_luhn(account)

    def _validate_us_bank_account(self, account: str) -> bool:
        """验证美国银行账号格式"""
        if not account.isdigit():
            return False

        bank_info = self.us_banks[self.bank_name]
        valid_lengths = bank_info["account_length"]

        return len(account) in valid_lengths

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.FINANCE

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "bank",
            "account_type",
            "include_bank_name",
            "format",
        ]

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项 - TODO: Implement generation logic"""
        return self._generate_raw(context)


@register_generator("bank_account", ["银行账号", "bank", "银行卡"])
class GenericBankAccountGenerator(BankAccountGenerator):
    """通用银行账号生成器注册版本"""

    pass
