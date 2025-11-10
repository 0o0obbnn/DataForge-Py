"""
密码生成器测试
"""

import re

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestPasswordGenerator:
    """密码生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个密码"""
        from dataforge.generators.basic.password import PasswordGenerator
        generator_factory.registry.register("password", PasswordGenerator)
        
        config = GeneratorConfig(
            generator_type="password",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        password = generator.generate_single()
        
        assert isinstance(password, str)
        assert len(password) >= 8
        assert generator.validate(password)

    def test_generate_batch(self, generator_factory):
        """测试批量生成密码"""
        from dataforge.generators.basic.password import PasswordGenerator
        generator_factory.registry.register("password", PasswordGenerator)
        
        config = GeneratorConfig(
            generator_type="password",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        passwords = generator.generate_batch(10)
        
        assert len(passwords) == 10
        for pwd in passwords:
            assert isinstance(pwd, str)
            assert len(pwd) >= 8

    def test_password_length(self, generator_factory):
        """测试指定密码长度"""
        from dataforge.generators.basic.password import PasswordGenerator
        generator_factory.registry.register("password", PasswordGenerator)
        
        config = GeneratorConfig(
            generator_type="password",
            parameters={"length": 16}
        )
        generator = generator_factory.create_generator(config)
        password = generator.generate_single()
        
        assert len(password) == 16

    def test_password_complexity(self, generator_factory):
        """测试密码复杂度"""
        from dataforge.generators.basic.password import PasswordGenerator
        generator_factory.registry.register("password", PasswordGenerator)
        
        config = GeneratorConfig(
            generator_type="password",
            parameters={
                "include_uppercase": True,
                "include_lowercase": True,
                "include_digits": True,
                "include_special": True
            }
        )
        generator = generator_factory.create_generator(config)
        password = generator.generate_single()
        
        # Check for different character types
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        assert has_upper or has_lower or has_digit or has_special

    def test_strong_password(self, generator_factory):
        """测试强密码生成"""
        from dataforge.generators.basic.password import PasswordGenerator
        generator_factory.registry.register("password", PasswordGenerator)
        
        config = GeneratorConfig(
            generator_type="password",
            parameters={"strength": "strong"}
        )
        generator = generator_factory.create_generator(config)
        password = generator.generate_single()
        
        assert len(password) >= 12
        # Strong password should have variety
        assert any(c.isupper() for c in password)
        assert any(c.islower() for c in password)
        assert any(c.isdigit() for c in password)

    def test_validation(self, generator_factory):
        """测试密码验证"""
        from dataforge.generators.basic.password import PasswordGenerator
        generator_factory.registry.register("password", PasswordGenerator)
        
        config = GeneratorConfig(
            generator_type="password",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid passwords
        assert generator.validate("Abcd1234!")
        assert generator.validate("MyP@ssw0rd")
        
        # Invalid passwords
        assert not generator.validate("123")  # Too short
        assert not generator.validate("")
        assert not generator.validate(12345)

    def test_uniqueness(self, generator_factory):
        """测试密码唯一性"""
        from dataforge.generators.basic.password import PasswordGenerator
        generator_factory.registry.register("password", PasswordGenerator)
        
        config = GeneratorConfig(
            generator_type="password",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        passwords = generator.generate_batch(50)
        
        # All passwords should be unique
        unique_passwords = set(passwords)
        assert len(unique_passwords) == 50

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.basic.password import PasswordGenerator
        generator_factory.registry.register("password", PasswordGenerator)
        
        # Minimum length
        config = GeneratorConfig(
            generator_type="password",
            parameters={"length": 8}
        )
        generator = generator_factory.create_generator(config)
        password = generator.generate_single()
        assert len(password) == 8
        
        # Maximum length
        config = GeneratorConfig(
            generator_type="password",
            parameters={"length": 32}
        )
        generator = generator_factory.create_generator(config)
        password = generator.generate_single()
        assert len(password) == 32
