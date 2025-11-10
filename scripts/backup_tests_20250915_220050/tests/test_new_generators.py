"""
测试新开发的数据生成器
"""

import pytest

from dataforge.generators.contact.landline import (
    FaxNumberGenerator,
    LandlineGenerator,
    TollFreeNumberGenerator,
)
from dataforge.generators.numeric.advanced import (
    CurrencyGenerator,
    DecimalGenerator,
    IntegerGenerator,
    PercentageGenerator,
    ScientificNumberGenerator,
)
from dataforge.generators.text.chinese import ChineseTextGenerator, EnglishTextGenerator
from dataforge.generators.text.special_chars import (
    SpecialCharGenerator,
    UnicodeSymbolGenerator,
)


class TestTextGenerators:
    """测试文本类生成器"""

    def test_chinese_text_generator(self):
        """测试中文文本生成器"""
        generator = ChineseTextGenerator()

        # 测试不同主题
        result = generator.generate(theme="general", text_type="sentence")
        assert isinstance(result, str)
        assert len(result) > 0

        result = generator.generate(theme="business", text_type="word")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_english_text_generator(self):
        """测试英文文本生成器"""
        generator = EnglishTextGenerator()

        # 测试lorem主题
        result = generator.generate(theme="lorem", text_type="sentence")
        assert isinstance(result, str)
        assert len(result) > 0

        # 测试general主题
        result = generator.generate(theme="general", text_type="paragraph")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_special_char_generator(self):
        """测试特殊字符生成器"""
        generator = SpecialCharGenerator()

        # 测试数学符号
        result = generator.generate(char_type="math")
        assert isinstance(result, str)
        assert len(result) == 1

        # 测试emoji
        result = generator.generate(char_type="emoji")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_unicode_symbol_generator(self):
        """测试Unicode符号生成器"""
        generator = UnicodeSymbolGenerator()

        # 测试箭头符号
        result = generator.generate(range_type="arrows")
        assert isinstance(result, str)
        assert len(result) == 1


class TestNumericGenerators:
    """测试数值类生成器"""

    def test_integer_generator(self):
        """测试整数生成器"""
        generator = IntegerGenerator()

        # 测试范围限制
        result = generator.generate(min_value=1, max_value=100, step=2)
        assert isinstance(result, int)
        assert 1 <= result <= 100
        assert result % 2 == 1  # 步长为2，从1开始

    def test_decimal_generator(self):
        """测试小数生成器"""
        generator = DecimalGenerator()

        # 测试精度控制
        result = generator.generate(min_value=0.1, max_value=1.0, precision=3)
        assert isinstance(result, float)
        assert 0.1 <= result <= 1.0
        # 检查小数位数
        decimal_places = len(str(result).split(".")[-1])
        assert decimal_places <= 3

    def test_percentage_generator(self):
        """测试百分比生成器"""
        generator = PercentageGenerator()

        result = generator.generate()
        assert isinstance(result, float)
        assert 0.0 <= result <= 100.0

    def test_currency_generator(self):
        """测试币种金额生成器"""
        generator = CurrencyGenerator()

        # 测试人民币
        result = generator.generate(currency="CNY", min_value=1.0, max_value=1000.0)
        assert isinstance(result, str)
        assert "¥" in result

        # 测试美元
        result = generator.generate(currency="USD", min_value=1.0, max_value=1000.0)
        assert isinstance(result, str)
        assert "$" in result

    def test_scientific_number_generator(self):
        """测试科学计数法生成器"""
        generator = ScientificNumberGenerator()

        result = generator.generate(min_value=1e-6, max_value=1e6)
        assert isinstance(result, str)
        assert "e" in result or "E" in result


class TestContactGenerators:
    """测试通信类生成器"""

    def test_landline_generator(self):
        """测试座机号码生成器"""
        generator = LandlineGenerator()

        # 测试国内号码
        result = generator.generate(country="CN")
        assert isinstance(result, str)
        assert len(result) >= 10

        # 测试国际号码
        result = generator.generate(country="US")
        assert isinstance(result, str)

    def test_fax_number_generator(self):
        """测试传真号码生成器"""
        generator = FaxNumberGenerator()

        result = generator.generate(country="CN")
        assert isinstance(result, str)
        assert "010" in result or result.startswith("+86")

    def test_toll_free_generator(self):
        """测试免费电话号码生成器"""
        generator = TollFreeNumberGenerator()

        # 测试400号码
        result = generator.generate(prefix="400")
        assert isinstance(result, str)
        assert result.startswith("400")

        # 测试800号码
        result = generator.generate(prefix="800")
        assert isinstance(result, str)
        assert result.startswith("800")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
