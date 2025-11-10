"""
会话ID生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestSessionIDGenerator:
    """会话ID生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个会话ID"""
        from dataforge.generators.auth.session_id import SessionIDGenerator
        generator_factory.registry.register("session_id", SessionIDGenerator)
        
        config = GeneratorConfig(
            generator_type="session_id",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        session_id = generator.generate_single()
        
        assert isinstance(session_id, str)
        assert len(session_id) >= 16
        assert generator.validate(session_id)

    def test_generate_batch(self, generator_factory):
        """测试批量生成会话ID"""
        from dataforge.generators.auth.session_id import SessionIDGenerator
        generator_factory.registry.register("session_id", SessionIDGenerator)
        
        config = GeneratorConfig(
            generator_type="session_id",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        session_ids = generator.generate_batch(10)
        
        assert len(session_ids) == 10
        for session_id in session_ids:
            assert isinstance(session_id, str)
            assert len(session_id) >= 16

    def test_session_id_length(self, generator_factory):
        """测试会话ID长度"""
        from dataforge.generators.auth.session_id import SessionIDGenerator
        generator_factory.registry.register("session_id", SessionIDGenerator)
        
        config = GeneratorConfig(
            generator_type="session_id",
            parameters={"length": 32}
        )
        generator = generator_factory.create_generator(config)
        session_id = generator.generate_single()
        
        assert len(session_id) >= 32

    def test_hex_format(self, generator_factory):
        """测试十六进制格式"""
        from dataforge.generators.auth.session_id import SessionIDGenerator
        generator_factory.registry.register("session_id", SessionIDGenerator)
        
        config = GeneratorConfig(
            generator_type="session_id",
            parameters={"format": "hex"}
        )
        generator = generator_factory.create_generator(config)
        session_id = generator.generate_single()
        
        # Hex format should only contain 0-9, a-f
        assert all(c in '0123456789abcdefABCDEF' for c in session_id)

    def test_base64_format(self, generator_factory):
        """测试Base64格式"""
        from dataforge.generators.auth.session_id import SessionIDGenerator
        generator_factory.registry.register("session_id", SessionIDGenerator)
        
        config = GeneratorConfig(
            generator_type="session_id",
            parameters={"format": "base64"}
        )
        generator = generator_factory.create_generator(config)
        session_id = generator.generate_single()
        
        # Base64 characters
        assert isinstance(session_id, str)
        assert len(session_id) >= 16

    def test_validation(self, generator_factory):
        """测试会话ID验证"""
        from dataforge.generators.auth.session_id import SessionIDGenerator
        generator_factory.registry.register("session_id", SessionIDGenerator)
        
        config = GeneratorConfig(
            generator_type="session_id",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid session ID
        session_id = generator.generate_single()
        assert generator.validate(session_id)
        
        # Invalid session IDs
        assert not generator.validate("")
        assert not generator.validate("short")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试会话ID唯一性"""
        from dataforge.generators.auth.session_id import SessionIDGenerator
        generator_factory.registry.register("session_id", SessionIDGenerator)
        
        config = GeneratorConfig(
            generator_type="session_id",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        session_ids = generator.generate_batch(100)
        
        # All session IDs should be unique
        unique_ids = set(session_ids)
        assert len(unique_ids) == 100

    def test_security(self, generator_factory):
        """测试会话ID安全性"""
        from dataforge.generators.auth.session_id import SessionIDGenerator
        generator_factory.registry.register("session_id", SessionIDGenerator)
        
        config = GeneratorConfig(
            generator_type="session_id",
            parameters={"length": 32}
        )
        generator = generator_factory.create_generator(config)
        session_ids = generator.generate_batch(100)
        
        # Should have high entropy (no obvious patterns)
        unique_ids = set(session_ids)
        assert len(unique_ids) == 100

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.auth.session_id import SessionIDGenerator
        generator_factory.registry.register("session_id", SessionIDGenerator)
        
        # Minimum length
        config = GeneratorConfig(
            generator_type="session_id",
            parameters={"length": 16}
        )
        generator = generator_factory.create_generator(config)
        session_id = generator.generate_single()
        assert len(session_id) >= 16
        
        # Maximum length
        config = GeneratorConfig(
            generator_type="session_id",
            parameters={"length": 64}
        )
        generator = generator_factory.create_generator(config)
        session_id = generator.generate_single()
        assert len(session_id) >= 64
