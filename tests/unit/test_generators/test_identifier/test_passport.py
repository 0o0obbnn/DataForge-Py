"""
护照号生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestPassportGenerator:
    """护照号生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个护照号"""
        from dataforge.generators.identifier.passport import PassportGenerator

        generator_factory.registry.register("passport", PassportGenerator)

        config = GeneratorConfig(generator_type="passport", parameters={})
        generator = generator_factory.create_generator(config)
        passport = generator.generate_single()

        assert isinstance(passport, str)
        assert len(passport) >= 8
        assert generator.validate(passport)

    def test_generate_batch(self, generator_factory):
        """测试批量生成护照号"""
        from dataforge.generators.identifier.passport import PassportGenerator

        generator_factory.registry.register("passport", PassportGenerator)

        config = GeneratorConfig(generator_type="passport", parameters={})
        generator = generator_factory.create_generator(config)
        passports = generator.generate_batch(10)

        assert len(passports) == 10
        for passport in passports:
            assert isinstance(passport, str)
            assert len(passport) >= 8

    def test_chinese_passport(self, generator_factory):
        """测试中国护照号"""
        from dataforge.generators.identifier.passport import PassportGenerator

        generator_factory.registry.register("passport", PassportGenerator)

        config = GeneratorConfig(
            generator_type="passport", parameters={"country": "china"}
        )
        generator = generator_factory.create_generator(config)
        passport = generator.generate_single()

        # Chinese passport: E + 8 digits or G + 8 digits
        assert len(passport) == 9
        assert passport[0] in ["E", "G", "P", "S", "D"]
        assert passport[1:].isdigit()

    def test_us_passport(self, generator_factory):
        """测试美国护照号"""
        from dataforge.generators.identifier.passport import PassportGenerator

        generator_factory.registry.register("passport", PassportGenerator)

        config = GeneratorConfig(
            generator_type="passport", parameters={"country": "usa"}
        )
        generator = generator_factory.create_generator(config)
        passport = generator.generate_single()

        # US passport: 9 digits
        assert isinstance(passport, str)
        assert len(passport) >= 8

    def test_passport_format(self, generator_factory):
        """测试护照号格式"""
        from dataforge.generators.identifier.passport import PassportGenerator

        generator_factory.registry.register("passport", PassportGenerator)

        config = GeneratorConfig(generator_type="passport", parameters={})
        generator = generator_factory.create_generator(config)
        passport = generator.generate_single()

        # Should be alphanumeric
        assert passport.isalnum()

    def test_validation(self, generator_factory):
        """测试护照号验证"""
        from dataforge.generators.identifier.passport import PassportGenerator

        generator_factory.registry.register("passport", PassportGenerator)

        config = GeneratorConfig(generator_type="passport", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid passports
        assert generator.validate("E12345678")
        assert generator.validate("G87654321")

        # Invalid passports
        assert not generator.validate("123")  # Too short
        assert not generator.validate("E123")  # Too short
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试护照号唯一性"""
        from dataforge.generators.identifier.passport import PassportGenerator

        generator_factory.registry.register("passport", PassportGenerator)

        config = GeneratorConfig(generator_type="passport", parameters={})
        generator = generator_factory.create_generator(config)
        passports = generator.generate_batch(50)

        # All passports should be unique
        unique_passports = set(passports)
        assert len(unique_passports) == 50

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.identifier.passport import PassportGenerator

        generator_factory.registry.register("passport", PassportGenerator)

        config = GeneratorConfig(generator_type="passport", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            passport = generator.generate_single()
            assert passport is not None
            assert len(passport) >= 8
            assert passport.isalnum()

    def test_passport_english_name_uses_config(self, monkeypatch):
        """英文护照姓名应使用 name_en 配置"""
        from dataforge.generators.identifier.passport import (
            PassportGenerator,
            PassportGeneratorConfig,
        )

        def _fake_name_en_config():
            return {
                "first_names_male": ["Alpha"],
                "first_names_female": ["Beta"],
                "last_names": ["Gamma"],
            }

        monkeypatch.setattr(
            "dataforge.generators.identifier.passport.load_name_en_config",
            _fake_name_en_config,
        )

        config = PassportGeneratorConfig(
            generator_type="passport_internal",
            parameters={
                "include_dates": False,
                "include_name": True,
                "string_only": False,
                "country_code": "USA",
            },
            passport_type="E",
            country_code="USA",
            include_dates=False,
            include_name=True,
        )
        generator = PassportGenerator(config)
        data = generator.generate_single()

        assert isinstance(data, dict)
        assert data.get("holder_name") in {"Alpha Gamma", "Beta Gamma"}
