#!/usr/bin/env python3
"""
高级时间戳生成器演示脚本

演示DataForge中高级时间戳生成器的各种功能特性：
- 多种精度支持（秒、毫秒、微秒、纳秒）
- 多种格式输出（Unix、ISO、自定义）
- 时区处理
- 日期范围限制
- 上下文关联
- 日期时间范围生成
"""

from datetime import datetime

from dataforge.generators.datetime import (
    GenericAdvancedDateTimeRangeGenerator,
    GenericAdvancedTimestampGenerator,
)


def demo_advanced_timestamp():
    """演示高级时间戳生成器"""
    print("🕐 高级时间戳生成器演示")
    print("=" * 50)

    # 1. 基础Unix时间戳（秒级）
    print("\n1️⃣ 基础Unix时间戳（秒级）")
    generator = GenericAdvancedTimestampGenerator()
    timestamp = generator.generate()
    print(f"Unix时间戳: {timestamp}")
    print(f"转换时间: {datetime.fromtimestamp(timestamp)}")

    # 2. 毫秒级时间戳
    print("\n2️⃣ 毫秒级时间戳")
    generator = GenericAdvancedTimestampGenerator({
        "precision": "MILLISECONDS",
        "format": "UNIX"
    })
    timestamp = generator.generate()
    print(f"毫秒级时间戳: {timestamp}")
    print(f"转换时间: {datetime.fromtimestamp(timestamp/1000)}")

    # 3. ISO8601格式
    print("\n3️⃣ ISO8601格式")
    generator = GenericAdvancedTimestampGenerator({
        "format": "ISO",
        "timezone_aware": True,
        "timezone": "UTC"
    })
    iso_time = generator.generate()
    print(f"ISO8601格式: {iso_time}")

    # 4. 自定义格式
    print("\n4️⃣ 自定义格式")
    generator = GenericAdvancedTimestampGenerator({
        "format": "CUSTOM",
        "custom_format": "%Y年%m月%d日 %H时%M分%S秒"
    })
    custom_time = generator.generate()
    print(f"自定义格式: {custom_time}")

    # 5. 日期范围限制
    print("\n5️⃣ 日期范围限制")
    generator = GenericAdvancedTimestampGenerator({
        "start_date": "2024-01-01T00:00:00",
        "end_date": "2024-12-31T23:59:59",
        "format": "ISO"
    })
    range_time = generator.generate()
    print(f"范围内时间: {range_time}")

    # 6. 相对时间偏移
    print("\n6️⃣ 相对时间偏移")
    generator = GenericAdvancedTimestampGenerator({
        "relative_to": "TODAY",
        "offset_days": 7,
        "format": "CUSTOM",
        "custom_format": "%Y-%m-%d %H:%M:%S"
    })
    offset_time = generator.generate()
    print(f"一周后时间: {offset_time}")


def demo_datetime_range():
    """演示日期时间范围生成器"""
    print("\n\n📅 日期时间范围生成器演示")
    print("=" * 50)

    # 1. 基础范围
    print("\n1️⃣ 基础日期范围")
    generator = GenericAdvancedDateTimeRangeGenerator({
        "duration_days": 7,
        "format": "RANGE"
    })
    date_range = generator.generate()
    print(f"日期范围: {date_range}")

    # 2. 持续时间格式
    print("\n2️⃣ 持续时间格式")
    generator = GenericAdvancedDateTimeRangeGenerator({
        "duration_days": 3,
        "duration_hours": 12,
        "format": "DURATION"
    })
    duration_str = generator.generate()
    print(f"持续时间: {duration_str}")

    # 3. 中文格式
    print("\n3️⃣ 中文格式")
    generator = GenericAdvancedDateTimeRangeGenerator({
        "duration_hours": 24,
        "format": "CN"
    })
    cn_format = generator.generate()
    print(f"中文格式: {cn_format}")

    # 4. 自定义起始时间
    print("\n4️⃣ 自定义起始时间")
    generator = GenericAdvancedDateTimeRangeGenerator({
        "start_datetime": "2024-06-15T08:30:00",
        "duration_hours": 2,
        "format": "SQL"
    })
    custom_range = generator.generate()
    print(f"自定义起始: {custom_range}")


def demo_validation():
    """演示验证功能"""
    print("\n\n✅ 验证功能演示")
    print("=" * 30)

    # 时间戳验证
    timestamp_gen = GenericAdvancedTimestampGenerator()

    valid_timestamps = [
        "1704067200",
        "2024-01-01T00:00:00",
        "2024年01月01日 00时00分00秒"
    ]

    for ts in valid_timestamps:
        is_valid = timestamp_gen.validate(ts)
        print(f"验证 '{ts}': {'✅' if is_valid else '❌'}")

    # 日期范围验证
    range_gen = GenericAdvancedDateTimeRangeGenerator()

    valid_ranges = [
        "2024-01-01 00:00:00",
        "2024-01-01 至 2024-01-02",
        "2024年01月01日 00时00分00秒"
    ]

    for range_str in valid_ranges:
        is_valid = range_gen.validate(range_str)
        print(f"验证 '{range_str}': {'✅' if is_valid else '❌'}")


def demo_batch_generation():
    """演示批量生成"""
    print("\n\n🔄 批量生成演示")
    print("=" * 30)

    # 批量生成时间戳
    generator = GenericAdvancedTimestampGenerator({
        "format": "ISO",
        "start_date": "2024-01-01T00:00:00",
        "end_date": "2024-01-31T23:59:59"
    })

    print("批量生成1月份时间戳（前5个）：")
    for i in range(5):
        timestamp = generator.generate()
        print(f"  {i+1}. {timestamp}")

    # 批量生成日期范围
    range_gen = GenericAdvancedDateTimeRangeGenerator({
        "duration_days": 1,
        "format": "RANGE"
    })

    print("\n批量生成日期范围（前3个）：")
    for i in range(3):
        date_range = range_gen.generate()
        print(f"  {i+1}. {date_range}")


if __name__ == "__main__":
    try:
        demo_advanced_timestamp()
        demo_datetime_range()
        demo_validation()
        demo_batch_generation()

        print("\n🎉 演示完成！")
        print("高级时间戳生成器已成功集成到DataForge系统中")

    except Exception as e:
        print(f"\n❌ 演示出错: {e}")
        import traceback
        traceback.print_exc()
