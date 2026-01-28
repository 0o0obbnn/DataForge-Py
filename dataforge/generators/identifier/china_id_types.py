"""
中国各类证件号码生成器
包括：户口簿、军官证、士兵证、武警官兵证、临时身份证、外国人居留证、警官证、
香港身份证、澳门身份证、台湾身份证、外国人永久居留身份证、外国护照等
"""

import re
import secrets
from typing import Any

from ...core.factory import register_generator
from ...core.generator import DataGenerator, GenerationContext, GeneratorConfig
from ...core.protocols import Validator
from ...core.types import GeneratorType

# ==================== 验证器 ====================


class HouseholdRegisterValidator(Validator):
    """户口簿验证器"""

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证户口簿号码"""
        if isinstance(data, dict):
            data = data.get("id_number", "")
        if not isinstance(data, str):
            return False
        # 户口簿号码格式：18位数字
        return bool(re.match(r"^\d{18}$", data))


class OfficerCardValidator(Validator):
    """军官证验证器"""

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证军官证号码"""
        if isinstance(data, dict):
            data = data.get("id_number", "")
        if not isinstance(data, str):
            return False
        # 军官证格式：军+数字 或 纯数字
        return bool(re.match(r"^军\d{8,12}$|^\d{9,18}$", data))


class SoldierCardValidator(Validator):
    """士兵证验证器"""

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证士兵证号码"""
        if isinstance(data, dict):
            data = data.get("id_number", "")
        if not isinstance(data, str):
            return False
        # 士兵证格式：士+数字 或 纯数字
        return bool(re.match(r"^士\d{8,12}$|^\d{9,18}$", data))


class TemporaryIDCardValidator(Validator):
    """临时身份证验证器"""

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证临时身份证号码"""
        if isinstance(data, dict):
            data = data.get("id_number", "")
        if not isinstance(data, str):
            return False
        # 临时身份证格式：与身份证相同，18位
        if len(data) != 18:
            return False
        if not data[:17].isdigit():
            return False
        if data[17].upper() not in [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "X",
        ]:
            return False
        return True


class ForeignerResidenceValidator(Validator):
    """外国人居留证验证器"""

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证外国人居留证号码"""
        if isinstance(data, dict):
            data = data.get("id_number", "")
        if not isinstance(data, str):
            return False
        # 外国人居留证格式：15位数字
        return bool(re.match(r"^\d{15}$", data))


class PoliceOfficerCardValidator(Validator):
    """警官证验证器"""

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证警官证号码"""
        if isinstance(data, dict):
            data = data.get("id_number", "")
        if not isinstance(data, str):
            return False
        # 警官证格式：警+数字 或 纯数字
        return bool(re.match(r"^警\d{8,12}$|^\d{9,18}$", data))


class WujingCardValidator(Validator):
    """武警官兵证验证器"""

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证武警官兵证号码"""
        if isinstance(data, dict):
            data = data.get("id_number", "")
        if not isinstance(data, str):
            return False
        # 武警官兵证格式：武+数字 或 纯数字
        return bool(re.match(r"^武\d{8,12}$|^\d{9,18}$", data))


class HongKongIDValidator(Validator):
    """香港身份证验证器"""

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证香港身份证号码"""
        if isinstance(data, dict):
            data = data.get("id_number", "")
        if not isinstance(data, str):
            return False
        # 香港身份证格式：1-2个字母+6位数字+(0-9或A)
        return bool(re.match(r"^[A-Z]{1,2}\d{6}\([0-9A]\)$", data))


class MacauIDValidator(Validator):
    """澳门身份证验证器"""

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证澳门身份证号码"""
        if isinstance(data, dict):
            data = data.get("id_number", "")
        if not isinstance(data, str):
            return False
        # 澳门身份证格式：1个数字+6位数字+(0-9或A)
        return bool(re.match(r"^\d{1}\d{6}\([0-9A]\)$", data))


class TaiwanIDValidator(Validator):
    """台湾身份证验证器"""

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证台湾身份证号码"""
        if isinstance(data, dict):
            data = data.get("id_number", "")
        if not isinstance(data, str):
            return False
        # 台湾身份证格式：1个字母+9位数字
        return bool(re.match(r"^[A-Z]{1}\d{9}$", data))


