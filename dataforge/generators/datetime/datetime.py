"""
时间/日历类生成器
"""
import random
import time
from datetime import datetime, date, timedelta, timezone
from typing import Optional, Dict, Any, List, Union
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator


class DateGenerator(ValidatedDataGenerator[str]):
    """日期生成器"""
    
    def _setup(self) -> None:
        self.start_date = self.parameters.get('start_date', '1970-01-01')
        self.end_date = self.parameters.get('end_date', '2030-12-31')
        self.format_style = self.parameters.get('format', 'YYYY-MM-DD')
        self.locale = self.parameters.get('locale', 'ISO')  # ISO, CN, US
        self.business_days_only = self.parameters.get('business_days_only', False)
        self.exclude_holidays = self.parameters.get('exclude_holidays', False)
        
        # 日期格式映射
        self.format_patterns = {
            'YYYY-MM-DD': '%Y-%m-%d',
            'YYYY/MM/DD': '%Y/%m/%d',
            'DD/MM/YYYY': '%d/%m/%Y',
            'MM/DD/YYYY': '%m/%d/%Y',
            'YYYYMMDD': '%Y%m%d',
            'DD-MM-YYYY': '%d-%m-%Y',
            'MM-DD-YYYY': '%m-%d-%Y'
        }
        
        # 中国节假日（简化版）
        self.chinese_holidays = [
            '01-01',  # 元旦
            '02-14',  # 春节（简化）
            '05-01',  # 劳动节
            '10-01',  # 国庆节
        ]
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始日期"""
        start = datetime.strptime(self.start_date, '%Y-%m-%d').date()
        end = datetime.strptime(self.end_date, '%Y-%m-%d').date()
        
        # 计算日期范围
        delta = end - start
        
        while True:
            # 生成随机日期
            random_days = random.randint(0, delta.days)
            generated_date = start + timedelta(days=random_days)
            
            # 检查工作日限制
            if self.business_days_only and generated_date.weekday() >= 5:  # 周末
                continue
            
            # 检查节假日限制
            if self.exclude_holidays and self._is_holiday(generated_date):
                continue
            
            break
        
        # 格式化输出
        return self._format_date(generated_date)
    
    def _format_date(self, date_obj: date) -> str:
        """格式化日期"""
        pattern = self.format_patterns.get(self.format_style, '%Y-%m-%d')
        
        if self.locale.upper() == 'CN':
            # 中文格式
            return f"{date_obj.year}年{date_obj.month:02d}月{date_obj.day:02d}日"
        else:
            return date_obj.strftime(pattern)
    
    def _is_holiday(self, date_obj: date) -> bool:
        """检查是否为节假日"""
        date_str = f"{date_obj.month:02d}-{date_obj.day:02d}"
        return date_str in self.chinese_holidays
    
    def validate(self, data: str) -> bool:
        """校验日期"""
        if not isinstance(data, str):
            return False
        
        try:
            if self.locale.upper() == 'CN':
                # 中文日期格式验证
                import re
                pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
                match = re.match(pattern, data)
                if match:
                    year, month, day = map(int, match.groups())
                    datetime(year, month, day)
                    return True
                return False
            else:
                # 标准格式验证
                pattern = self.format_patterns.get(self.format_style, '%Y-%m-%d')
                datetime.strptime(data, pattern)
                return True
        except (ValueError, AttributeError):
            return False
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.DATETIME
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['start_date', 'end_date', 'format', 'locale', 'business_days_only', 'exclude_holidays']


class TimeGenerator(ValidatedDataGenerator[str]):
    """时间生成器"""
    
    def _setup(self) -> None:
        self.format_style = self.parameters.get('format', '24H')  # 24H, 12H, SECONDS, MILLISECONDS
        self.include_seconds = self.parameters.get('include_seconds', True)
        self.include_milliseconds = self.parameters.get('include_milliseconds', False)
        self.timezone_aware = self.parameters.get('timezone_aware', False)
        self.timezone = self.parameters.get('timezone', 'UTC')
        self.time_range = self.parameters.get('time_range', None)  # ('09:00', '17:00')
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始时间"""
        if self.time_range:
            return self._generate_time_in_range()
        
        # 生成随机时间
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        millisecond = random.randint(0, 999)
        
        return self._format_time(hour, minute, second, millisecond)
    
    def _generate_time_in_range(self) -> str:
        """在指定时间范围内生成时间"""
        start_time, end_time = self.time_range
        
        # 解析时间范围
        start_parts = start_time.split(':')
        end_parts = end_time.split(':')
        
        start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
        end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])
        
        # 生成范围内的随机分钟数
        if end_minutes < start_minutes:  # 跨天情况
            if random.random() < 0.5:
                random_minutes = random.randint(start_minutes, 24 * 60 - 1)
            else:
                random_minutes = random.randint(0, end_minutes)
        else:
            random_minutes = random.randint(start_minutes, end_minutes)
        
        hour = random_minutes // 60
        minute = random_minutes % 60
        second = random.randint(0, 59) if self.include_seconds else 0
        millisecond = random.randint(0, 999) if self.include_milliseconds else 0
        
        return self._format_time(hour, minute, second, millisecond)
    
    def _format_time(self, hour: int, minute: int, second: int, millisecond: int) -> str:
        """格式化时间"""
        if self.format_style.upper() == '12H':
            # 12小时制
            am_pm = 'AM' if hour < 12 else 'PM'
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
            if self.timezone.upper() == 'UTC':
                time_str += ' UTC'
            else:
                time_str += f' {self.timezone}'
        
        return time_str
    
    def validate(self, data: str) -> bool:
        """校验时间"""
        if not isinstance(data, str):
            return False
        
        try:
            # 移除时区和AM/PM信息进行基本验证
            clean_time = data.replace(' UTC', '').replace(' AM', '').replace(' PM', '')
            
            # 基本时间格式验证
            import re
            if self.format_style.upper() == '12H':
                pattern = r'^(1[0-2]|0?[1-9]):[0-5][0-9](:[0-5][0-9])?(\.[0-9]{3})?$'
            else:
                pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?(\.[0-9]{3})?$'
            
            return bool(re.match(pattern, clean_time))
        except:
            return False
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.DATETIME
    
    @property
    def supported_parameters(self) -> List[str]:
        return [
            'format', 'include_seconds', 'include_milliseconds', 
            'timezone_aware', 'timezone', 'time_range'
        ]


