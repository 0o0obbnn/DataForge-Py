"""
社保号生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestSocialInsuranceGenerator:
    """社保号生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个社保号"""
        from dataforge.generators.identifier.social_insurance import (
            SocialInsuranceGenerator,
        )

        generator_factory.registry.register(
            "social_insurance", SocialInsuranceGenerator
        )

        config = GeneratorConfig(generator_type="social_insurance", parameters={})
        generator = generator_factory.create_generator(config)
        ssn = generator.generate_single()

        assert isinstance(ssn, str)
        assert len(ssn) >= 9
        assert generator.validate(ssn)

    def test_generate_batch(self, generator_factory):
        """测试批量生成社保号"""
        from dataforge.generators.identifier.social_insurance import (
            SocialInsuranceGenerator,
        )

        generator_factory.registry.register(
            "social_insurance", SocialInsuranceGenerator
        )

        config = GeneratorConfig(generator_type="social_insurance", parameters={})
        generator = generator_factory.create_generator(config)
        ssns = generator.generate_batch(10)

        assert len(ssns) == 10
        for ssn in ssns:
            assert isinstance(ssn, str)
            assert len(ssn) >= 9

    def test_chinese_format(self, generator_factory):
        """测试中国社保号格式"""
        from dataforge.generators.identifier.social_insurance import (
            SocialInsuranceGenerator,
        )

        generator_factory.registry.register(
            "social_insurance", SocialInsuranceGenerator
        )

        config = GeneratorConfig(
            generator_type="social_insurance", parameters={"country": "china"}
        )
        generator = generator_factory.create_generator(config)
        ssn = generator.generate_single()

        # Chinese social insurance number format
        assert isinstance(ssn, str)
        assert len(ssn) >= 9

    def test_us_format(self, generator_factory):
        """测试美国社保号格式"""
        from dataforge.generators.identifier.social_insurance import (
            SocialInsuranceGenerator,
        )

        generator_factory.registry.register(
            "social_insurance", SocialInsuranceGenerator
        )

        config = GeneratorConfig(
            generator_type="social_insurance", parameters={"country": "usa"}
        )
        generator = generator_factory.create_generator(config)
        ssn = generator.generate_single()

        # US SSN format: XXX-XX-XXXX or XXXXXXXXX
        if "-" in ssn:
            parts = ssn.split("-")
            assert len(parts) == 3
            assert len(parts[0]) == 3
            assert len(parts[1]) == 2
            assert len(parts[2]) == 4
        else:
            assert len(ssn) == 9
            assert ssn.isdigit()

    def test_with_region(self, generator_factory):
        """测试指定地区"""
        from dataforge.generators.identifier.social_insurance import (
            SocialInsuranceGenerator,
        )

        generator_factory.registry.register(
            "social_insurance", SocialInsuranceGenerator
        )

        config = GeneratorConfig(
            generator_type="social_insurance", parameters={"region": "110000"}
        )
        generator = generator_factory.create_generator(config)
        ssn = generator.generate_single()

        assert isinstance(ssn, str)

    def test_validation(self, generator_factory):
        """测试社保号验证"""
        from dataforge.generators.identifier.social_insurance import (
            SocialInsuranceGenerator,
        )

        generator_factory.registry.register(
            "social_insurance", SocialInsuranceGenerator
        )

        config = GeneratorConfig(generator_type="social_insurance", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid SSN
        ssn = generator.generate_single()
        assert generator.validate(ssn)

        # Invalid SSNs
        assert not generator.validate("123")  # Too short
        assert not generator.validate("ABCDEFGHI")  # Not valid
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试社保号唯一性"""
        from dataforge.generators.identifier.social_insurance import (
            SocialInsuranceGenerator,
        )

        generator_factory.registry.register(
            "social_insurance", SocialInsuranceGenerator
        )

        config = GeneratorConfig(generator_type="social_insurance", parameters={})
        generator = generator_factory.create_generator(config)
        ssns = generator.generate_batch(50)

        # All SSNs should be unique
        unique_ssns = set(ssns)
        assert len(unique_ssns) == 50

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.identifier.social_insurance import (
            SocialInsuranceGenerator,
        )

        generator_factory.registry.register(
            "social_insurance", SocialInsuranceGenerator
        )

        config = GeneratorConfig(generator_type="social_insurance", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            ssn = generator.generate_single()
            assert ssn is not None
            assert len(ssn) >= 9