class ForeignPermanentResidenceValidator(Validator):
    """外国人永久居留身份证验证器"""

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证外国人永久居留身份证号码"""
        if isinstance(data, dict):
            data = data.get("id_number", "")
        if not isinstance(data, str):
            return False
        # 外国人永久居留身份证格式：15位数字
        return bool(re.match(r"^\d{15}$", data))


class ForeignPassportValidator(Validator):
    """外国护照验证器"""

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证外国护照号码"""
        if isinstance(data, dict):
            data = data.get("id_number", "")
        if not isinstance(data, str):
            return False
        # 外国护照格式：各国不同，常见格式：2个字母+7位数字
        return bool(re.match(r"^[A-Z]{2}\d{7}$", data))


# ==================== 生成器 ====================


@register_generator("household_register", aliases=["户口簿", "户薄"])
class HouseholdRegisterGenerator(DataGenerator[str]):
    """户口簿号码生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = HouseholdRegisterValidator()

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成户口簿号码"""
        # 户口簿号码格式：18位数字
        return "".join(str(secrets.randbelow(10)) for _ in range(18))

    def validate(self, data: str) -> bool:
        """验证户口簿号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        return []


@register_generator("officer_card", aliases=["军官证"])
class OfficerCardGenerator(DataGenerator[str]):
    """军官证号码生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = OfficerCardValidator()
        self.with_prefix = self.parameters.get("with_prefix", True)

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成军官证号码"""
        # 军官证格式：军+8-12位数字 或 纯数字
        if self.with_prefix and secrets.randbelow(2):
            prefix = "军"
            digits = "".join(
                str(secrets.randbelow(10)) for _ in range(secrets.randbelow(5) + 8)
            )
            return f"{prefix}{digits}"
        else:
            return "".join(
                str(secrets.randbelow(10)) for _ in range(secrets.randbelow(10) + 9)
            )

    def validate(self, data: str) -> bool:
        """验证军官证号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        return ["with_prefix"]


@register_generator("soldier_card", aliases=["士兵证"])
class SoldierCardGenerator(DataGenerator[str]):
    """士兵证号码生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = SoldierCardValidator()
        self.with_prefix = self.parameters.get("with_prefix", True)

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成士兵证号码"""
        # 士兵证格式：士+8-12位数字 或 纯数字
        if self.with_prefix and secrets.randbelow(2):
            prefix = "士"
            digits = "".join(
                str(secrets.randbelow(10)) for _ in range(secrets.randbelow(5) + 8)
            )
            return f"{prefix}{digits}"
        else:
            return "".join(
                str(secrets.randbelow(10)) for _ in range(secrets.randbelow(10) + 9)
            )

    def validate(self, data: str) -> bool:
        """验证士兵证号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        return ["with_prefix"]


@register_generator("temporary_idcard", aliases=["临时身份证"])
class TemporaryIDCardGenerator(DataGenerator[str]):
    """临时身份证号码生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = TemporaryIDCardValidator()

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成临时身份证号码"""
        # 临时身份证格式：与身份证相同，18位
        # 这里简化处理，生成18位数字，最后一位可能是X
        first_17 = "".join(str(secrets.randbelow(10)) for _ in range(17))
        check_digit = str(secrets.randbelow(10))
        return f"{first_17}{check_digit}"

    def validate(self, data: str) -> bool:
        """验证临时身份证号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        return []


@register_generator("foreigner_residence", aliases=["外国人居留证"])
class ForeignerResidenceGenerator(DataGenerator[str]):
    """外国人居留证号码生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = ForeignerResidenceValidator()

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成外国人居留证号码"""
        # 外国人居留证格式：15位数字
        return "".join(str(secrets.randbelow(10)) for _ in range(15))

    def validate(self, data: str) -> bool:
        """验证外国人居留证号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        return []


@register_generator("police_officer_card", aliases=["警官证"])
class PoliceOfficerCardGenerator(DataGenerator[str]):
    """警官证号码生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = PoliceOfficerCardValidator()
        self.with_prefix = self.parameters.get("with_prefix", True)

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成警官证号码"""
        # 警官证格式：警+8-12位数字 或 纯数字
        if self.with_prefix and secrets.randbelow(2):
            prefix = "警"
            digits = "".join(
                str(secrets.randbelow(10)) for _ in range(secrets.randbelow(5) + 8)
            )
            return f"{prefix}{digits}"
        else:
            return "".join(
                str(secrets.randbelow(10)) for _ in range(secrets.randbelow(10) + 9)
            )

    def validate(self, data: str) -> bool:
        """验证警官证号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        return ["with_prefix"]


