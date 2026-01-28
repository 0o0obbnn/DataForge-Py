"""
高级时间戳/日期时间生成器 - 符合DEVELOPMENT_PLAN.md的P0级要求
"""

import secrets
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Union

from ...core.factory import register_generator
from ...core.generator import DataGenerator, GenerationContext
from ...core.types import GeneratorType

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


@register_generator("advanced_timestamp", ["高级时间戳", "时间戳"])
class AdvancedTimestampGenerator(DataGenerator[Union[int, str]]):
    """
    高级时间戳生成器

    功能特性：
    - 支持秒级、毫秒级、微秒级、纳秒级精度
    - 支持Unix时间戳、ISO8601格式、自定义格式
    - 支持时区处理（UTC、本地时区、指定时区）
    - 支持日期范围限定
    - 支持相对时间（现在、昨天、明天等）
    - 支持上下文关联生成
    """

    def __init__(self, config: dict[str, Any] | None = None):
        """初始化高级时间戳生成器"""
        if config is None:
            config = {}

        # 兼容旧版配置格式
        from ...core.generator import GeneratorConfig

        generator_config = GeneratorConfig(
            generator_type="advanced_timestamp", parameters=config
        )
        super().__init__(generator_config)

    def _setup(self) -> None:
        """设置生成器参数"""
        # 精度设置
        self.precision = self.parameters.get("precision", "SECONDS").upper()
        self.output_format = self.parameters.get("format", "UNIX").upper()

        # 时区设置
        self.timezone_aware = self.parameters.get("timezone_aware", False)
        self.timezone = self.parameters.get("timezone", "UTC")

        # 日期范围设置
        self.start_date = self.parameters.get("start_date")
        self.end_date = self.parameters.get("end_date")

        # 相对时间设置
        self.relative_to = self.parameters.get(
            "relative_to", "NOW"
        )  # NOW, TODAY, YESTERDAY, TOMORROW
        self.offset_days = self.parameters.get("offset_days", 0)
        self.offset_hours = self.parameters.get("offset_hours", 0)
        self.offset_minutes = self.parameters.get("offset_minutes", 0)

        # 自定义格式
        self.custom_format = self.parameters.get("custom_format", "%Y-%m-%d %H:%M:%S")

    def _generate_raw(
        self, context: GenerationContext | None = None
    ) -> int | str:
        """生成时间戳"""
        # 获取基础时间
        base_time = self._get_base_datetime()

        # 应用偏移
        if self.offset_days or self.offset_hours or self.offset_minutes:
            offset = timedelta(
                days=self.offset_days,
                hours=self.offset_hours,
                minutes=self.offset_minutes,
            )
            base_time += offset

        # 应用日期范围限制
        if self.start_date or self.end_date:
            base_time = self._apply_date_range(base_time)

        # 应用时区
        if self.timezone_aware:
            base_time = self._apply_timezone(base_time)

        # 根据精度生成时间戳
        return self._format_timestamp(base_time)

    def _apply_date_range(self, dt: datetime) -> datetime:
        """应用日期范围限制"""
        # 解析开始日期
        if self.start_date:
            try:
                start_dt = datetime.fromisoformat(
                    self.start_date.replace("Z", "+00:00")
                )
            except ValueError:
                start_dt = datetime.strptime(self.start_date, "%Y-%m-%dT%H:%M:%S")
        else:
            start_dt = datetime(1970, 1, 1)

        # 解析结束日期
        if self.end_date:
            try:
                end_dt = datetime.fromisoformat(self.end_date.replace("Z", "+00:00"))
            except ValueError:
                end_dt = datetime.strptime(self.end_date, "%Y-%m-%dT%H:%M:%S")
        else:
            end_dt = datetime.now() + timedelta(days=365)

        # 确保在范围内
        if dt < start_dt:
            dt = start_dt + timedelta(
                seconds=secrets.randbelow(int((end_dt - start_dt).total_seconds()) + 1)
            )
        elif dt > end_dt:
            dt = start_dt + timedelta(
                seconds=secrets.randbelow(int((end_dt - start_dt).total_seconds()) + 1)
            )

        # 随机生成在范围内的日期
        total_seconds = int((end_dt - start_dt).total_seconds())
        if total_seconds > 0:
            random_seconds = secrets.randbelow(total_seconds + 1)
            dt = start_dt + timedelta(seconds=random_seconds)

        return dt

    def _get_base_datetime(self) -> datetime:
        """获取基础日期时间"""
        now = datetime.now()

        if self.relative_to == "TODAY":
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif self.relative_to == "YESTERDAY":
            return (now - timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif self.relative_to == "TOMORROW":
            return (now + timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif self.relative_to == "NOW":
            return now
        else:
            return now

    def _apply_timezone(self, dt: datetime) -> datetime:
        """应用时区"""
        if self.timezone.upper() == "UTC":
            return dt.replace(tzinfo=timezone.utc)
        elif self.timezone.upper() == "LOCAL":
            return dt.astimezone()
        else:
            # 尝试使用pytz时区
            try:
                import pytz

                tz = pytz.timezone(self.timezone)
                return tz.localize(dt)
            except ImportError:
                # 如果pytz不可用，使用UTC
                return dt.replace(tzinfo=timezone.utc)

    def _format_timestamp(self, dt: datetime) -> int | str:
        """格式化时间戳"""
        if self.output_format == "UNIX":
            # Unix时间戳
            if self.precision == "SECONDS":
                return int(dt.timestamp())
            elif self.precision == "MILLISECONDS":
                return int(dt.timestamp() * 1000)
            elif self.precision == "MICROSECONDS":
                return int(dt.timestamp() * 1_000_000)
            elif self.precision == "NANOSECONDS":
                return int(dt.timestamp() * 1_000_000_000)

        elif self.output_format == "ISO":
            # ISO8601格式
            return dt.isoformat()

        elif self.output_format == "CUSTOM":
            # 自定义格式
            return dt.strftime(self.custom_format)

        elif self.output_format == "STRING":
            # 字符串格式的时间戳
            if self.precision == "SECONDS":
                return str(int(dt.timestamp()))
            elif self.precision == "MILLISECONDS":
                return str(int(dt.timestamp() * 1000))
            else:
                return str(int(dt.timestamp()))

        return int(dt.timestamp())

    def validate(self, data: int | str) -> bool:
        """验证时间戳"""
        try:
            if isinstance(data, str):
                if data.isdigit():
                    timestamp = int(data)
                elif self.output_format == "ISO":
                    datetime.fromisoformat(data.replace("Z", "+00:00"))
                    return True
                elif self.output_format == "CUSTOM":
                    datetime.strptime(data, self.custom_format)
                    return True
                else:
                    return False
            elif isinstance(data, int):
                timestamp = data
            else:
                return False

            # 检查时间戳是否在合理范围内
            current_time = int(time.time())

            # 根据精度调整检查
            if self.precision == "SECONDS":
                max_future = current_time + 86400 * 365  # 未来一年
                return 0 <= timestamp <= max_future
            elif self.precision == "MILLISECONDS":
                max_future = (current_time * 1000) + (86400 * 365 * 1000)
                return 0 <= timestamp <= max_future
            elif self.precision == "MICROSECONDS":
                max_future = (current_time * 1_000_000) + (86400 * 365 * 1_000_000)
                return 0 <= timestamp <= max_future
            else:
                return 0 <= timestamp <= current_time + 86400 * 365

        except (ValueError, OSError):
            return False

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "precision",  # 精度: SECONDS, MILLISECONDS, MICROSECONDS, NANOSECONDS
            "format",  # 格式: UNIX, ISO, CUSTOM, STRING
            "timezone_aware",  # 是否使用时区
            "timezone",  # 时区: UTC, LOCAL, 具体时区名
            "start_date",  # 开始日期 (ISO格式)
            "end_date",  # 结束日期 (ISO格式)
            "relative_to",  # 相对时间: NOW, TODAY, YESTERDAY, TOMORROW
            "offset_days",  # 天数偏移
            "offset_hours",  # 小时偏移
            "offset_minutes",  # 分钟偏移
            "custom_format",  # 自定义格式字符串
        ]

    def generate_single(
        self, context: GenerationContext | None = None
    ) -> int | str:
        """生成单个数据项 - TODO: Implement generation logic"""
        return self._generate_raw(context)


@register_generator("datetime_range", ["日期时间范围", "时间范围"])
class AdvancedDateTimeRangeGenerator(DataGenerator[str]):
    """
    高级日期时间范围生成器

    功能特性：
    - 生成日期时间范围字符串
    - 支持多种格式输出
    - 支持时区处理
    - 支持持续时间设置
    """

    def __init__(self, config: dict[str, Any] | None = None):
        """初始化日期时间范围生成器"""
        if config is None:
            config = {}

        from ...core.generator import GeneratorConfig

        generator_config = GeneratorConfig(
            generator_type="datetime_range", parameters=config
        )
        super().__init__(generator_config)

    def _setup(self) -> None:
        """设置生成器参数"""
        self.format = self.parameters.get("format", "ISO")
        self.duration_days = self.parameters.get("duration_days", 1)
        self.duration_hours = self.parameters.get("duration_hours", 0)
        self.duration_minutes = self.parameters.get("duration_minutes", 0)

        self.start_datetime = self.parameters.get("start_datetime")
        self.end_datetime = self.parameters.get("end_datetime")

        self.include_timezone = self.parameters.get("include_timezone", False)
        self.timezone = self.parameters.get("timezone", "UTC")

        # 格式映射
        self.format_patterns = {
            "ISO": "%Y-%m-%dT%H:%M:%S",
            "ISO_MS": "%Y-%m-%dT%H:%M:%S.%f",
            "SQL": "%Y-%m-%d %H:%M:%S",
            "US": "%m/%d/%Y %I:%M:%S %p",
            "CN": "%Y年%m月%d日 %H时%M分%S秒",
            "RANGE": "%Y-%m-%d %H:%M:%S 至 %Y-%m-%d %H:%M:%S",
            "DURATION": "%Y-%m-%d %H:%M:%S (持续 %d天 %d小时 %d分钟)",
        }

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        """生成日期时间范围"""
        # 计算持续时间
        duration = timedelta(
            days=self.duration_days,
            hours=self.duration_hours,
            minutes=self.duration_minutes,
        )

        # 获取起始时间
        if self.start_datetime:
            start_dt = datetime.fromisoformat(self.start_datetime)
        else:
            start_dt = datetime.now()

        # 计算结束时间
        if self.end_datetime:
            end_dt = datetime.fromisoformat(self.end_datetime)
        else:
            end_dt = start_dt + duration

        # 应用时区
        if self.include_timezone:
            start_dt = self._apply_timezone(start_dt)
            end_dt = self._apply_timezone(end_dt)

        # 格式化输出
        return self._format_range(start_dt, end_dt, duration)

    def _apply_timezone(self, dt: datetime) -> datetime:
        """应用时区"""
        if self.timezone.upper() == "UTC":
            return dt.replace(tzinfo=timezone.utc)
        else:
            try:
                import pytz

                tz = pytz.timezone(self.timezone)
                return tz.localize(dt)
            except ImportError:
                return dt.replace(tzinfo=timezone.utc)

    def _format_range(self, start: datetime, end: datetime, duration: timedelta) -> str:
        """格式化日期时间范围"""
        if self.format == "RANGE":
            return f"{start.strftime('%Y-%m-%d %H:%M:%S')} 至 {end.strftime('%Y-%m-%d %H:%M:%S')}"
        elif self.format == "DURATION":
            total_seconds = int(duration.total_seconds())
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60

            duration_parts = []
            if days > 0:
                duration_parts.append(f"{days}天")
            if hours > 0:
                duration_parts.append(f"{hours}小时")
            if minutes > 0:
                duration_parts.append(f"{minutes}分钟")

            duration_str = " ".join(duration_parts) if duration_parts else "0分钟"
            return f"{start.strftime('%Y-%m-%d %H:%M:%S')} (持续 {duration_str})"
        elif self.format in self.format_patterns:
            pattern = self.format_patterns[self.format]
            return start.strftime(pattern)
        else:
            return start.strftime("%Y-%m-%d %H:%M:%S")

    def validate(self, data: str) -> bool:
        """验证日期时间范围字符串"""
        try:
            # 支持多种格式验证
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d",
                "%Y年%m月%d日 %H时%M分%S秒",
            ]

            # 先尝试直接解析
            for fmt in formats:
                try:
                    datetime.strptime(data, fmt)
                    return True
                except ValueError:
                    continue

            # 检查是否是范围格式
            if "至" in data or "-" in data:
                separators = ["至", "-"]
                for sep in separators:
                    if sep in data:
                        parts = data.split(sep)
                        if len(parts) >= 2:
                            start_str = parts[0].strip()
                            end_str = parts[1].strip()
                            try:
                                datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
                                datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
                                return True
                            except ValueError:
                                try:
                                    datetime.strptime(start_str, "%Y-%m-%d")
                                    datetime.strptime(end_str, "%Y-%m-%d")
                                    return True
                                except ValueError:
                                    continue

            # 检查是否包含中文格式
            if "年" in data and "月" in data and "日" in data:
                try:
                    datetime.strptime(data, "%Y年%m月%d日 %H时%M分%S秒")
                    return True
                except ValueError:
                    pass

            return False
        except Exception:
            return False

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "format",  # 输出格式: ISO, SQL, US, CN, RANGE, DURATION
            "duration_days",  # 持续天数
            "duration_hours",  # 持续小时数
            "duration_minutes",  # 持续分钟数
            "start_datetime",  # 开始日期时间 (ISO格式)
            "end_datetime",  # 结束日期时间 (ISO格式)
            "include_timezone",  # 是否包含时区信息
            "timezone",  # 时区设置
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项 - TODO: Implement generation logic"""
        return self._generate_raw(context)
