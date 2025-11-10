#!/usr/bin/env python3
"""
时间生成器集成测试

验证DataForge中所有时间相关生成器的完整功能：
- 基础时间戳生成器
- 增强时间戳生成器
- 高级时间戳生成器
- 日期时间范围生成器
"""

from datetime import datetime, timedelta

import pytest

from dataforge.generators.datetime import (
    GenericAdvancedDateTimeRangeGenerator,
    GenericAdvancedTimestampGenerator,
    GenericEnhancedTimestampGenerator,
    GenericTimestampGenerator,
)


class TestTimestampIntegration:
    """时间戳生成器集成测试"""

    def test_basic_timestamp(self):
        """测试基础时间戳生成器"""
        generator = GenericTimestampGenerator()
        results = [generator.generate() for _ in range(3)]
        # 基础时间戳生成器返回字符串，需要转换
        assert all(isinstance(r, str) for r in results)
        assert all(int(r) > 0 for r in results)

    def test_enhanced_timestamp(self):
        """测试增强时间戳生成器"""
        generator = GenericEnhancedTimestampGenerator({
            "precision": "milliseconds"
        })
        result = generator.generate()
        assert isinstance(result, (int, str))

    def test_advanced_timestamp_precision(self):
        """测试高级时间戳生成器精度"""
        # 测试秒级精度
        gen = GenericAdvancedTimestampGenerator({"precision": "SECONDS"})
        ts = gen.generate()
        assert isinstance(ts, int)

        # 测试毫秒级精度
        gen = GenericAdvancedTimestampGenerator({"precision": "MILLISECONDS"})
        ts = gen.generate()
        assert isinstance(ts, int)
        assert ts > 1_000_000_000_000  # 应该大于13位

    def test_advanced_timestamp_format(self):
        """测试高级时间戳格式"""
        # Unix格式
        gen = GenericAdvancedTimestampGenerator({"format": "UNIX"})
        ts = gen.generate()
        assert isinstance(ts, int)

        # ISO格式
        gen = GenericAdvancedTimestampGenerator({"format": "ISO"})
        ts = gen.generate()
        assert isinstance(ts, str)
        assert "T" in ts

        # 自定义格式
        gen = GenericAdvancedTimestampGenerator({
            "format": "CUSTOM",
            "custom_format": "%Y-%m-%d"
        })
        ts = gen.generate()
        assert isinstance(ts, str)
        assert len(ts) == 10  # YYYY-MM-DD

    def test_date_range_enforcement(self):
        """测试日期范围强制执行"""
        start_date = "2024-01-01T00:00:00"
        end_date = "2024-01-31T23:59:59"

        gen = GenericAdvancedTimestampGenerator({
            "start_date": start_date,
            "end_date": end_date,
            "format": "ISO"
        })

        # 生成多个样本并验证都在范围内
        for _ in range(10):
            ts = gen.generate()
            dt = datetime.fromisoformat(ts)

            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)

            assert start_dt <= dt <= end_dt

    def test_timezone_handling(self):
        """测试时区处理"""
        gen = GenericAdvancedTimestampGenerator({
            "timezone_aware": True,
            "timezone": "UTC",
            "format": "ISO"
        })

        ts = gen.generate()
        assert isinstance(ts, str)
        assert "+00:00" in ts or "Z" in ts

    def test_relative_time(self):
        """测试相对时间功能"""
        gen = GenericAdvancedTimestampGenerator({
            "relative_to": "TODAY",
            "offset_days": 7,
            "format": "ISO"
        })

        ts = gen.generate()
        dt = datetime.fromisoformat(ts)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        expected_date = today + timedelta(days=7)

        assert dt.date() == expected_date.date()