@register_generator("wujing_card", aliases=["武警官兵证", "武警证"])
class WujingCardGenerator(DataGenerator[str]):
    """武警官兵证号码生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = WujingCardValidator()
        self.with_prefix = self.parameters.get("with_prefix", True)

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成武警官兵证号码"""
        # 武警官兵证格式：武+8-12位数字 或 纯数字
        if self.with_prefix and secrets.randbelow(2):
            prefix = "武"
            digits = "".join(
                str(secrets.randbelow(10)) for _ in range(secrets.randbelow(5) + 8)
            )
            return f"{prefix}{digits}"
        else:
            return "".join(
                str(secrets.randbelow(10)) for _ in range(secrets.randbelow(10) + 9)
            )

    def validate(self, data: str) -> bool:
        """验证武警官兵证号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        return ["with_prefix"]


@register_generator("hong_kong_id", aliases=["香港身份证", "HKID"])
class HongKongIDGenerator(DataGenerator[str]):
    """香港身份证号码生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = HongKongIDValidator()

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成香港身份证号码"""
        # 香港身份证格式：1-2个字母+6位数字+(0-9或A)
        letters_count = 1 if secrets.randbelow(2) else 2
        letters = "".join(
            secrets.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(letters_count)
        )
        digits = "".join(str(secrets.randbelow(10)) for _ in range(6))
        check_char = str(secrets.randbelow(10)) if secrets.randbelow(10) else "A"
        return f"{letters}{digits}({check_char})"

    def validate(self, data: str) -> bool:
        """验证香港身份证号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        return []


@register_generator("macau_id", aliases=["澳门身份证", "MacauID"])
class MacauIDGenerator(DataGenerator[str]):
    """澳门身份证号码生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = MacauIDValidator()

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成澳门身份证号码"""
        # 澳门身份证格式：1个数字+6位数字+(0-9或A)
        first_digit = str(secrets.randbelow(10))
        digits = "".join(str(secrets.randbelow(10)) for _ in range(6))
        check_char = str(secrets.randbelow(10)) if secrets.randbelow(10) else "A"
        return f"{first_digit}{digits}({check_char})"

    def validate(self, data: str) -> bool:
        """验证澳门身份证号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        return []


@register_generator("taiwan_id", aliases=["台湾身份证", "TaiwanID"])
class TaiwanIDGenerator(DataGenerator[str]):
    """台湾身份证号码生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = TaiwanIDValidator()
        # 台湾地区字母代码
        self.area_codes = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成台湾身份证号码"""
        # 台湾身份证格式：1个字母+9位数字
        area_letter = secrets.choice(self.area_codes)
        digits = "".join(str(secrets.randbelow(10)) for _ in range(9))
        return f"{area_letter}{digits}"

    def validate(self, data: str) -> bool:
        """验证台湾身份证号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        return []


@register_generator("foreign_permanent_residence", aliases=["外国人永久居留身份证"])
class ForeignPermanentResidenceGenerator(DataGenerator[str]):
    """外国人永久居留身份证号码生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = ForeignPermanentResidenceValidator()
        # 常见国家代码
        self.country_codes = [
            "001",  # 美国
            "002",  # 英国
            "003",  # 法国
            "004",  # 德国
            "005",  # 日本
            "006",  # 韩国
            "007",  # 澳大利亚
            "008",  # 加拿大
            "009",  # 俄罗斯
            "010",  # 巴西
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成外国人永久居留身份证号码"""
        # 外国人永久居留身份证格式：15位数字
        # 前3位：国家代码，后12位：个人编号
        country_code = secrets.choice(self.country_codes)
        person_number = "".join(str(secrets.randbelow(10)) for _ in range(12))
        return f"{country_code}{person_number}"

    def validate(self, data: str) -> bool:
        """验证外国人永久居留身份证号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        return []


@register_generator("foreign_passport", aliases=["外国护照"])
class ForeignPassportGenerator(DataGenerator[str]):
    """外国护照号码生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.validator = ForeignPassportValidator()
        # 常见国家代码
        self.country_codes = [
            "US",  # 美国
            "GB",  # 英国
            "FR",  # 法国
            "DE",  # 德国
            "JP",  # 日本
            "KR",  # 韩国
            "AU",  # 澳大利亚
            "CA",  # 加拿大
            "RU",  # 俄罗斯
            "BR",  # 巴西
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成外国护照号码"""
        # 外国护照格式：2个字母+7位数字
        country_code = secrets.choice(self.country_codes)
        passport_number = "".join(str(secrets.randbelow(10)) for _ in range(7))
        return f"{country_code}{passport_number}"

    def validate(self, data: str) -> bool:
        """验证外国护照号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        return []
