#!/usr/bin/env python3
"""
DataForge 完整时间生成器演示脚本

展示DataForge中所有时间相关生成器的完整功能：
1. 基础时间戳生成器
2. 增强时间戳生成器
3. 高级时间戳生成器
4. 日期时间范围生成器

运行方法:
    python demo_complete_datetime.py
"""

import sys
from datetime import datetime

# 确保DataForge在路径中
sys.path.insert(0, '.')

from dataforge.generators.datetime import (
    GenericAdvancedDateTimeRangeGenerator,
    GenericAdvancedTimestampGenerator,
    GenericEnhancedTimestampGenerator,
    GenericTimestampGenerator,
)


def demo_basic_timestamp():
    """演示基础时间戳生成器"""
    print("🔍 基础时间戳生成器演示")
    print("=" * 50)

    gen = GenericTimestampGenerator()

    # 基础生成
    result = gen.generate()
    print(f"基础Unix时间戳: {result}")

    # 验证功能
    is_valid = gen.validate(result)
    print(f"验证结果: {is_valid}")

    print()


def demo_enhanced_timestamp():
    """演示增强时间戳生成器"""
    print("⚡ 增强时间戳生成器演示")
    print("=" * 50)

    # 毫秒级精度
    gen_ms = GenericEnhancedTimestampGenerator({
        "precision": "milliseconds",
        "output_format": "INTEGER"
    })
    result_ms = gen_ms.generate()
    print(f"毫秒级时间戳: {result_ms}")

    # ISO格式
    gen_iso = GenericEnhancedTimestampGenerator({
        "precision": "seconds",
        "output_format": "ISO"
    })
    result_iso = gen_iso.generate()
    print(f"ISO格式时间戳: {result_iso}")

    print()


def demo_advanced_timestamp():
    """演示高级时间戳生成器"""
    print("🚀 高级时间戳生成器演示")
    print("=" * 50)

    # 1. 多种精度支持
    precisions = ["SECONDS", "MILLISECONDS", "MICROSECONDS", "NANOSECONDS"]
    for precision in precisions:
        gen = GenericAdvancedTimestampGenerator({
            "precision": precision,
            "format": "UNIX"
        })
        result = gen.generate()
        print(f"{precision}精度: {result}")

    print()

    # 2. 格式输出
    formats = ["UNIX", "ISO", "CUSTOM"]
    for fmt in formats:
        gen = GenericAdvancedTimestampGenerator({
            "format": fmt,
            "custom_format": "%Y-%m-%d %H:%M:%S" if fmt == "CUSTOM" else None
        })
        result = gen.generate()
        print(f"{fmt}格式: {result}")

    print()

    # 3. 时区处理
    gen_utc = GenericAdvancedTimestampGenerator({
        "timezone_aware": True,
        "timezone": "UTC",
        "format": "ISO"
    })
    result_utc = gen_utc.generate()
    print(f"UTC时区: {result_utc}")

    gen_local = GenericAdvancedTimestampGenerator({
        "timezone_aware": True,
        "timezone": "Asia/Shanghai",
        "format": "ISO"
    })
    result_local = gen_local.generate()
    print(f"上海时区: {result_local}")

    print()

    # 4. 日期范围限制
    gen_range = GenericAdvancedTimestampGenerator({
        "start_date": "2024-01-01T00:00:00",
        "end_date": "2024-12-31T23:59:59",
        "format": "ISO"
    })
    result_range = gen_range.generate()
    print(f"日期范围限制: {result_range}")

    # 验证范围
    dt = datetime.fromisoformat(result_range)
    start_dt = datetime.fromisoformat("2024-01-01T00:00:00")
    end_dt = datetime.fromisoformat("2024-12-31T23:59:59")
    print(f"验证范围: {start_dt <= dt <= end_dt}")

    print()

    # 5. 相对时间
    gen_relative = GenericAdvancedTimestampGenerator({
        "relative_to": "TODAY",
        "offset_days": 7,
        "offset_hours": 12,
        "format": "ISO"
    })
    result_relative = gen_relative.generate()
    print(f"相对时间(7天12小时后): {result_relative}")

    print()


