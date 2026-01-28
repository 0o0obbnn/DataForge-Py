"""
银行卡号生成器测试
"""

import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from dataforge.core.factory import default_factory
from dataforge.core.generator import GeneratorConfig
from dataforge.generators.identifier import GenericBankCardGenerator


def test_basic_bankcard_generation():
    """测试基本银行卡号生成"""
    config = GeneratorConfig(generator_type="bankcard", parameters={}, count=5)

    generator = default_factory.create_generator(config)
    results = generator.generate_batch(5)

    print("=== 基本银行卡号生成测试 ===")
    for i, card_number in enumerate(results, 1):
        print(f"{i}. {card_number}")
        # 调试信息
        clean_number = card_number.replace(" ", "").replace("-", "")
        print(f"  清理后: {clean_number}")
        print(f"  长度: {len(clean_number)}")
        print(f"  是否为数字: {clean_number.isdigit()}")

        assert len(clean_number) in [
            15,
            16,
            19,
        ], f"卡号长度应为15, 16或19位，实际为{len(clean_number)}"
        assert clean_number.isdigit(), "卡号应只包含数字"
        assert generator.validate(card_number), f"生成的卡号应通过验证: {card_number}"
    print()


def test_specific_bank_generation():
    """测试特定银行银行卡号生成"""
    config = GeneratorConfig(
        generator_type="bankcard", parameters={"bank_code": "ICBC"}, count=3
    )

    generator = default_factory.create_generator(config)
    results = generator.generate_batch(3)

    print("=== 工商银行银行卡号生成测试 ===")
    for i, card_number in enumerate(results, 1):
        info = generator.get_bank_info(card_number)
        print(
            f"{i}. {card_number} - 银行: {info['bank_name']}, 类型: {info['card_type']}"
        )
    print()


def test_card_type_generation():
    """测试卡类型银行卡号生成"""
    config = GeneratorConfig(
        generator_type="bankcard", parameters={"card_type": "UNIONPAY"}, count=3
    )

    generator = default_factory.create_generator(config)
    results = generator.generate_batch(3)

    print("=== 银联卡银行卡号生成测试 ===")
    for i, card_number in enumerate(results, 1):
        info = generator.get_bank_info(card_number)
        print(
            f"{i}. {card_number} - 银行: {info['bank_name']}, 类型: {info['card_type']}"
        )
    print()


def test_formatted_generation():
    """测试格式化银行卡号生成"""
    config = GeneratorConfig(
        generator_type="bankcard", parameters={"format_with_spaces": True}, count=3
    )

    generator = default_factory.create_generator(config)
    results = generator.generate_batch(3)

    print("=== 格式化银行卡号生成测试（带空格）===")
    for i, card_number in enumerate(results, 1):
        print(f"{i}. {card_number}")
    print()


def test_validation():
    """测试银行卡号验证"""
    config = GeneratorConfig(generator_type="bankcard", parameters={})
    generator = GenericBankCardGenerator(config)

    # 测试有效卡号
    valid_cards = [
        "6222021234567890",  # 工行格式
        "6227001234567890",  # 建行格式
        "6216611234567890",  # 中行格式
    ]

    # 测试无效卡号
    invalid_cards = [
        "1234567890123456",  # 无效BIN
        "622202123456789012",  # 无效校验位
        "abc1234567890123",  # 非数字
        "622202123456789012345",  # 长度过长
    ]

    print("=== 银行卡号验证测试 ===")

    print("有效卡号验证:")
    for card in valid_cards:
        # 检查卡号是否符合Luhn算法
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))

        is_luhn_valid = checksum % 10 == 0
        is_valid = generator.validate(card)
        print(
            f"{card}: {'✅ 有效' if is_valid else '❌ 无效'} (Luhn校验: {'✅' if is_luhn_valid else '❌'})"
        )

    print("\n无效卡号验证:")
    for card in invalid_cards:
        is_valid = generator.validate(card)
        print(f"{card}: {'✅ 有效' if is_valid else '❌ 无效'}")
    print()


def test_bank_info():
    """测试银行卡信息获取"""
    config = GeneratorConfig(generator_type="bankcard", parameters={})
    generator = GenericBankCardGenerator(config)

    # 生成一些卡号并获取信息
    config = GeneratorConfig(
        generator_type="bankcard",
        parameters={"bank_code": "CMB", "format_with_spaces": True},
        count=2,
    )

    generator_instance = default_factory.create_generator(config)
    results = generator_instance.generate_batch(2)

    print("=== 银行卡信息获取测试 ===")
    for card_number in results:
        info = generator.get_bank_info(card_number)
        print(f"卡号: {card_number}")
        print(f"  银行: {info['bank_name']}")
        print(f"  类型: {info['card_type']}")
        print(f"  有效: {'是' if info['is_valid'] else '否'}")
        print()


if __name__ == "__main__":
    try:
        test_basic_bankcard_generation()
        test_specific_bank_generation()
        test_card_type_generation()
        test_formatted_generation()
        test_validation()
        test_bank_info()

        print("🎉 所有银行卡号生成器测试通过！")

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()
