#!/usr/bin/env python3
"""
DataForge 完整功能演示
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataforge.core.factory import default_factory
from dataforge.core.generator import GenerationContext, GeneratorConfig
from dataforge.output.formatter import OutputFormatter


def demo_single_generators():
    """演示单个生成器功能"""
    print("=== 单个生成器演示 ===")

    # 身份证生成器
    print("1. 身份证生成器:")
    idcard_config = GeneratorConfig(
        generator_type="idcard", parameters={"region": "110000", "gender": "MALE"}
    )
    idcard_gen = default_factory.create_generator(idcard_config)
    idcards = idcard_gen.generate_batch(3)
    for i, idcard in enumerate(idcards, 1):
        print(f"   {i}. {idcard} (有效: {idcard_gen.validate(idcard)})")

    # 姓名生成器
    print("\n2. 姓名生成器:")
    name_config = GeneratorConfig(
        generator_type="name", parameters={"gender": "FEMALE", "include_pinyin": True}
    )
    name_gen = default_factory.create_generator(name_config)
    names = name_gen.generate_batch(3)
    for i, name in enumerate(names, 1):
        print(f"   {i}. {name}")

    # 银行卡生成器
    print("\n3. 银行卡生成器:")
    bankcard_config = GeneratorConfig(
        generator_type="bankcard", parameters={"type": "DEBIT", "bank": "ICBC"}
    )
    bankcard_gen = default_factory.create_generator(bankcard_config)
    bankcards = bankcard_gen.generate_batch(3)
    for i, card in enumerate(bankcards, 1):
        print(f"   {i}. {card} (Luhn校验: {bankcard_gen.validate(card)})")

    print()


def demo_related_generation():
    """演示关联数据生成"""
    print("=== 关联数据生成演示 ===")

    # 个人信息完整档案
    print("1. 个人信息完整档案:")
    configs = [
        GeneratorConfig(generator_type="age", parameters={"min": 18, "max": 65}),
        GeneratorConfig(generator_type="idcard", parameters={"region": "440000"}),
        GeneratorConfig(generator_type="name", parameters={}),
        GeneratorConfig(generator_type="address", parameters={"province": "广东省"}),
    ]

    # 生成5个完整的个人档案
    records = []
    for _ in range(5):
        context = GenerationContext()
        result = default_factory.generate_batch_with_relations(configs, context)
        records.append(result)

    # 格式化输出
    formatter = OutputFormatter()
    formatted_output = formatter.format(records, "json", pretty=True)
    print(formatted_output)

    print("\n2. 验证数据关联性:")
    for i, record in enumerate(records, 1):
        idcard = record.get("idcard", "")
        age = record.get("age", 0)

        if len(idcard) == 18 and idcard[:17].isdigit():
            birth_year = int(idcard[6:10])
            from datetime import datetime

            expected_age = datetime.now().year - birth_year
            match_status = "✓" if age == expected_age else "✗"
            print(
                f"   记录{i}: 年龄匹配 {match_status} (身份证:{birth_year}年, 年龄:{age}岁)"
            )

    print()


def demo_output_formats():
    """演示多种输出格式"""
    print("=== 输出格式演示 ===")

    # 生成测试数据
    configs = [
        GeneratorConfig(generator_type="name", parameters={}),
        GeneratorConfig(generator_type="phone", parameters={"operator": "MOBILE"}),
    ]

    records = []
    for _ in range(3):
        context = GenerationContext()
        result = default_factory.generate_batch_with_relations(configs, context)
        records.append(result)

    formatter = OutputFormatter()

    # JSON格式
    print("1. JSON格式:")
    json_output = formatter.format(records, "json", pretty=True)
    print(json_output)

    # CSV格式
    print("\n2. CSV格式:")
    csv_output = formatter.format(records, "csv")
    print(csv_output)

    # SQL格式
    print("3. SQL格式:")
    sql_output = formatter.format(records, "sql", table_name="user_contacts")
    print(sql_output)

    print()


def demo_validation_features():
    """演示数据校验功能"""
    print("=== 数据校验功能演示 ===")

    # 测试身份证校验
    print("1. 身份证校验:")
    idcard_gen = default_factory.create_generator(
        GeneratorConfig(generator_type="idcard", parameters={})
    )

    test_idcards = [
        "110000199001010008",  # 有效身份证
        "110000199001010009",  # 校验位错误
        "11000019900101000",  # 长度错误
        "ABC000199001010008",  # 包含字母
    ]

    for idcard in test_idcards:
        is_valid = idcard_gen.validate(idcard)
        status = "有效" if is_valid else "无效"
        print(f"   {idcard}: {status}")

    # 测试银行卡校验
    print("\n2. 银行卡Luhn算法校验:")
    bankcard_gen = default_factory.create_generator(
        GeneratorConfig(generator_type="bankcard", parameters={})
    )

    test_cards = [
        "6222000000000000",  # 有效卡号
        "6222000000000001",  # Luhn校验失败
        "622200000000000",  # 长度错误
    ]

    for card in test_cards:
        is_valid = bankcard_gen.validate(card)
        status = "有效" if is_valid else "无效"
        print(f"   {card}: {status}")

    print()


def demo_performance():
    """演示性能测试"""
    print("=== 性能测试演示 ===")

    import time

    # 大批量单个数据生成
    print("1. 大批量单个数据生成 (10000条身份证):")
    start_time = time.time()

    idcard_gen = default_factory.create_generator(
        GeneratorConfig(generator_type="idcard", parameters={})
    )
    large_batch = idcard_gen.generate_batch(10000)

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"   生成时间: {elapsed:.3f}秒")
    print(f"   生成速度: {len(large_batch) / elapsed:.0f}条/秒")

    # 关联数据批量生成
    print("\n2. 关联数据批量生成 (1000条个人档案):")
    start_time = time.time()

    configs = [
        GeneratorConfig(generator_type="idcard", parameters={}),
        GeneratorConfig(generator_type="name", parameters={}),
        GeneratorConfig(generator_type="age", parameters={}),
    ]

    related_records = []
    for _ in range(1000):
        context = GenerationContext()
        result = default_factory.generate_batch_with_relations(configs, context)
        related_records.append(result)

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"   生成时间: {elapsed:.3f}秒")
    print(f"   生成速度: {len(related_records) / elapsed:.0f}条/秒")

    print()


def main():
    """主演示函数"""
    print("DataForge - 高效、灵活的测试数据生成工具")
    print("=" * 60)
    print("完整功能演示")
    print("=" * 60)

    try:
        demo_single_generators()
        demo_related_generation()
        demo_output_formats()
        demo_validation_features()
        demo_performance()

        print("🎉 DataForge 演示完成！")
        print("\n主要特性:")
        print("✓ 中文本地化数据生成")
        print("✓ 智能数据关联和依赖管理")
        print("✓ 多种输出格式支持")
        print("✓ 完整的数据校验机制")
        print("✓ 高性能批量生成")
        print("✓ 插件化架构设计")
        print("✓ 命令行界面支持")

    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
