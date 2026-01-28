"""
金融数据配置加载器
提供配置文件的加载和缓存功能
"""

import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


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
        "stock_symbols": {
            "US": ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "NVDA", "META"],
            "CHINA": [
                "000001",
                "000002",
                "600000",
                "600036",
                "600519",
                "000858",
                "002415",
            ],
        },
        "etf_option_symbols": {
            "CHINA": ["510050", "510300", "159915", "510500"],
        },
        "currencies": ["USD", "EUR", "CNY", "JPY", "GBP", "AUD", "CAD", "HKD", "SGD"],
        "currency_symbols": {
            "CNY": "¥",
            "USD": "$",
            "EUR": "€",
            "JPY": "¥",
            "GBP": "£",
            "AUD": "A$",
            "CAD": "C$",
            "HKD": "HK$",
            "SGD": "S$",
        },
        "tenors": ["1M", "3M", "6M", "1Y", "2Y", "5Y"],
        "stock_futures": {
            "CHINA": ["IF", "IC", "IH", "TF", "TS"],
        },
        "commodity_futures": {
            "CU": "沪铜",
            "AL": "沪铝",
            "ZN": "沪锌",
            "PB": "沪铅",
            "AU": "沪金",
            "AG": "沪银",
            "RB": "螺纹钢",
            "HC": "热卷",
            "SC": "原油",
            "FU": "燃料油",
            "BU": "沥青",
            "RU": "橡胶",
        },
    }


@lru_cache(maxsize=1)
def load_finance_data_config(locale: str = "zh_CN") -> dict[str, Any]:
    """加载金融数据配置

    Args:
        locale: 语言环境，默认 zh_CN

    Returns:
        dict: 金融数据配置字典
    """
    config_file = _get_resource_path("finance_data.yaml")

    try:
        if config_file.exists():
            with open(config_file, encoding="utf-8") as f:
                config_data = yaml.safe_load(f)  # type: ignore

            if config_data and "finance" in config_data:
                finance_config = config_data["finance"]

                # 验证并返回配置
                result = {
                    "stock_symbols": finance_config.get("stock_symbols", {}),
                    "etf_option_symbols": finance_config.get("etf_option_symbols", {}),
                    "currencies": finance_config.get("currencies", []),
                    "currency_symbols": finance_config.get("currency_symbols", {}),
                    "tenors": finance_config.get("tenors", []),
                    "stock_futures": finance_config.get("stock_futures", {}),
                    "commodity_futures": finance_config.get("commodity_futures", {}),
                }

                # 补充缺失的键
                default_config = _load_default_config()
                for key in default_config:
                    if key not in result or not result[key]:
                        result[key] = default_config[key]
                        logger.warning(
                            f"Missing key '{key}' in finance_data.yaml, using default"
                        )

                logger.info(
                    f"Successfully loaded finance data config from {config_file}"
                )
                return result
            else:
                logger.warning(
                    "Invalid structure in finance_data.yaml, using default config"
                )
                return _load_default_config()
        else:
            logger.warning(
                f"Finance data config file not found: {config_file}, using default config"
            )
            return _load_default_config()
    except Exception as e:
        logger.error(f"Error loading finance data config: {e}, using default config")
        return _load_default_config()


def clear_config_cache() -> None:
    """清除配置缓存（主要用于测试）"""
    load_finance_data_config.cache_clear()
