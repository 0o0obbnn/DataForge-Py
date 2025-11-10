"""
时间/日历类生成器测试套件
"""

from datetime import datetime
from unittest.mock import patch

from dataforge.generators.datetime.datetime import (
    CronExpressionGenerator,
    DateGenerator,
    TimeGenerator,
    TimestampGenerator,
)


class TestDateGenerator:
    """日期生成器测试类"""

    def test_basic_date_generation(self):
        """测试基本日期生成"""
        gen = DateGenerator({})
        result = gen.generate()
        assert isinstance(result, str)
        assert len(result.split('-')) == 3  # YYYY-MM-DD格式

    def test_custom_date_range(self):
        """测试自定义日期范围"""
        gen = DateGenerator({
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        })
        result = gen.generate()
        date_obj = datetime.strptime(result, "%Y-%m-%d").date()
        assert datetime(2023, 1, 1).date() <= date_obj <= datetime(2023, 12, 31).date()

    def test_chinese_format(self):
        """测试中文格式"""
        gen = DateGenerator({
            "locale": "CN",
            "start_date": "2023-01-01",
            "end_date": "2023-01-01"
        })
        result = gen.generate()
        assert "年" in result and "月" in result and "日" in result
        assert "2023年01月01日" == result

    def test_business_days_only(self):
        """测试仅工作日生成"""
        gen = DateGenerator({
            "business_days_only": True,
            "start_date": "2023-01-01",
            "end_date": "2023-01-31"
        })

        # 生成多个日期并验证都是工作日
        for _ in range(10):
            result = gen.generate()
            date_obj = datetime.strptime(result, "%Y-%m-%d").date()
            assert date_obj.weekday() < 5  # 周一到周五

    def test_exclude_holidays(self):
        """测试排除节假日"""
        gen = DateGenerator({
            "exclude_holidays": True,
            "start_date": "2023-01-01",
            "end_date": "2023-01-02"
        })

        # 元旦是节假日，应该只返回1月2日
        result = gen.generate()
        assert result == "2023-01-02"

    def test_date_validation(self):
        """测试日期验证"""
        gen = DateGenerator()
        assert gen.validate("2023-12-25") is True
        assert gen.validate("2023-13-25") is False
        assert gen.validate("invalid-date") is False

    def test_chinese_date_validation(self):
        """测试中文日期验证"""
        gen = DateGenerator({"locale": "CN"})
        assert gen.validate("2023年12月25日") is True
        assert gen.validate("2023年13月25日") is False


class TestTimeGenerator:
    """时间生成器测试类"""

    def test_basic_time_generation(self):
        """测试基本时间生成"""
        gen = TimeGenerator()
        result = gen.generate()
        assert isinstance(result, str)
        assert len(result.split(':')) >= 2  # 至少有时:分

    def test_12_hour_format(self):
        """测试12小时制"""
        gen = TimeGenerator({"format": "12H"})
        result = gen.generate()
        assert "AM" in result or "PM" in result

    def test_time_range_generation(self):
        """测试时间范围生成"""
        gen = TimeGenerator({
            "time_range": ("09:00", "17:00")
        })
        result = gen.generate()

        # 解析时间并验证在范围内
        time_parts = result.split(':')
        hour = int(time_parts[0])
        assert 9 <= hour <= 17

    def test_timezone_aware(self):
        """测试时区信息"""
        gen = TimeGenerator({
            "timezone_aware": True,
            "timezone": "UTC"
        })
        result = gen.generate()
        assert "UTC" in result

    def test_seconds_and_milliseconds(self):
        """测试秒和毫秒"""
        gen = TimeGenerator({
            "include_seconds": True,
            "include_milliseconds": True
        })
        result = gen.generate()
        assert '.' in result  # 应该包含毫秒

    def test_time_validation(self):
        """测试时间验证"""
        gen = TimeGenerator()
        assert gen.validate("14:30") is True
        assert gen.validate("25:30") is False
        assert gen.validate("invalid-time") is False


