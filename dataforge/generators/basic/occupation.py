#!/usr/bin/env python3
"""
职业/职位信息生成器

提供基于中国职业分类大典的职业信息生成，支持多行业、多级别配置
"""

import random
from typing import Optional

from dataforge.core.context import GenerationContext
from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GeneratorConfig

from ...core.types import GeneratorType


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
        # 行业分类
        self.industries = {
            "IT": {
                "name": "IT/互联网",
                "positions": {
                    "SENIOR": [
                        "技术总监",
                        "架构师",
                        "CTO",
                        "技术VP",
                        "研发总监",
                        "产品总监",
                        "设计总监",
                        "测试总监",
                        "运维总监",
                    ],
                    "MIDDLE": [
                        "高级工程师",
                        "技术经理",
                        "产品经理",
                        "项目经理",
                        "测试经理",
                        "运维经理",
                        "数据分析师",
                        "UI设计师",
                    ],
                    "JUNIOR": [
                        "软件工程师",
                        "前端工程师",
                        "后端工程师",
                        "测试工程师",
                        "运维工程师",
                        "产品助理",
                        "UI设计师",
                        "数据分析师",
                    ],
                    "INTERN": [
                        "软件开发实习生",
                        "前端实习生",
                        "后端实习生",
                        "测试实习生",
                        "产品实习生",
                        "设计实习生",
                        "运维实习生",
                    ],
                },
            },
            "FINANCE": {
                "name": "金融",
                "positions": {
                    "SENIOR": [
                        "投资总监",
                        "风控总监",
                        "财务总监",
                        "CFO",
                        "基金经理",
                        "投行总监",
                        "资产管理总监",
                        "合规总监",
                    ],
                    "MIDDLE": [
                        "投资经理",
                        "风控经理",
                        "财务经理",
                        "基金经理助理",
                        "投行经理",
                        "资产管理经理",
                        "合规经理",
                    ],
                    "JUNIOR": [
                        "投资分析师",
                        "风控专员",
                        "财务分析师",
                        "基金会计",
                        "投行分析师",
                        "资产管理专员",
                        "合规专员",
                    ],
                    "INTERN": [
                        "投资实习生",
                        "风控实习生",
                        "财务实习生",
                        "基金实习生",
                        "投行实习生",
                        "资产管理实习生",
                        "合规实习生",
                    ],
                },
            },
            "RETAIL": {
                "name": "零售",
                "positions": {
                    "SENIOR": [
                        "运营总监",
                        "市场总监",
                        "销售总监",
                        "采购总监",
                        "电商总监",
                        "品牌总监",
                        "供应链总监",
                    ],
                    "MIDDLE": [
                        "运营经理",
                        "市场经理",
                        "销售经理",
                        "采购经理",
                        "电商经理",
                        "品牌经理",
                        "供应链经理",
                    ],
                    "JUNIOR": [
                        "运营专员",
                        "市场专员",
                        "销售代表",
                        "采购专员",
                        "电商专员",
                        "品牌专员",
                        "供应链专员",
                    ],
                    "INTERN": [
                        "运营实习生",
                        "市场实习生",
                        "销售实习生",
                        "采购实习生",
                        "电商实习生",
                        "品牌实习生",
                        "供应链实习生",
                    ],
                },
            },
            "MANUFACTURING": {
                "name": "制造业",
                "positions": {
                    "SENIOR": [
                        "生产总监",
                        "质量总监",
                        "工程总监",
                        "设备总监",
                        "采购总监",
                        "供应链总监",
                        "厂长",
                    ],
                    "MIDDLE": [
                        "生产经理",
                        "质量经理",
                        "工程经理",
                        "设备经理",
                        "采购经理",
                        "供应链经理",
                        "车间主任",
                    ],
                    "JUNIOR": [
                        "生产主管",
                        "质量工程师",
                        "工艺工程师",
                        "设备工程师",
                        "采购工程师",
                        "供应链专员",
                        "班组长",
                    ],
                    "INTERN": [
                        "生产实习生",
                        "质量实习生",
                        "工程实习生",
                        "设备实习生",
                        "采购实习生",
                        "供应链实习生",
                    ],
                },
            },
            "EDUCATION": {
                "name": "教育",
                "positions": {
                    "SENIOR": [
                        "校长",
                        "副校长",
                        "教务主任",
                        "系主任",
                        "教研室主任",
                        "年级组长",
                        "学科组长",
                    ],
                    "MIDDLE": [
                        "高级教师",
                        "骨干教师",
                        "班主任",
                        "备课组长",
                        "教务老师",
                        "辅导员",
                        "培训师",
                    ],
                    "JUNIOR": [
                        "教师",
                        "助教",
                        "教务助理",
                        "辅导员助理",
                        "课程顾问",
                        "学习管理师",
                    ],
                    "INTERN": ["教师实习生", "助教实习生", "教务实习生"],
                },
            },
            "MEDICAL": {
                "name": "医疗",
                "positions": {
                    "SENIOR": [
                        "主任医师",
                        "副主任医师",
                        "科室主任",
                        "院长",
                        "护理部主任",
                        "药剂科主任",
                        "检验科主任",
                    ],
                    "MIDDLE": [
                        "主治医师",
                        "护士长",
                        "主管药师",
                        "主管检验师",
                        "医疗管理师",
                        "康复治疗师",
                    ],
                    "JUNIOR": [
                        "住院医师",
                        "护士",
                        "药师",
                        "检验师",
                        "康复治疗师",
                        "医疗助理",
                    ],
                    "INTERN": ["医师实习生", "护士实习生", "药师实习生"],
                },
            },
            "MEDIA": {
                "name": "传媒",
                "positions": {
                    "SENIOR": [
                        "主编",
                        "总监",
                        "制片人",
                        "导演",
                        "总编",
                        "策划总监",
                        "运营总监",
                    ],
                    "MIDDLE": [
                        "编辑",
                        "记者",
                        "编导",
                        "策划",
                        "摄影师",
                        "设计师",
                        "运营经理",
                    ],
                    "JUNIOR": [
                        "助理编辑",
                        "实习记者",
                        "摄影助理",
                        "设计助理",
                        "新媒体专员",
                        "内容专员",
                    ],
                    "INTERN": ["编辑实习生", "记者实习生", "摄影实习生"],
                },
            },
        }

        # 通用职位（不指定行业）
        self.generic_positions = {
            "SENIOR": [
                "总监",
                "经理",
                "主管",
                "主任",
                "负责人",
                "首席",
                "专家",
                "顾问",
                "合伙人",
            ],
            "MIDDLE": [
                "经理",
                "主管",
                "专员",
                "工程师",
                "分析师",
                "设计师",
                "培训师",
                "咨询师",
            ],
            "JUNIOR": [
                "助理",
                "专员",
                "实习生",
                "助理工程师",
                "初级专员",
                "见习生",
                "学员",
                "练习生",
            ],
            "INTERN": ["实习生", "见习生", "助理实习生", "暑期实习生"],
        }

        # 部门分类
        self.departments = {
            "IT": ["技术部", "研发部", "产品部", "测试部", "运维部", "数据部"],
            "FINANCE": ["财务部", "投资部", "风控部", "审计部", "基金部", "投行部"],
            "RETAIL": ["运营部", "市场部", "销售部", "采购部", "客服部", "电商部"],
            "MANUFACTURING": [
                "生产部",
                "质量部",
                "工程部",
                "设备部",
                "采购部",
                "供应链部",
            ],
            "EDUCATION": ["教学部", "教务部", "学生部", "行政部", "教研部", "培训部"],
            "MEDICAL": ["医务部", "护理部", "药剂科", "检验科", "行政部", "后勤部"],
            "MEDIA": ["编辑部", "记者部", "策划部", "设计部", "运营部", "新媒体部"],
        }

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成职业/职位信息"""
        # 获取参数
        industry = self.config.parameters.get("industry", "ANY").upper()
        level = self.config.parameters.get("level", "ALL").upper()
        department = self.config.parameters.get("department", False)
        format_type = self.config.parameters.get("format", "CHINESE").upper()

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
        translation_map = {
            # IT行业
            "技术总监": "Technical Director",
            "架构师": "Architect",
            "CTO": "CTO",
            "技术VP": "VP of Technology",
            "研发总监": "R&D Director",
            "产品总监": "Product Director",
            "设计总监": "Design Director",
            "测试总监": "QA Director",
            "运维总监": "Operations Director",
            "高级工程师": "Senior Engineer",
            "技术经理": "Technical Manager",
            "产品经理": "Product Manager",
            "项目经理": "Project Manager",
            "测试经理": "QA Manager",
            "运维经理": "Operations Manager",
            "数据分析师": "Data Analyst",
            "UI设计师": "UI Designer",
            "软件工程师": "Software Engineer",
            "前端工程师": "Frontend Engineer",
            "后端工程师": "Backend Engineer",
            "测试工程师": "QA Engineer",
            "运维工程师": "DevOps Engineer",
            "产品助理": "Product Assistant",
            "软件开发实习生": "Software Development Intern",
            "前端实习生": "Frontend Intern",
            "后端实习生": "Backend Intern",
            "测试实习生": "QA Intern",
            "产品实习生": "Product Intern",
            "设计实习生": "Design Intern",
            "运维实习生": "Operations Intern",
            # 教育行业
            "校长": "Principal",
            "副校长": "Vice Principal",
            "教务主任": "Academic Director",
            "系主任": "Department Head",
            "教研室主任": "Research Director",
            "年级组长": "Grade Leader",
            "学科组长": "Subject Leader",
            "高级教师": "Senior Teacher",
            "骨干教师": "Key Teacher",
            "班主任": "Class Teacher",
            "备课组长": "Lesson Prep Leader",
            "教务老师": "Academic Teacher",
            "辅导员": "Counselor",
            "培训师": "Trainer",
            "教师": "Teacher",
            "助教": "Teaching Assistant",
            "教务助理": "Academic Assistant",
            "辅导员助理": "Counselor Assistant",
            "课程顾问": "Course Consultant",
            "学习管理师": "Learning Manager",
            "教师实习生": "Teacher Intern",
            "助教实习生": "TA Intern",
            "教务实习生": "Academic Intern",
            # 通用职位
            "总监": "Director",
            "经理": "Manager",
            "主管": "Supervisor",
            "专员": "Specialist",
            "助理": "Assistant",
            "实习生": "Intern",
        }
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

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个职业信息"""
        # 支持language参数（兼容性）
        language = self.parameters.get("language", "").lower()

        # 如果没有指定行业，随机选择一个
        industry = self.parameters.get("industry", "").upper()
        if not industry or industry not in self.industries:
            industry = random.choice(list(self.industries.keys()))

        # 如果没有指定级别，随机选择一个
        level = self.parameters.get("level", "").upper()
        positions = self.industries[industry]["positions"]
        if not level or level not in positions:
            level = random.choice(list(positions.keys()))

        position = random.choice(positions[level])

        # 根据language参数转换为英文
        if language == "english":
            return self._to_english(position)

        return position

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
        english_positions = [
            "Technical Director",
            "Architect",
            "CTO",
            "VP of Technology",
            "R&D Director",
            "Product Director",
            "Design Director",
            "QA Director",
            "Operations Director",
            "Senior Engineer",
            "Technical Manager",
            "Product Manager",
            "Project Manager",
            "QA Manager",
            "Operations Manager",
            "Data Analyst",
            "UI Designer",
            "Software Engineer",
            "Frontend Engineer",
            "Backend Engineer",
            "QA Engineer",
            "DevOps Engineer",
            "Product Assistant",
            "Doctor",
            "Nurse",
            "Engineer",
            "Manager",
            "Director",
            "Supervisor",
            "Specialist",
            "Assistant",
            "Intern",
            "Professional",
            "Teacher",
            "Principal",
            "Academic Director",
        ]

        if value in english_positions:
            return True

        # 检查是否包含常见职业关键词（更宽松的验证）
        common_keywords = [
            "工程师",
            "经理",
            "总监",
            "主管",
            "专员",
            "助理",
            "实习生",
            "医生",
            "医师",
            "护士",
            "教师",
            "老师",
            "校长",
            "主任",
            "分析师",
            "设计师",
            "顾问",
            "师",
            "长",
            "员",
        ]

        if any(keyword in value for keyword in common_keywords):
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

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
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
