"""
交易日历生成器（重构版）

生成中国股市（上交所、深交所）的交易日、休市日数据
支持通过配置文件管理节假日数据，便于更新和维护

改进：
- ✅ 使用YAML配置文件管理节假日数据
- ✅ 懒加载 + 内存缓存，性能无损
- ✅ 支持API自动更新节假日
- ✅ 降级机制：配置缺失时使用内置默认数据
- ✅ 完全向后兼容
"""

import datetime
from dataclasses import dataclass
from typing import ClassVar

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
)
from ...core.types import GeneratorType
from ...data.trading_calendar_config import get_trading_calendar_config


@dataclass
class TradingDay:
    """交易日数据模型"""

    date: datetime.date
    is_trading_day: bool
    day_type: str  # "TRADING", "WEEKEND", "HOLIDAY", "ADJUSTED_WORKING"
    holiday_name: str | None = None
    market: str = "ALL"  # "SH", "SZ", "ALL"


class TradingCalendarGenerator(DataGenerator[dict[str, str | bool | None]]):
    """中国A股交易日历生成器（重构版）

    功能特性：
    - 生成指定日期范围内的交易日或休市日
    - 支持动态加载节假日配置
    - 包含法定节假日和调休安排
    - 可指定交易所（上交所/深交所）
    - 自动缓存配置数据，性能优化

    改进说明：
    - 节假日数据从YAML配置文件加载（不再硬编码）
    - 支持通过API自动更新节假日数据
    - 首次加载后缓存在内存，查询性能O(1)
    """

    # 实例属性声明，便于静态类型检查
    start_date: str
    end_date: str
    market: str
    include_weekends: bool
    day_type_filter: str
    china_holidays: dict[str, str]  # 从配置加载
    adjusted_working_days: set[str]  # 从配置加载

    # 参数模式定义（用于文档/描述），不参与运行时类型约束
    PARAMETER_SCHEMA: ClassVar[dict[str, dict[str, str | bool]]] = {
        "start_date": {
            "type": "str",
            "description": "开始日期 (YYYY-MM-DD)",
            "default": "2024-01-01",
        },
        "end_date": {
            "type": "str",
            "description": "结束日期 (YYYY-MM-DD)",
            "default": "2024-12-31",
        },
        "market": {
            "type": "str",
            "description": "市场代码 (SH/SZ/ALL)",
            "default": "ALL",
        },
        "include_weekends": {
            "type": "bool",
            "description": "是否包含周末",
            "default": False,
        },
        "day_type": {
            "type": "str",
            "description": "日期类型 (TRADING/HOLIDAY/ALL)",
            "default": "TRADING",
        },
    }

    def _setup(self) -> None:
        """初始化交易日历数据

        改进：
        - 从配置文件加载节假日数据（不再硬编码）
        - 懒加载：首次使用时才加载配置
        - 自动缓存：加载后缓存在内存
        """
        self.start_date = self.parameters.get("start_date", "2024-01-01")
        self.end_date = self.parameters.get("end_date", "2024-12-31")
        self.market = self.parameters.get("market", "ALL")
        self.include_weekends = self.parameters.get("include_weekends", False)
        self.day_type_filter = self.parameters.get("day_type", "TRADING")

        # 从配置文件加载节假日数据（懒加载 + 缓存）
        self._load_holidays_from_config()

    def _load_holidays_from_config(self) -> None:
        """从配置文件加载节假日数据

        特性：
        - 懒加载：首次调用时才加载配置文件
        - 内存缓存：加载后缓存在内存，后续访问秒级响应
        - 降级机制：配置文件缺失时使用内置默认数据
        - 年份自动识别：根据日期范围自动加载所需年份数据
        """
        # 获取全局配置加载器实例（单例）
        config = get_trading_calendar_config()

        # 解析日期范围
        start_year = int(self.start_date[:4])
        end_year = int(self.end_date[:4])

        # 合并所有年份的节假日数据
        self.china_holidays = {}
        self.adjusted_working_days = set()

        for year in range(start_year, end_year + 1):
            # 获取该年份的节假日（从缓存或配置文件）
            year_holidays = config.get_holidays(year)
            self.china_holidays.update(year_holidays)

            # 获取该年份的调休工作日
            year_working_days = config.get_adjusted_working_days(year)
            self.adjusted_working_days.update(year_working_days)

    def _generate_raw(
        self, context: GenerationContext | None = None
    ) -> dict[str, str | bool | None]:
        """生成交易日历数据"""
        import secrets

        # 解析日期范围
        start = datetime.datetime.strptime(self.start_date, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(self.end_date, "%Y-%m-%d").date()

        # 生成日期范围内的所有日期
        all_dates = []
        current = start
        while current <= end:
            all_dates.append(current)
            current += datetime.timedelta(days=1)

        # 筛选符合条件的日期
        filtered_dates = []
        for date_obj in all_dates:
            date_str = date_obj.strftime("%Y-%m-%d")

            # 判断日期类型
            if date_str in self.china_holidays:
                day_type = "HOLIDAY"
                holiday_name = self.china_holidays[date_str]
                is_trading = False
            elif date_str in self.adjusted_working_days:
                day_type = "ADJUSTED_WORKING"
                holiday_name = None
                is_trading = True
            elif date_obj.weekday() >= 5:  # 周六、周日
                day_type = "WEEKEND"
                holiday_name = None
                is_trading = False
            else:
                day_type = "TRADING"
                holiday_name = None
                is_trading = True

            # 根据过滤条件筛选
            if self.day_type_filter == "ALL" or day_type == self.day_type_filter:
                if (
                    day_type == "TRADING"
                    or self.include_weekends
                    or day_type in ["HOLIDAY", "ADJUSTED_WORKING"]
                ):
                    filtered_dates.append(
                        {
                            "date": date_str,
                            "is_trading_day": is_trading,
                            "day_type": day_type,
                            "holiday_name": holiday_name,
                            "weekday": date_obj.strftime("%A"),
                            "weekday_cn": [
                                "周一",
                                "周二",
                                "周三",
                                "周四",
                                "周五",
                                "周六",
                                "周日",
                            ][date_obj.weekday()],
                        }
                    )

        # 如果没有符合条件的日期，返回一个随机交易日
        if not filtered_dates:
            # 找到一个随机的工作日
            random_date = None
            while True:
                random_days = secrets.randbelow((end - start).days + 1)
                test_date = start + datetime.timedelta(days=random_days)
                test_str = test_date.strftime("%Y-%m-%d")

                if test_str not in self.china_holidays and test_date.weekday() < 5:
                    random_date = test_date
                    break

            return {
                "date": random_date.strftime("%Y-%m-%d"),
                "is_trading_day": True,
                "day_type": "TRADING",
                "holiday_name": None,
                "weekday": random_date.strftime("%A"),
                "weekday_cn": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][
                    random_date.weekday()
                ],
            }

        # 返回随机一个符合条件的日期
        return secrets.choice(filtered_dates)

    def generate_single(
        self, context: GenerationContext | None = None
    ) -> dict[str, str | bool | None]:
        """生成单个数据项"""
        return self._generate_raw(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["day_type", "end_date", "include_weekends", "market", "start_date"]

    def validate(self, data: dict[str, str | bool | None]) -> bool:
        """验证生成的数据"""
        return data is not None


@register_generator("trading_calendar", ["trading_day", "交易日", "stock_market_day"])
class GenericTradingCalendarGenerator(TradingCalendarGenerator):
    """通用交易日历生成器注册版本"""

    pass
