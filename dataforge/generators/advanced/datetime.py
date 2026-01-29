"""
时间/日历类生成器
"""

import random  # TODO: Convert to secrets
import secrets
from datetime import date, datetime, timedelta, timezone

from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
)
from ...core.protocols import Validator
from ...core.types import GeneratorType

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   secrets.randbelow(b - a + 1) + a → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   secrets.randbelow(b - a + 1) + a → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   secrets.randbelow(b - a + 1) + a → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   secrets.randbelow(b - a + 1) + a → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


class DateValidator(Validator):
    """Validator for dates."""

    def __init__(self, format_pattern: str = "%Y-%m-%d"):
        self.format_pattern = format_pattern

    def validate(self, data: str) -> bool:
        """校验日期"""
        if not isinstance(data, str):
            return False

        try:
            # 尝试用标准格式解析
            datetime.strptime(data, "%Y-%m-%d")
            return True
        except ValueError:
            try:
                # 尝试用自定义格式解析
                datetime.strptime(data, self.format_pattern)
                return True
            except ValueError:
                # 尝试解析中文格式
                if "年" in data and "月" in data and "日" in data:
                    import re

                    pattern = r"(\d{4})年(\d{1,2})月(\d{1,2})日"
                    match = re.match(pattern, data)
                    if match:
                        year, month, day = match.groups()
                        try:
                            datetime(int(year), int(month), int(day))
                            return True
                        except ValueError:
                            return False
                return False

    @property
    def error_message(self) -> str:
        return "Invalid date format"


class DateGenerator(DataGenerator[str]):
    """日期生成器"""

    def __init__(self, config: GeneratorConfig | dict | None = None):
        """初始化日期生成器"""
        if config is None:
            config = {}

        # 兼容旧版配置格式
        if isinstance(config, dict):
            generator_config = GeneratorConfig(generator_type="date", parameters=config)
        else:
            generator_config = config

        super().__init__(generator_config)
        self.start_date = self.parameters.get("start_date", "1970-01-01")
        self.end_date = self.parameters.get("end_date", "2030-12-31")
        self.format_pattern = self.parameters.get("format", "%Y-%m-%d")
        self.locale = self.parameters.get("locale", "ISO")  # ISO, CN, US
        self.business_days_only = self.parameters.get("business_days_only", False)
        self.exclude_holidays = self.parameters.get("exclude_holidays", False)
        self.validator = DateValidator(self.format_pattern)

        # 日期格式映射
        self.format_patterns = {
            "YYYY-MM-DD": "%Y-%m-%d",
            "YYYY/MM/DD": "%Y/%m/%d",
            "DD/MM/YYYY": "%d/%m/%Y",
            "MM/DD/YYYY": "%m/%d/%Y",
            "YYYYMMDD": "%Y%m%d",
            "DD-MM-YYYY": "%d-%m-%Y",
            "MM-DD-YYYY": "%m-%d-%Y",
        }

        # 中国节假日（简化版）
        self.chinese_holidays = [
            "01-01",  # 元旦
            "02-14",  # 春节（简化）
            "05-01",  # 劳动节
            "10-01",  # 国庆节
        ]

    def _setup(self) -> None:
        self.start_date = self.parameters.get("start_date", "1970-01-01")
        self.end_date = self.parameters.get("end_date", "2030-12-31")
        self.format_pattern = self.parameters.get("format", "%Y-%m-%d")
        self.locale = self.parameters.get("locale", "ISO")  # ISO, CN, US
        self.business_days_only = self.parameters.get("business_days_only", False)
        self.exclude_holidays = self.parameters.get("exclude_holidays", False)

    def generate(self, context: GenerationContext | None = None) -> str:
        """生成原始日期字符串"""
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(self.end_date, "%Y-%m-%d")

        # 计算日期范围的天数
        delta_days = (end_date - start_date).days

        # 生成随机日期，考虑工作日和节假日限制
        max_attempts = 100  # 防止无限循环
        for _ in range(max_attempts):
            random_days = secrets.randbelow(max(delta_days, 0 + 1))
            random_date = start_date + timedelta(days=random_days)
            date_obj = random_date.date()

            # 检查工作日限制
            if self.business_days_only and date_obj.weekday() >= 5:  # 周六(5)或周日(6)
                continue

            # 检查节假日限制
            if self.exclude_holidays and self._is_holiday(date_obj):
                continue

            # 找到符合条件的日期
            break
        else:
            # 如果找不到符合条件的日期，使用原始逻辑
            random_days = secrets.randbelow(max(delta_days, 0 + 1))
            random_date = start_date + timedelta(days=random_days)

        # 检查是否需要中文格式
        if self.locale.upper() == "CN" or "年" in self.format_pattern:
            return (
                f"{random_date.year}年{random_date.month:02d}月{random_date.day:02d}日"
            )

        # 使用指定的格式返回日期字符串
        return random_date.strftime(self.format_pattern)

    def _format_date(self, date_obj: date) -> str:
        """格式化日期"""
        pattern = self.format_patterns.get(self.format_pattern, "%Y-%m-%d")

        if self.locale.upper() == "CN":
            # 中文格式
            return f"{date_obj.year}年{date_obj.month:02d}月{date_obj.day:02d}日"
        else:
            return date_obj.strftime(pattern)

    def _is_holiday(self, date_obj: date) -> bool:
        """检查是否为节假日"""
        date_str = f"{date_obj.month:02d}-{date_obj.day:02d}"
        return date_str in self.chinese_holidays

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return [
            "business_days_only",
            "end_date",
            "exclude_holidays",
            "format",
            "locale",
            "start_date",
        ]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class TimeValidator(Validator):
    """Validator for time strings."""

    def __init__(self, format_pattern: str = "%H:%M:%S"):
        self.format_pattern = format_pattern

    def validate(self, data: str) -> bool:
        """校验时间"""
        if not isinstance(data, str):
            return False

        try:
            # 尝试用指定格式解析时间
            datetime.strptime(data, self.format_pattern)
            return True
        except ValueError:
            # 尝试常见的时间格式
            common_formats = ["%H:%M:%S", "%H:%M", "%I:%M:%S %p", "%I:%M %p"]
            for fmt in common_formats:
                try:
                    datetime.strptime(data, fmt)
                    return True
                except ValueError:
                    continue
            return False

    @property
    def error_message(self) -> str:
        return "Invalid time string format"


