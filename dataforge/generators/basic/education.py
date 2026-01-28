#!/usr/bin/env python3
"""
教育水平/学历信息生成器

提供中国教育体系和国际教育体系的学历信息生成，支持多种学历级别和格式
"""

import random

from dataforge.core.context import GenerationContext
from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GeneratorConfig
from dataforge.core.types import GeneratorType

from ...resources.education_loader import load_education_config


@register_generator("education")
class EducationGenerator(DataGenerator):
    """教育水平/学历信息生成器

    支持中国教育体系和国际教育体系的学历信息生成

    中国教育体系：
    - PRIMARY: 小学
    - JUNIOR: 初中
    - HIGH: 高中/中专/技校
    - UNIVERSITY: 大学/本科
    - MASTER: 硕士
    - PHD: 博士

    国际教育体系：
    - HIGH_SCHOOL: 高中
    - BACHELOR: 学士
    - MASTER: 硕士
    - PHD: 博士
    - POSTDOC: 博士后
    """

    def __init__(self, config: GeneratorConfig | None = None):
        # 如果没有提供config，创建一个默认的
        if config is None:
            config = GeneratorConfig(generator_type="education", parameters={})
        super().__init__(config)
        self._setup()

    def _setup(self) -> None:
        """初始化教育数据"""
        # 从配置文件加载数据（支持locale参数，默认为zh_CN）
        locale = self.parameters.get("locale", "zh_CN")
        config = load_education_config(locale=locale)

        # 中国教育体系（从配置文件加载）
        self.china_system = config.get("china_system", {})

        # 国际教育体系（从配置文件加载）
        self.international_system = config.get("international_system", {})

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个学历信息"""
        # 支持language参数（兼容性）
        language = self.parameters.get("language", "").lower()
        if language == "chinese":
            system = "CHINA"
        elif language == "english":
            system = "INTERNATIONAL"
        else:
            system = self.parameters.get("system", "CHINA").upper()

        level = self.parameters.get("level", "UNIVERSITY").upper()
        format_type = self.parameters.get("format", "DEGREE").upper()

        if system == "CHINA":
            system_data = self.china_system
        elif system == "INTERNATIONAL":
            system_data = self.international_system
        else:
            system_data = self.china_system

        # 如果指定的级别不存在，使用默认级别
        if level not in system_data:
            level = "UNIVERSITY" if system == "CHINA" else "BACHELOR"

        level_data = system_data[level]

        if format_type == "SCHOOL":
            return random.choice(level_data["schools"])
        elif format_type == "FULL":
            degree = random.choice(level_data["degrees"])
            school = random.choice(level_data["schools"])
            return f"{degree} - {school}"
        else:  # DEGREE
            return random.choice(level_data["degrees"])

    def validate(self, data: str) -> bool:
        """验证学历信息是否有效"""
        if not isinstance(data, str):
            return False

        data = data.strip()
        if not data:
            return False

        # 检查是否包含有效的学历或学校名称
        all_valid_parts = []
        for system in [self.china_system, self.international_system]:
            for level_data in system.values():
                all_valid_parts.extend(level_data["degrees"])
                all_valid_parts.extend(level_data["schools"])

        # 检查是否是直接的学历或学校名称
        if data in all_valid_parts:
            return True

        # 检查组合格式（如"Master's Degree - Stanford University"）
        parts = data.split(" - ")
        if len(parts) == 2:
            degree_part, school_part = parts[0].strip(), parts[1].strip()

            # 检查degree部分是否有效
            valid_degrees = []
            for system in [self.china_system, self.international_system]:
                for level_data in system.values():
                    valid_degrees.extend(level_data["degrees"])

            # 检查school部分是否有效
            valid_schools = []
            for system in [self.china_system, self.international_system]:
                for level_data in system.values():
                    valid_schools.extend(level_data["schools"])

            return degree_part in valid_degrees and school_part in valid_schools

        return False

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["system", "level", "format", "locale", "language"]


@register_generator("generic_education")
class GenericEducationGenerator(DataGenerator):
    """通用教育生成器

    生成通用的教育水平信息
    """

    def __init__(self, config: GeneratorConfig | None = None):
        # 如果没有提供config，创建一个默认的
        if config is None:
            config = GeneratorConfig(generator_type="education", parameters={})
        super().__init__(config)
        self._setup()

    def _setup(self) -> None:
        """初始化通用教育数据"""
        # 从配置文件加载数据（支持locale参数，默认为zh_CN）
        locale = self.parameters.get("locale", "zh_CN")
        config = load_education_config(locale=locale)

        # 通用教育水平（从配置文件加载）
        generic_levels = config.get("generic_levels", {})
        self.education_levels = generic_levels.get("chinese", [])
        self.international_levels = generic_levels.get("english", [])

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个通用教育水平"""
        format_type = self.parameters.get("format", "CHINESE").upper()

        if format_type == "ENGLISH":
            return random.choice(self.international_levels)
        else:
            return random.choice(self.education_levels)

    def validate(self, data: str) -> bool:
        """验证教育水平是否有效"""
        if not isinstance(data, str):
            return False
        all_levels = self.education_levels + self.international_levels
        s = data.strip()
        return bool(s) and (s in all_levels)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["system", "level", "format", "locale", "language"]
