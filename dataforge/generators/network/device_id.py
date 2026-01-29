"""
设备ID/IMEI/IMSI生成器模块
支持生成各种设备标识符
"""

import string
from typing import Any

from ...core.context import GenerationContext
from ...core.crypto_utils import generate_random_alphanumeric, generate_random_string
from ...core.factory import register_generator
from ...core.generator import DataGenerator, GeneratorConfig
from ...core.luhn import calculate_luhn_check_digit
from ...core.protocols import Validator
from ...core.types import GeneratorType


class DeviceIDValidator(Validator):
    """Validator for device IDs."""

    def __init__(self, device_type: str = "IMEI"):
        self.device_type = device_type

    def validate(self, data: str) -> bool:
        """验证设备ID格式"""
        if not data or not isinstance(data, str):
            return False

        # 清理格式
        clean_value = data.replace("-", "").replace(" ", "")

        if self.device_type == "IMEI":
            if len(clean_value) != 15:
                return False
            # 验证Luhn算法
            base = clean_value[:14]
            check_digit = clean_value[14]
            return calculate_luhn_check_digit(base) == int(check_digit)

        elif self.device_type == "IMSI":
            return (
                len(clean_value) >= 12
                and len(clean_value) <= 16
                and clean_value.isdigit()
            )

        elif self.device_type == "ANDROID_ID":
            return len(clean_value) == 16 and all(
                c in "abcdef0123456789" for c in clean_value.lower()
            )

        elif self.device_type == "IOS_UDID":
            return len(clean_value) == 40 and all(
                c in string.hexdigits for c in clean_value.upper()
            )

        else:  # DEVICE_ID
            return len(clean_value) >= 8 and len(clean_value) <= 32

    @property
    def error_message(self) -> str:
        return "Invalid device ID format"


@register_generator("device_id", aliases=["deviceid", "imei", "imsi"])
class DeviceIDGenerator(DataGenerator[str]):
    """设备ID/IMEI/IMSI生成器"""

    # 声明validator类型
    validator: "DeviceIDValidator | None"

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.device_type = "IMEI"
        self.format = "standard"
        self.country_code = "460"
        self.network_code = "00"
        self.validator = None

    def _setup(self) -> None:
        """配置生成器参数"""
        self.device_type = self.parameters.get("type", "IMEI")
        self.format = self.parameters.get("format", "standard")
        self.country_code = self.parameters.get("country_code", "460")
        self.network_code = self.parameters.get("network_code", "00")
        self.validator = DeviceIDValidator(self.device_type)

    def generate(self, context: GenerationContext | None = None) -> str:
        """生成原始设备ID"""
        if self.validator is None:
            # Re-initialize validator if it's None
            self.validator = DeviceIDValidator(self.device_type)

        if self.device_type == "IMEI":
            return self._generate_imei()
        elif self.device_type == "IMSI":
            return self._generate_imsi()
        elif self.device_type == "DEVICE_ID":
            return self._generate_device_id()
        elif self.device_type == "ANDROID_ID":
            return self._generate_android_id()
        elif self.device_type == "IOS_UDID":
            return self._generate_ios_udid()
        else:
            return self._generate_device_id()

    def _generate_imei(self) -> str:
        """生成IMEI号码"""
        # 生成14位TAC+SNR
        tac = generate_random_string(8)  # Type Allocation Code
        snr = generate_random_string(6)  # Serial Number

        # 计算Luhn校验位
        base = tac + snr
        if self.validator is None:
            self.validator = DeviceIDValidator(self.device_type)
        check_digit = calculate_luhn_check_digit(base)

        imei = base + str(check_digit)

        # 格式化
        if self.format == "hyphenated":
            return f"{imei[:2]}-{imei[2:6]}-{imei[6:8]}-{imei[8:14]}-{imei[14:]}"
        elif self.format == "compact":
            return imei
        else:
            return imei

    def _generate_imsi(self) -> str:
        """生成IMSI号码"""
        # MCC + MNC + MSIN
        mcc = self.country_code.zfill(3)
        mnc = (
            self.network_code.zfill(2)
            if len(self.network_code) <= 2
            else self.network_code[:3]
        )
        msin = generate_random_string(9 - len(mnc))

        imsi = mcc + mnc + msin

        if self.format == "hyphenated":
            return f"{mcc}-{mnc}-{msin}"
        elif self.format == "compact":
            return imsi
        else:
            return imsi

    def _generate_device_id(self) -> str:
        """生成通用设备ID"""
        device_id = generate_random_alphanumeric(16, uppercase=True)

        if self.format == "hyphenated":
            return "-".join([device_id[i : i + 4] for i in range(0, len(device_id), 4)])
        else:
            return device_id

    def _generate_android_id(self) -> str:
        """生成Android ID"""
        android_id = generate_random_alphanumeric(16, uppercase=False)

        if self.format == "hyphenated":
            return "-".join(
                [android_id[i : i + 4] for i in range(0, len(android_id), 4)]
            )
        else:
            return android_id

    def _generate_ios_udid(self) -> str:
        """生成iOS UDID"""
        udid = generate_random_alphanumeric(40, uppercase=True)

        if self.format == "hyphenated":
            return "-".join([udid[i : i + 8] for i in range(0, len(udid), 8)])
        else:
            return udid

    def get_device_info(self, value: str) -> dict:
        """获取设备信息"""
        clean_value = value.replace("-", "").replace(" ", "")

        info: dict[str, Any] = {
            "type": self.device_type,
            "length": len(clean_value),
            "format": self.format,
        }

        if self.device_type == "IMEI":
            info["tac"] = clean_value[:8]  # Type Allocation Code
            info["snr"] = clean_value[8:14]  # Serial Number
            info["check_digit"] = clean_value[14]  # Check Digit

        elif self.device_type == "IMSI":
            mcc: str = clean_value[:3]  # Mobile Country Code
            mnc: str = (
                clean_value[3:5] if len(clean_value[3:5]) == 2 else clean_value[3:6]
            )  # Mobile Network Code
            info["mcc"] = mcc
            info["mnc"] = mnc
            info["msin"] = clean_value[
                len(mcc) + len(mnc) :
            ]  # Mobile Subscription Identification Number

        return info

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.NETWORK

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["country_code", "format", "network_code", "type"]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if self.validator is not None and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class GenericDeviceIDGenerator(DeviceIDGenerator):
    """通用设备ID生成器"""

    pass