class TimeGenerator(DataGenerator[str]):
    """时间生成器"""

    def __init__(self, config: GeneratorConfig | dict | None = None):
        """初始化时间生成器"""
        if config is None:
            config = {}

        # 兼容旧版配置格式
        if isinstance(config, dict):
            generator_config = GeneratorConfig(generator_type="time", parameters=config)
        else:
            generator_config = config

        super().__init__(generator_config)
        self.format_pattern = self.parameters.get("format", "%H:%M:%S")
        self.include_seconds = self.parameters.get("include_seconds", True)
        self.include_milliseconds = self.parameters.get("include_milliseconds", False)
        self.timezone_aware = self.parameters.get("timezone_aware", False)
        self.timezone = self.parameters.get("timezone", "UTC")
        self.validator = TimeValidator(self.format_pattern)

        # 时间范围处理
        start_time_str = self.parameters.get("start_time", "00:00:00")
        end_time_str = self.parameters.get("end_time", "23:59:59")

        self.start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
        self.end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()
        self.format_style = self.parameters.get(
            "format", "24H"
        )  # 24H, 12H, SECONDS, MILLISECONDS
        self.include_seconds = self.parameters.get("include_seconds", True)
        self.include_milliseconds = self.parameters.get("include_milliseconds", False)
        self.timezone_aware = self.parameters.get("timezone_aware", False)
        self.timezone = self.parameters.get("timezone", "UTC")
        self.time_range = self.parameters.get("time_range", None)  # ('09:00', '17:00')

    def _setup(self) -> None:
        self.format_pattern = self.parameters.get("format", "%H:%M:%S")
        self.include_seconds = self.parameters.get("include_seconds", True)
        self.include_milliseconds = self.parameters.get("include_milliseconds", False)
        self.timezone_aware = self.parameters.get("timezone_aware", False)
        self.timezone = self.parameters.get("timezone", "UTC")

        # 时间范围处理
        start_time_str = self.parameters.get("start_time", "00:00:00")
        end_time_str = self.parameters.get("end_time", "23:59:59")

        self.start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
        self.end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()
        self.format_style = self.parameters.get(
            "format", "24H"
        )  # 24H, 12H, SECONDS, MILLISECONDS
        self.include_seconds = self.parameters.get("include_seconds", True)
        self.include_milliseconds = self.parameters.get("include_milliseconds", False)
        self.timezone_aware = self.parameters.get("timezone_aware", False)
        self.timezone = self.parameters.get("timezone", "UTC")
        self.time_range = self.parameters.get("time_range", None)  # ('09:00', '17:00')

    def generate(self, context: GenerationContext | None = None) -> str:
        """生成原始时间字符串"""
        if self.time_range:
            # 使用time_range参数生成时间
            return self._generate_time_in_range()
        elif self.start_time and self.end_time:
            # 在指定时间范围内生成
            start_seconds = (
                self.start_time.hour * 3600
                + self.start_time.minute * 60
                + self.start_time.second
            )
            end_seconds = (
                self.end_time.hour * 3600
                + self.end_time.minute * 60
                + self.end_time.second
            )

            random_seconds = (
                secrets.randbelow(end_seconds - start_seconds + 1) + start_seconds
            )
            hours = random_seconds // 3600
            minutes = (random_seconds % 3600) // 60
            seconds = random_seconds % 60
        else:
            # 随机生成时间
            hours = secrets.randbelow(23 + 1)
            minutes = secrets.randbelow(59 + 1)
            seconds = secrets.randbelow(59 + 1)

        # 使用格式化方法而不是strftime
        milliseconds = secrets.randbelow(999 + 1) if self.include_milliseconds else 0
        return self._format_time(hours, minutes, seconds, milliseconds)

    def _generate_time_in_range(self) -> str:
        """在指定时间范围内生成时间"""
        # 检查time_range是否为None
        if not self.time_range:
            # 如果time_range为None，则回退到随机生成时间
            hours = secrets.randbelow(23 + 1)
            minutes = secrets.randbelow(59 + 1)
            seconds = secrets.randbelow(59 + 1)
            milliseconds = (
                secrets.randbelow(999 + 1) if self.include_milliseconds else 0
            )
            return self._format_time(hours, minutes, seconds, milliseconds)

        start_time, end_time = self.time_range

        # 解析时间范围
        start_parts = start_time.split(":")
        end_parts = end_time.split(":")

        start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
        end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])

        # 生成范围内的随机分钟数
        if end_minutes < start_minutes:  # 跨天情况
            if (secrets.randbelow(1000000) / 1000000) < 0.5:
                random_minutes = (
                    secrets.randbelow(24 * 60 - 1 - start_minutes + 1) + start_minutes
                )
            else:
                random_minutes = secrets.randbelow(end_minutes + 1)
        else:
            random_minutes = (
                secrets.randbelow(end_minutes - start_minutes + 1) + start_minutes
            )

        hour = random_minutes // 60
        minute = random_minutes % 60
        second = secrets.randbelow(59 + 1) if self.include_seconds else 0
        millisecond = secrets.randbelow(999 + 1) if self.include_milliseconds else 0

        return self._format_time(hour, minute, second, millisecond)

    def _format_time(
        self, hour: int, minute: int, second: int, millisecond: int
    ) -> str:
        """格式化时间"""
        # 如果format_pattern是strftime格式（包含%），使用strftime
        if self.format_pattern and "%" in self.format_pattern:
            time_obj = datetime(2000, 1, 1, hour, minute, second, millisecond * 1000)
            return time_obj.strftime(self.format_pattern)

        # 否则使用format_style
        if self.format_style.upper() == "12H":
            # 12小时制
            am_pm = "AM" if hour < 12 else "PM"
            display_hour = hour if hour <= 12 else hour - 12
            display_hour = 12 if display_hour == 0 else display_hour

            time_str = f"{display_hour:02d}:{minute:02d}"
            if self.include_seconds:
                time_str += f":{second:02d}"
            if self.include_milliseconds:
                time_str += f".{millisecond:03d}"
            time_str += f" {am_pm}"
        else:
            # 24小时制
            time_str = f"{hour:02d}:{minute:02d}"
            if self.include_seconds:
                time_str += f":{second:02d}"
            if self.include_milliseconds:
                time_str += f".{millisecond:03d}"

        # 添加时区信息
        if self.timezone_aware:
            if self.timezone.upper() == "UTC":
                time_str += " UTC"
            else:
                time_str += f" {self.timezone}"

        return time_str

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return [
            "end_time",
            "format",
            "include_milliseconds",
            "include_seconds",
            "start_time",
            "time_range",
            "timezone",
            "timezone_aware",
        ]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class TimestampValidator(Validator):
    """Validator for timestamps."""

    def __init__(self, output_format: str = "INTEGER"):
        self.output_format = output_format

    def validate(self, data: int | str) -> bool:
        """校验时间戳"""
        if isinstance(data, str):
            if self.output_format.upper() == "ISO":
                try:
                    datetime.fromisoformat(data.replace("Z", "+00:00"))
                    return True
                except (ValueError, TypeError):
                    return False
            else:
                try:
                    int(data)
                    return True
                except (ValueError, TypeError):
                    return False
        elif isinstance(data, int):
            return data >= 0

        return False

    @property
    def error_message(self) -> str:
        return "Invalid timestamp format or value"


