"""
企业名称生成器配置加载器
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
    # 获取当前模块所在目录
    current_dir = Path(__file__).parent
    return current_dir / filename


def _load_default_config() -> dict[str, Any]:
    """加载默认配置（硬编码的fallback数据）

    Returns:
        dict: 默认配置数据
    """
    return {
        "regions": [
            "北京",
            "上海",
            "深圳",
            "广州",
            "杭州",
            "苏州",
            "成都",
            "武汉",
            "西安",
            "南京",
            "天津",
            "重庆",
            "青岛",
            "大连",
            "宁波",
            "厦门",
            "长沙",
            "郑州",
            "无锡",
            "佛山",
            "东莞",
            "合肥",
            "昆明",
            "福州",
            "哈尔滨",
            "济南",
            "长春",
            "石家庄",
            "常州",
            "嘉兴",
        ],
        "industry_keywords": {
            "IT": [
                "科技",
                "信息",
                "网络",
                "软件",
                "数据",
                "云计算",
                "智能",
                "互联网",
                "电子",
                "通信",
                "技术",
                "系统",
                "平台",
                "数字",
                "创新",
                "智慧",
            ],
            "FINANCE": [
                "金融",
                "投资",
                "资本",
                "财富",
                "基金",
                "证券",
                "银行",
                "保险",
                "资产",
                "理财",
                "信托",
                "租赁",
                "担保",
                "小贷",
                "支付",
                "金服",
            ],
            "RETAIL": [
                "商贸",
                "贸易",
                "销售",
                "零售",
                "批发",
                "商城",
                "购物",
                "百货",
                "超市",
                "连锁",
                "专卖",
                "代理",
                "经销",
                "营销",
                "电商",
                "商业",
            ],
            "MANUFACTURING": [
                "制造",
                "生产",
                "工业",
                "机械",
                "设备",
                "加工",
                "装备",
                "重工",
                "轻工",
                "化工",
                "材料",
                "能源",
                "环保",
                "新材料",
                "精密",
                "自动化",
            ],
            "EDUCATION": [
                "教育",
                "培训",
                "学校",
                "学院",
                "大学",
                "研究",
                "科研",
                "学术",
                "文化",
                "艺术",
                "体育",
                "健康",
                "医疗",
                "咨询",
                "服务",
                "管理",
            ],
            "REAL_ESTATE": [
                "房地产",
                "地产",
                "置业",
                "物业",
                "建设",
                "建筑",
                "工程",
                "装饰",
                "设计",
                "规划",
                "开发",
                "投资",
                "置地",
                "城建",
                "基建",
                "园区",
            ],
        },
        "general_keywords": [
            "华",
            "中",
            "国",
            "民",
            "天",
            "地",
            "人",
            "和",
            "信",
            "诚",
            "德",
            "正",
            "金",
            "银",
            "宝",
            "珠",
            "玉",
            "龙",
            "凤",
            "麒",
            "麟",
            "鹤",
            "鹏",
            "燕",
            "东",
            "西",
            "南",
            "北",
            "中",
            "上",
            "下",
            "大",
            "小",
            "新",
            "老",
            "古",
            "春",
            "夏",
            "秋",
            "冬",
            "晨",
            "晚",
            "阳",
            "月",
            "星",
            "云",
            "海",
            "山",
            "兴",
            "发",
            "达",
            "通",
            "顺",
            "盛",
            "昌",
            "泰",
            "安",
            "康",
            "富",
            "贵",
            "美",
            "好",
            "优",
            "佳",
            "精",
            "品",
            "质",
            "高",
            "尚",
            "雅",
            "洁",
            "净",
        ],
        "company_types": {
            "CO_LTD": ["有限公司", "有限责任公司"],
            "GROUP": ["集团", "集团有限公司", "控股集团"],
            "INSTITUTE": ["研究所", "研究院", "技术研究院"],
            "CORP": ["公司", "企业", "实业"],
            "TECH": ["科技有限公司", "技术有限公司"],
            "TRADING": ["贸易有限公司", "商贸有限公司"],
            "INVESTMENT": ["投资有限公司", "资本管理有限公司"],
        },
    }


@lru_cache(maxsize=1)
def load_company_name_config(locale: str = "zh_CN") -> dict[str, Any]:
    """加载企业名称生成器配置

    使用LRU缓存确保配置只加载一次，提高性能。
    如果配置文件不存在或加载失败，会回退到默认配置。

    Args:
        locale: 语言环境，默认为 "zh_CN"

    Returns:
        dict: 配置数据，包含以下键：
            - regions: 地区列表
            - industry_keywords: 行业关键词字典
            - general_keywords: 通用关键词列表
            - company_types: 公司类型字典
    """
    cache_key = f"company_name_{locale}"

    # 检查缓存
    if cache_key in _config_cache:
        return _config_cache[cache_key]  # type: ignore

    # 根据locale选择配置文件
    if locale == "zh_CN":
        config_file = "company_name_zh.yaml"
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

        company_name_config = yaml_data.get("company_name", {})

        if not company_name_config:
            logger.warning(
                "Config file missing 'company_name' key, using default config"
            )
            default_config = _load_default_config()
            _config_cache[cache_key] = default_config
            return default_config

        # 验证必需字段
        config = {
            "regions": company_name_config.get("regions", []),
            "industry_keywords": company_name_config.get("industry_keywords", {}),
            "general_keywords": company_name_config.get("general_keywords", []),
            "company_types": company_name_config.get("company_types", {}),
        }

        # 如果配置不完整，使用默认值补充
        default_config = _load_default_config()
        if not config["regions"]:
            logger.warning("No regions in config, using default")
            config["regions"] = default_config["regions"]
        if not config["industry_keywords"]:
            logger.warning("No industry_keywords in config, using default")
            config["industry_keywords"] = default_config["industry_keywords"]
        if not config["general_keywords"]:
            logger.warning("No general_keywords in config, using default")
            config["general_keywords"] = default_config["general_keywords"]
        if not config["company_types"]:
            logger.warning("No company_types in config, using default")
            config["company_types"] = default_config["company_types"]

        # 缓存配置
        _config_cache[cache_key] = config
        logger.info(f"Loaded company name config from {config_path}")
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
    load_company_name_config.cache_clear()