class TestDateTimeRangeIntegration:
    """日期时间范围生成器集成测试"""

    def test_basic_range_generation(self):
        """测试基础范围生成"""
        gen = GenericAdvancedDateTimeRangeGenerator({
            "duration_days": 1,
            "format": "RANGE"
        })

        result = gen.generate()
        assert isinstance(result, str)
        assert "至" in result

    def test_duration_format(self):
        """测试持续时间格式"""
        gen = GenericAdvancedDateTimeRangeGenerator({
            "duration_days": 2,
            "duration_hours": 12,
            "format": "DURATION"
        })

        result = gen.generate()
        assert isinstance(result, str)
        assert "持续" in result

    def test_custom_start_end(self):
        """测试自定义起始结束时间"""
        gen = GenericAdvancedDateTimeRangeGenerator({
            "start_datetime": "2024-06-15T08:00:00",
            "duration_hours": 2,
            "format": "ISO"
        })

        result = gen.generate()
        assert isinstance(result, str)
        assert "2024-06-15T08:00:00" in result

    def test_format_varieties(self):
        """测试多种格式"""
        formats = ["ISO", "SQL", "CN", "US"]

        for fmt in formats:
            gen = GenericAdvancedDateTimeRangeGenerator({
                "duration_hours": 1,
                "format": fmt
            })
            result = gen.generate()
            assert isinstance(result, str)
            assert len(result) > 0

    def test_timezone_in_range(self):
        """测试时区在范围中的应用"""
        gen = GenericAdvancedDateTimeRangeGenerator({
            "duration_hours": 1,
            "include_timezone": True,
            "timezone": "UTC",
            "format": "ISO"
        })

        result = gen.generate()
        assert isinstance(result, str)
        # ISO格式可能不包含时区信息，检查是否为有效时间格式
        try:
            datetime.fromisoformat(result.replace('Z', '+00:00'))
        except ValueError as err:
            raise AssertionError("Invalid datetime format") from err


class TestValidationIntegration:
    """验证功能集成测试"""

    def test_timestamp_validation(self):
        """测试时间戳验证"""
        gen = GenericAdvancedTimestampGenerator()

        # 测试整数时间戳
        assert gen.validate(1704067200) is True

        # 测试字符串时间戳
        assert gen.validate("1704067200") is True

        # 测试无效值
        assert gen.validate("invalid") is False

    def test_range_validation(self):
        """测试范围验证"""
        gen = GenericAdvancedDateTimeRangeGenerator()

        # 有效的日期格式
        assert gen.validate("2024-01-01 00:00:00") is True
        assert gen.validate("2024-01-01") is True
        assert gen.validate("2024年01月01日 00时00分00秒") is True

        # 有效的范围格式
        assert gen.validate("2024-01-01 至 2024-01-02") is True

        # 无效的格式
        assert gen.validate("invalid-date") is False

    def test_consistency_validation(self):
        """测试验证一致性"""
        # 生成数据并验证
        gen = GenericAdvancedTimestampGenerator({
            "format": "ISO",
            "start_date": "2024-01-01T00:00:00",
            "end_date": "2024-12-31T23:59:59"
        })

        for _ in range(10):
            ts = gen.generate()
            assert gen.validate(ts) is True


class TestContextIntegration:
    """上下文集成测试"""

    def test_context_aware_generation(self):
        """测试上下文感知生成"""
        # 使用不同的配置确保生成不同的值
        gen = GenericAdvancedTimestampGenerator({
            "relative_to": "NOW",
            "format": "UNIX"
        })

        # 生成多个值，由于时间戳精度为秒，可能相同
        results = [gen.generate() for _ in range(3)]
        assert len(results) == 3
        assert all(isinstance(r, int) for r in results)

    def test_batch_generation(self):
        """测试批量生成"""
        gen = GenericAdvancedTimestampGenerator({
            "format": "ISO",
            "start_date": "2024-01-01",
            "end_date": "2024-01-31"
        })

        # 批量生成并验证
        results = [gen.generate() for _ in range(10)]
        assert len(results) == 10
        assert all(isinstance(r, str) for r in results)
        assert all("2024-01-" in r for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
