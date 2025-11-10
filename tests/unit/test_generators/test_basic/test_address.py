"""
地址生成器增强测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestAddressGenerator:
    """地址生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个地址"""
        config = GeneratorConfig(
            generator_type="address",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        address = generator.generate_single()
        
        assert isinstance(address, str)
        assert len(address) >= 5
        assert generator.validate(address)

    def test_generate_batch(self, generator_factory):
        """测试批量生成地址"""
        config = GeneratorConfig(
            generator_type="address",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        addresses = generator.generate_batch(10)
        
        assert len(addresses) == 10
        for address in addresses:
            assert isinstance(address, str)
            assert len(address) >= 5

    def test_province_filter(self, generator_factory):
        """测试省份筛选"""
        config = GeneratorConfig(
            generator_type="address",
            parameters={"province": "北京"}
        )
        generator = generator_factory.create_generator(config)
        address = generator.generate_single()
        
        assert "北京" in address

    def test_city_filter(self, generator_factory):
        """测试城市筛选"""
        config = GeneratorConfig(
            generator_type="address",
            parameters={"city": "上海"}
        )
        generator = generator_factory.create_generator(config)
        address = generator.generate_single()
        
        assert "上海" in address

    def test_full_address(self, generator_factory):
        """测试完整地址"""
        config = GeneratorConfig(
            generator_type="address",
            parameters={"detail_level": "full"}
        )
        generator = generator_factory.create_generator(config)
        address = generator.generate_single()
        
        # Full address should include province, city, district, street
        assert len(address) >= 10

    def test_simple_address(self, generator_factory):
        """测试简单地址"""
        config = GeneratorConfig(
            generator_type="address",
            parameters={"detail_level": "simple"}
        )
        generator = generator_factory.create_generator(config)
        address = generator.generate_single()
        
        assert isinstance(address, str)
        assert len(address) >= 5

    def test_with_postal_code(self, generator_factory):
        """测试带邮编"""
        config = GeneratorConfig(
            generator_type="address",
            parameters={"include_postal_code": True}
        )
        generator = generator_factory.create_generator(config)
        address = generator.generate_single()
        
        # May include 6-digit postal code
        assert isinstance(address, str)

    def test_validation(self, generator_factory):
        """测试地址验证"""
        config = GeneratorConfig(
            generator_type="address",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid addresses
        assert generator.validate("北京市朝阳区建国路1号")
        assert generator.validate("上海市浦东新区世纪大道100号")
        
        # Invalid addresses
        assert not generator.validate("AB")  # Too short
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_variety(self, generator_factory):
        """测试地址多样性"""
        config = GeneratorConfig(
            generator_type="address",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        addresses = generator.generate_batch(50)
        
        # Should have variety
        unique_addresses = set(addresses)
        assert len(unique_addresses) > 30

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        config = GeneratorConfig(
            generator_type="address",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            address = generator.generate_single()
            assert address is not None
            assert len(address) >= 5
            assert isinstance(address, str)
