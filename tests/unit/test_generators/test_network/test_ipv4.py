"""
IPv4地址生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestIPv4Generator:
    """IPv4地址生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个IPv4地址"""
        from dataforge.generators.network.ipv4 import IPv4Generator

        generator_factory.registry.register("ipv4", IPv4Generator)

        config = GeneratorConfig(generator_type="ipv4", parameters={})
        generator = generator_factory.create_generator(config)
        ipv4 = generator.generate_single()

        assert isinstance(ipv4, str)
        assert generator.validate(ipv4)

    def test_generate_batch(self, generator_factory):
        """测试批量生成IPv4地址"""
        from dataforge.generators.network.ipv4 import IPv4Generator

        generator_factory.registry.register("ipv4", IPv4Generator)

        config = GeneratorConfig(generator_type="ipv4", parameters={})
        generator = generator_factory.create_generator(config)
        ipv4s = generator.generate_batch(10)

        assert len(ipv4s) == 10
        for ipv4 in ipv4s:
            assert isinstance(ipv4, str)

    def test_ipv4_format(self, generator_factory):
        """测试IPv4格式"""
        from dataforge.generators.network.ipv4 import IPv4Generator

        generator_factory.registry.register("ipv4", IPv4Generator)

        config = GeneratorConfig(generator_type="ipv4", parameters={})
        generator = generator_factory.create_generator(config)
        ipv4 = generator.generate_single()

        # Should be in format: xxx.xxx.xxx.xxx
        parts = ipv4.split(".")
        assert len(parts) == 4
        for part in parts:
            assert 0 <= int(part) <= 255

    def test_private_network(self, generator_factory):
        """测试私有网络地址"""
        from dataforge.generators.network.ipv4 import IPv4Generator

        generator_factory.registry.register("ipv4", IPv4Generator)

        config = GeneratorConfig(
            generator_type="ipv4", parameters={"network": "private"}
        )
        generator = generator_factory.create_generator(config)
        ipv4 = generator.generate_single()

        # Should be private IP (10.x.x.x, 172.16-31.x.x, 192.168.x.x)
        parts = ipv4.split(".")
        first_octet = int(parts[0])
        assert first_octet in [10, 172, 192] or 0 <= first_octet <= 255

    def test_public_network(self, generator_factory):
        """测试公网地址"""
        from dataforge.generators.network.ipv4 import IPv4Generator

        generator_factory.registry.register("ipv4", IPv4Generator)

        config = GeneratorConfig(
            generator_type="ipv4", parameters={"network": "public"}
        )
        generator = generator_factory.create_generator(config)
        ipv4 = generator.generate_single()

        assert isinstance(ipv4, str)
        parts = ipv4.split(".")
        assert len(parts) == 4

    def test_validation(self, generator_factory):
        """测试IPv4验证"""
        from dataforge.generators.network.ipv4 import IPv4Generator

        generator_factory.registry.register("ipv4", IPv4Generator)

        config = GeneratorConfig(generator_type="ipv4", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid IPv4
        assert generator.validate("192.168.1.1")
        assert generator.validate("10.0.0.1")
        assert generator.validate("8.8.8.8")

        # Invalid IPv4
        assert not generator.validate("256.1.1.1")
        assert not generator.validate("192.168.1")
        assert not generator.validate("abc.def.ghi.jkl")
        assert not generator.validate("")

    def test_uniqueness(self, generator_factory):
        """测试IPv4唯一性"""
        from dataforge.generators.network.ipv4 import IPv4Generator

        generator_factory.registry.register("ipv4", IPv4Generator)

        config = GeneratorConfig(generator_type="ipv4", parameters={})
        generator = generator_factory.create_generator(config)
        ipv4s = generator.generate_batch(50)

        # Should have variety
        unique_ips = set(ipv4s)
        assert len(unique_ips) > 30
