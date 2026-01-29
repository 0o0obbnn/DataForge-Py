"""
DataForge 高级时间生成器示例
演示各种时间戳、日期格式等生成器的使用方法
"""

import json
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dataforge import GeneratorConfig, default_factory


def basic_usage():
    """基础用法示例"""
    print("1. 基础用法示例")
    print("=" * 60)

    # 高级时间戳生成器
    print("\n高级时间戳生成器 (advanced_timestamp):")
    config = GeneratorConfig("advanced_timestamp", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        timestamp = generator.generate()
        print(f"  示例 {i+1}: {timestamp}")

    # 日期时间范围生成器
    print("\n日期时间范围生成器 (datetime_range):")
    config = GeneratorConfig("datetime_range", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        date_range = generator.generate()
        print(f"  示例 {i+1}: {date_range}")


def parameter_configuration():
    """参数配置示例"""
    print("\n\n2. 参数配置示例")
    print("=" * 60)

    # 高级时间戳 - 不同格式
    print("\n高级时间戳生成器 - 格式配置:")
    timestamp_formats = [
        {"format": "unix"},
        {"format": "iso8601"},
        {"format": "rfc3339"},
        {"format": "human_readable"},
        {"format": "database"},
        {"timezone": "UTC"},
        {"timezone": "Asia/Shanghai"},
        {"timezone": "America/New_York"},
    ]
    for i, params in enumerate(timestamp_formats, 1):
        config = GeneratorConfig("advanced_timestamp", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # 日期时间范围 - 不同范围
    print("\n日期时间范围生成器 - 范围配置:")
    range_configs = [
        {"start": "2020-01-01", "end": "2020-12-31"},
        {"start": "2023-01-01", "days": 365},
        {"start": "2024-01-01", "years": 1},
        {"format": "daily", "count": 7},
        {"format": "hourly", "count": 24},
        {"format": "monthly", "count": 12},
        {"format": "yearly", "count": 5},
    ]
    for i, params in enumerate(range_configs, 1):
        config = GeneratorConfig("datetime_range", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")


def batch_generation():
    """批量生成示例"""
    print("\n\n3. 批量生成示例")
    print("=" * 60)

    print("\n批量生成时间序列数据:")

    # 生成时间戳序列
    timestamp_config = GeneratorConfig(
        "advanced_timestamp", parameters={"format": "iso8601", "timezone": "UTC"}
    )
    timestamp_gen = default_factory.create_generator(timestamp_config)

    # 生成日期范围
    range_config = GeneratorConfig(
        "datetime_range",
        parameters={"start": "2024-01-01", "days": 30, "format": "daily"},
    )
    range_gen = default_factory.create_generator(range_config)

    # 生成5个时间序列
    time_series = []
    for i in range(5):
        series = {
            "timestamp": timestamp_gen.generate(),
            "date_range": range_gen.generate(),
            "created_at": datetime.now().isoformat(),
            "series_id": f"TS_{i+1:03d}",
        }
        time_series.append(series)

    # 打印时间序列
    print("-" * 100)
    print(f"{'序列ID':<8} | {'时间戳':<25} | {'日期范围':<40} | {'创建时间'}")
    print("-" * 100)
    for series in time_series:
        series_id = series["series_id"]
        timestamp = series["timestamp"]
        # 处理整数时间戳
        if isinstance(timestamp, int):
            timestamp_str = str(timestamp)
            timestamp = (
                timestamp_str[:23] + "..." if len(timestamp_str) > 25 else timestamp_str
            )
        else:
            timestamp = timestamp[:23] + "..." if len(timestamp) > 25 else timestamp

        date_range = series["date_range"]
        date_range = date_range[:37] + "..." if len(date_range) > 40 else date_range
        created = series["created_at"][:19]
        print(f"{series_id:<8} | {timestamp:<25} | {date_range:<40} | {created}")
    print("-" * 100)


def validation_examples():
    """数据验证示例"""
    print("\n\n4. 数据验证示例")
    print("=" * 60)

    # 时间戳验证
    print("\n时间戳格式验证:")
    config = GeneratorConfig("advanced_timestamp", parameters={"format": "unix"})
    generator = default_factory.create_generator(config)

    for i in range(3):
        timestamp = generator.generate()
        is_valid = generator.validate(timestamp)
        print(f"  {i+1}. {timestamp}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        try:
            ts_int = int(timestamp)
            dt = datetime.fromtimestamp(ts_int)
            print(f"     转换日期: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        except:
            print("     转换日期: 无法转换")

    # 日期范围验证
    print("\n日期范围格式验证:")
    config = GeneratorConfig(
        "datetime_range", parameters={"start": "2024-01-01", "end": "2024-12-31"}
    )
    generator = default_factory.create_generator(config)

    for i in range(3):
        date_range = generator.generate()
        is_valid = generator.validate(date_range)
        print(f"  {i+1}. {date_range}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        # 检查是否包含时间范围分隔符
        has_separator = " - " in date_range or " to " in date_range
        print(f"     包含分隔符: {'✅ 是' if has_separator else '❌ 否'}")


def error_handling():
    """错误处理示例"""
    print("\n\n5. 错误处理示例")
    print("=" * 60)

    # 处理无效的时间格式
    print("\n处理无效的时间格式:")
    try:
        config = GeneratorConfig("advanced_timestamp", parameters={"format": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的时间戳: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效时间格式错误: {type(e).__name__}")

    # 处理无效的日期范围
    print("\n处理无效的日期范围:")
    try:
        config = GeneratorConfig(
            "datetime_range", parameters={"start": "invalid-date", "end": "2024-12-31"}
        )
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的日期范围: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效日期范围错误: {type(e).__name__}")

    # 处理无效的时区
    print("\n处理无效的时区:")
    try:
        config = GeneratorConfig(
            "advanced_timestamp", parameters={"timezone": "Invalid/Timezone"}
        )
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的时间戳: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效时区错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print("\n\n6. 最佳实践示例")
    print("=" * 60)

    # 实践1: 生成完整的时间序列配置
    print("\n实践1: 生成完整的时间序列配置")
    time_config = {
        "timestamp_settings": {
            "default_format": "iso8601",
            "default_timezone": "UTC",
            "supported_formats": [
                "unix",
                "iso8601",
                "rfc3339",
                "human_readable",
                "database",
            ],
            "supported_timezones": [
                "UTC",
                "Asia/Shanghai",
                "America/New_York",
                "Europe/London",
            ],
        },
        "range_settings": {
            "default_format": "daily",
            "max_range_days": 3650,
            "min_interval_hours": 1,
            "supported_formats": ["daily", "hourly", "monthly", "yearly"],
        },
        "validation_rules": {
            "min_timestamp": 0,
            "max_timestamp": 253402300799,  # 2050-01-01 00:00:00 UTC
            "allow_future": False,
            "allow_past": True,
        },
    }

    print("  时间序列配置:")
    for key, value in time_config.items():
        print(f"    {key}:")
        for sub_key, sub_value in value.items():
            print(f"      {sub_key}: {sub_value}")

    # 实践2: 批量导出时间数据
    print("\n实践2: 批量导出时间数据 (JSON格式)")
    time_data = []

    for i in range(3):
        time_record = {
            "record_id": f"record_{i+1:03d}",
            "timestamps": {
                "creation": default_factory.create_generator(
                    GeneratorConfig(
                        "advanced_timestamp",
                        parameters={"format": "iso8601", "timezone": "UTC"},
                    )
                ).generate(),
                "last_modified": default_factory.create_generator(
                    GeneratorConfig(
                        "advanced_timestamp",
                        parameters={"format": "unix", "timezone": "UTC"},
                    )
                ).generate(),
                "expiry": default_factory.create_generator(
                    GeneratorConfig(
                        "advanced_timestamp",
                        parameters={"format": "rfc3339", "timezone": "Asia/Shanghai"},
                    )
                ).generate(),
            },
            "date_ranges": {
                "active_period": default_factory.create_generator(
                    GeneratorConfig(
                        "datetime_range",
                        parameters={
                            "start": "2024-01-01",
                            "days": 30,
                            "format": "daily",
                        },
                    )
                ).generate(),
                "project_lifecycle": default_factory.create_generator(
                    GeneratorConfig(
                        "datetime_range",
                        parameters={
                            "start": "2020-01-01",
                            "end": "2024-12-31",
                            "format": "monthly",
                        },
                    )
                ).generate(),
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator_version": "1.0.0",
                "data_quality": "high",
            },
        }
        time_data.append(time_record)

    print("  JSON格式输出:")
    print(json.dumps(time_data, ensure_ascii=False, indent=2))


def time_series_demo():
    """时间序列演示"""
    print("\n\n7. 时间序列演示")
    print("=" * 60)

    print("\n生成时间序列数据:")

    # 生成过去一年的每日数据
    daily_config = GeneratorConfig(
        "datetime_range",
        parameters={"start": "2023-01-01", "days": 365, "format": "daily"},
    )
    daily_gen = default_factory.create_generator(daily_config)
    daily_data = daily_gen.generate()

    print("  每日数据 (2023年):")
    print(f"    范围: {daily_data}")

    # 生成过去一个月的小时数据
    hourly_config = GeneratorConfig(
        "datetime_range",
        parameters={"start": "2024-01-01", "days": 30, "format": "hourly"},
    )
    hourly_gen = default_factory.create_generator(hourly_config)
    hourly_data = hourly_gen.generate()

    print("\n  小时数据 (2024年1月):")
    print(f"    范围: {hourly_data}")

    # 生成时间戳序列
    timestamp_config = GeneratorConfig(
        "advanced_timestamp", parameters={"format": "unix", "timezone": "UTC"}
    )
    timestamp_gen = default_factory.create_generator(timestamp_config)

    print("\n  生成时间戳序列:")
    for i in range(5):
        timestamp = timestamp_gen.generate()
        dt = datetime.fromtimestamp(int(timestamp))
        print(f"    {timestamp} -> {dt.strftime('%Y-%m-%d %H:%M:%S')}")

    # 生成不同时区的时间
    print("\n  不同时区的时间对比:")
    timezones = ["UTC", "Asia/Shanghai", "America/New_York", "Europe/London"]

    base_timestamp = "1704067200"  # 2024-01-01 00:00:00 UTC

    for tz in timezones:
        config = GeneratorConfig(
            "advanced_timestamp",
            parameters={
                "format": "iso8601",
                "timezone": tz,
                "timestamp": base_timestamp,
            },
        )
        gen = default_factory.create_generator(config)
        result = gen.generate()
        print(f"    {tz}: {result}")

    # 生成业务相关的时间范围
    print("\n  业务时间范围:")
    business_ranges = [
        {
            "name": "Q1 2024",
            "start": "2024-01-01",
            "end": "2024-03-31",
            "format": "monthly",
        },
        {
            "name": "H1 2024",
            "start": "2024-01-01",
            "end": "2024-06-30",
            "format": "monthly",
        },
        {
            "name": "项目周期",
            "start": "2023-01-01",
            "end": "2024-12-31",
            "format": "quarterly",
        },
        {"name": "冲刺阶段", "start": "2024-11-01", "days": 30, "format": "daily"},
    ]

    for range_def in business_ranges:
        config = GeneratorConfig("datetime_range", parameters=range_def)
        gen = default_factory.create_generator(config)
        result = gen.generate()
        print(f"    {range_def['name']}: {result}")


def main():
    """主函数"""
    print("🎯 DataForge 高级时间生成器示例")
    print("本示例展示了时间相关生成器的各种使用方法\n")

    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        time_series_demo()

        print("\n" + "=" * 60)
        print("✅ 示例演示完成")
        print("=" * 60)
        print("🎉 所有高级时间生成器示例已成功运行！")

        print("\n📚 相关文档:")
        print("  • 查看 examples/advanced/format_demo.py 了解格式化相关生成器")
        print("  • 查看 examples/advanced/security_demo.py 了解安全相关生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")

    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
