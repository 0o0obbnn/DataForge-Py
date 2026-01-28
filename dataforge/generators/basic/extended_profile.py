#!/usr/bin/env python3
"""
扩展个人信息生成器

提供星座、民族、血型、婚姻状况等扩展个人信息的生成
"""

import random

from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GenerationContext, GeneratorConfig
from dataforge.core.types import GeneratorType


@register_generator("zodiac")
class ZodiacGenerator(DataGenerator):
    """星座生成器

    生成12星座名称，支持中英文格式
    """

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self._setup()

    def _setup(self) -> None:
        """初始化星座数据"""
        self.chinese_zodiacs = [
            "白羊座",
            "金牛座",
            "双子座",
            "巨蟹座",
            "狮子座",
            "处女座",
            "天秤座",
            "天蝎座",
            "射手座",
            "摩羯座",
            "水瓶座",
            "双鱼座",
        ]

        self.english_zodiacs = [
            "Aries",
            "Taurus",
            "Gemini",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个星座"""
        format_type = self.config.parameters.get("format", "CHINESE").upper()

        if format_type == "ENGLISH":
            return random.choice(self.english_zodiacs)
        else:
            return random.choice(self.chinese_zodiacs)

    def validate(self, data: str) -> bool:
        """验证星座是否有效"""
        all_zodiacs = self.chinese_zodiacs + self.english_zodiacs
        if not isinstance(data, str):
            return False
        s = data.strip()
        return bool(s) and (s in all_zodiacs)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


@register_generator("ethnicity")
class EthnicityGenerator(DataGenerator):
    """民族生成器

    生成中国56个民族名称，支持常用民族权重
    """

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self._setup()

    def _setup(self) -> None:
        """初始化民族数据"""
        # 常见民族（权重较高）
        self.common_ethnicities = [
            "汉族",
            "壮族",
            "回族",
            "满族",
            "维吾尔族",
            "苗族",
            "彝族",
            "土家族",
            "藏族",
            "蒙古族",
            "侗族",
            "布依族",
            "瑶族",
            "白族",
            "朝鲜族",
            "哈尼族",
        ]

        # 全部56个民族
        self.all_ethnicities = [
            "汉族",
            "壮族",
            "回族",
            "满族",
            "维吾尔族",
            "苗族",
            "彝族",
            "土家族",
            "藏族",
            "蒙古族",
            "侗族",
            "布依族",
            "瑶族",
            "白族",
            "朝鲜族",
            "哈尼族",
            "哈萨克族",
            "黎族",
            "傣族",
            "畲族",
            "傈僳族",
            "仡佬族",
            "东乡族",
            "高山族",
            "拉祜族",
            "水族",
            "佤族",
            "纳西族",
            "羌族",
            "土族",
            "仫佬族",
            "锡伯族",
            "柯尔克孜族",
            "达斡尔族",
            "景颇族",
            "毛南族",
            "撒拉族",
            "布朗族",
            "塔吉克族",
            "阿昌族",
            "普米族",
            "鄂温克族",
            "怒族",
            "京族",
            "基诺族",
            "德昂族",
            "保安族",
            "俄罗斯族",
            "裕固族",
            "乌孜别克族",
            "门巴族",
            "鄂伦春族",
            "独龙族",
            "塔塔尔族",
            "赫哲族",
            "珞巴族",
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个民族"""
        use_common = self.config.parameters.get("common", True)

        if use_common:
            # 80%概率选择常见民族
            if random.random() < 0.8:
                return random.choice(self.common_ethnicities)
            else:
                return random.choice(self.all_ethnicities)
        else:
            return random.choice(self.all_ethnicities)

    def validate(self, data: str) -> bool:
        """验证民族是否有效"""
        if not isinstance(data, str):
            return False
        s = data.strip()
        return bool(s) and (s in self.all_ethnicities)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


@register_generator("blood_type")
class BloodTypeGenerator(DataGenerator):
    """血型生成器

    生成A/B/AB/O四种血型，支持Rh因子
    """

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self._setup()

    def _setup(self) -> None:
        """初始化血型数据"""
        self.blood_types = ["A", "B", "AB", "O"]
        self.rh_factors = ["+", "-"]

        # 中国人群血型分布比例（近似）
        self.china_distribution = {"A": 0.28, "B": 0.24, "AB": 0.07, "O": 0.41}

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个血型"""
        include_rh = self.config.parameters.get("rh", False)
        format_type = self.config.parameters.get("format", "SIMPLE").upper()

        # 根据分布比例选择血型
        blood_type = random.choices(
            list(self.china_distribution.keys()),
            weights=list(self.china_distribution.values()),
        )[0]

        if include_rh:
            # Rh因子分布：85% Rh+，15% Rh-
            rh_factor = "+" if random.random() < 0.85 else "-"
            blood_type = f"{blood_type}型{rh_factor}"
        else:
            if format_type == "FORMAL":
                blood_type = f"{blood_type}型血"
            else:
                blood_type = f"{blood_type}型"

        return blood_type

    def validate(self, data: str) -> bool:
        """验证血型是否有效"""
        if not isinstance(data, str):
            return False

        s = data.strip().upper()
        if not s:
            return False

        # 检查基本格式
        valid_patterns = ["A", "B", "AB", "O"]
        for pattern in valid_patterns:
            if pattern in s:
                return True

        return False

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


# 注意：这个类已被 dataforge/generators/basic/marital_status.py 中的实现替代
# @register_generator("marital_status")  # 移除重复注册
class MaritalStatusGeneratorLegacy(DataGenerator):
    """婚姻状况生成器

    生成婚姻状况，支持不同年龄段的真实分布
    """

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self._setup()

    def _setup(self) -> None:
        """初始化婚姻状况数据"""
        # 不同年龄段的中国婚姻状况分布（近似）
        self.age_distribution = {
            "YOUNG": {  # 18-25岁
                "未婚": 0.85,
                "已婚": 0.12,
                "离异": 0.02,
                "丧偶": 0.01,
            },
            "MIDDLE": {  # 26-35岁
                "未婚": 0.35,
                "已婚": 0.60,
                "离异": 0.04,
                "丧偶": 0.01,
            },
            "OLD": {  # 36-50岁
                "未婚": 0.15,
                "已婚": 0.75,
                "离异": 0.08,
                "丧偶": 0.02,
            },
            "ELDERLY": {  # 50岁以上
                "未婚": 0.05,
                "已婚": 0.75,
                "离异": 0.08,
                "丧偶": 0.12,
            },
        }

        self.english_status = {
            "未婚": "Single",
            "已婚": "Married",
            "离异": "Divorced",
            "丧偶": "Widowed",
        }

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个婚姻状况"""
        age_group = self.config.parameters.get("age_group", "MIDDLE").upper()
        format_type = self.config.parameters.get("format", "CHINESE").upper()

        # 确定年龄组
        if age_group not in self.age_distribution:
            age_group = "MIDDLE"

        distribution = self.age_distribution[age_group]
        status = random.choices(
            list(distribution.keys()), weights=list(distribution.values())
        )[0]

        if format_type == "ENGLISH":
            return self.english_status.get(status, status)
        else:
            return status

    def validate(self, data: str) -> bool:
        """验证婚姻状况是否有效"""
        valid_status = [
            "未婚",
            "已婚",
            "离异",
            "丧偶",
            "Single",
            "Married",
            "Divorced",
            "Widowed",
        ]
        if not isinstance(data, str):
            return False
        s = data.strip()
        return bool(s) and (s in valid_status)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []
