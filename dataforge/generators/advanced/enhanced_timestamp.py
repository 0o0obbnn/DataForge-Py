import time
from datetime import datetime, timedelta

import pytz

from dataforge.core.generator import DataGenerator, GenerationContext, GeneratorConfig
from dataforge.core.protocols import Validator

from ...core.types import GeneratorType


class EnhancedTimestampValidator(Validator):
    """Validator for EnhancedTimestampGenerator."""

    def validate(self, data: int | float | str) -> bool:
        """验证时间戳"""
        try:
            if isinstance(data, str):
                if data.isdigit():
                    timestamp = int(data)
                elif "ISO" in data.upper():  # Check for ISO format string
                    datetime.fromisoformat(data.replace("Z", "+00:00"))
                    return True
                else:
                    return False
            elif isinstance(data, (int, float)):
                timestamp = int(data)
            else:
                return False

            # 检查时间戳是否在合理范围内
            current_time = int(time.time())
            return 0 <= timestamp <= current_time + 86400 * 365  # 允许未来一年

        except (ValueError, OSError):
            return False

    @property
    def error_message(self) -> str:
        return "Invalid timestamp format or value"


class EnhancedTimestampGenerator(DataGenerator[int | float | str]):
    """增强版时间戳生成器，支持多种精度和格式"""

    def __init__(self, config: GeneratorConfig | dict | None = None):
        """初始化增强版时间戳生成器"""
        if config is None:
            config = {}

        # 兼容旧版配置格式
        if isinstance(config, dict):
            generator_config = GeneratorConfig(
                generator_type="enhanced_timestamp", parameters=config
            )
        else:
            generator_config = config

        super().__init__(generator_config)
        self.validator = EnhancedTimestampValidator()

    def _setup(self) -> None:
        """初始化设置"""
        self.precision = self.parameters.get("precision", "SECONDS").upper()
        self.output_format = self.parameters.get("output_format", "INTEGER").upper()
        self.start_date = self.parameters.get("start_date")
        self.end_date = self.parameters.get("end_date")
        self.timezone_aware = self.parameters.get("timezone_aware", False)
        self.timezone = self.parameters.get("timezone", "UTC")
        self.relative_to = self.parameters.get("relative_to", "EPOCH")
        self.offset_seconds = self.parameters.get("offset_seconds", 0)

    def generate(self, context: GenerationContext | None = None) -> int | float | str:
        """生成原始时间戳"""
        base_time = self._get_base_time()

        # 添加偏移
        if self.offset_seconds:
            base_time += timedelta(seconds=self.offset_seconds)

        # 根据精度生成时间戳
        if self.precision == "SECONDS":
            timestamp = int(base_time.timestamp())
        elif self.precision == "MILLISECONDS":
            timestamp = int(base_time.timestamp() * 1000)
        elif self.precision == "MICROSECONDS":
            timestamp = int(base_time.timestamp() * 1_000_000)
        elif self.precision == "NANOSECONDS":
            timestamp = int(base_time.timestamp() * 1_000_000_000)
        else:
            timestamp = int(base_time.timestamp())

        # 根据输出格式返回
        if self.output_format == "INTEGER":
            return timestamp
        elif self.output_format == "FLOAT":
            return float(base_time.timestamp())
        elif self.output_format == "STRING":
            return str(timestamp)
        elif self.output_format == "ISO":
            return base_time.isoformat()
        else:
            return timestamp

    def _get_base_time(self) -> datetime:
        """获取基础时间"""
        if self.relative_to == "NOW":
            base_time = datetime.now()
        elif self.relative_to == "TODAY":
            base_time = datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif self.relative_to == "YESTERDAY":
            base_time = (datetime.now() - timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif self.relative_to == "TOMORROW":
            base_time = (datetime.now() + timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        else:  # EPOCH
            base_time = datetime.now()

        # 应用时区
        if self.timezone_aware:
            tz = pytz.timezone(self.timezone)
            base_time = tz.localize(base_time)

        # 应用日期范围
        if self.start_date or self.end_date:
            start_dt = None
            end_dt = None

            if self.start_date:
                start_dt = datetime.fromisoformat(self.start_date)
            if self.end_date:
                end_dt = datetime.fromisoformat(self.end_date)

            if start_dt and end_dt:
                import secrets

                delta = end_dt - start_dt
                random_seconds = secrets.randbelow(int(delta.total_seconds()) + 1)
                base_time = start_dt + timedelta(seconds=random_seconds)
            elif start_dt:
                base_time = start_dt
            elif end_dt:
                base_time = end_dt

        return base_time

    def generate_single(
        self, context: GenerationContext | None = None
    ) -> int | float | str:
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
            "end_date",
            "offset_seconds",
            "output_format",
            "precision",
            "relative_to",
            "start_date",
            "timezone",
            "timezone_aware",
        ]

    def validate(self, data: int | float | str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class DateTimeRangeValidator(Validator):
    """Validator for DateTimeRangeGenerator."""

    def validate(self, data: str) -> bool:
        """验证日期时间字符串"""
        try:
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S.%f%z",
                "%Y/%m/%d %H:%M:%S",
                "%m/%d/%Y %I:%M:%S %p",
                "%Y年%m月%d日 %H时%M分%S秒",
            ]

            for fmt in formats:
                try:
                    datetime.strptime(data, fmt)
                    return True
                except ValueError:
                    continue

            # 尝试ISO格式
            try:
                datetime.fromisoformat(data.replace("Z", "+00:00"))
                return True
            except ValueError:
                return False

        except Exception:
            return False

    @property
    def error_message(self) -> str:
        return "Invalid datetime string format"


class DateTimeRangeGenerator(DataGenerator[str]):
    """日期时间范围生成器"""

    def __init__(self, config: GeneratorConfig | dict | None = None):
        """初始化日期时间范围生成器"""
        if config is None:
            config = {}

        # 兼容旧版配置格式
        if isinstance(config, dict):
            generator_config = GeneratorConfig(
                generator_type="datetime_range", parameters=config
            )
        else:
            generator_config = config

        super().__init__(generator_config)
        self.validator = DateTimeRangeValidator()

    def _setup(self) -> None:
        """初始化设置"""
        self.format = self.parameters.get("format", "ISO")
        self.start_datetime = self.parameters.get("start_datetime")
        self.end_datetime = self.parameters.get("end_datetime")
        self.include_timezone = self.parameters.get("include_timezone", False)
        self.timezone = self.parameters.get("timezone", "UTC")

    def generate(self, context: GenerationContext | None = None) -> str:
        """生成日期时间字符串"""
        start_dt = None
        end_dt = None

        if self.start_datetime:
            start_dt = datetime.fromisoformat(self.start_datetime)
        else:
            start_dt = datetime.now() - timedelta(days=30)

        if self.end_datetime:
            end_dt = datetime.fromisoformat(self.end_datetime)
        else:
            end_dt = datetime.now() + timedelta(days=30)

        # 生成范围内的随机时间
        import secrets

        delta = end_dt - start_dt
        random_seconds = secrets.randbelow(int(delta.total_seconds()) + 1)
        dt = start_dt + timedelta(seconds=random_seconds)

        # 应用时区
        if self.include_timezone:
            tz = pytz.timezone(self.timezone)
            dt = tz.localize(dt)

        return self._format_datetime(dt)

    def _format_datetime(self, dt: datetime) -> str:
        """格式化日期时间"""
        if self.format == "ISO":
            return dt.isoformat()
        elif self.format == "ISO_MS":
            return dt.isoformat(timespec="milliseconds")
        elif self.format == "SQL":
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        elif self.format == "US":
            return dt.strftime("%m/%d/%Y %I:%M:%S %p")
        elif self.format == "CN":
            return dt.strftime("%Y年%m月%d日 %H时%M分%S秒")
        elif self.format.startswith("%"):  # 自定义格式
            return dt.strftime(self.format)
        else:
            return dt.isoformat()

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
            "end_datetime",
            "format",
            "include_timezone",
            "start_datetime",
            "timezone",
        ]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True
