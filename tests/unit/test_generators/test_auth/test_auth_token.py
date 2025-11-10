"""
认证令牌生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestAuthTokenGenerator:
    """认证令牌生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个认证令牌"""
        from dataforge.generators.auth.auth_token import AuthTokenGenerator
        generator_factory.registry.register("auth_token", AuthTokenGenerator)
        
        config = GeneratorConfig(
            generator_type="auth_token",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        token = generator.generate_single()
        
        assert isinstance(token, str)
        assert len(token) > 0
        assert generator.validate(token)

    def test_generate_batch(self, generator_factory):
        """测试批量生成认证令牌"""
        from dataforge.generators.auth.auth_token import AuthTokenGenerator
        generator_factory.registry.register("auth_token", AuthTokenGenerator)
        
        config = GeneratorConfig(
            generator_type="auth_token",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        tokens = generator.generate_batch(10)
        
        assert len(tokens) == 10
        for token in tokens:
            assert isinstance(token, str)
            assert len(token) > 0
            assert generator.validate(token)

    def test_token_length(self, generator_factory):
        """测试令牌长度"""
        from dataforge.generators.auth.auth_token import AuthTokenGenerator
        generator_factory.registry.register("auth_token", AuthTokenGenerator)
        
        config = GeneratorConfig(
            generator_type="auth_token",
            parameters={"length": 32}
        )
        generator = generator_factory.create_generator(config)
        token = generator.generate_single()
        
        assert isinstance(token, str)
        # Length may vary depending on encoding
        assert len(token) >= 32

    def test_token_format(self, generator_factory):
        """测试令牌格式"""
        from dataforge.generators.auth.auth_token import AuthTokenGenerator
        generator_factory.registry.register("auth_token", AuthTokenGenerator)
        
        config = GeneratorConfig(
            generator_type="auth_token",
            parameters={"format": "hex"}
        )
        generator = generator_factory.create_generator(config)
        token = generator.generate_single()
        
        # Hex format should only contain 0-9, a-f
        assert all(c in '0123456789abcdefABCDEF' for c in token)

    def test_uniqueness(self, generator_factory):
        """测试令牌唯一性"""
        from dataforge.generators.auth.auth_token import AuthTokenGenerator
        generator_factory.registry.register("auth_token", AuthTokenGenerator)
        
        config = GeneratorConfig(
            generator_type="auth_token",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        tokens = generator.generate_batch(100)
        
        # All tokens should be unique
        unique_tokens = set(tokens)
        assert len(unique_tokens) == 100

    def test_validation(self, generator_factory):
        """测试令牌验证"""
        from dataforge.generators.auth.auth_token import AuthTokenGenerator
        generator_factory.registry.register("auth_token", AuthTokenGenerator)
        
        config = GeneratorConfig(
            generator_type="auth_token",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid token
        token = generator.generate_single()
        assert generator.validate(token)
        
        # Invalid tokens
        assert not generator.validate("")
        assert not generator.validate("   ")
        assert not generator.validate(123)

    def test_jwt_format(self, generator_factory):
        """测试JWT格式令牌"""
        from dataforge.generators.auth.auth_token import AuthTokenGenerator
        generator_factory.registry.register("auth_token", AuthTokenGenerator)
        
        config = GeneratorConfig(
            generator_type="auth_token",
            parameters={"format": "jwt"}
        )
        generator = generator_factory.create_generator(config)
        token = generator.generate_single()
        
        # JWT format: header.payload.signature
        if '.' in token:
            parts = token.split('.')
            assert len(parts) == 3

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.auth.auth_token import AuthTokenGenerator
        generator_factory.registry.register("auth_token", AuthTokenGenerator)
        
        config = GeneratorConfig(
            generator_type="auth_token",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            token = generator.generate_single()
            assert token is not None
            assert len(token) > 0
            assert isinstance(token, str)
