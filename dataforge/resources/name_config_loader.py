"""
姓名与拼音配置加载器。

提供英文姓名与中文拼音映射的统一加载入口，带有安全的默认 fallback。
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)
_BASE_DIR = Path(__file__).parent


def _load_yaml(filename: str) -> dict[str, Any]:
    """加载 YAML 文件为字典，结构异常时返回空字典。"""
    path = _BASE_DIR / filename
    if not path.exists():
        logger.warning("Name config file not found: %s", path)
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception as exc:  # pragma: no cover - 极端 IO/解析错误
        logger.error("Error loading YAML %s: %s", path, exc)
        return {}
    if not isinstance(data, dict):
        logger.warning("Invalid YAML structure in %s", path)
        return {}
    return data


@lru_cache(maxsize=1)
def load_name_en_config() -> dict[str, list[str]]:
    """加载英文姓名配置。

    Returns:
        dict: 包含 first_names_male / first_names_female / last_names 的字典。
    """
    raw = _load_yaml("name_en.yaml").get("name_en", {})

    defaults = {
        "first_names_male": [
            "James",
            "John",
            "Robert",
            "Michael",
            "William",
            "David",
            "Richard",
            "Charles",
            "Joseph",
            "Thomas",
            "Christopher",
            "Daniel",
            "Paul",
            "Mark",
            "Donald",
            "Steven",
        ],
        "first_names_female": [
            "Mary",
            "Patricia",
            "Jennifer",
            "Linda",
            "Elizabeth",
            "Barbara",
            "Susan",
            "Jessica",
            "Sarah",
            "Karen",
            "Nancy",
            "Lisa",
            "Betty",
            "Helen",
            "Sandra",
            "Donna",
        ],
        "last_names": [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
            "Hernandez",
            "Lopez",
            "Gonzalez",
            "Wilson",
            "Anderson",
            "Thomas",
        ],
    }

    result: dict[str, list[str]] = {}
    for key, default_val in defaults.items():
        value = raw.get(key) or default_val
        if not isinstance(value, list):
            logger.warning("Invalid '%s' in name_en.yaml, using default", key)
            value = default_val
        result[key] = value
    return result


@lru_cache(maxsize=1)
def load_pinyin_map() -> dict[str, dict[str, str]]:
    """加载中文拼音映射配置。

    Returns:
        dict: {"surname": {...}, "given_char": {...}}
    """
    raw = _load_yaml("pinyin_map.yaml").get("pinyin_map", {})
    surname = raw.get("surname") or {}
    given_char = raw.get("given_char") or {}

    surname_default = {
        "张": "zhang",
        "王": "wang",
        "李": "li",
        "赵": "zhao",
        "刘": "liu",
        "陈": "chen",
        "杨": "yang",
        "黄": "huang",
        "周": "zhou",
        "吴": "wu",
        "徐": "xu",
        "孙": "sun",
        "胡": "hu",
        "朱": "zhu",
        "高": "gao",
        "林": "lin",
        "何": "he",
        "郭": "guo",
        "马": "ma",
        "罗": "luo",
    }
    given_default = {
        "伟": "wei",
        "强": "qiang",
        "磊": "lei",
        "军": "jun",
        "洋": "yang",
        "丽": "li",
        "美": "mei",
        "红": "hong",
        "燕": "yan",
        "芳": "fang",
        "嘉": "jia",
        "欣": "xin",
        "悦": "yue",
        "乐": "le",
        "安": "an",
        "志": "zhi",
        "建": "jian",
        "国": "guo",
        "华": "hua",
        "淑": "shu",
        "英": "ying",
        "娟": "juan",
        "敏": "min",
        "思": "si",
        "琪": "qi",
        "涵": "han",
        "萱": "xuan",
        "雅": "ya",
        "洁": "jie",
    }

    if not isinstance(surname, dict):
        surname = surname_default
    else:
        surname = {**surname_default, **surname}
    if not isinstance(given_char, dict):
        given_char = given_default
    else:
        given_char = {**given_default, **given_char}

    return {"surname": surname, "given_char": given_char}


def clear_name_config_cache() -> None:
    """清除姓名配置缓存（主要用于测试）。"""
    load_name_en_config.cache_clear()
    load_pinyin_map.cache_clear()
