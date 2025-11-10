"""
增强版日期时间生成器测试
"""
from dataforge.generators.datetime.enhanced_timestamp import (
    DateTimeRangeGenerator,
    EnhancedTimestampGenerator,
)


class TestDateTimeRangeGenerator:
    """日期时间范围生成器测试"""

    def test_basic_generation(self):
        """测试基础日期时间范围生成"""
        gen = DateTimeRangeGenerator({})
        result = gen.generate()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_custom_format(self):
        """测试自定义格式"""
        gen = DateTimeRangeGenerator({"format": "%Y/%m/%d %H:%M:%S"})
        result = gen.generate()
        assert "/" in result

    def test_date_range_constraints(self):
        """测试日期范围约束"""
        gen = DateTimeRangeGenerator({
            "start_datetime": "2024-01-01T00:00:00",
            "end_datetime": "2024-01-31T23:59:59",
        })
        result = gen.generate()
        assert "2024-01" in result

    def test_validation(self):
        """测试日期时间范围校验"""
        gen = DateTimeRangeGenerator({})

        # 有效格式
        assert gen.validate("2024-01-01T12:00:00") is True
        assert gen.validate("2024-01-01 12:00:00") is True

        # 无效格式
        assert gen.validate("invalid") is False


class TestEnhancedTimestampGenerator:
    """增强版时间戳生成器测试"""

    def test_basic_generation(self):
        """测试基础时间戳生成"""
        gen = EnhancedTimestampGenerator({})
        timestamp = gen.generate()
        assert isinstance(timestamp, int)
        assert timestamp > 0

    def test_millisecond_precision(self):
        """测试毫秒级精度"""
        gen = EnhancedTimestampGenerator({"precision": "MILLISECONDS"})
        timestamp = gen.generate()
        assert isinstance(timestamp, int)

    def test_microsecond_precision(self):
        """测试微秒级精度"""
        gen = EnhancedTimestampGenerator({"precision": "MICROSECONDS"})
        timestamp = gen.generate()
        assert isinstance(timestamp, int)

    def test_range_constraints(self):
        """测试范围约束"""
        gen = EnhancedTimestampGenerator({
            "start_date": "2021-01-01",
            "end_date": "2021-01-31",
        })
        timestamp = gen.generate()
        assert isinstance(timestamp, int)

    def test_string_output_format(self):
        """测试字符串输出格式"""
        gen = EnhancedTimestampGenerator({"output_format": "STRING"})
        timestamp = gen.generate()
        assert isinstance(timestamp, str)

    def test_iso_output_format(self):
        """测试ISO格式输出"""
        gen = EnhancedTimestampGenerator({"output_format": "ISO"})
        timestamp = gen.generate()
        assert isinstance(timestamp, str)
        assert "T" in timestamp

    def test_validation(self):
        """测试时间戳校验"""
        gen = EnhancedTimestampGenerator({})

        # 有效时间戳
        assert gen.validate(1609459200) is True
        assert gen.validate("1609459200") is True

        # 无效时间戳
        assert gen.validate("invalid") is False
        assert gen.validate(-1000) is False

    def test_edge_cases(self):
        """测试边界情况"""
        # 测试空参数
        gen = EnhancedTimestampGenerator({})
        timestamp = gen.generate()
        assert isinstance(timestamp, int)
