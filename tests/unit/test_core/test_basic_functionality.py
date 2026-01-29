"""
DataForge核心功能测试 (pytest风格)
"""

import json

import pytest

from dataforge.core.exceptions import GeneratorNotFoundError
from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig
from dataforge.generators.basic.idcard import IDCardGenerator
from dataforge.output.formatter import OutputFormatter

# --- Test IDCardGenerator ---


def test_idcard_generate_single(generator_factory: GeneratorFactory):
    """测试生成单个身份证号"""
    config = GeneratorConfig(generator_type="idcard", parameters={})
    generator = generator_factory.create_generator(config)
    id_card = generator.generate_single()

    assert isinstance(id_card, str)
    assert len(id_card) == 18
    assert generator.validate(id_card)


def test_idcard_generate_batch(generator_factory: GeneratorFactory):
    """测试批量生成身份证号"""
    config = GeneratorConfig(generator_type="idcard", parameters={})
    generator = generator_factory.create_generator(config)
    id_cards = generator.generate_batch(10)

    assert len(id_cards) == 10
    for id_card in id_cards:
        assert generator.validate(id_card)


def test_idcard_gender_constraint(generator_factory: GeneratorFactory):
    """测试身份证性别约束"""
    male_config = GeneratorConfig(
        generator_type="idcard", parameters={"gender": "MALE"}
    )
    male_generator = generator_factory.create_generator(male_config)

    for _ in range(10):
        id_card = male_generator.generate_single()
        gender_digit = int(id_card[16])
        assert gender_digit % 2 == 1  # 奇数表示男性


# --- Test BankCardGenerator ---


def test_bankcard_generate_single(generator_factory: GeneratorFactory):
    """测试生成单个银行卡号"""
    config = GeneratorConfig(generator_type="bankcard", parameters={"valid": True})
    generator = generator_factory.create_generator(config)
    card = generator.generate_single()

    assert isinstance(card, str)
    assert 13 <= len(card) <= 19
    assert card.isdigit()
    assert generator.validate(card)


def test_bankcard_luhn_algorithm(generator_factory: GeneratorFactory):
    """测试Luhn算法校验"""
    # We need an instance to call the method, even if it doesn't use self
    config = GeneratorConfig(generator_type="bankcard", parameters={})
    generator = generator_factory.create_generator(config)

    valid_cards = ["4111111111111111", "5555555555554444"]
    for card in valid_cards:
        assert generator._luhn_validate(card)

    invalid_cards = ["4111111111111112", "1234567890123456"]
    for card in invalid_cards:
        assert not generator._luhn_validate(card)


# --- Test PhoneGenerator ---


def test_phone_generate_single(generator_factory: GeneratorFactory):
    """测试生成单个手机号"""
    config = GeneratorConfig(generator_type="phone", parameters={"valid": True})
    generator = generator_factory.create_generator(config)
    phone = generator.generate_single()

    assert isinstance(phone, str)
    assert len(phone) == 11
    assert phone.isdigit()
    assert generator.validate(phone)


# --- TestGeneratorFactory ---


def test_create_generator(generator_factory: GeneratorFactory):
    """测试创建生成器"""
    config = GeneratorConfig(generator_type="idcard", parameters={"region": "上海"})
    generator = generator_factory.create_generator(config)
    assert isinstance(generator, IDCardGenerator)


def test_unknown_generator(empty_registry: GeneratorRegistry):
    """测试当生成器未注册时, 工厂应抛出GeneratorNotFoundError."""
    # Use a factory with an empty registry for this test
    factory = GeneratorFactory(empty_registry)
    config = GeneratorConfig(generator_type="unknown_type", parameters={})

    with pytest.raises(GeneratorNotFoundError) as excinfo:
        factory.create_generator(config)

    assert "'unknown_type' not found" in str(excinfo.value)


# --- TestOutputFormatter ---


@pytest.fixture
def output_formatter_data() -> dict:
    return {
        "idcard": ["110101199001011234", "110101199001012345"],
        "phone": ["13800138000", "13800138001"],
    }


def test_json_format(output_formatter_data: dict):
    """测试JSON格式化"""
    formatter = OutputFormatter()
    result = formatter.format(output_formatter_data, "json")
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert parsed == output_formatter_data


def test_csv_format(output_formatter_data: dict):
    """测试CSV格式化"""
    formatter = OutputFormatter()
    result = formatter.format(output_formatter_data, "csv")
    assert isinstance(result, str)
    assert "idcard" in result
    assert "phone" in result


def test_xml_format(output_formatter_data: dict):
    """测试XML格式化"""
    formatter = OutputFormatter()
    result = formatter.format(output_formatter_data, "xml")
    assert isinstance(result, str)
    assert "<dataforge_output>" in result
    assert "</dataforge_output>" in result
