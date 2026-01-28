#!/usr/bin/env python3
"""
职业/职位信息生成器

提供基于中国职业分类大典的职业信息生成，支持多行业、多级别配置
"""

import random

from dataforge.core.context import GenerationContext
from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GeneratorConfig

from ...core.types import GeneratorType
from ...resources.occupation_loader import load_occupation_config


@register_generator("occupation")
class OccupationGenerator(DataGenerator):
    """职业/职位信息生成器

    基于中国职业分类大典，支持以下行业：
    - IT: 互联网/科技行业
    - FINANCE: 金融/银行/投资
    - RETAIL: 零售/电商
    - MANUFACTURING: 制造业
    - EDUCATION: 教育行业
    - MEDICAL: 医疗行业
    - MEDIA: 传媒/广告

    支持级别：
    - SENIOR: 高级职位（总监、经理、专家）
    - MID: 中级职位（主管、工程师）
    - JUNIOR: 初级职位（专员、助理）
    - INTERN: 实习职位
    """

    def __init__(self, config: GeneratorConfig) -> None:
        super().__init__(config)
        self._setup()

    def _setup(self) -> None:
        """初始化职业数据"""
        # 从配置文件加载数据（支持locale参数，默认为zh_CN）
        locale = self.parameters.get("locale", "zh_CN")
        config = load_occupation_config(locale=locale)

        # 行业分类（从配置文件加载）
        self.industries = config.get("industries", {})

        # 如果配置中没有 industries，使用空字典（fallback 已在 loader 中处理）
        if not self.industries:
            self.industries = {}

        # 通用职位（不指定行业，从配置文件加载）
        self.generic_positions = config.get("generic_positions", {})

        # 如果配置中没有 generic_positions，使用空字典
        if not self.generic_positions:
            self.generic_positions = {}

        # 部门分类（从 industries 配置中提取）
        self.departments = {}
        for industry_key, industry_data in self.industries.items():
            if isinstance(industry_data, dict) and "departments" in industry_data:
                self.departments[industry_key] = industry_data["departments"]

        # 翻译映射（从配置文件加载）
        self.translations = config.get("translations", {})

        # 常见关键词（从配置文件加载，用于验证）
        self.common_keywords = config.get("common_keywords", [])

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        """生成职业/职位信息"""
        # 获取参数
        industry = self.config.parameters.get("industry", "ANY").upper()
        level = self.config.parameters.get("level", "ALL").upper()
        department = self.config.parameters.get("department", False)

        # 支持 format 和 language 参数（language 用于向后兼容）
        format_type = self.config.parameters.get("format", "CHINESE").upper()
        language = self.config.parameters.get("language", "").lower()

        # 如果指定了 language 参数，转换为 format
        if language == "english":
            format_type = "ENGLISH"
        elif language == "chinese":
            format_type = "CHINESE"

        # 确定行业
        if industry == "ANY":
            industry = random.choice(list(self.industries.keys()))

        # 确定级别
        if level == "ALL":
            level = random.choice(["SENIOR", "MIDDLE", "JUNIOR", "INTERN"])

        # 获取职位列表
        if industry in self.industries:
            positions = self.industries[industry]["positions"][level]
        else:
            positions = self.generic_positions[level]

        # 选择职位
        position = random.choice(positions)

        # 添加部门信息
        if department and industry in self.departments:
            dept = random.choice(self.departments[industry])
            position = f"{dept}{position}"

        # 格式化输出
        if format_type == "ENGLISH":
            return self._to_english(position)
        elif format_type == "MIXED":
            if random.random() < 0.5:
                return self._to_english(position)
            else:
                return position
        else:  # CHINESE
            return position

    def _to_english(self, chinese_position: str) -> str:
        """转换为英文职位"""
        # 使用配置文件中的翻译映射
        translation_map = self.translations

        # 如果找不到精确匹配，尝试部分匹配
        result = translation_map.get(chinese_position)
        if result:
            return result

        # 尝试部分匹配（如果包含某些关键词）
        for cn, en in translation_map.items():
            if cn in chinese_position:
                return en

        # 如果都找不到，生成一个通用的英文职位
        # 根据职位中的关键词进行简单翻译
        if "医师" in chinese_position or "医生" in chinese_position:
            return "Doctor"
        elif "护士" in chinese_position:
            return "Nurse"
        elif "工程师" in chinese_position:
            return "Engineer"
        elif "经理" in chinese_position:
            return "Manager"
        elif "总监" in chinese_position:
            return "Director"
        elif "主管" in chinese_position:
            return "Supervisor"
        elif "专员" in chinese_position:
            return "Specialist"
        elif "助理" in chinese_position:
            return "Assistant"
        elif "实习生" in chinese_position:
            return "Intern"

        # 最后返回通用职位
        return "Professional"

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个职业信息"""
        # 使用 _generate_raw 方法生成，它已经处理了所有参数
        return self._generate_raw(context)

    def validate(self, data: str) -> bool:
        """验证职业信息是否有效"""
        if not isinstance(data, str):
            return False

        value = data.strip()
        if not value or len(value) < 2:
            return False

        # 检查是否在任何一个行业的职位列表中（中文）
        for industry_data in self.industries.values():
            for level_positions in industry_data["positions"].values():
                if value in level_positions:
                    return True

        # 检查是否是英文职位（通过翻译映射）
        english_positions = list(self.translations.values())

        if value in english_positions:
            return True

        # 检查是否包含常见职业关键词（更宽松的验证，使用配置文件中的关键词）
        if any(keyword in value for keyword in self.common_keywords):
            return True

        return False

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["industry", "level", "department", "format", "locale", "language"]


@register_generator("generic_occupation")
class GenericOccupationGenerator(DataGenerator):
    """通用职业生成器

    生成通用的职业信息，不区分行业
    """

    def __init__(self, config: GeneratorConfig) -> None:
        super().__init__(config)
        self._setup()

    def _setup(self) -> None:
        """初始化通用职业数据"""
        self.occupations = [
            "软件工程师",
            "医生",
            "教师",
            "会计师",
            "律师",
            "设计师",
            "销售经理",
            "项目经理",
            "运营专员",
            "人力资源",
            "市场营销",
            "产品经理",
            "数据分析师",
            "客服专员",
            "行政助理",
            "记者",
            "摄影师",
            "厨师",
            "司机",
            "工人",
            "农民",
            "商人",
            "公务员",
            "军人",
            "警察",
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个通用职业信息"""
        return random.choice(self.occupations)

    def validate(self, data: str) -> bool:
        """验证通用职业信息是否有效"""
        return bool(
            isinstance(data, str) and data.strip() and data.strip() in self.occupations
        )

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        # TODO: 根据实际参数更新此列表
        return []
