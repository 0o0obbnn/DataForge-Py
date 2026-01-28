"""
职业/职位生成器配置加载器
提供配置文件的加载和缓存功能
"""

import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# 配置缓存
_config_cache: dict[str, Any] = {}


def _get_resource_path(filename: str) -> Path:
    """获取资源文件的绝对路径

    Args:
        filename: 资源文件名

    Returns:
        Path: 资源文件的绝对路径
    """
    current_dir = Path(__file__).parent
    return current_dir / filename


def _load_default_config() -> dict[str, Any]:
    """加载默认配置（硬编码的fallback数据）

    Returns:
        dict: 默认配置数据
    """
    return {
        "industries": {
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
                "departments": [
                    "技术部",
                    "研发部",
                    "产品部",
                    "测试部",
                    "运维部",
                    "数据部",
                ],
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
                "departments": [
                    "财务部",
                    "投资部",
                    "风控部",
                    "审计部",
                    "基金部",
                    "投行部",
                ],
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
                "departments": [
                    "运营部",
                    "市场部",
                    "销售部",
                    "采购部",
                    "客服部",
                    "电商部",
                ],
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
                "departments": [
                    "生产部",
                    "质量部",
                    "工程部",
                    "设备部",
                    "采购部",
                    "供应链部",
                ],
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
                "departments": [
                    "教学部",
                    "教务部",
                    "学生部",
                    "行政部",
                    "教研部",
                    "培训部",
                ],
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
                "departments": [
                    "医务部",
                    "护理部",
                    "药剂科",
                    "检验科",
                    "行政部",
                    "后勤部",
                ],
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
                "departments": [
                    "编辑部",
                    "记者部",
                    "策划部",
                    "设计部",
                    "运营部",
                    "新媒体部",
                ],
            },
        },
        "generic_positions": {
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
        },
        "translations": {
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
            "总监": "Director",
            "经理": "Manager",
            "主管": "Supervisor",
            "专员": "Specialist",
            "助理": "Assistant",
            "实习生": "Intern",
        },
        "common_keywords": [
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
        ],
    }


@lru_cache(maxsize=1)
def load_occupation_config(locale: str = "zh_CN") -> dict[str, Any]:
    """加载职业/职位生成器配置

    使用LRU缓存确保配置只加载一次，提高性能。
    如果配置文件不存在或加载失败，会回退到默认配置。

    Args:
        locale: 语言环境，默认为 "zh_CN"

    Returns:
        dict: 配置数据，包含以下键：
            - industries: 行业分类字典
            - generic_positions: 通用职位字典
            - translations: 翻译映射字典
            - common_keywords: 常见关键词列表
    """
    cache_key = f"occupation_{locale}"

    # 检查缓存
    if cache_key in _config_cache:
        return _config_cache[cache_key]  # type: ignore

    # 根据locale选择配置文件
    if locale == "zh_CN":
        config_file = "occupation_zh.yaml"
    else:
        # 其他语言环境暂不支持，使用默认配置
        logger.warning(f"Locale {locale} not supported, using default config")
        default_config = _load_default_config()
        _config_cache[cache_key] = default_config
        return default_config

    config_path = _get_resource_path(config_file)

    # 尝试加载配置文件
    try:
        if not config_path.exists():
            logger.warning(
                f"Config file not found: {config_path}, using default config"
            )
            default_config = _load_default_config()
            _config_cache[cache_key] = default_config
            return default_config

        with open(config_path, encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)

        # 验证和提取配置
        if not isinstance(yaml_data, dict):
            raise ValueError("YAML root must be a dictionary")

        occupation_config = yaml_data.get("occupation", {})

        if not occupation_config:
            logger.warning("Config file missing 'occupation' key, using default config")
            default_config = _load_default_config()
            _config_cache[cache_key] = default_config
            return default_config

        # 验证必需字段
        config = {
            "industries": occupation_config.get("industries", {}),
            "generic_positions": occupation_config.get("generic_positions", {}),
            "translations": occupation_config.get("translations", {}),
            "common_keywords": occupation_config.get("common_keywords", []),
        }

        # 如果配置不完整，使用默认值补充
        default_config = _load_default_config()
        if not config["industries"]:
            logger.warning("No industries in config, using default")
            config["industries"] = default_config["industries"]
        if not config["generic_positions"]:
            logger.warning("No generic_positions in config, using default")
            config["generic_positions"] = default_config["generic_positions"]
        if not config["translations"]:
            logger.warning("No translations in config, using default")
            config["translations"] = default_config["translations"]
        if not config["common_keywords"]:
            logger.warning("No common_keywords in config, using default")
            config["common_keywords"] = default_config["common_keywords"]

        # 为每个行业添加 departments（如果配置中有）
        for industry_key in config["industries"]:
            if "departments" not in config["industries"][industry_key]:
                # 从配置文件中获取 departments
                industry_data = occupation_config.get("industries", {}).get(
                    industry_key, {}
                )
                if "departments" in industry_data:
                    config["industries"][industry_key]["departments"] = industry_data[
                        "departments"
                    ]
                elif industry_key in default_config["industries"]:
                    config["industries"][industry_key]["departments"] = default_config[
                        "industries"
                    ][industry_key].get("departments", [])

        # 缓存配置
        _config_cache[cache_key] = config
        logger.info(f"Loaded occupation config from {config_path}")
        return config

    except yaml.YAMLError as e:
        logger.error(f"Failed to parse YAML config: {e}, using default config")
        default_config = _load_default_config()
        _config_cache[cache_key] = default_config
        return default_config
    except Exception as e:
        logger.error(f"Failed to load config: {e}, using default config")
        default_config = _load_default_config()
        _config_cache[cache_key] = default_config
        return default_config


def clear_config_cache() -> None:
    """清除配置缓存（主要用于测试）"""
    global _config_cache
    _config_cache.clear()
    load_occupation_config.cache_clear()
