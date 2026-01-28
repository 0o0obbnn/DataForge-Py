"""
车牌号生成器
"""

import secrets

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
)
from ...core.types import GeneratorType
from ...resources.license_plate_loader import load_license_plate_config


class LicensePlateGenerator(DataGenerator[str]):
    """中国车牌号生成器"""

    def _setup(self) -> None:
        self.plate_type = self.parameters.get("type", "BOTH")  # FUEL, NEW_ENERGY, BOTH
        self.province = self.parameters.get("province", None)  # 省份简称
        self.city = self.parameters.get("city", None)  # 城市字母代码
        self.include_io = self.parameters.get("include_io", False)  # 是否包含I和O
        self.valid = self.parameters.get("valid", True)  # 是否保证符合基本格式规则

        # 从配置文件加载数据（支持locale参数，默认为zh_CN）
        locale = self.parameters.get("locale", "zh_CN")
        config = load_license_plate_config(locale=locale)

        # 省份简称映射（从配置文件加载）
        self.provinces = config.get("provinces", {})

        # 城市代码字母（从配置文件加载）
        self.city_codes = config.get("city_codes", []).copy()
        if self.include_io:
            if "I" not in self.city_codes:
                self.city_codes.append("I")
            if "O" not in self.city_codes:
                self.city_codes.append("O")

        # 车牌字符（从配置文件加载）
        self.plate_chars = config.get("plate_chars", []).copy()
        if self.include_io:
            if "I" not in self.plate_chars:
                self.plate_chars.append("I")
            if "O" not in self.plate_chars:
                self.plate_chars.append("O")

        # 新能源车牌前缀（从配置文件加载）
        self.new_energy_prefixes = config.get("new_energy_prefixes", ["D", "F"])

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        """生成原始车牌号"""
        # 先生成一个有效车牌
        if self.plate_type == "NEW_ENERGY":
            plate = self._generate_new_energy_plate()
        elif self.plate_type == "FUEL":
            plate = self._generate_fuel_plate()
        else:  # BOTH
            if (secrets.randbelow(1000000) / 1000000) < 0.2:  # 20%概率生成新能源车牌
                plate = self._generate_new_energy_plate()
            else:
                plate = self._generate_fuel_plate()
        # 根据 valid 参数决定是否返回无效车牌
        if self.valid:
            return plate
        else:
            return self._corrupt_plate(plate)

    def _generate_fuel_plate(self) -> str:
        """生成燃油车牌号（7位）"""
        # 选择省份简称
        if self.province and self.province in self.provinces:
            province_code = self.province
        else:
            province_code = secrets.choice(list(self.provinces.keys()))

        # 选择城市代码
        if self.city and self.city in self.city_codes:
            city_code = self.city
        else:
            city_code = secrets.choice(self.city_codes)

        # 生成5位字母数字组合
        plate_suffix = "".join(secrets.choice(self.plate_chars) for _ in range(5))

        return f"{province_code}{city_code}{plate_suffix}"

    def _generate_new_energy_plate(self) -> str:
        """生成新能源车牌号（8位，绿牌）"""
        # 选择省份简称
        if self.province and self.province in self.provinces:
            province_code = self.province
        else:
            province_code = secrets.choice(list(self.provinces.keys()))

        # 选择城市代码
        if self.city and self.city in self.city_codes:
            city_code = self.city
        else:
            city_code = secrets.choice(self.city_codes)

        # 新能源车牌以D或F开头（从配置加载）
        new_energy_prefix = secrets.choice(self.new_energy_prefixes)

        # 生成5位字母数字组合
        plate_suffix = "".join(secrets.choice(self.plate_chars) for _ in range(5))

        return f"{province_code}{city_code}{new_energy_prefix}{plate_suffix}"

    def _corrupt_plate(self, plate: str) -> str:
        """基于有效车牌构造无效车牌（用于 valid=False 场景）"""
        try:
            if len(plate) == 7:
                # 燃油车牌：长度错误或非法字符
                if (secrets.randbelow(1000000) / 1000000) < 0.5:
                    # 长度错误：多加一个非法字符
                    return plate + "*"
                else:
                    # 非法字符：将某一位替换成禁止字符
                    idx = secrets.randbelow(5) + 2  # 替换后缀范围字符
                    bad_char = "*" if not self.include_io else "!"
                    return plate[:idx] + bad_char + plate[idx + 1 :]
            elif len(plate) == 8:
                # 新能源车牌：第3位不是 D/F 或长度错误
                if (secrets.randbelow(1000000) / 1000000) < 0.5:
                    return plate[:2] + "A" + plate[3:]
                else:
                    return plate[:-1]
        except Exception:
            pass
        # 兜底：插入非法字符
        return plate + "*"

    def validate(self, data: str) -> bool:
        """校验车牌号"""
        if not isinstance(data, str):
            return False

        # 基本长度检查
        if len(data) not in [7, 8]:
            return False

        # 检查第一位是否为中文省份简称
        if data[0] not in self.provinces:
            return False

        # 检查第二位是否为字母
        if not data[1].isalpha() or data[1] not in self.city_codes:
            return False

        # 检查后续字符
        if len(data) == 7:  # 燃油车牌
            # 后5位应该是字母或数字
            for char in data[2:]:
                if char not in self.plate_chars:
                    return False
        elif len(data) == 8:  # 新能源车牌
            # 第3位应该是D或F（从配置加载）
            if data[2] not in self.new_energy_prefixes:
                return False
            # 后5位应该是字母或数字
            for char in data[3:]:
                if char not in self.plate_chars:
                    return False

        return True

    def get_plate_info(self, plate: str) -> dict:
        """获取车牌信息"""
        if not self.validate(plate):
            return {"valid": False, "error": "无效车牌号"}

        result = {
            "valid": True,
            "plate": plate,
            "province_code": plate[0],
            "province_name": self.provinces.get(plate[0], "未知"),
            "city_code": plate[1],
            "type": "new_energy" if len(plate) == 8 else "fuel",
            "length": len(plate),
        }

        if len(plate) == 8:
            result["new_energy_prefix"] = plate[2]
            result["suffix"] = plate[3:]
        else:
            result["suffix"] = plate[2:]

        return result

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO

    @property
    def supported_parameters(self) -> list[str]:
        return ["type", "province", "city", "include_io", "valid", "locale"]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项 - Implemented generation logic"""
        return self._generate_raw(context)


@register_generator("license_plate", ["plate", "车牌号", "车牌"])
class ChineseLicensePlateGenerator(LicensePlateGenerator):
    """中国车牌号生成器注册版本"""

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        return super().validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC_INFO

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return super().supported_parameters


# 重复注册已移除，避免与 'license_plate' 主注册冲突
