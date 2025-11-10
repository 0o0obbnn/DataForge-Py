"""
LEI(法人机构识别编码)生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestLEIGenerator:
    """LEI生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个LEI"""
        config = GeneratorConfig(
            generator_type="lei",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        lei = generator.generate_single()
        
        assert isinstance(lei, str)
        assert len(lei) == 20
        assert generator.validate(lei)

    def test_generate_batch(self, generator_factory):
        """测试批量生成LEI"""
        config = GeneratorConfig(
            generator_type="lei",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        leis = generator.generate_batch(10)
        
        assert len(leis) == 10
        for lei in leis:
            assert isinstance(lei, str)
            assert len(lei) == 20
            assert generator.validate(lei)

    def test_lei_format(self, generator_factory):
        """测试LEI格式"""
        config = GeneratorConfig(
            generator_type="lei",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        lei = generator.generate_single()
        
        # LEI format: 20 alphanumeric characters
        assert len(lei) == 20
        assert lei.isalnum()
        assert lei.isupper()

    def test_lei_structure(self, generator_factory):
        """测试LEI结构"""
        config = GeneratorConfig(
            generator_type="lei",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        lei = generator.generate_single()
        
        # LEI structure:
        # Characters 1-4: LOU identifier
        # Characters 5-6: Reserved (usually 00)
        # Characters 7-18: Entity identifier
        # Characters 19-20: Check digits
        assert len(lei) == 20
        assert lei[4:6].isdigit()  # Reserved characters

    def test_validation(self, generator_factory):
        """测试LEI验证"""
        config = GeneratorConfig(
            generator_type="lei",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid LEI (generated)
        lei = generator.generate_single()
        assert generator.validate(lei)
        
        # Invalid LEIs
        assert not generator.validate("12345")  # Too short
        assert not generator.validate("12345678901234567890123")  # Too long
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试LEI唯一性"""
        config = GeneratorConfig(
            generator_type="lei",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        leis = generator.generate_batch(50)
        
        # All LEIs should be unique
        unique_leis = set(leis)
        assert len(unique_leis) == 50

    def test_checksum(self, generator_factory):
        """测试校验码"""
        config = GeneratorConfig(
            generator_type="lei",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        lei = generator.generate_single()
        
        # Last 2 characters are check digits
        check_digits = lei[-2:]
        assert check_digits.isdigit()
        assert 0 <= int(check_digits) <= 99

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        config = GeneratorConfig(
            generator_type="lei",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            lei = generator.generate_single()
            assert lei is not None
            assert len(lei) == 20
            assert lei.isalnum()
            assert lei.isupper()
