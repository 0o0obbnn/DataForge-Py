"""
邮箱验证码生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestEmailVerificationGenerator:
    """邮箱验证码生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个邮箱验证码"""
        from dataforge.generators.auth.email_verification import (
            EmailVerificationGenerator,
        )

        generator_factory.registry.register(
            "email_verification", EmailVerificationGenerator
        )

        config = GeneratorConfig(generator_type="email_verification", parameters={})
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()

        assert isinstance(code, str)
        assert len(code) >= 4
        assert generator.validate(code)

    def test_generate_batch(self, generator_factory):
        """测试批量生成邮箱验证码"""
        from dataforge.generators.auth.email_verification import (
            EmailVerificationGenerator,
        )

        generator_factory.registry.register(
            "email_verification", EmailVerificationGenerator
        )

        config = GeneratorConfig(generator_type="email_verification", parameters={})
        generator = generator_factory.create_generator(config)
        codes = generator.generate_batch(10)

        assert len(codes) == 10
        for code in codes:
            assert isinstance(code, str)
            assert len(code) >= 4

    def test_numeric_code(self, generator_factory):
        """测试纯数字验证码"""
        from dataforge.generators.auth.email_verification import (
            EmailVerificationGenerator,
        )

        generator_factory.registry.register(
            "email_verification", EmailVerificationGenerator
        )

        config = GeneratorConfig(
            generator_type="email_verification",
            parameters={"type": "numeric", "length": 6},
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()

        assert code.isdigit()
        assert len(code) == 6

    def test_alphanumeric_code(self, generator_factory):
        """测试字母数字验证码"""
        from dataforge.generators.auth.email_verification import (
            EmailVerificationGenerator,
        )

        generator_factory.registry.register(
            "email_verification", EmailVerificationGenerator
        )

        config = GeneratorConfig(
            generator_type="email_verification",
            parameters={"type": "alphanumeric", "length": 8},
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()

        assert code.isalnum()
        assert len(code) == 8

    def test_code_length_4(self, generator_factory):
        """测试4位验证码"""
        from dataforge.generators.auth.email_verification import (
            EmailVerificationGenerator,
        )

        generator_factory.registry.register(
            "email_verification", EmailVerificationGenerator
        )

        config = GeneratorConfig(
            generator_type="email_verification", parameters={"length": 4}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()

        assert len(code) == 4

    def test_code_length_8(self, generator_factory):
        """测试8位验证码"""
        from dataforge.generators.auth.email_verification import (
            EmailVerificationGenerator,
        )

        generator_factory.registry.register(
            "email_verification", EmailVerificationGenerator
        )

        config = GeneratorConfig(
            generator_type="email_verification", parameters={"length": 8}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()

        assert len(code) == 8

    def test_validation(self, generator_factory):
        """测试验证码验证"""
        from dataforge.generators.auth.email_verification import (
            EmailVerificationGenerator,
        )

        generator_factory.registry.register(
            "email_verification", EmailVerificationGenerator
        )

        config = GeneratorConfig(generator_type="email_verification", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid codes
        assert generator.validate("123456")
        assert generator.validate("ABC123")

        # Invalid codes
        assert not generator.validate("12")  # Too short
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_distribution(self, generator_factory):
        """测试验证码分布"""
        from dataforge.generators.auth.email_verification import (
            EmailVerificationGenerator,
        )

        generator_factory.registry.register(
            "email_verification", EmailVerificationGenerator
        )

        config = GeneratorConfig(
            generator_type="email_verification", parameters={"length": 6}
        )
        generator = generator_factory.create_generator(config)
        codes = generator.generate_batch(100)

        # Should have variety
        unique_codes = set(codes)
        assert len(unique_codes) > 50

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.auth.email_verification import (
            EmailVerificationGenerator,
        )

        generator_factory.registry.register(
            "email_verification", EmailVerificationGenerator
        )

        # Minimum length
        config = GeneratorConfig(
            generator_type="email_verification", parameters={"length": 4}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()
        assert len(code) == 4

        # Maximum common length
        config = GeneratorConfig(
            generator_type="email_verification", parameters={"length": 10}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()
        assert len(code) == 10
