"""
交易日历配置加载器

支持：
- YAML配置文件加载
- 懒加载：首次使用时才加载
- 内存缓存：加载后缓存在内存
- 降级机制：配置文件缺失时使用内置默认数据
- 热更新：检测文件变化自动重新加载
"""

import json
import os
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Optional

# 使用find_spec检查yaml是否可用，避免F401错误
YAML_AVAILABLE = find_spec("yaml") is not None


class TradingCalendarConfig:
    """交易日历配置加载器

    特性：
    - 懒加载：首次访问时才加载配置文件
    - 内存缓存：加载后缓存在内存，后续访问秒级响应
    - 自动降级：配置文件缺失时使用内置默认数据
    - 热更新：检测文件修改时间，自动重新加载

    使用示例：
        >>> config = TradingCalendarConfig()
        >>> holidays = config.get_holidays(2024)
        >>> working_days = config.get_adjusted_working_days(2024)
    """

    # 单例实例
    _instance: Optional["TradingCalendarConfig"] = None

    # 缓存数据
    _cache: dict[str, Any] | None = None
    _last_modified: float | None = None

    def __new__(cls):
        """单例模式：确保全局只有一个实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化配置加载器"""
        # 避免重复初始化
        if hasattr(self, "_initialized"):
            return

        self._initialized = True
        self._config_file = self._get_config_file_path()

    def _get_config_file_path(self) -> Path:
        """获取配置文件路径

        优先级：
        1. 用户自定义路径（环境变量 DATAFORGE_TRADING_CALENDAR_CONFIG）
        2. 项目配置目录：config/trading_calendar.yaml
        3. 降级到内置数据
        """
        # 环境变量指定的路径
        env_path = os.getenv("DATAFORGE_TRADING_CALENDAR_CONFIG")
        if env_path:
            path = Path(env_path)
            if path.exists():
                return path

        # 默认配置路径
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        default_path = project_root / "config" / "trading_calendar.yaml"

        return default_path

    def _load_config(self) -> dict[str, Any]:
        """加载配置文件

        Returns:
            配置字典
        """
        # 检查配置文件是否存在
        if not self._config_file.exists():
            print(f"警告: 配置文件不存在 {self._config_file}，使用内置默认数据")
            return self._get_default_config()

        # 检查是否需要重新加载（文件被修改）
        current_mtime = self._config_file.stat().st_mtime
        if self._cache is not None and self._last_modified == current_mtime:
            # 缓存有效，直接返回
            return self._cache

        # 加载配置文件
        try:
            with open(self._config_file, encoding="utf-8") as f:
                if YAML_AVAILABLE:
                    import yaml  # type: ignore

                    config = yaml.safe_load(f)
                else:
                    # YAML库不可用，尝试作为JSON加载
                    print("警告: PyYAML未安装，尝试作为JSON加载")
                    config = json.load(f)

            # 更新缓存
            self._cache = config
            self._last_modified = current_mtime

            return config  # type: ignore

        except Exception as e:
            print(f"错误: 加载配置文件失败 {e}，使用内置默认数据")
            return self._get_default_config()

    def _get_default_config(self) -> dict[str, Any]:
        """获取内置默认配置（降级方案）

        包含2024-2025年的基本节假日数据
        """
        return {
            "version": "2025.1",
            "holidays": {
                2024: [
                    {"date": "2024-01-01", "name": "元旦", "type": "LEGAL"},
                    {"date": "2024-02-09", "name": "春节", "type": "LEGAL"},
                    {"date": "2024-02-12", "name": "春节", "type": "LEGAL"},
                    {"date": "2024-02-13", "name": "春节", "type": "LEGAL"},
                    {"date": "2024-04-04", "name": "清明节", "type": "LEGAL"},
                    {"date": "2024-05-01", "name": "劳动节", "type": "LEGAL"},
                    {"date": "2024-06-10", "name": "端午节", "type": "LEGAL"},
                    {"date": "2024-09-16", "name": "中秋节", "type": "LEGAL"},
                    {"date": "2024-10-01", "name": "国庆节", "type": "LEGAL"},
                ],
                2025: [
                    {"date": "2025-01-01", "name": "元旦", "type": "LEGAL"},
                    {"date": "2025-01-29", "name": "春节", "type": "LEGAL"},
                    {"date": "2025-04-04", "name": "清明节", "type": "LEGAL"},
                    {"date": "2025-05-01", "name": "劳动节", "type": "LEGAL"},
                    {"date": "2025-06-02", "name": "端午节", "type": "LEGAL"},
                    {"date": "2025-10-01", "name": "国庆节", "type": "LEGAL"},
                ],
            },
            "adjusted_working_days": {
                2024: ["2024-02-04", "2024-02-18", "2024-04-07"],
                2025: ["2025-01-26", "2025-02-08", "2025-04-27"],
            },
        }

    def get_holidays(self, year: int) -> dict[str, str]:
        """获取指定年份的节假日数据

        Args:
            year: 年份

        Returns:
            节假日字典 {日期: 节日名称}
        """
        config = self._load_config()

        holidays_list = config.get("holidays", {}).get(year, [])

        # 转换为字典格式
        result = {}
        for item in holidays_list:
            date = item.get("date")
            name = item.get("name")
            if date and name:
                result[date] = name

        return result

    def get_adjusted_working_days(self, year: int) -> set[str]:
        """获取指定年份的调休工作日

        Args:
            year: 年份

        Returns:
            调休工作日集合
        """
        config = self._load_config()

        working_days = config.get("adjusted_working_days", {}).get(year, [])

        return set(working_days)

    def get_all_years(self) -> list[int]:
        """获取配置文件中包含的所有年份

        Returns:
            年份列表
        """
        config = self._load_config()

        years = set()

        # 从节假日数据获取年份
        holidays = config.get("holidays", {})
        years.update(holidays.keys())

        # 从调休工作日获取年份
        working_days = config.get("adjusted_working_days", {})
        years.update(working_days.keys())

        return sorted(years)

    def get_version(self) -> str:
        """获取配置文件版本号

        Returns:
            版本号字符串
        """
        config = self._load_config()
        version = config.get("version", "unknown")
        if isinstance(version, str):
            return version
        return str(version)

    def reload(self) -> None:
        """强制重新加载配置文件

        用于手动刷新配置数据
        """
        self._cache = None
        self._last_modified = None
        self._load_config()

    def is_cached(self) -> bool:
        """检查配置是否已缓存

        Returns:
            是否已缓存
        """
        return self._cache is not None

    def clear_cache(self) -> None:
        """清空缓存

        用于释放内存或强制重新加载
        """
        self._cache = None
        self._last_modified = None

    def __repr__(self) -> str:
        """返回配置加载器的字符串表示"""
        cached = "已缓存" if self.is_cached() else "未缓存"
        years = self.get_all_years() if self.is_cached() else []
        return f"<TradingCalendarConfig: version={self.get_version() if self.is_cached() else 'N/A'}, years={years}, status={cached}>"


# 全局单例实例
_global_config = TradingCalendarConfig()


def get_trading_calendar_config() -> TradingCalendarConfig:
    """获取全局配置实例

    Returns:
        配置加载器单例
    """
    return _global_config
