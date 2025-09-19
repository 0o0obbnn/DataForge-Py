#!/usr/bin/env python3
"""
DataForge 扩展功能演示
演示新增的生成器功能
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataforge.core.factory import default_factory
from dataforge.core.generator import GenerationContext, GeneratorConfig
from dataforge.output.formatter import OutputFormatter


def demo_email_generator():
    """演示邮箱生成器"""
    print("=== 邮箱生成器演示 ===")

    # 基础邮箱生成
    print("1. 基础邮箱生成:")
    config = GeneratorConfig(generator_type="email", parameters={})
    generator = default_factory.create_generator(config)
    emails = generator.generate_batch(3)
    for email in emails:
        print(f"   {email} (有效: {generator.validate(email)})")

    # 企业邮箱
    print("\n2. 企业邮箱生成:")
    config = GeneratorConfig(
        generator_type="email",
        parameters={"type": "ENTERPRISE", "domains": ["company.com", "corp.cn"]},
    )
    generator = default_factory.create_generator(config)
    emails = generator.generate_batch(3)
    for email in emails:
        print(f"   {email}")

    print()


def demo_gender_generator():
    """演示性别生成器"""
    print("=== 性别生成器演示 ===")

    # 不同格式的性别
    formats = ["ENGLISH", "CHINESE", "SYMBOL", "NUMERIC"]

    for fmt in formats:
        print(f"{fmt}格式:")
        config = GeneratorConfig(
            generator_type="gender", parameters={"format": fmt, "type": "BINARY"}
        )
        generator = default_factory.create_generator(config)
        genders = generator.generate_batch(5)
        print(f"   {', '.join(map(str, genders))}")

    print()


def demo_numeric_generators():
    """演示数值生成器"""
    print("=== 数值生成器演示 ===")

    # 整数生成器
    print("1. 整数生成器:")
    config = GeneratorConfig(
        generator_type="integer",
        parameters={"min": 1, "max": 100, "distribution": "NORMAL"},
    )
    generator = default_factory.create_generator(config)
    numbers = generator.generate_batch(5)
    print(f"   正态分布整数: {numbers}")

    # 小数生成器
    print("\n2. 小数生成器:")
    config = GeneratorConfig(
        generator_type="decimal", parameters={"min": 0.0, "max": 1.0, "precision": 3}
    )
    generator = default_factory.create_generator(config)
    decimals = generator.generate_batch(5)
    print(f"   三位小数: {decimals}")

    # 随机数字串
    print("\n3. 随机数字串:")
    config = GeneratorConfig(
        generator_type="random_number", parameters={"format": "###-###-###"}
    )
    generator = default_factory.create_generator(config)
    numbers = generator.generate_batch(3)
    print(f"   格式化数字: {numbers}")

    print()


def demo_text_generators():
    """演示文本生成器"""
    print("=== 文本生成器演示 ===")

    # 字符串生成器
    print("1. 字符串生成器:")
    config = GeneratorConfig(
        generator_type="string",
        parameters={
            "length": 8,
            "charset": "ALPHANUMERIC",
            "must_include": ["DIGITS", "UPPERCASE"],
        },
    )
    generator = default_factory.create_generator(config)
    strings = generator.generate_batch(3)
    print(f"   包含数字和大写字母: {strings}")

    # 布尔值生成器
    print("\n2. 布尔值生成器:")
    formats = ["BOOLEAN", "CHINESE", "YN"]
    for fmt in formats:
        config = GeneratorConfig(
            generator_type="boolean", parameters={"format": fmt, "true_ratio": 0.7}
        )
        generator = default_factory.create_generator(config)
        bools = generator.generate_batch(3)
        print(f"   {fmt}格式: {bools}")

    # 枚举生成器
    print("\n3. 枚举生成器:")
    config = GeneratorConfig(
        generator_type="enum",
        parameters={
            "values": ["优秀", "良好", "一般", "较差"],
            "weights": [0.2, 0.4, 0.3, 0.1],
        },
    )
    generator = default_factory.create_generator(config)
    enums = generator.generate_batch(10)
    print(f"   评级分布: {enums}")

    print()


def demo_identifier_generators():
    """演示标识类生成器"""
    print("=== 标识类生成器演示 ===")

    # UUID生成器
    print("1. UUID生成器:")
    versions = [1, 3, 4, 5]
    for version in versions:
        config = GeneratorConfig(generator_type="uuid", parameters={"version": version})
        generator = default_factory.create_generator(config)
        uuid_val = generator.generate()
        print(f"   UUID v{version}: {uuid_val}")

    # ULID生成器
    print("\n2. ULID生成器:")
    config = GeneratorConfig(generator_type="ulid", parameters={})
    generator = default_factory.create_generator(config)
    ulids = generator.generate_batch(3)
    for ulid in ulids:
        print(f"   {ulid}")

    # 业务单据号
    print("\n3. 业务单据号:")
    business_types = ["ORDER", "INVOICE", "PAYMENT"]
    for biz_type in business_types:
        config = GeneratorConfig(
            generator_type="business_number",
            parameters={
                "type": biz_type,
                "date_format": "YYYYMMDD",
                "checksum": True,
                "separator": "-",
            },
        )
        generator = default_factory.create_generator(config)
        number = generator.generate()
        print(f"   {biz_type}: {number}")

    print()


def demo_related_generation():
    """演示复杂关联数据生成"""
    print("=== 复杂关联数据生成演示 ===")

    # 完整用户档案
    configs = [
        GeneratorConfig(generator_type="name", parameters={}),
        GeneratorConfig(generator_type="gender", parameters={"format": "CHINESE"}),
        GeneratorConfig(generator_type="age", parameters={"min": 18, "max": 65}),
        GeneratorConfig(generator_type="email", parameters={}),
        GeneratorConfig(generator_type="phone", parameters={}),
        GeneratorConfig(generator_type="address", parameters={}),
        GeneratorConfig(generator_type="uuid", parameters={"format": "NO_HYPHENS"}),
    ]

    records = []
    for _ in range(3):
        context = GenerationContext()
        result = default_factory.generate_batch_with_relations(configs, context)
        records.append(result)

    formatter = OutputFormatter()
    output = formatter.format(records, "json", pretty=True)
    print(output)

    print()


def demo_performance_test():
    """演示性能测试"""
    print("=== 性能测试演示 ===")

    import time

    # 测试各类生成器的性能
    generators_config = [
        ("UUID", GeneratorConfig(generator_type="uuid", parameters={})),
        ("Email", GeneratorConfig(generator_type="email", parameters={})),
        ("String", GeneratorConfig(generator_type="string", parameters={"length": 10})),
        (
            "Integer",
            GeneratorConfig(
                generator_type="integer", parameters={"min": 1, "max": 1000}
            ),
        ),
        ("Boolean", GeneratorConfig(generator_type="boolean", parameters={})),
    ]

    test_count = 10000

    for name, config in generators_config:
        generator = default_factory.create_generator(config)

        start_time = time.time()
        generator.generate_batch(test_count)
        end_time = time.time()

        elapsed = end_time - start_time
        speed = test_count / elapsed

        print(f"{name:>10}: {elapsed:.4f}秒, {speed:.0f}条/秒")

    print()


def main():
    """主演示函数"""
    print("DataForge - 扩展功能演示")
    print("=" * 60)

    try:
        demo_email_generator()
        demo_gender_generator()
        demo_numeric_generators()
        demo_text_generators()
        demo_identifier_generators()
        demo_related_generation()
        demo_performance_test()

        print("🎉 扩展功能演示完成！")
        print("\n新增功能:")
        print("✓ Email邮箱生成器")
        print("✓ Gender性别生成器")
        print("✓ 数值生成器(Integer, Decimal, RandomNumber)")
        print("✓ 文本生成器(String, Boolean, Enum)")
        print("✓ 标识类生成器(UUID, ULID, BusinessNumber)")
        print("✓ 更多输出格式和关联选项")

    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