class TimestampGenerator(ValidatedDataGenerator[Union[int, str]]):
    """时间戳生成器"""
    
    def _setup(self) -> None:
        self.start_timestamp = self.parameters.get('start_timestamp', 0)
        self.end_timestamp = self.parameters.get('end_timestamp', int(time.time()))
        self.precision = self.parameters.get('precision', 'SECONDS')  # SECONDS, MILLISECONDS, MICROSECONDS
        self.output_format = self.parameters.get('output_format', 'INTEGER')  # INTEGER, STRING, ISO
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> Union[int, str]:
        """生成原始时间戳"""
        # 生成随机时间戳
        if self.precision.upper() == 'MILLISECONDS':
            start = self.start_timestamp * 1000
            end = self.end_timestamp * 1000
            timestamp = random.randint(start, end)
        elif self.precision.upper() == 'MICROSECONDS':
            start = self.start_timestamp * 1000000
            end = self.end_timestamp * 1000000
            timestamp = random.randint(start, end)
        else:  # SECONDS
            timestamp = random.randint(self.start_timestamp, self.end_timestamp)
        
        # 格式化输出
        if self.output_format.upper() == 'STRING':
            return str(timestamp)
        elif self.output_format.upper() == 'ISO':
            # 转换为ISO格式
            if self.precision.upper() == 'MILLISECONDS':
                dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
            elif self.precision.upper() == 'MICROSECONDS':
                dt = datetime.fromtimestamp(timestamp / 1000000, tz=timezone.utc)
            else:
                dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            return dt.isoformat()
        else:  # INTEGER
            return timestamp
    
    def validate(self, data: Union[int, str]) -> bool:
        """校验时间戳"""
        if isinstance(data, str):
            if self.output_format.upper() == 'ISO':
                try:
                    datetime.fromisoformat(data.replace('Z', '+00:00'))
                    return True
                except:
                    return False
            else:
                try:
                    int(data)
                    return True
                except:
                    return False
        elif isinstance(data, int):
            return data >= 0
        
        return False
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.DATETIME
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['start_timestamp', 'end_timestamp', 'precision', 'output_format']


