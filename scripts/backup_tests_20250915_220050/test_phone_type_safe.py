#!/usr/bin/env python3
"""
测试电话号码生成器（类型安全版本）
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataforge.core.generator import GeneratorConfig
from dataforge.generators.contact.phone import (
    GenericPhoneNumberGenerator,
    PhoneNumberGenerator,
)


def test_phone_number_generation():
    """测试电话号码生成"""
    print("=== 测试电话号码生成 ===")

    # 测试不同号码类型
    for number_type in ["MOBILE", "LANDLINE", "TOLL_FREE", "MIXED"]:
        config = GeneratorConfig(
            generator_type="phone",
            parameters={
                "type": number_type,
                "format": "STANDARD",
                "region": "北京" if number_type == "LANDLINE" else None,
            },
        )
        # 直接创建具体的生成器实例以避免类型检查问题
        generator: PhoneNumberGenerator = GenericPhoneNumberGenerator(config)
        phone = generator.generate()
        print(f"生成的{number_type}号码: {phone}")
        print(f"校验结果: {generator.validate(phone)}")
        print(f"号码类型: {generator.get_number_type(phone)}")
        print()


def test_phone_number_formats():
    """测试电话号码格式"""
    print("=== 测试电话号码格式 ===")

    # 测试不同格式
    for format_type in ["STANDARD", "COMPACT", "INTERNATIONAL"]:
        config = GeneratorConfig(
            generator_type="phone", parameters={"type": "MOBILE", "format": format_type}
        )
        # 直接创建具体的生成器实例
        generator: PhoneNumberGenerator = GenericPhoneNumberGenerator(config)
        phone = generator.generate()
        print(f"配置: {{'format': '{format_type}'}}")
        print(f"生成的号码: {phone}")
        print(f"校验结果: {generator.validate(phone)}")
        print(f"号码类型: {generator.get_number_type(phone)}")
        print()


def test_phone_number_validation():
    """测试电话号码校验"""
    print("=== 测试电话号码校验 ===")

    # 测试有效号码
    valid_numbers = [
        "15 2099 3721",  # 有效手机号（标准格式）
        "010-65518443",  # 有效固定电话（标准格式）
        "4007 6279 4121",  # 有效400号码（标准格式）
        "1306930916",  # 有效手机号（紧凑格式）
        "0891748055",  # 有效固定电话（紧凑格式）
        "400679972722",  # 有效400号码（紧凑格式）
        "+86 18 6624 1822",  # 有效手机号（国际格式）
        "+86 028 85518443",  # 有效固定电话（国际格式）
        "+86 4007 6279 4121",  # 有效400号码（国际格式）
    ]

    print("测试有效号码:")
    for number in valid_numbers:
        print(f"号码: {number}")
        # 创建生成器实例
        config = GeneratorConfig(generator_type="phone", parameters={})
        generator: PhoneNumberGenerator = GenericPhoneNumberGenerator(config)
        print(f"校验结果: {generator.validate(number)}")
        print(f"号码类型: {generator.get_number_type(number)}")
        print()

    # 测试无效号码
    invalid_numbers = [
        "12 2099 3721",  # 无效手机号（前缀不正确）
        "010-6551844312",  # 无效固定电话（号码过长）
        "4007 6279 412",  # 无效400号码（号码过短）
        "+86 12 6624 1822",  # 无效手机号（国际格式）
        "+86 4007 6279 412",  # 无效400号码（国际格式）
    ]

    print("测试无效号码:")
    for number in invalid_numbers:
        print(f"号码: {number}")
        config = GeneratorConfig(generator_type="phone", parameters={})
        generator: PhoneNumberGenerator = GenericPhoneNumberGenerator(config)
        print(f"校验结果: {generator.validate(number)}")
        print(f"号码类型: {generator.get_number_type(number)}")
        print()


def main():
    """主测试函数"""
    print("DataForge 电话号码生成器测试（类型安全版本）")
    print("=" * 60)
    print()

    test_phone_number_generation()
    test_phone_number_formats()
    test_phone_number_validation()

    print("所有测试完成！")
    return 0


if __name__ == "__main__":
    sys.exit(main())
