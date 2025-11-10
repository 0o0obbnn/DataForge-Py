"""
IPv6地址生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestIPv6Generator:
    """IPv6地址生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个IPv6地址"""
        from dataforge.generators.network.ipv6 import IPv6Generator
        generator_factory.registry.register("ipv6", IPv6Generator)
        
        config = GeneratorConfig(
            generator_type="ipv6",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        ipv6 = generator.generate_single()
        
        assert isinstance(ipv6, str)
        assert generator.validate(ipv6)

    def test_generate_batch(self, generator_factory):
        """测试批量生成IPv6地址"""
        from dataforge.generators.network.ipv6 import IPv6Generator
        generator_factory.registry.register("ipv6", IPv6Generator)
        
        config = GeneratorConfig(
            generator_type="ipv6",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        ipv6s = generator.generate_batch(10)
        
        assert len(ipv6s) == 10
        for ipv6 in ipv6s:
            assert isinstance(ipv6, str)

    def test_ipv6_format(self, generator_factory):
        """测试IPv6格式"""
        from dataforge.generators.network.ipv6 import IPv6Generator
        generator_factory.registry.register("ipv6", IPv6Generator)
        
        config = GeneratorConfig(
            generator_type="ipv6",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        ipv6 = generator.generate_single()
        
        # Should contain colons
        assert ':' in ipv6
        # Should be hexadecimal
        for char in ipv6.replace(':', ''):
            assert char in '0123456789abcdefABCDEF'

    def test_full_format(self, generator_factory):
        """测试完整格式"""
        from dataforge.generators.network.ipv6 import IPv6Generator
        generator_factory.registry.register("ipv6", IPv6Generator)
        
        config = GeneratorConfig(
            generator_type="ipv6",
            parameters={"format": "full"}
        )
        generator = generator_factory.create_generator(config)
        ipv6 = generator.generate_single()
        
        # Full format should have 8 groups
        if '::' not in ipv6:
            parts = ipv6.split(':')
            assert len(parts) <= 8

    def test_compressed_format(self, generator_factory):
        """测试压缩格式"""
        from dataforge.generators.network.ipv6 import IPv6Generator
        generator_factory.registry.register("ipv6", IPv6Generator)
        
        config = GeneratorConfig(
            generator_type="ipv6",
            parameters={"format": "compressed"}
        )
        generator = generator_factory.create_generator(config)
        ipv6 = generator.generate_single()
        
        assert isinstance(ipv6, str)
        assert ':' in ipv6

    def test_validation(self, generator_factory):
        """测试IPv6验证"""
        from dataforge.generators.network.ipv6 import IPv6Generator
        generator_factory.registry.register("ipv6", IPv6Generator)
        
        config = GeneratorConfig(
            generator_type="ipv6",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid IPv6
        ipv6 = generator.generate_single()
        assert generator.validate(ipv6)
        
        # Invalid IPv6
        assert not generator.validate("192.168.1.1")
        assert not generator.validate("gggg::1")
        assert not generator.validate("")

    def test_uniqueness(self, generator_factory):
        """测试IPv6唯一性"""
        from dataforge.generators.network.ipv6 import IPv6Generator
        generator_factory.registry.register("ipv6", IPv6Generator)
        
        config = GeneratorConfig(
            generator_type="ipv6",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        ipv6s = generator.generate_batch(50)
        
        # Should have variety
        unique_ips = set(ipv6s)
        assert len(unique_ips) > 40
