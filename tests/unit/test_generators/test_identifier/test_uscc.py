"""
统一社会信用代码生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestUSCCGenerator:
    """统一社会信用代码生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个统一社会信用代码"""
        config = GeneratorConfig(generator_type="uscc", parameters={})
        generator = generator_factory.create_generator(config)
        uscc = generator.generate_single()

        assert isinstance(uscc, str)
        assert len(uscc) == 18
        assert generator.validate(uscc)

    def test_generate_batch(self, generator_factory):
        """测试批量生成统一社会信用代码"""
        config = GeneratorConfig(generator_type="uscc", parameters={})
        generator = generator_factory.create_generator(config)
        usccs = generator.generate_batch(10)

        assert len(usccs) == 10
        for uscc in usccs:
            assert isinstance(uscc, str)
            assert len(uscc) == 18
            assert generator.validate(uscc)

    def test_format_structure(self, generator_factory):
        """测试代码格式结构"""
        config = GeneratorConfig(generator_type="uscc", parameters={})
        generator = generator_factory.create_generator(config)
        uscc = generator.generate_single()

        # USCC format: 18 characters (numbers and uppercase letters)
        assert len(uscc) == 18
        assert uscc.isalnum()
        assert uscc.isupper() or uscc.isdigit()

    def test_registration_authority(self, generator_factory):
        """测试登记管理部门代码"""
        config = GeneratorConfig(
            generator_type="uscc",
            parameters={"authority": "1"},  # 机构编制
        )
        generator = generator_factory.create_generator(config)
        uscc = generator.generate_single()

        # First character should be the authority code
        assert uscc[0] in "1234569NY"

    def test_organization_type(self, generator_factory):
        """测试机构类别代码"""
        config = GeneratorConfig(
            generator_type="uscc",
            parameters={"org_type": "1"},  # 企业
        )
        generator = generator_factory.create_generator(config)
        uscc = generator.generate_single()

        # Second character should be organization type
        assert uscc[1] in "123459"

    def test_validation(self, generator_factory):
        """测试统一社会信用代码验证"""
        config = GeneratorConfig(generator_type="uscc", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid USCC (example)
        # Note: Real validation requires checksum calculation
        generated = generator.generate_single()
        assert generator.validate(generated)

        # Invalid USCCs
        assert not generator.validate("12345")  # Too short
        assert not generator.validate("123456789012345678901")  # Too long
        assert not generator.validate("")

    def test_uniqueness(self, generator_factory):
        """测试统一社会信用代码唯一性"""
        config = GeneratorConfig(generator_type="uscc", parameters={})
        generator = generator_factory.create_generator(config)
        usccs = generator.generate_batch(50)

        # All codes should be unique
        unique_usccs = set(usccs)
        assert len(unique_usccs) == 50

    def test_checksum(self, generator_factory):
        """测试校验码"""
        config = GeneratorConfig(generator_type="uscc", parameters={})
        generator = generator_factory.create_generator(config)
        uscc = generator.generate_single()

        # Last character is checksum
        # Verify it's valid character
        assert uscc[-1] in "0123456789ABCDEFGHJKLMNPQRTUWXY"

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        config = GeneratorConfig(generator_type="uscc", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            uscc = generator.generate_single()
            assert uscc is not None
            assert len(uscc) == 18
            assert uscc.isalnum()