class CronExpressionGenerator(ValidatedDataGenerator[str]):
    """Cron表达式生成器"""
    
    def _setup(self) -> None:
        self.format_type = self.parameters.get('format', 'STANDARD')  # STANDARD, EXTENDED
        self.preset_type = self.parameters.get('preset', None)  # DAILY, WEEKLY, MONTHLY, HOURLY
        self.allow_special_chars = self.parameters.get('allow_special_chars', True)
        
        # 预设Cron表达式
        self.presets = {
            'HOURLY': '0 * * * *',
            'DAILY': '0 0 * * *',
            'WEEKLY': '0 0 * * 0',
            'MONTHLY': '0 0 1 * *',
            'YEARLY': '0 0 1 1 *'
        }
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始Cron表达式"""
        if self.preset_type and self.preset_type.upper() in self.presets:
            return self.presets[self.preset_type.upper()]
        
        # 生成随机Cron表达式
        minute = self._generate_field(0, 59, 'minute')
        hour = self._generate_field(0, 23, 'hour')
        day = self._generate_field(1, 31, 'day')
        month = self._generate_field(1, 12, 'month')
        weekday = self._generate_field(0, 6, 'weekday')
        
        cron_expr = f"{minute} {hour} {day} {month} {weekday}"
        
        # 扩展格式包含秒
        if self.format_type.upper() == 'EXTENDED':
            second = self._generate_field(0, 59, 'second')
            cron_expr = f"{second} {cron_expr}"
        
        return cron_expr
    
    def _generate_field(self, min_val: int, max_val: int, field_type: str) -> str:
        """生成Cron字段"""
        if not self.allow_special_chars or random.random() < 0.3:
            # 30%概率生成具体数值
            return str(random.randint(min_val, max_val))
        
        # 生成特殊字符表达式
        special_type = random.choice(['wildcard', 'range', 'list', 'step'])
        
        if special_type == 'wildcard':
            return '*'
        elif special_type == 'range':
            start = random.randint(min_val, max_val - 1)
            end = random.randint(start + 1, max_val)
            return f"{start}-{end}"
        elif special_type == 'list':
            count = random.randint(2, 4)
            values = random.sample(range(min_val, max_val + 1), count)
            return ','.join(map(str, sorted(values)))
        else:  # step
            step = random.randint(2, 5)
            if random.random() < 0.5:
                return f"*/{step}"
            else:
                start = random.randint(min_val, max_val // 2)
                return f"{start}/{step}"
    
    def validate(self, data: str) -> bool:
        """校验Cron表达式"""
        if not isinstance(data, str):
            return False
        
        parts = data.strip().split()
        
        # 检查字段数量
        if self.format_type.upper() == 'EXTENDED':
            if len(parts) != 6:
                return False
        else:
            if len(parts) != 5:
                return False
        
        # 基本格式检查
        import re
        cron_field_pattern = r'^(\*|[0-9]+(-[0-9]+)?(,[0-9]+(-[0-9]+)?)*)(\/[0-9]+)?$'
        
        for part in parts:
            if not re.match(cron_field_pattern, part):
                return False
        
        return True
    
    def get_next_run_time(self, cron_expr: str) -> Optional[datetime]:
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
        except:
            return None
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.DATETIME
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['format', 'preset', 'allow_special_chars']


@register_generator('date', ['日期'])
class GenericDateGenerator(DateGenerator):
    """通用日期生成器注册版本"""
    pass


@register_generator('time', ['时间'])
class GenericTimeGenerator(TimeGenerator):
    """通用时间生成器注册版本"""
    pass


@register_generator('timestamp', ['时间戳'])
class GenericTimestampGenerator(TimestampGenerator):
    """通用时间戳生成器注册版本"""
    pass


@register_generator('cron', ['cron表达式'])
class GenericCronExpressionGenerator(CronExpressionGenerator):
    """通用Cron表达式生成器注册版本"""
    pass