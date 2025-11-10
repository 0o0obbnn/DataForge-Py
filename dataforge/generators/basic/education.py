from ...core.types import GeneratorType

#!/usr/bin/env python3
"""
教育水平/学历信息生成器

提供中国教育体系和国际教育体系的学历信息生成，支持多种学历级别和格式
"""

import random
from typing import Any, Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GeneratorConfig
from dataforge.core.context import GenerationContext


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

    def __init__(self, config: Optional[GeneratorConfig] = None):
        # 如果没有提供config，创建一个默认的
        if config is None:
            config = GeneratorConfig(
                generator_type="education",
                parameters={}
            )
        super().__init__(config)
        self._setup()

    def _setup(self) -> None:
        """初始化教育数据"""
        # 中国教育体系
        self.china_system = {
            "PRIMARY": {
                "name": "小学",
                "degrees": ["小学", "小学毕业", "小学学历"],
                "schools": ["中心小学", "实验小学", "第一小学", "第二小学"],
            },
            "JUNIOR": {
                "name": "初中",
                "degrees": ["初中", "初中毕业", "初中学历", "初中文凭"],
                "schools": ["第一中学", "第二中学", "实验中学", "初级中学"],
            },
            "HIGH": {
                "name": "高中/中专/技校",
                "degrees": ["高中", "高中毕业", "中专", "技校", "职高"],
                "schools": ["第一中学", "第二中学", "职业高中", "技工学校", "中专学校"],
            },
            "UNIVERSITY": {
                "name": "大学/本科",
                "degrees": ["本科", "学士", "大学本科", "本科学历"],
                "schools": [
                    "北京大学",
                    "清华大学",
                    "复旦大学",
                    "上海交通大学",
                    "浙江大学",
                    "南京大学",
                    "武汉大学",
                    "中山大学",
                    "华中科技大学",
                    "四川大学",
                    "吉林大学",
                    "山东大学",
                    "中南大学",
                    "西安交通大学",
                    "哈尔滨工业大学",
                ],
            },
            "MASTER": {
                "name": "硕士",
                "degrees": ["硕士", "硕士研究生", "研究生学历", "硕士学位"],
                "schools": [
                    "北京大学",
                    "清华大学",
                    "复旦大学",
                    "上海交通大学",
                    "浙江大学",
                    "南京大学",
                    "武汉大学",
                    "中山大学",
                    "华中科技大学",
                    "四川大学",
                ],
            },
            "PHD": {
                "name": "博士",
                "degrees": ["博士", "博士研究生", "博士学历", "博士学位"],
                "schools": [
                    "北京大学",
                    "清华大学",
                    "复旦大学",
                    "上海交通大学",
                    "浙江大学",
                    "南京大学",
                    "武汉大学",
                    "中山大学",
                    "华中科技大学",
                    "中国科学院",
                ],
            },
        }

        # 国际教育体系
        self.international_system = {
            "HIGH_SCHOOL": {
                "name": "高中",
                "degrees": ["High School", "High School Diploma", "Secondary School"],
                "schools": [
                    "Harvard-Westlake School",
                    "Phillips Exeter Academy",
                    "Choate Rosemary Hall",
                    "Lawrenceville School",
                    "Hotchkiss School",
                ],
            },
            "BACHELOR": {
                "name": "学士",
                "degrees": ["Bachelor", "Bachelor's Degree", "Undergraduate"],
                "schools": [
                    "Harvard University",
                    "Stanford University",
                    "MIT",
                    "Yale University",
                    "Princeton University",
                    "Columbia University",
                    "University of Chicago",
                    "University of Pennsylvania",
                    "Caltech",
                    "UC Berkeley",
                ],
            },
            "MASTER": {
                "name": "硕士",
                "degrees": ["Master", "Master's Degree", "Graduate"],
                "schools": [
                    "Harvard University",
                    "Stanford University",
                    "MIT",
                    "Yale University",
                    "Princeton University",
                    "Columbia University",
                    "University of Chicago",
                    "University of Pennsylvania",
                    "Caltech",
                    "UC Berkeley",
                ],
            },
            "PHD": {
                "name": "博士",
                "degrees": ["PhD", "Doctor", "Doctorate"],
                "schools": [
                    "Harvard University",
                    "Stanford University",
                    "MIT",
                    "Yale University",
                    "Princeton University",
                    "Columbia University",
                    "University of Chicago",
                    "University of Pennsylvania",
                    "Caltech",
                    "UC Berkeley",
                ],
            },
            "POSTDOC": {
                "name": "博士后",
                "degrees": [
                    "Postdoc",
                    "Postdoctoral Fellow",
                    "Postdoctoral Researcher",
                ],
                "schools": [
                    "Harvard University",
                    "Stanford University",
                    "MIT",
                    "Yale University",
                    "Princeton University",
                    "Columbia University",
                    "University of Chicago",
                ],
            },
        }

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
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
        return ["system", "level", "format"]
@register_generator("generic_education")
class GenericEducationGenerator(DataGenerator):
    """通用教育生成器

    生成通用的教育水平信息
    """

    def __init__(self, config: Optional[GeneratorConfig] = None):
        # 如果没有提供config，创建一个默认的
        if config is None:
            config = GeneratorConfig(
                generator_type="education",
                parameters={}
            )
        super().__init__(config)
        self._setup()

    def _setup(self) -> None:
        """初始化通用教育数据"""
        self.education_levels = [
            "小学",
            "初中",
            "高中",
            "中专",
            "大专",
            "本科",
            "硕士",
            "博士",
            "博士后",
        ]

        self.international_levels = [
            "Primary School",
            "Secondary School",
            "High School",
            "Associate Degree",
            "Bachelor's Degree",
            "Master's Degree",
            "PhD",
            "Postdoc",
        ]

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
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
        return ["system", "level", "format"]
