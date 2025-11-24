"""
固定电话和传真号码生成器
支持生成各种格式的座机固话和传真号码
"""

import secrets
from typing import Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
    GeneratorType,
)


class LandlineGenerator(DataGenerator[str]):
    """座机固话生成器"""

    # 中国地区号段配置
    CHINA_AREA_CODES = {
        "北京": {
            "code": "010",
            "formats": ["010-####-####", "(010)####-####", "010########"],
        },
        "上海": {
            "code": "021",
            "formats": ["021-####-####", "(021)####-####", "021########"],
        },
        "广州": {
            "code": "020",
            "formats": ["020-####-####", "(020)####-####", "020########"],
        },
        "深圳": {
            "code": "0755",
            "formats": ["0755-####-####", "(0755)####-####", "0755########"],
        },
        "天津": {
            "code": "022",
            "formats": ["022-####-####", "(022)####-####", "022########"],
        },
        "重庆": {
            "code": "023",
            "formats": ["023-####-####", "(023)####-####", "023########"],
        },
        "杭州": {
            "code": "0571",
            "formats": ["0571-####-####", "(0571)####-####", "0571########"],
        },
        "南京": {
            "code": "025",
            "formats": ["025-####-####", "(025)####-####", "025########"],
        },
        "武汉": {
            "code": "027",
            "formats": ["027-####-####", "(027)####-####", "027########"],
        },
        "成都": {
            "code": "028",
            "formats": ["028-####-####", "(028)####-####", "028########"],
        },
        "西安": {
            "code": "029",
            "formats": ["029-####-####", "(029)####-####", "029########"],
        },
        "青岛": {
            "code": "0532",
            "formats": ["0532-####-####", "(0532)####-####", "0532########"],
        },
        "大连": {
            "code": "0411",
            "formats": ["0411-####-####", "(0411)####-####", "0411########"],
        },
        "厦门": {
            "code": "0592",
            "formats": ["0592-####-####", "(0592)####-####", "0592########"],
        },
        "苏州": {
            "code": "0512",
            "formats": ["0512-####-####", "(0512)####-####", "0512########"],
        },
    }

    # 国际常用地区号段
    INTERNATIONAL_CODES = {
        "US": {
            "code": "1",
            "formats": ["+1-###-###-####", "1-###-###-####", "(###)###-####"],
        },
        "UK": {"code": "44", "formats": ["+44-####-###-####", "44-####-###-####"]},
        "JP": {"code": "81", "formats": ["+81-##-####-####", "81-##-####-####"]},
        "KR": {"code": "82", "formats": ["+82-##-####-####", "82-##-####-####"]},
        "DE": {"code": "49", "formats": ["+49-###-###-####", "49-###-###-####"]},
        "FR": {"code": "33", "formats": ["+33-#-##-##-##-##", "33-#-##-##-##-##"]},
        "AU": {"code": "61", "formats": ["+61-#-####-####", "61-#-####-####"]},
        "CA": {"code": "1", "formats": ["+1-###-###-####", "1-###-###-####"]},
    }

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "country",
            "city",
            "format_type",
            "include_area_code",
            "include_country_code",
            "separator",
            "extension_digits",
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.country = self.parameters.get("country", "CN")
        self.city = self.parameters.get("city", None)
        self.format_type = self.parameters.get("format_type", "standard")
        self.include_area_code = self.parameters.get("include_area_code", True)
        self.include_country_code = self.parameters.get("include_country_code", False)
        self.separator = self.parameters.get("separator", "-")
        self.extension_digits = self.parameters.get("extension_digits", 0)

    def _generate_china_landline(self) -> str:
        """生成中国座机号码"""
        if self.city and self.city in self.CHINA_AREA_CODES:
            area_config = self.CHINA_AREA_CODES[self.city]
        else:
            # 随机选择一个城市
            city = secrets.choice(list(self.CHINA_AREA_CODES.keys()))
            area_config = self.CHINA_AREA_CODES[city]

        # 选择格式
        if self.format_type == "compact":
            format_str = area_config["formats"][2]  # 无分隔符格式
        elif self.format_type == "parentheses":
            format_str = area_config["formats"][1]  # 括号格式
        else:
            format_str = area_config["formats"][0]  # 标准格式

        # 生成号码
        result = format_str

        # 替换#为随机数字
        while "#" in result:
            result = result.replace("#", str(secrets.randbelow(10)), 1)

        # 添加分机号
        if self.extension_digits > 0:
            extension = "".join(
                [str(secrets.randbelow(10)) for _ in range(self.extension_digits)]
            )
            result += f"-{extension}"

        return result

    def _generate_international_landline(self) -> str:
        """生成国际座机号码"""
        if self.country.upper() in self.INTERNATIONAL_CODES:
            country_config = self.INTERNATIONAL_CODES[self.country.upper()]
        else:
            # 默认使用美国格式
            country_config = self.INTERNATIONAL_CODES["US"]

        country_code = country_config["code"]
        format_str = country_config["formats"][0]  # 使用第一个格式

        # 生成号码
        result = format_str

        # 替换#为随机数字
        while "#" in result:
            result = result.replace("#", str(secrets.randbelow(10)), 1)

        # 根据国家调整格式
        if not self.include_country_code:
            # 移除国家代码
            if result.startswith("+"):
                result = result.split("-", 1)[1] if "-" in result else result
            elif result.startswith(country_code + "-"):
                result = result[len(country_code) + 1 :]

        return result

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成座机号码"""
        if self.country.upper() == "CN":
            return self._generate_china_landline()
        else:
            return self._generate_international_landline()

    def validate(self, data: str) -> bool:
        """验证座机号码格式"""
        import re

        pattern = r"^[\d\s\-\(\)\+]+$"
        return bool(re.match(pattern, data))

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context) if context else self._generate_raw()


class FaxNumberGenerator(DataGenerator[str]):
    """传真号码生成器"""

    # 传真号码前缀
    FAX_PREFIXES = {
        "CN": ["传真", "FAX", "传真号", "FAX号"],
        "US": ["FAX", "Fax", "fax"],
        "UK": ["FAX", "Fax"],
        "JP": ["ファックス", "FAX"],
        "KR": ["팩스", "FAX"],
    }

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "country",
            "city",
            "include_prefix",
            "prefix_type",
            "format_type",
            "extension_digits",
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.country = self.parameters.get("country", "CN")
        self.city = self.parameters.get("city", None)
        self.include_prefix = self.parameters.get("include_prefix", True)
        self.prefix_type = self.parameters.get("prefix_type", "standard")
        self.format_type = self.parameters.get("format_type", "standard")
        self.extension_digits = self.parameters.get("extension_digits", 0)

    def _get_prefix(self) -> str:
        """获取传真前缀"""
        if not self.include_prefix:
            return ""

        country = self.country.upper()
        if country in self.FAX_PREFIXES:
            prefixes = self.FAX_PREFIXES[country]
            prefix = secrets.choice(prefixes)
        else:
            prefix = "FAX"

        if self.prefix_type == "short":
            return f"{prefix}: "
        elif self.prefix_type == "full":
            return f"{prefix}号码: "
        else:
            return f"{prefix} "

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成传真号码"""
        # 使用座机生成器生成基础号码
        config = GeneratorConfig(
            generator_type="landline",
            parameters=self.parameters,
            count=1,
            validate=True,
        )
        landline_gen = LandlineGenerator(config)
        base_number = landline_gen.generate_single()

        # 添加传真前缀
        prefix = self._get_prefix()

        return f"{prefix}{base_number}"

    def validate(self, data: str) -> bool:
        """验证传真号码格式"""
        import re

        pattern = r"^\+?[\d\s\-\(\)]+(?:ext\d+)?$"
        return bool(re.match(pattern, data))

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context) if context else self._generate_raw()


