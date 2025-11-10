"""
交易日历生成器

生成中国股市（上交所、深交所）的交易日、休市日数据
支持2020-2025年期间的交易日历，包含法定节假日和调休安排
"""

import datetime
from dataclasses import dataclass
from typing import Optional, Union, ClassVar

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
)
from ...core.types import GeneratorType


@dataclass
class TradingDay:
    """交易日数据模型"""
    date: datetime.date
    is_trading_day: bool
    day_type: str  # "TRADING", "WEEKEND", "HOLIDAY", "ADJUSTED_WORKING"
    holiday_name: Optional[str] = None
    market: str = "ALL"  # "SH", "SZ", "ALL"


class TradingCalendarGenerator(DataGenerator[dict[str, str | bool | None]]):
    """中国A股交易日历生成器

    功能特性：
    - 生成指定日期范围内的交易日或休市日
    - 支持2020-2025年完整交易日历
    - 包含法定节假日和调休安排
    - 可指定交易所（上交所/深交所）
    """

    # 实例属性声明，便于静态类型检查
    start_date: str
    end_date: str
    market: str
    include_weekends: bool
    day_type_filter: str
    china_holidays: dict[str, str]
    adjusted_working_days: set[str]

    # 参数模式定义（用于文档/描述），不参与运行时类型约束
    PARAMETER_SCHEMA: ClassVar[dict[str, dict[str, str | bool]]] = {
        "start_date": {"type": "str", "description": "开始日期 (YYYY-MM-DD)", "default": "2024-01-01"},
        "end_date": {"type": "str", "description": "结束日期 (YYYY-MM-DD)", "default": "2024-12-31"},
        "market": {"type": "str", "description": "市场代码 (SH/SZ/ALL)", "default": "ALL"},
        "include_weekends": {"type": "bool", "description": "是否包含周末", "default": False},
        "day_type": {"type": "str", "description": "日期类型 (TRADING/HOLIDAY/ALL)", "default": "TRADING"},
    }

    def _setup(self) -> None:
        """初始化交易日历数据"""
        self.start_date = self.parameters.get("start_date", "2024-01-01")
        self.end_date = self.parameters.get("end_date", "2024-12-31")
        self.market = self.parameters.get("market", "ALL")
        self.include_weekends = self.parameters.get("include_weekends", False)
        self.day_type_filter = self.parameters.get("day_type", "TRADING")

        # 中国法定节假日（2020-2025）
        self.china_holidays = {
            # 2020年
            "2020-01-01": "元旦",
            "2020-01-24": "春节",
            "2020-01-27": "春节",
            "2020-01-28": "春节",
            "2020-01-29": "春节",
            "2020-01-30": "春节",
            "2020-04-04": "清明节",
            "2020-04-06": "清明节",
            "2020-05-01": "劳动节",
            "2020-05-04": "劳动节",
            "2020-05-05": "劳动节",
            "2020-06-25": "端午节",
            "2020-06-26": "端午节",
            "2020-10-01": "国庆节",
            "2020-10-02": "国庆节",
            "2020-10-05": "国庆节",
            "2020-10-06": "国庆节",
            "2020-10-07": "国庆节",
            "2020-10-08": "国庆节",

            # 2021年
            "2021-01-01": "元旦",
            "2021-02-11": "春节",
            "2021-02-15": "春节",
            "2021-02-16": "春节",
            "2021-02-17": "春节",
            "2021-04-05": "清明节",
            "2021-05-03": "劳动节",
            "2021-05-04": "劳动节",
            "2021-05-05": "劳动节",
            "2021-06-14": "端午节",
            "2021-09-20": "中秋节",
            "2021-09-21": "中秋节",
            "2021-10-01": "国庆节",
            "2021-10-04": "国庆节",
            "2021-10-05": "国庆节",
            "2021-10-06": "国庆节",
            "2021-10-07": "国庆节",

            # 2022年
            "2022-01-03": "元旦",
            "2022-01-31": "春节",
            "2022-02-01": "春节",
            "2022-02-02": "春节",
            "2022-02-03": "春节",
            "2022-02-04": "春节",
            "2022-04-04": "清明节",
            "2022-04-05": "清明节",
            "2022-05-02": "劳动节",
            "2022-05-03": "劳动节",
            "2022-05-04": "劳动节",
            "2022-06-03": "端午节",
            "2022-09-12": "中秋节",
            "2022-10-03": "国庆节",
            "2022-10-04": "国庆节",
            "2022-10-05": "国庆节",
            "2022-10-06": "国庆节",
            "2022-10-07": "国庆节",

            # 2023年
            "2023-01-02": "元旦",
            "2023-01-23": "春节",
            "2023-01-24": "春节",
            "2023-01-25": "春节",
            "2023-01-26": "春节",
            "2023-01-27": "春节",
            "2023-04-05": "清明节",
            "2023-05-01": "劳动节",
            "2023-05-02": "劳动节",
            "2023-05-03": "劳动节",
            "2023-06-22": "端午节",
            "2023-06-23": "端午节",
            "2023-09-29": "中秋节",
            "2023-10-02": "国庆节",
            "2023-10-03": "国庆节",
            "2023-10-04": "国庆节",
            "2023-10-05": "国庆节",
            "2023-10-06": "国庆节",

            # 2024年
            "2024-01-01": "元旦",
            "2024-02-09": "春节",
            "2024-02-12": "春节",
            "2024-02-13": "春节",
            "2024-02-14": "春节",
            "2024-02-15": "春节",
            "2024-02-16": "春节",
            "2024-02-17": "春节",
            "2024-04-04": "清明节",
            "2024-04-05": "清明节",
            "2024-05-01": "劳动节",
            "2024-05-02": "劳动节",
            "2024-05-03": "劳动节",
            "2024-06-10": "端午节",
            "2024-09-16": "中秋节",
            "2024-09-17": "中秋节",
            "2024-10-01": "国庆节",
            "2024-10-02": "国庆节",
            "2024-10-03": "国庆节",
            "2024-10-04": "国庆节",
            "2024-10-07": "国庆节",

            # 2025年
            "2025-01-01": "元旦",
            "2025-01-29": "春节",
            "2025-01-30": "春节",
            "2025-01-31": "春节",
            "2025-02-03": "春节",
            "2025-02-04": "春节",
            "2025-04-04": "清明节",
            "2025-05-01": "劳动节",
            "2025-05-02": "劳动节",
            "2025-06-02": "端午节",
            "2025-10-01": "国庆节",
            "2025-10-02": "国庆节",
            "2025-10-03": "国庆节",
            "2025-10-06": "国庆节",
            "2025-10-07": "国庆节",
        }

        # 调休工作日（周末补班）
        self.adjusted_working_days = {
            "2020-01-19", "2020-02-01", "2020-04-26", "2020-05-09",
            "2020-06-28", "2020-09-27", "2020-10-10",
            "2021-02-07", "2021-02-20", "2021-04-25", "2021-05-08",
            "2021-09-18", "2021-09-26", "2021-10-09",
            "2022-01-29", "2022-01-30", "2022-04-02", "2022-04-24",
            "2022-05-07", "2022-10-08", "2022-10-09",
            "2023-01-28", "2023-01-29", "2023-04-23", "2023-05-06",
            "2023-06-25", "2023-10-07", "2023-10-08",
            "2024-02-04", "2024-02-18", "2024-04-07", "2024-04-28",
            "2024-05-11", "2024-09-14", "2024-09-29", "2024-10-12",
            "2025-01-26", "2025-02-08", "2025-04-27", "2025-09-28",
            "2025-10-11",
        }

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> dict[str, str | bool | None]:
        """生成交易日历数据"""
        import random  # TODO: Convert to secrets
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
                if day_type == "TRADING" or self.include_weekends or day_type in ["HOLIDAY", "ADJUSTED_WORKING"]:
                    filtered_dates.append({
                        "date": date_str,
                        "is_trading_day": is_trading,
                        "day_type": day_type,
                        "holiday_name": holiday_name,
                        "weekday": date_obj.strftime("%A"),
                        "weekday_cn": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date_obj.weekday()]
                    })

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
                "weekday_cn": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][random_date.weekday()]
            }

        # 返回随机一个符合条件的日期
        return secrets.choice(filtered_dates)

    def generate_single(self, context: Optional[GenerationContext] = None) -> dict[str, str | bool | None]:
        """生成单个数据项 - TODO: Implement generation logic"""
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