def demo_datetime_range():
    """演示日期时间范围生成器"""
    print("📅 日期时间范围生成器演示")
    print("=" * 50)

    # 1. 基础范围生成
    gen_range = GenericAdvancedDateTimeRangeGenerator({
        "duration_days": 7,
        "format": "RANGE"
    })
    result_range = gen_range.generate()
    print(f"7天范围: {result_range}")

    # 2. 持续时间格式
    gen_duration = GenericAdvancedDateTimeRangeGenerator({
        "duration_days": 2,
        "duration_hours": 12,
        "format": "DURATION"
    })
    result_duration = gen_duration.generate()
    print(f"持续时间: {result_duration}")

    # 3. 自定义起始时间
    gen_custom = GenericAdvancedDateTimeRangeGenerator({
        "start_datetime": "2024-06-15T08:00:00",
        "duration_hours": 3,
        "format": "ISO"
    })
    result_custom = gen_custom.generate()
    print(f"自定义起始: {result_custom}")

    # 4. 多种格式
    formats = ["ISO", "SQL", "CN", "US"]
    for fmt in formats:
        gen = GenericAdvancedDateTimeRangeGenerator({
            "duration_hours": 1,
            "format": fmt
        })
        result = gen.generate()
        print(f"{fmt}格式: {result}")

    # 5. 时区支持
    gen_tz = GenericAdvancedDateTimeRangeGenerator({
        "duration_hours": 2,
        "include_timezone": True,
        "timezone": "UTC",
        "format": "ISO"
    })
    result_tz = gen_tz.generate()
    print(f"UTC时区范围: {result_tz}")

    print()


def demo_batch_generation():
    """演示批量生成功能"""
    print("📊 批量生成功能演示")
    print("=" * 50)

    # 高级时间戳批量生成
    gen = GenericAdvancedTimestampGenerator({
        "format": "ISO",
        "start_date": "2024-01-01T00:00:00",
        "end_date": "2024-01-31T23:59:59"
    })

    print("生成10个随机时间戳:")
    for i, ts in enumerate(gen.generate_batch(10), 1):
        print(f"  {i:2d}. {ts}")

    print()

    # 日期范围批量生成
    range_gen = GenericAdvancedDateTimeRangeGenerator({
        "duration_days": 1,
        "format": "RANGE"
    })

    print("生成5个日期范围:")
    for i, range_str in enumerate(range_gen.generate_batch(5), 1):
        print(f"  {i:2d}. {range_str}")

    print()


def demo_validation():
    """演示验证功能"""
    print("✅ 验证功能演示")
    print("=" * 50)

    # 高级时间戳验证
    gen = GenericAdvancedTimestampGenerator()

    test_values = [
        1704067200,                    # 有效Unix时间戳
        "1704067200",                  # 有效字符串
        "2024-01-01T00:00:00",         # 有效ISO格式
        "invalid",                     # 无效值
        -1,                            # 无效负数
    ]

    for value in test_values:
        is_valid = gen.validate(value)
        print(f"验证 {value}: {is_valid}")

    print()

    # 日期范围验证
    range_gen = GenericAdvancedDateTimeRangeGenerator()

    test_ranges = [
        "2024-01-01 00:00:00 至 2024-01-02 00:00:00",
        "invalid range",
        "2024-13-01 00:00:00 至 2024-01-02 00:00:00",  # 无效日期
    ]

    for range_str in test_ranges:
        is_valid = range_gen.validate(range_str)
        print(f"验证范围 '{range_str}': {is_valid}")

    print()


def main():
    """主函数"""
    print("🎯 DataForge 时间生成器完整演示")
    print("=" * 60)

    try:
        # 按顺序演示各个功能
        demo_basic_timestamp()
        demo_enhanced_timestamp()
        demo_advanced_timestamp()
        demo_datetime_range()
        demo_batch_generation()
        demo_validation()

        print("🎉 所有演示完成！DataForge时间生成器已完全集成并正常工作。")

    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