class TollFreeNumberGenerator(DataGenerator[str]):
    """800/400客服号码生成器"""

    def _setup(self) -> None:
        """配置客服号码参数"""
        self.country = self.parameters.get("country", "CN")
        self.number_type = self.parameters.get("number_type", "400")  # 400或800
        self.format_type = self.parameters.get("format_type", "standard")
        self.separator = self.parameters.get("separator", "-")

    def _generate_cn_toll_free(self) -> str:
        """生成中国客服号码"""
        if self.number_type == "400":
            # 400号码：400-XXX-XXXX
            middle = "".join([str(secrets.randbelow(10)) for _ in range(3)])
            last = "".join([str(secrets.randbelow(10)) for _ in range(4)])
            return f"400{self.separator}{middle}{self.separator}{last}"
        else:  # 800号码
            # 800号码：800-XXX-XXXX
            middle = "".join([str(secrets.randbelow(10)) for _ in range(3)])
            last = "".join([str(secrets.randbelow(10)) for _ in range(4)])
            return f"800{self.separator}{middle}{self.separator}{last}"

    def _generate_international_toll_free(self) -> str:
        """生成国际客服号码"""
        toll_free_prefixes = {
            "US": ["800", "888", "877", "866", "855", "844", "833"],
            "UK": ["800", "808"],
            "CA": ["800", "833", "844", "855", "866", "877", "888"],
            "AU": ["1800"],
            "JP": ["0120", "0800"],
            "KR": ["080", "1588", "1670"],
        }

        prefixes = toll_free_prefixes.get(self.country.upper(), ["800"])
        prefix = secrets.choice(prefixes)

        # 根据前缀长度生成剩余号码
        if len(prefix) == 3:  # 800, 888等
            number = "".join([str(secrets.randbelow(10)) for _ in range(7)])
            return f"{prefix}{self.separator}{number[:3]}{self.separator}{number[3:7]}"
        elif len(prefix) == 4:  # 0120, 1800等
            number = "".join([str(secrets.randbelow(10)) for _ in range(6)])
            return f"{prefix}{self.separator}{number[:2]}{self.separator}{number[2:6]}"
        else:  # 其他情况
            number = "".join([str(secrets.randbelow(10)) for _ in range(6)])
            return f"{prefix}{self.separator}{number}"

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成客服号码"""
        if self.country.upper() == "CN":
            return self._generate_cn_toll_free()
        else:
            return self._generate_international_toll_free()

    def validate(self, data: str) -> bool:
        """验证客服号码格式"""
        import re

        pattern = r"^(400|800|\+?\d{3,4})[-\s]?\d{2,4}[-\s]?\d{3,7}$"
        return bool(re.match(pattern, data))

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.TEXT

    @property
    def supported_parameters(self) -> list[str]:
        return ["country", "number_type", "format_type", "separator"]

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context) if context else self._generate_raw()


class ExtensionGenerator(DataGenerator[str]):
    """分机号生成器"""

    def _setup(self) -> None:
        """配置分机号参数"""
        self.min_extension = self.parameters.get("min_extension", 100)
        self.max_extension = self.parameters.get("max_extension", 9999)
        self.prefix = self.parameters.get("prefix", "ext")
        self.format_type = self.parameters.get("format_type", "short")  # short, long

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成分机号"""
        extension = str(
            secrets.randbelow(self.max_extension - self.min_extension + 1)
            + self.min_extension
        )

        if self.format_type == "long":
            return f"{self.prefix} {extension}"
        else:
            return extension

    def validate(self, data: str) -> bool:
        """验证分机号格式"""
        import re

        pattern = r"^(ext\s*)?\d{2,5}$"
        return bool(re.match(pattern, data.lower()))

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.TEXT

    @property
    def supported_parameters(self) -> list[str]:
        return ["min_extension", "max_extension", "prefix", "format_type"]

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context) if context else self._generate_raw()


# 注册生成器及其别名
for name, aliases, generator_class in [
    ("landline", ["固话", "座机", "电话"], LandlineGenerator),
    ("fax", ["传真", "传真号", "FAX"], FaxNumberGenerator),
    ("tollfree", ["400", "800", "客服号码"], TollFreeNumberGenerator),
    ("extension", ["分机", "分机号"], ExtensionGenerator),
]:
    # 先注册生成器主名称
    register_generator(name, generator_class)
    # 为每个别名单独注册相同的生成器类
    for alias in aliases:
        register_generator(alias, generator_class)
