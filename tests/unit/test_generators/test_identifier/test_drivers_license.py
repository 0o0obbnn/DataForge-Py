"""
驾驶证号生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestDriversLicenseGenerator:
    """驾驶证号生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个驾驶证号"""
        from dataforge.generators.identifier.drivers_license import (
            DriversLicenseGenerator,
        )

        generator_factory.registry.register("drivers_license", DriversLicenseGenerator)

        config = GeneratorConfig(generator_type="drivers_license", parameters={})
        generator = generator_factory.create_generator(config)
        license_num = generator.generate_single()

        assert isinstance(license_num, str)
        assert len(license_num) == 18
        assert generator.validate(license_num)

    def test_generate_batch(self, generator_factory):
        """测试批量生成驾驶证号"""
        from dataforge.generators.identifier.drivers_license import (
            DriversLicenseGenerator,
        )

        generator_factory.registry.register("drivers_license", DriversLicenseGenerator)

        config = GeneratorConfig(generator_type="drivers_license", parameters={})
        generator = generator_factory.create_generator(config)
        licenses = generator.generate_batch(10)

        assert len(licenses) == 10
        for license_num in licenses:
            assert isinstance(license_num, str)
            assert len(license_num) == 18

    def test_license_format(self, generator_factory):
        """测试驾驶证号格式"""
        from dataforge.generators.identifier.drivers_license import (
            DriversLicenseGenerator,
        )

        generator_factory.registry.register("drivers_license", DriversLicenseGenerator)

        config = GeneratorConfig(generator_type="drivers_license", parameters={})
        generator = generator_factory.create_generator(config)
        license_num = generator.generate_single()

        # Chinese driver's license: 18 digits (same format as ID card)
        assert len(license_num) == 18
        assert license_num.isdigit() or (
            license_num[:-1].isdigit() and license_num[-1] in "X0123456789"
        )

    def test_with_region(self, generator_factory):
        """测试指定地区"""
        from dataforge.generators.identifier.drivers_license import (
            DriversLicenseGenerator,
        )

        generator_factory.registry.register("drivers_license", DriversLicenseGenerator)

        config = GeneratorConfig(
            generator_type="drivers_license", parameters={"region": "110000"}  # Beijing
        )
        generator = generator_factory.create_generator(config)
        license_num = generator.generate_single()

        # Should start with Beijing region code
        assert license_num.startswith("11")

    def test_validation(self, generator_factory):
        """测试驾驶证号验证"""
        from dataforge.generators.identifier.drivers_license import (
            DriversLicenseGenerator,
        )

        generator_factory.registry.register("drivers_license", DriversLicenseGenerator)

        config = GeneratorConfig(generator_type="drivers_license", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid license
        license_num = generator.generate_single()
        assert generator.validate(license_num)

        # Invalid licenses
        assert not generator.validate("123")  # Too short
        assert not generator.validate("ABCDEFGHIJ12345678")  # Not numeric
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试驾驶证号唯一性"""
        from dataforge.generators.identifier.drivers_license import (
            DriversLicenseGenerator,
        )

        generator_factory.registry.register("drivers_license", DriversLicenseGenerator)

        config = GeneratorConfig(generator_type="drivers_license", parameters={})
        generator = generator_factory.create_generator(config)
        licenses = generator.generate_batch(50)

        # All licenses should be unique
        unique_licenses = set(licenses)
        assert len(unique_licenses) == 50

    def test_checksum(self, generator_factory):
        """测试校验码"""
        from dataforge.generators.identifier.drivers_license import (
            DriversLicenseGenerator,
        )

        generator_factory.registry.register("drivers_license", DriversLicenseGenerator)

        config = GeneratorConfig(generator_type="drivers_license", parameters={})
        generator = generator_factory.create_generator(config)
        license_num = generator.generate_single()

        # Last character is checksum (0-9 or X)
        assert license_num[-1] in "0123456789X"

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.identifier.drivers_license import (
            DriversLicenseGenerator,
        )

        generator_factory.registry.register("drivers_license", DriversLicenseGenerator)

        config = GeneratorConfig(generator_type="drivers_license", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            license_num = generator.generate_single()
            assert license_num is not None
            assert len(license_num) == 18