class TestTimestampGenerator:
    """时间戳生成器测试类"""

    def test_basic_timestamp_generation(self):
        """测试基本时间戳生成"""
        gen = TimestampGenerator()
        result = gen.generate()
        assert isinstance(result, int)
        assert result > 0

    def test_string_output_format(self):
        """测试字符串输出格式"""
        gen = TimestampGenerator({"output_format": "STRING"})
        result = gen.generate()
        assert isinstance(result, str)
        assert result.isdigit()

    def test_iso_output_format(self):
        """测试ISO格式输出"""
        gen = TimestampGenerator({"output_format": "ISO"})
        result = gen.generate()
        assert isinstance(result, str)
        assert 'T' in result  # ISO格式包含T分隔符

    def test_millisecond_precision(self):
        """测试毫秒精度"""
        gen = TimestampGenerator({
            "precision": "MILLISECONDS",
            "output_format": "STRING"
        })
        result = int(gen.generate())
        # 毫秒时间戳应该更大
        assert result > 1_000_000_000_000

    def test_microsecond_precision(self):
        """测试微秒精度"""
        gen = TimestampGenerator({
            "precision": "MICROSECONDS",
            "output_format": "STRING"
        })
        result = int(gen.generate())
        # 微秒时间戳应该更大
        assert result > 1_000_000_000_000_000

    def test_custom_timestamp_range(self):
        """测试自定义时间戳范围"""
        start_ts = 1_600_000_000  # 2020-09-13
        end_ts = 1_700_000_000    # 2023-11-14

        gen = TimestampGenerator({
            "start_timestamp": start_ts,
            "end_timestamp": end_ts
        })
        result = gen.generate()
        assert start_ts <= result <= end_ts

    def test_timestamp_validation(self):
        """测试时间戳验证"""
        gen = TimestampGenerator()
        assert gen.validate(1_600_000_000) is True
        assert gen.validate("1600000000") is True
        assert gen.validate("invalid") is False

    def test_iso_timestamp_validation(self):
        """测试ISO时间戳验证"""
        gen = TimestampGenerator({"output_format": "ISO"})
        assert gen.validate("2023-12-25T10:30:00") is True
        assert gen.validate("invalid-iso") is False


class TestCronExpressionGenerator:
    """Cron表达式生成器测试类"""

    def test_basic_cron_generation(self):
        """测试基本Cron表达式生成"""
        gen = CronExpressionGenerator()
        result = gen.generate()
        assert isinstance(result, str)
        assert len(result.split()) == 5  # 标准5字段格式

    def test_preset_cron_expressions(self):
        """测试预设Cron表达式"""
        gen = CronExpressionGenerator({"preset": "DAILY"})
        result = gen.generate()
        assert result == "0 0 * * *"

    def test_extended_format(self):
        """测试扩展格式（包含秒）"""
        gen = CronExpressionGenerator({
            "format": "EXTENDED"
        })
        result = gen.generate()
        assert len(result.split()) == 6  # 扩展6字段格式

    def test_cron_validation(self):
        """测试Cron表达式验证"""
        gen = CronExpressionGenerator()
        assert gen.validate("0 0 * * *") is True
        assert gen.validate("60 0 * * *") is False  # 分钟不能为60
        assert gen.validate("invalid cron") is False

    def test_special_characters(self):
        """测试特殊字符生成"""
        gen = CronExpressionGenerator({"allow_special_chars": True})
        result = gen.generate()
        # 可能包含特殊字符
        assert any(char in result for char in ['*', '-', ',', '/'])

    def test_next_run_time(self):
        """测试下次执行时间计算"""
        gen = CronExpressionGenerator()
        cron_expr = "0 0 * * *"
        next_run = gen.get_next_run_time(cron_expr)
        assert next_run is not None
        assert isinstance(next_run, datetime)

    def test_cron_field_generation(self):
        """测试各个字段的生成"""
        gen = CronExpressionGenerator()

        # 测试分钟字段
        minute_field = gen._generate_field(0, 59, "minute")
        assert isinstance(minute_field, str)

        # 测试通配符
        with patch('random.random', return_value=0.8):
            with patch('random.choice', return_value='wildcard'):
                result = gen._generate_field(0, 59, "test")
                assert result == "*"

    def test_cron_range_generation(self):
        """测试范围格式生成"""
        gen = CronExpressionGenerator()

        with patch('random.randint', side_effect=[10, 20]):
            result = gen._generate_field(0, 59, "minute")
            assert result == "10-20"

    def test_cron_list_generation(self):
        """测试列表格式生成"""
        gen = CronExpressionGenerator()

        with patch('random.sample', return_value=[5, 15, 25]):
            result = gen._generate_field(0, 59, "minute")
            assert result == "5,15,25"

    def test_cron_step_generation(self):
        """测试步长格式生成"""
        gen = CronExpressionGenerator()

        with patch('random.randint', side_effect=[0, 5]):
            with patch('random.random', return_value=0.3):
                result = gen._generate_field(0, 59, "minute")
                assert result == "*/5"
