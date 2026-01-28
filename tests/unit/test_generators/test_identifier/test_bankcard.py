"""
银行卡号生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestBankCardGenerator:
    """银行卡号生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个银行卡号"""
        config = GeneratorConfig(generator_type="bankcard", parameters={})
        generator = generator_factory.create_generator(config)
        card_number = generator.generate_single()

        assert isinstance(card_number, str)
        assert 16 <= len(card_number) <= 19
        assert card_number.isdigit()
        assert generator.validate(card_number)

    def test_generate_batch(self, generator_factory):
        """测试批量生成银行卡号"""
        config = GeneratorConfig(generator_type="bankcard", parameters={})
        generator = generator_factory.create_generator(config)
        card_numbers = generator.generate_batch(10)

        assert len(card_numbers) == 10
        for card in card_numbers:
            assert isinstance(card, str)
            assert card.isdigit()
            assert generator.validate(card)

    def test_luhn_algorithm(self, generator_factory):
        """测试Luhn算法校验"""
        config = GeneratorConfig(generator_type="bankcard", parameters={})
        generator = generator_factory.create_generator(config)
        card_number = generator.generate_single()

        # Verify Luhn checksum
        def luhn_check(card_num):
            digits = [int(d) for d in card_num]
            checksum = 0
            for i, digit in enumerate(reversed(digits)):
                if i % 2 == 1:
                    digit *= 2
                    if digit > 9:
                        digit -= 9
                checksum += digit
            return checksum % 10 == 0

        assert luhn_check(card_number)

    def test_specific_bank(self, generator_factory):
        """测试指定银行卡号"""
        config = GeneratorConfig(generator_type="bankcard", parameters={"bank": "ICBC"})
        generator = generator_factory.create_generator(config)
        card_number = generator.generate_single()

        assert isinstance(card_number, str)
        assert card_number.isdigit()

    def test_card_type(self, generator_factory):
        """测试卡类型"""
        config = GeneratorConfig(
            generator_type="bankcard", parameters={"card_type": "debit"}
        )
        generator = generator_factory.create_generator(config)
        card_number = generator.generate_single()

        assert isinstance(card_number, str)
        assert generator.validate(card_number)

    def test_validation(self, generator_factory):
        """测试银行卡号验证"""
        config = GeneratorConfig(generator_type="bankcard", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid card numbers (with valid Luhn checksum)
        assert generator.validate(
            "6222021234567894"
        )  # Valid ICBC card with Luhn checksum

        # Invalid card numbers
        assert not generator.validate("123")  # Too short
        assert not generator.validate("ABCD1234567890")  # Not numeric
        assert not generator.validate("")

    def test_uniqueness(self, generator_factory):
        """测试银行卡号唯一性"""
        config = GeneratorConfig(generator_type="bankcard", parameters={})
        generator = generator_factory.create_generator(config)
        cards = generator.generate_batch(50)

        # All cards should be unique
        unique_cards = set(cards)
        assert len(unique_cards) == 50

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        config = GeneratorConfig(generator_type="bankcard", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            card = generator.generate_single()
            assert card is not None
            assert 16 <= len(card) <= 19
            assert card.isdigit()
