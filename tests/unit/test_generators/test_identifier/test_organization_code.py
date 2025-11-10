"""
组织机构代码生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestOrganizationCodeGenerator:
    """组织机构代码生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个组织机构代码"""
        config = GeneratorConfig(
            generator_type="organization_code",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()
        
        assert isinstance(code, str)
        assert len(code) in [9, 10]  # 9位本体码 或 9位+1位校验码
        assert generator.validate(code)

    def test_generate_batch(self, generator_factory):
        """测试批量生成组织机构代码"""
        config = GeneratorConfig(
            generator_type="organization_code",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        codes = generator.generate_batch(10)
        
        assert len(codes) == 10
        for code in codes:
            assert isinstance(code, str)
            assert len(code) in [9, 10]

    def test_code_format(self, generator_factory):
        """测试代码格式"""
        config = GeneratorConfig(
            generator_type="organization_code",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()
        
        # Format: 8 digits + 1 letter/digit (checksum)
        if len(code) == 9:
            assert code[:8].isdigit()
            assert code[8].isalnum()

    def test_with_hyphen(self, generator_factory):
        """测试带连字符格式"""
        config = GeneratorConfig(
            generator_type="organization_code",
            parameters={"format": "hyphen"}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()
        
        # May contain hyphen: XXXXXXXX-X
        assert isinstance(code, str)

    def test_checksum(self, generator_factory):
        """测试校验码"""
        config = GeneratorConfig(
            generator_type="organization_code",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()
        
        # Last character is checksum
        if len(code) == 9:
            assert code[-1].isalnum()

    def test_validation(self, generator_factory):
        """测试组织机构代码验证"""
        config = GeneratorConfig(
            generator_type="organization_code",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid code
        code = generator.generate_single()
        assert generator.validate(code)
        
        # Invalid codes
        assert not generator.validate("123")  # Too short
        assert not generator.validate("ABCDEFGHI")  # Not valid format
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试组织机构代码唯一性"""
        config = GeneratorConfig(
            generator_type="organization_code",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        codes = generator.generate_batch(50)
        
        # All codes should be unique
        unique_codes = set(codes)
        assert len(unique_codes) == 50

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        config = GeneratorConfig(
            generator_type="organization_code",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            code = generator.generate_single()
            assert code is not None
            assert len(code) in [9, 10]
            assert code[:8].isdigit()
