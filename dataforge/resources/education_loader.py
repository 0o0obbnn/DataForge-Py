"""
教育水平/学历生成器配置加载器
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
        "china_system": {
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
        },
        "international_system": {
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
        },
        "generic_levels": {
            "chinese": [
                "小学",
                "初中",
                "高中",
                "中专",
                "大专",
                "本科",
                "硕士",
                "博士",
                "博士后",
            ],
            "english": [
                "Primary School",
                "Secondary School",
                "High School",
                "Associate Degree",
                "Bachelor's Degree",
                "Master's Degree",
                "PhD",
                "Postdoc",
            ],
        },
    }


@lru_cache(maxsize=1)
def load_education_config(locale: str = "zh_CN") -> dict[str, Any]:
    """加载教育水平/学历生成器配置

    使用LRU缓存确保配置只加载一次，提高性能。
    如果配置文件不存在或加载失败，会回退到默认配置。

    Args:
        locale: 语言环境，默认为 "zh_CN"

    Returns:
        dict: 配置数据，包含以下键：
            - china_system: 中国教育体系字典
            - international_system: 国际教育体系字典
            - generic_levels: 通用教育水平字典
    """
    cache_key = f"education_{locale}"

    # 检查缓存
    if cache_key in _config_cache:
        return _config_cache[cache_key]  # type: ignore

    # 根据locale选择配置文件
    if locale == "zh_CN":
        config_file = "education_zh.yaml"
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

        education_config = yaml_data.get("education", {})

        if not education_config:
            logger.warning("Config file missing 'education' key, using default config")
            default_config = _load_default_config()
            _config_cache[cache_key] = default_config
            return default_config

        # 验证必需字段
        config = {
            "china_system": education_config.get("china_system", {}),
            "international_system": education_config.get("international_system", {}),
            "generic_levels": education_config.get("generic_levels", {}),
        }

        # 如果配置不完整，使用默认值补充
        default_config = _load_default_config()
        if not config["china_system"]:
            logger.warning("No china_system in config, using default")
            config["china_system"] = default_config["china_system"]
        if not config["international_system"]:
            logger.warning("No international_system in config, using default")
            config["international_system"] = default_config["international_system"]
        if not config["generic_levels"]:
            logger.warning("No generic_levels in config, using default")
            config["generic_levels"] = default_config["generic_levels"]

        # 缓存配置
        _config_cache[cache_key] = config
        logger.info(f"Loaded education config from {config_path}")
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
    load_education_config.cache_clear()
