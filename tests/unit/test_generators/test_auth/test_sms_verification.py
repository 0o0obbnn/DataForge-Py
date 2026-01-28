"""
短信验证码生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestSMSVerificationGenerator:
    """短信验证码生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个短信验证码"""
        from dataforge.generators.auth.sms_verification import SMSVerificationGenerator

        generator_factory.registry.register(
            "sms_verification", SMSVerificationGenerator
        )

        config = GeneratorConfig(generator_type="sms_verification", parameters={})
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()

        assert isinstance(code, str)
        assert code.isdigit()
        assert generator.validate(code)

    def test_generate_batch(self, generator_factory):
        """测试批量生成短信验证码"""
        from dataforge.generators.auth.sms_verification import SMSVerificationGenerator

        generator_factory.registry.register(
            "sms_verification", SMSVerificationGenerator
        )

        config = GeneratorConfig(generator_type="sms_verification", parameters={})
        generator = generator_factory.create_generator(config)
        codes = generator.generate_batch(10)

        assert len(codes) == 10
        for code in codes:
            assert isinstance(code, str)
            assert code.isdigit()

    def test_code_length_4(self, generator_factory):
        """测试4位验证码"""
        from dataforge.generators.auth.sms_verification import SMSVerificationGenerator

        generator_factory.registry.register(
            "sms_verification", SMSVerificationGenerator
        )

        config = GeneratorConfig(
            generator_type="sms_verification", parameters={"length": 4}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()

        assert len(code) == 4
        assert code.isdigit()

    def test_code_length_6(self, generator_factory):
        """测试6位验证码"""
        from dataforge.generators.auth.sms_verification import SMSVerificationGenerator

        generator_factory.registry.register(
            "sms_verification", SMSVerificationGenerator
        )

        config = GeneratorConfig(
            generator_type="sms_verification", parameters={"length": 6}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()

        assert len(code) == 6
        assert code.isdigit()

    def test_numeric_only(self, generator_factory):
        """测试纯数字验证码"""
        from dataforge.generators.auth.sms_verification import SMSVerificationGenerator

        generator_factory.registry.register(
            "sms_verification", SMSVerificationGenerator
        )

        config = GeneratorConfig(
            generator_type="sms_verification", parameters={"type": "numeric"}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()

        assert code.isdigit()

    def test_validation(self, generator_factory):
        """测试验证码验证"""
        from dataforge.generators.auth.sms_verification import SMSVerificationGenerator

        generator_factory.registry.register(
            "sms_verification", SMSVerificationGenerator
        )

        config = GeneratorConfig(generator_type="sms_verification", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid codes
        assert generator.validate("123456")
        assert generator.validate("0000")

        # Invalid codes
        assert not generator.validate("12")  # Too short
        assert not generator.validate("ABCD")  # Not numeric
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_distribution(self, generator_factory):
        """测试验证码分布"""
        from dataforge.generators.auth.sms_verification import SMSVerificationGenerator

        generator_factory.registry.register(
            "sms_verification", SMSVerificationGenerator
        )

        config = GeneratorConfig(
            generator_type="sms_verification", parameters={"length": 4}
        )
        generator = generator_factory.create_generator(config)
        codes = generator.generate_batch(100)

        # Should have variety
        unique_codes = set(codes)
        assert len(unique_codes) > 50

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.auth.sms_verification import SMSVerificationGenerator

        generator_factory.registry.register(
            "sms_verification", SMSVerificationGenerator
        )

        # Minimum length
        config = GeneratorConfig(
            generator_type="sms_verification", parameters={"length": 4}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()
        assert len(code) == 4
        assert code.isdigit()

        # Maximum common length
        config = GeneratorConfig(
            generator_type="sms_verification", parameters={"length": 8}
        )
        generator = generator_factory.create_generator(config)
        code = generator.generate_single()
        assert len(code) == 8
        assert code.isdigit()
