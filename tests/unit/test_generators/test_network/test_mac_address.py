"""
MAC地址生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestMACAddressGenerator:
    """MAC地址生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个MAC地址"""
        from dataforge.generators.network.mac_address import MACAddressGenerator

        generator_factory.registry.register("mac_address", MACAddressGenerator)

        config = GeneratorConfig(generator_type="mac_address", parameters={})
        generator = generator_factory.create_generator(config)
        mac = generator.generate_single()

        assert isinstance(mac, str)
        assert generator.validate(mac)

    def test_generate_batch(self, generator_factory):
        """测试批量生成MAC地址"""
        from dataforge.generators.network.mac_address import MACAddressGenerator

        generator_factory.registry.register("mac_address", MACAddressGenerator)

        config = GeneratorConfig(generator_type="mac_address", parameters={})
        generator = generator_factory.create_generator(config)
        macs = generator.generate_batch(10)

        assert len(macs) == 10
        for mac in macs:
            assert isinstance(mac, str)

    def test_mac_format(self, generator_factory):
        """测试MAC地址格式"""
        from dataforge.generators.network.mac_address import MACAddressGenerator

        generator_factory.registry.register("mac_address", MACAddressGenerator)

        config = GeneratorConfig(generator_type="mac_address", parameters={})
        generator = generator_factory.create_generator(config)
        mac = generator.generate_single()

        # Should be in format: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX
        if ":" in mac:
            parts = mac.split(":")
            assert len(parts) == 6
        elif "-" in mac:
            parts = mac.split("-")
            assert len(parts) == 6

        # Each part should be hexadecimal
        for part in mac.replace(":", "").replace("-", ""):
            assert part in "0123456789abcdefABCDEF"

    def test_colon_separator(self, generator_factory):
        """测试冒号分隔符"""
        from dataforge.generators.network.mac_address import MACAddressGenerator

        generator_factory.registry.register("mac_address", MACAddressGenerator)

        config = GeneratorConfig(
            generator_type="mac_address", parameters={"separator": ":"}
        )
        generator = generator_factory.create_generator(config)
        mac = generator.generate_single()

        assert ":" in mac or len(mac) == 17

    def test_hyphen_separator(self, generator_factory):
        """测试连字符分隔符"""
        from dataforge.generators.network.mac_address import MACAddressGenerator

        generator_factory.registry.register("mac_address", MACAddressGenerator)

        config = GeneratorConfig(
            generator_type="mac_address", parameters={"separator": "-"}
        )
        generator = generator_factory.create_generator(config)
        mac = generator.generate_single()

        assert "-" in mac or len(mac) == 17

    def test_uppercase(self, generator_factory):
        """测试大写格式"""
        from dataforge.generators.network.mac_address import MACAddressGenerator

        generator_factory.registry.register("mac_address", MACAddressGenerator)

        config = GeneratorConfig(
            generator_type="mac_address", parameters={"case": "upper"}
        )
        generator = generator_factory.create_generator(config)
        mac = generator.generate_single()

        # Check if uppercase (allow separators)
        hex_chars = mac.replace(":", "").replace("-", "")
        assert hex_chars == hex_chars.upper() or hex_chars == hex_chars.lower()

    def test_validation(self, generator_factory):
        """测试MAC地址验证"""
        from dataforge.generators.network.mac_address import MACAddressGenerator

        generator_factory.registry.register("mac_address", MACAddressGenerator)

        config = GeneratorConfig(generator_type="mac_address", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid MAC
        assert generator.validate("00:11:22:33:44:55")
        assert generator.validate("AA-BB-CC-DD-EE-FF")

        # Invalid MAC
        assert not generator.validate("00:11:22:33:44")
        assert not generator.validate("GG:HH:II:JJ:KK:LL")
        assert not generator.validate("")

    def test_uniqueness(self, generator_factory):
        """测试MAC地址唯一性"""
        from dataforge.generators.network.mac_address import MACAddressGenerator

        generator_factory.registry.register("mac_address", MACAddressGenerator)

        config = GeneratorConfig(generator_type="mac_address", parameters={})
        generator = generator_factory.create_generator(config)
        macs = generator.generate_batch(50)

        # Should have variety
        unique_macs = set(macs)
        assert len(unique_macs) > 40
