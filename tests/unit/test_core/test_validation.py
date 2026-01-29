#!/usr/bin/env python3
"""
DataForge 校验功能测试 (pytest风格)
"""

import pytest

from dataforge.core.factory import GeneratorFactory
from dataforge.core.generator import GeneratorConfig

# --- 身份证校验测试 ---


@pytest.mark.parametrize(
    "id_card_number, expected_validity",
    [
        ("110101199003071356", True),  # 有效（修正校验码）
        ("110000199001010005", True),  # 有效（修正校验码）
        ("110101199003071355", False),  # 校验位错误
        ("11010119900307135X", False),  # X大写, 但校验位错误
        ("440582199901010017", True),  # 有效（修正校验码）
        ("123456789012345678", False),  # 无效格式
    ],
)
def test_idcard_static_validation(
    generator_factory: GeneratorFactory, id_card_number: str, expected_validity: bool
):
    """测试固定的身份证号校验"""
    config = GeneratorConfig(generator_type="idcard", parameters={})
    generator = generator_factory.create_generator(config)
    assert generator.validate(id_card_number) == expected_validity


def test_idcard_generated_validation(generator_factory: GeneratorFactory):
    """测试生成的身份证号的有效性"""
    config = GeneratorConfig(generator_type="idcard", parameters={"valid": True})
    generator = generator_factory.create_generator(config)

    for _ in range(10):
        id_card = generator.generate()
        assert generator.validate(id_card), f"生成的身份证 {id_card} 未通过校验"


def test_idcard_invalid_generation(generator_factory: GeneratorFactory):
    """测试生成的无效身份证号"""
    config = GeneratorConfig(generator_type="idcard", parameters={"valid": False})
    generator = generator_factory.create_generator(config)

    # It's hard to guarantee 100% invalid generation, but a high probability should fail
    invalid_cards = [generator.generate() for _ in range(10)]
    assert any(
        not generator.validate(card) for card in invalid_cards
    ), "生成的无效身份证中应至少有一个是无效的"


# --- 银行卡校验测试 ---


@pytest.mark.parametrize(
    "card_number, expected_validity",
    [
        ("4111111111111111", True),  # Visa测试卡
        ("5555555555554444", True),  # MasterCard测试卡
        ("6222021001234567896", True),  # ICBC（修正校验码）
        ("4111111111111112", False),  # 校验位错误
        ("1234567890123456", False),  # 无效卡号
    ],
)
def test_bankcard_static_validation(
    generator_factory: GeneratorFactory, card_number: str, expected_validity: bool
):
    """测试固定的银行卡号Luhn校验"""
    config = GeneratorConfig(generator_type="bankcard", parameters={})
    generator = generator_factory.create_generator(config)
    # The _luhn_validate method is protected, so we test through the public validate method
    assert generator.validate(card_number) == expected_validity


def test_bankcard_generated_validation(generator_factory: GeneratorFactory):
    """测试生成的银行卡号的有效性"""
    config = GeneratorConfig(generator_type="bankcard", parameters={"valid": True})
    generator = generator_factory.create_generator(config)

    for _ in range(10):
        bank_card = generator.generate()
        assert generator.validate(bank_card), f"生成的银行卡 {bank_card} 未通过校验"
