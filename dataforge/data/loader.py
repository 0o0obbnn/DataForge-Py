import json
import os
from typing import Any

import pandas as pd

_cache: dict[str, Any] = {}


def _get_data_path(filename: str) -> str:
    """获取数据文件的绝对路径"""
    return os.path.join(os.path.dirname(__file__), "chinese", filename)


def load_json(filename: str) -> Any:
    """
    加载指定名称的JSON数据文件。
    使用缓存避免重复加载。
    """
    if filename in _cache:
        return _cache[filename]

    file_path = _get_data_path(filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
        _cache[filename] = data
        return data


def load_regions_df() -> pd.DataFrame:
    """
    加载行政区划代码数据，并转换为Pandas DataFrame以便于查询。
    缓存DataFrame以提高性能。
    """
    cache_key = "regions_df"
    if cache_key in _cache:
        return _cache[cache_key]

    regions_data = load_json("regions.json")

    all_districts: list[dict[str, Any]] = []
    for province in regions_data.get("provinces", []):
        province_code = province["code"]
        # 处理直辖市等特殊情况
        if province_code in regions_data.get("major_cities", {}):
            for city in regions_data["major_cities"][province_code]:
                for district in city.get("districts", []):
                    all_districts.append(
                        {
                            "province_code": province_code,
                            "province_name": province["name"],
                            "city_code": city["code"],
                            "city_name": city["name"],
                            "district_code": district["code"],
                            "district_name": district["name"],
                            "zipcode": district.get("zipcode"),
                        }
                    )

    if not all_districts:
        raise ValueError("No district data found in regions.json")

    df = pd.DataFrame(all_districts)
    _cache[cache_key] = df
    return df
