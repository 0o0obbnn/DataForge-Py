"""
港澳台居民证件类型生成器
包括：
- 港澳居民来往内地通行证 (回乡证)
- 台湾居民来往大陆通行证 (台胞证)
- 港澳台居民居住证
"""

import re
import secrets
from typing import Any, Union

from ...core.factory import register_generator
from ...core.generator import DataGenerator, GenerationContext, GeneratorConfig
from ...core.protocols import Validator
from ...core.types import GeneratorType


class HkMoTwIdValidator(Validator):
    """港澳台证件类型验证器"""

    def __init__(self, id_type: str = "all"):
        self.id_type = id_type

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证港澳台证件号码"""
        if isinstance(data, dict):
            if "id_number" in data:
                id_number = data["id_number"]
            else:
                return False
        elif isinstance(data, str):
            id_number = data
        else:
            return False

        if not isinstance(id_number, str):
            return False

        # 根据证件类型验证格式
        if self.id_type in ["hk_mc", "all"]:
            if self._validate_hk_mc_passport(id_number):
                return True

        if self.id_type in ["tw_mc", "all"]:
            if self._validate_tw_mc_passport(id_number):
                return True

        if self.id_type in ["residence", "all"]:
            if self._validate_residence_permit(id_number):
                return True

        return False

    def _validate_hk_mc_passport(self, id_number: str) -> bool:
        """验证港澳居民来往内地通行证 (回乡证)"""
        # 港澳通行证格式：H/M + 10位数字
        pattern = r"^[HM]\d{10}$"
        return bool(re.match(pattern, id_number))

    def _validate_tw_mc_passport(self, id_number: str) -> bool:
        """验证台湾居民来往大陆通行证 (台胞证)"""
        # 台湾通行证格式：台 + 8位数字 或者 8位数字
        pattern1 = r"^台\d{8}$"
        pattern2 = r"^\d{8}$"
        return bool(re.match(pattern1, id_number)) or bool(
            re.match(pattern2, id_number)
        )

    def _validate_residence_permit(self, id_number: str) -> bool:
        """验证港澳台居民居住证"""
        # 居住证格式：18位数字，类似身份证
        if len(id_number) != 18:
            return False

        # 前17位应为数字
        if not id_number[:17].isdigit():
            return False

        # 最后一位可以是数字或X
        if id_number[17].upper() not in [
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

        # 验证校验位
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]

        total = sum(int(id_number[i]) * weights[i] for i in range(17))
        return check_codes[total % 11] == id_number[17].upper()

    @property
    def error_message(self) -> str:
        return "Invalid Hong Kong, Macao or Taiwan resident ID format"


class HkMoTwIdGenerator(DataGenerator[Union[str, dict[str, Any]]]):
    """港澳台居民证件生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.id_type = self.parameters.get("type", "all").lower()
        self.include_details = self.parameters.get("include_details", False)
        self.validator = HkMoTwIdValidator(self.id_type)

    def _setup(self) -> None:
        """初始化配置参数"""
        self.id_type = self.parameters.get("type", "all").lower()
        self.include_details = self.parameters.get("include_details", False)

    def generate_single(
        self, context: GenerationContext | None = None
    ) -> str | dict[str, Any]:
        """生成港澳台证件号码"""
        id_number = self._generate_id_number()

        if self.include_details:
            details = self._get_id_details(id_number)
            return {
                "id_number": id_number,
                "type": details["type"],
                "type_name": details["type_name"],
                "region": details["region"],
            }
        else:
            return id_number

    def _generate_id_number(self) -> str:
        """根据指定类型生成证件号码"""
        if self.id_type == "hk_mc":
            return self._generate_hk_mc_passport()
        elif self.id_type == "tw_mc":
            return self._generate_tw_mc_passport()
        elif self.id_type == "residence":
            return self._generate_residence_permit()
        else:  # all or default
            # 随机选择一种证件类型
            id_types = ["hk_mc", "tw_mc", "residence"]
            chosen_type = secrets.choice(id_types)

            if chosen_type == "hk_mc":
                return self._generate_hk_mc_passport()
            elif chosen_type == "tw_mc":
                return self._generate_tw_mc_passport()
            else:
                return self._generate_residence_permit()

    def _generate_hk_mc_passport(self) -> str:
        """生成港澳居民来往内地通行证 (回乡证)"""
        # 格式：H/M + 10位数字
        prefix = secrets.choice(["H", "M"])  # H代表香港，M代表澳门
        digits = "".join(str(secrets.randbelow(10)) for _ in range(10))
        return f"{prefix}{digits}"

    def _generate_tw_mc_passport(self) -> str:
        """生成台湾居民来往大陆通行证 (台胞证)"""
        # 格式：台 + 8位数字 或者 8位数字
        if secrets.randbelow(2):  # 50%概率生成带"台"字前缀的
            digits = "".join(str(secrets.randbelow(10)) for _ in range(8))
            return f"台{digits}"
        else:
            digits = "".join(str(secrets.randbelow(10)) for _ in range(8))
            return digits

    def _generate_residence_permit(self) -> str:
        """生成港澳台居民居住证 (18位，类似身份证)"""
        # 生成18位居住证号码，格式与身份证类似
        # 前6位：地区代码 (使用港澳台相关地区代码)
        region_codes = [
            "810000",  # 香港特别行政区
            "820000",  # 澳门特别行政区
            "710000",  # 台湾省
            "440000",  # 广东省 (港澳台居民常居住地)
            "310000",  # 上海市
            "110000",  # 北京市
            "320000",  # 江苏省
            "330000",  # 浙江省
        ]
        region_code = secrets.choice(region_codes)

        # 第7-14位：出生日期 (YYYYMMDD)
        year = secrets.randbelow(40) + 1980  # 1980-2019
        month = secrets.randbelow(12) + 1
        day = secrets.randbelow(28) + 1  # 简化处理，避免闰年等问题
        birth_date = f"{year:04d}{month:02d}{day:02d}"

        # 第15-17位：顺序码 (3位)
        sequence = f"{secrets.randbelow(1000):03d}"

        # 前17位组合
        id_17 = f"{region_code}{birth_date}{sequence}"

        # 计算校验位
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]

        total = sum(int(id_17[i]) * weights[i] for i in range(17))
        check_digit = check_codes[total % 11]

        return f"{id_17}{check_digit}"

    def _get_id_details(self, id_number: str) -> dict[str, str]:
        """获取证件详情"""
        if re.match(r"^[HM]\d{10}$", id_number):
            region = "香港" if id_number[0] == "H" else "澳门"
            return {
                "type": "hk_mc",
                "type_name": "港澳居民来往内地通行证",
                "region": region,
            }
        elif re.match(r"^台\d{8}$", id_number) or re.match(r"^\d{8}$", id_number):
            return {
                "type": "tw_mc",
                "type_name": "台湾居民来往大陆通行证",
                "region": "台湾",
            }
        elif self._is_valid_residence_permit(id_number):
            # 判断具体是哪个地区的居住证
            region_code = id_number[:6]
            if region_code.startswith("81"):
                region = "香港"
            elif region_code.startswith("82"):
                region = "澳门"
            elif region_code.startswith("71"):
                region = "台湾"
            else:
                region = "中国大陆"

            return {
                "type": "residence",
                "type_name": "港澳台居民居住证",
                "region": region,
            }
        else:
            return {"type": "unknown", "type_name": "未知证件类型", "region": "未知"}

    def _is_valid_residence_permit(self, id_number: str) -> bool:
        """检查是否为有效的居住证号码"""
        if len(id_number) != 18:
            return False
        if not id_number[:17].isdigit():
            return False
        if id_number[17].upper() not in [
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

        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]

        total = sum(int(id_number[i]) * weights[i] for i in range(17))
        return check_codes[total % 11] == id_number[17].upper()

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证生成的证件号码"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["type", "include_details"]


@register_generator("hk_mo_tw_id", aliases=["港澳台证件", "回乡证", "台胞证", "居住证"])
class GenericHkMoTwIdGenerator(HkMoTwIdGenerator):
    """注册港澳台证件生成器"""

    pass
