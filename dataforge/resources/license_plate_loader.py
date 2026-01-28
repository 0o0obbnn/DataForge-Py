"""
车牌号生成器配置加载器
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
        "provinces": {
            "京": "北京",
            "津": "天津",
            "冀": "河北",
            "晋": "山西",
            "蒙": "内蒙古",
            "辽": "辽宁",
            "吉": "吉林",
            "黑": "黑龙江",
            "沪": "上海",
            "苏": "江苏",
            "浙": "浙江",
            "皖": "安徽",
            "闽": "福建",
            "赣": "江西",
            "鲁": "山东",
            "豫": "河南",
            "鄂": "湖北",
            "湘": "湖南",
            "粤": "广东",
            "桂": "广西",
            "琼": "海南",
            "渝": "重庆",
            "川": "四川",
            "贵": "贵州",
            "云": "云南",
            "藏": "西藏",
            "陕": "陕西",
            "甘": "甘肃",
            "青": "青海",
            "宁": "宁夏",
            "新": "新疆",
        },
        "city_codes": list("ABCDEFGHJKLMNPQRSTUVWXYZ"),
        "plate_chars": list("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789"),
        "new_energy_prefixes": ["D", "F"],
    }


@lru_cache(maxsize=1)
def load_license_plate_config(locale: str = "zh_CN") -> dict[str, Any]:
    """加载车牌号生成器配置

    使用LRU缓存确保配置只加载一次，提高性能。
    如果配置文件不存在或加载失败，会回退到默认配置。

    Args:
        locale: 语言环境，默认为 "zh_CN"

    Returns:
        dict: 配置数据，包含以下键：
            - provinces: 省份简称映射字典
            - city_codes: 城市代码列表
            - plate_chars: 车牌字符列表
            - new_energy_prefixes: 新能源车牌前缀列表
    """
    cache_key = f"license_plate_{locale}"

    # 检查缓存
    if cache_key in _config_cache:
        return _config_cache[cache_key]  # type: ignore

    # 根据locale选择配置文件
    if locale == "zh_CN":
        config_file = "license_plate_zh.yaml"
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

        license_plate_config = yaml_data.get("license_plate", {})

        if not license_plate_config:
            logger.warning(
                "Config file missing 'license_plate' key, using default config"
            )
            default_config = _load_default_config()
            _config_cache[cache_key] = default_config
            return default_config

        # 验证必需字段
        config = {
            "provinces": license_plate_config.get("provinces", {}),
            "city_codes": license_plate_config.get("city_codes", []),
            "plate_chars": license_plate_config.get("plate_chars", []),
            "new_energy_prefixes": license_plate_config.get("new_energy_prefixes", []),
        }

        # 如果配置不完整，使用默认值补充
        default_config = _load_default_config()
        if not config["provinces"]:
            logger.warning("No provinces in config, using default")
            config["provinces"] = default_config["provinces"]
        if not config["city_codes"]:
            logger.warning("No city_codes in config, using default")
            config["city_codes"] = default_config["city_codes"]
        if not config["plate_chars"]:
            logger.warning("No plate_chars in config, using default")
            config["plate_chars"] = default_config["plate_chars"]
        if not config["new_energy_prefixes"]:
            logger.warning("No new_energy_prefixes in config, using default")
            config["new_energy_prefixes"] = default_config["new_energy_prefixes"]

        # 缓存配置
        _config_cache[cache_key] = config
        logger.info(f"Loaded license plate config from {config_path}")
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
    load_license_plate_config.cache_clear()
