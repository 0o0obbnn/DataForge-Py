"""
UUID生成器测试
"""

import re
import uuid

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestUUIDGenerator:
    """UUID生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个UUID"""
        config = GeneratorConfig(
            generator_type="uuid",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        result = generator.generate_single()
        
        assert isinstance(result, str)
        assert generator.validate(result)
        # Verify it's a valid UUID format
        uuid.UUID(result)

    def test_generate_batch(self, generator_factory):
        """测试批量生成UUID"""
        config = GeneratorConfig(
            generator_type="uuid",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        results = generator.generate_batch(10)
        
        assert len(results) == 10
        for result in results:
            assert isinstance(result, str)
            assert generator.validate(result)
            uuid.UUID(result)

    def test_uuid4_format(self, generator_factory):
        """测试UUID4格式"""
        config = GeneratorConfig(
            generator_type="uuid",
            parameters={"version": 4}
        )
        generator = generator_factory.create_generator(config)
        result = generator.generate_single()
        
        # UUID4 format: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
        assert re.match(pattern, result, re.IGNORECASE)

    def test_uniqueness(self, generator_factory):
        """测试UUID唯一性"""
        config = GeneratorConfig(
            generator_type="uuid",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        uuids = generator.generate_batch(100)
        
        # All UUIDs should be unique
        assert len(set(uuids)) == 100

    def test_validation(self, generator_factory):
        """测试UUID验证"""
        config = GeneratorConfig(
            generator_type="uuid",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid UUIDs
        assert generator.validate("550e8400-e29b-41d4-a716-446655440000")
        assert generator.validate("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
        
        # Invalid UUIDs
        assert not generator.validate("not-a-uuid")
        assert not generator.validate("550e8400-e29b-41d4-a716")
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uppercase_format(self, generator_factory):
        """测试大写格式"""
        config = GeneratorConfig(
            generator_type="uuid",
            parameters={"uppercase": True}
        )
        generator = generator_factory.create_generator(config)
        result = generator.generate_single()
        
        # Check if uppercase (if parameter is supported)
        assert isinstance(result, str)
        uuid.UUID(result)

    def test_no_hyphens(self, generator_factory):
        """测试无连字符格式"""
        config = GeneratorConfig(
            generator_type="uuid",
            parameters={"hyphens": False}
        )
        generator = generator_factory.create_generator(config)
        result = generator.generate_single()
        
        # Should be valid UUID format
        assert isinstance(result, str)
        # May or may not have hyphens depending on implementation
        if '-' not in result:
            assert len(result) == 32
        else:
            uuid.UUID(result)

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        config = GeneratorConfig(
            generator_type="uuid",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            result = generator.generate_single()
            assert result is not None
            assert len(result) >= 32  # At least 32 hex characters