class TimestampGenerator(DataGenerator[int | str]):
    """时间戳生成器"""

    def __init__(self, config: GeneratorConfig | dict | None = None):
        """初始化时间戳生成器"""
        if config is None:
            config = {}

        # 兼容旧版配置格式
        if isinstance(config, dict):
            generator_config = GeneratorConfig(
                generator_type="timestamp", parameters=config
            )
        else:
            generator_config = config

        super().__init__(generator_config)
        self.start_timestamp = self.parameters.get(
            "start_timestamp", 1577836800
        )  # 2020-01-01
        self.end_timestamp = self.parameters.get(
            "end_timestamp", 1893456000
        )  # 2030-01-01
        self.precision = self.parameters.get(
            "precision", "SECONDS"
        )  # SECONDS, MILLISECONDS, MICROSECONDS
        self.output_format = self.parameters.get(
            "output_format", "INTEGER"
        )  # STRING, ISO, INTEGER
        self.validator = TimestampValidator(self.output_format)

    def _setup(self) -> None:
        self.start_timestamp = self.parameters.get(
            "start_timestamp", 1577836800
        )  # 2020-01-01
        self.end_timestamp = self.parameters.get(
            "end_timestamp", 1893456000
        )  # 2030-01-01
        self.precision = self.parameters.get(
            "precision", "SECONDS"
        )  # SECONDS, MILLISECONDS, MICROSECONDS
        self.output_format = self.parameters.get(
            "output_format", "INTEGER"
        )  # STRING, ISO, INTEGER

    def generate(self, context: GenerationContext | None = None) -> int | str:
        """生成原始时间戳"""
        # 生成随机时间戳
        if self.precision.upper() == "MILLISECONDS":
            timestamp = (
                secrets.randbelow(
                    self.end_timestamp * 1000 - self.start_timestamp * 1000 + 1
                )
                + self.start_timestamp * 1000
            )
        elif self.precision.upper() == "MICROSECONDS":
            timestamp = (
                secrets.randbelow(
                    self.end_timestamp * 1000000 - self.start_timestamp * 1000000 + 1
                )
                + self.start_timestamp * 1000000
            )
        else:  # SECONDS
            timestamp = (
                secrets.randbelow(self.end_timestamp - self.start_timestamp + 1)
                + self.start_timestamp
            )

        # 根据输出格式返回相应类型
        if self.output_format.upper() == "STRING":
            return str(timestamp)
        elif self.output_format.upper() == "ISO":
            # 转换为ISO格式
            if self.precision.upper() == "MILLISECONDS":
                dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
            elif self.precision.upper() == "MICROSECONDS":
                dt = datetime.fromtimestamp(timestamp / 1000000, tz=timezone.utc)
            else:
                dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            return dt.isoformat()
        else:  # INTEGER - 返回整数
            return timestamp

    def generate_single(self, context: GenerationContext | None = None) -> int | str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["end_timestamp", "output_format", "precision", "start_timestamp"]

    def validate(self, data: int | str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class CronExpressionValidator(Validator):
    """Validator for Cron expressions."""

    def __init__(self, format_type: str = "STANDARD"):
        self.format_type = format_type

    def validate(self, data: str) -> bool:
        """校验Cron表达式"""
        if not isinstance(data, str):
            return False

        parts = data.strip().split()

        # 检查字段数量
        if self.format_type.upper() == "EXTENDED":
            if len(parts) != 6:
                return False
            field_ranges = [
                (0, 59),
                (0, 23),
                (1, 31),
                (1, 12),
                (0, 6),
                (0, 59),
            ]  # 秒 分 时 日 月 星期
        else:
            if len(parts) != 5:
                return False
            field_ranges = [
                (0, 59),
                (0, 23),
                (1, 31),
                (1, 12),
                (0, 6),
            ]  # 分 时 日 月 星期

        # 星期文字映射
        weekday_map = {
            "SUN": 0,
            "MON": 1,
            "TUE": 2,
            "WED": 3,
            "THU": 4,
            "FRI": 5,
            "SAT": 6,
        }

        def validate_field(
            field: str, min_val: int, max_val: int, is_weekday: bool = False
        ) -> bool:
            """验证单个字段"""
            field = field.upper()

            # 通配符
            if field == "*":
                return True

            # 步进格式
            if "/" in field:
                base, step = field.split("/", 1)
                if base != "*" and not validate_field(
                    base, min_val, max_val, is_weekday
                ):
                    return False
                try:
                    step_val = int(step)
                    return min_val <= step_val <= max_val
                except ValueError:
                    return False

            # 列表格式
            if "," in field:
                values = field.split(",")
                return all(
                    validate_field(v.strip(), min_val, max_val, is_weekday)
                    for v in values
                )

            # 范围格式
            if "-" in field:
                start, end = field.split("-", 1)

                # 处理星期文字
                if is_weekday:
                    start_num = weekday_map.get(start.upper(), start)
                    end_num = weekday_map.get(end.upper(), end)
                else:
                    start_num, end_num = start, end

                try:
                    start_val = int(start_num)
                    end_val = int(end_num)
                    return (
                        min_val <= start_val <= max_val
                        and min_val <= end_val <= max_val
                        and start_val <= end_val
                    )
                except ValueError:
                    return False

            # 单个值
            if is_weekday and field in weekday_map:
                return True

            try:
                val = int(field)
                return min_val <= val <= max_val
            except ValueError:
                return False

        # 验证每个字段
        for i, (part, (min_val, max_val)) in enumerate(
            zip(parts, field_ranges, strict=False)
        ):
            is_weekday = (i == 4 and self.format_type.upper() != "EXTENDED") or (
                i == 5 and self.format_type.upper() == "EXTENDED"
            )
            if not validate_field(part, min_val, max_val, is_weekday):
                return False

        return True

    @property
    def error_message(self) -> str:
        return "Invalid Cron expression format"


class CronExpressionGenerator(DataGenerator[str]):
    """Cron表达式生成器"""

    def __init__(self, config: GeneratorConfig | dict | None = None):
        """初始化Cron表达式生成器"""
        if config is None:
            config = {}

        # 兼容旧版配置格式
        if isinstance(config, dict):
            generator_config = GeneratorConfig(
                generator_type="cron_expression", parameters=config
            )
        else:
            generator_config = config

        super().__init__(generator_config)
        self.format_type = self.parameters.get(
            "format", "STANDARD"
        )  # STANDARD, EXTENDED
        self.preset_type = self.parameters.get(
            "preset", None
        )  # HOURLY, DAILY, WEEKLY, MONTHLY
        self.allow_special_chars = self.parameters.get("allow_special_chars", True)
        self.minute_range = self.parameters.get("minute_range", (0, 59))
        self.hour_range = self.parameters.get("hour_range", (0, 23))
        self.day_range = self.parameters.get("day_range", (1, 31))
        self.month_range = self.parameters.get("month_range", (1, 12))
        self.weekday_range = self.parameters.get("weekday_range", (0, 6))
        self.validator = CronExpressionValidator(self.format_type)

        # 预设Cron表达式
        self.presets = {
            "HOURLY": "0 * * * *",
            "DAILY": "0 0 * * *",
            "WEEKLY": "0 0 * * 0",
            "MONTHLY": "0 0 1 * *",
            "YEARLY": "0 0 1 1 *",
        }

    def _setup(self) -> None:
        self.format_type = self.parameters.get(
            "format", "STANDARD"
        )  # STANDARD, EXTENDED
        self.preset_type = self.parameters.get(
            "preset", None
        )  # HOURLY, DAILY, WEEKLY, MONTHLY
        self.allow_special_chars = self.parameters.get("allow_special_chars", True)
        self.minute_range = self.parameters.get("minute_range", (0, 59))
        self.hour_range = self.parameters.get("hour_range", (0, 23))
        self.day_range = self.parameters.get("day_range", (1, 31))
        self.month_range = self.parameters.get("month_range", (1, 12))
        self.weekday_range = self.parameters.get("weekday_range", (0, 6))

    def generate(self, context: GenerationContext | None = None) -> str:
        """生成原始Cron表达式"""
        if self.preset_type and self.preset_type.upper() in self.presets:
            return self.presets[self.preset_type.upper()]

        # 生成随机Cron表达式
        minute = self._generate_field(0, 59, "minute")
        hour = self._generate_field(0, 23, "hour")
        day = self._generate_field(1, 31, "day")
        month = self._generate_field(1, 12, "month")
        weekday = self._generate_field(0, 6, "weekday")

        cron_expr = f"{minute} {hour} {day} {month} {weekday}"

        # 扩展格式包含秒
        if self.format_type.upper() == "EXTENDED":
            second = self._generate_field(0, 59, "second")
            cron_expr = f"{second} {cron_expr}"

        return cron_expr

    def _generate_field(self, min_val: int, max_val: int, field_type: str) -> str:
        """生成Cron字段"""
        if not self.allow_special_chars or (secrets.randbelow(1000000) / 1000000) < 0.3:
            # 30%概率生成具体数值
            return str(secrets.randbelow(max_val - min_val + 1) + min_val)

        # 生成特殊字符表达式
        special_type = secrets.choice(["wildcard", "range", "list", "step"])

        if special_type == "wildcard":
            return "*"
        elif special_type == "range":
            start = secrets.randbelow(max_val - 1 - min_val + 1) + min_val
            end = secrets.randbelow(max_val - start + 1 + 1) + start + 1
            return f"{start}-{end}"
        elif special_type == "list":
            count = secrets.randbelow(3) + 2
            values = random.sample(range(min_val, max_val + 1), count)
            return ",".join(map(str, sorted(values)))
        else:  # step
            step = secrets.randbelow(4) + 2
            if (secrets.randbelow(1000000) / 1000000) < 0.5:
                return f"*/{step}"
            else:
                start = secrets.randbelow(max_val // 2 - min_val + 1) + min_val
                return f"{start}/{step}"

    def get_next_run_time(self, cron_expr: str) -> datetime | None:
        """获取下次执行时间（简化实现）"""
        # 这是一个简化的实现，实际应该使用专业的cron库
        try:
            parts = cron_expr.split()
            if len(parts) < 5:
                return None

            # 简单计算下次执行时间
            now = datetime.now()
            next_time = now.replace(second=0, microsecond=0) + timedelta(minutes=1)

            return next_time
        except (ValueError, TypeError):
            return None

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return [
            "allow_special_chars",
            "day_range",
            "format",
            "hour_range",
            "minute_range",
            "month_range",
            "preset",
            "weekday_range",
        ]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class GenericDateGenerator(DateGenerator):
    """通用日期生成器注册版本"""

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return [
            "start_date",
            "end_date",
            "format",
            "locale",
            "business_days_only",
            "exclude_holidays",
        ]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return isinstance(data, str) and bool(data.strip())


class GenericTimeGenerator(TimeGenerator):
    """通用时间生成器注册版本"""

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return [
            "format",
            "include_seconds",
            "include_milliseconds",
            "timezone_aware",
            "timezone",
            "time_range",
            "start_time",
            "end_time",
        ]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return isinstance(data, str) and bool(data.strip())


class GenericTimestampGenerator(TimestampGenerator):
    """通用时间戳生成器注册版本"""

    def generate_single(self, context: GenerationContext | None = None) -> int | str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["start_timestamp", "end_timestamp", "precision", "output_format"]

    def validate(self, data: int | str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return isinstance(data, (int, str)) and bool(str(data).strip())


class GenericCronExpressionGenerator(CronExpressionGenerator):
    """通用Cron表达式生成器注册版本"""

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return [
            "format",
            "preset",
            "allow_special_chars",
            "minute_range",
            "hour_range",
            "day_range",
            "month_range",
            "weekday_range",
        ]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return isinstance(data, str) and bool(data.strip())
