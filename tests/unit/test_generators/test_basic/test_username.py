"""
用户名生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestUsernameGenerator:
    """用户名生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个用户名"""
        from dataforge.generators.basic.username import UsernameGenerator

        generator_factory.registry.register("username", UsernameGenerator)

        config = GeneratorConfig(generator_type="username", parameters={})
        generator = generator_factory.create_generator(config)
        username = generator.generate_single()

        assert isinstance(username, str)
        assert len(username) >= 3
        assert generator.validate(username)

    def test_generate_batch(self, generator_factory):
        """测试批量生成用户名"""
        from dataforge.generators.basic.username import UsernameGenerator

        generator_factory.registry.register("username", UsernameGenerator)

        config = GeneratorConfig(generator_type="username", parameters={})
        generator = generator_factory.create_generator(config)
        usernames = generator.generate_batch(10)

        assert len(usernames) == 10
        for username in usernames:
            assert isinstance(username, str)
            assert len(username) >= 3

    def test_username_length(self, generator_factory):
        """测试指定用户名长度"""
        from dataforge.generators.basic.username import UsernameGenerator

        generator_factory.registry.register("username", UsernameGenerator)

        config = GeneratorConfig(
            generator_type="username", parameters={"min_length": 5, "max_length": 10}
        )
        generator = generator_factory.create_generator(config)
        username = generator.generate_single()

        assert 5 <= len(username) <= 10

    def test_alphanumeric_username(self, generator_factory):
        """测试字母数字用户名"""
        from dataforge.generators.basic.username import UsernameGenerator

        generator_factory.registry.register("username", UsernameGenerator)

        config = GeneratorConfig(
            generator_type="username", parameters={"format": "alphanumeric"}
        )
        generator = generator_factory.create_generator(config)
        username = generator.generate_single()

        # Should only contain letters and numbers
        assert username.replace("_", "").replace("-", "").isalnum()

    def test_with_prefix(self, generator_factory):
        """测试带前缀的用户名"""
        from dataforge.generators.basic.username import UsernameGenerator

        generator_factory.registry.register("username", UsernameGenerator)

        config = GeneratorConfig(
            generator_type="username", parameters={"prefix": "user_"}
        )
        generator = generator_factory.create_generator(config)
        username = generator.generate_single()

        assert username.startswith("user_")

    def test_validation(self, generator_factory):
        """测试用户名验证"""
        from dataforge.generators.basic.username import UsernameGenerator

        generator_factory.registry.register("username", UsernameGenerator)

        config = GeneratorConfig(generator_type="username", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid usernames
        assert generator.validate("john_doe")
        assert generator.validate("user123")
        assert generator.validate("test-user")

        # Invalid usernames
        assert not generator.validate("ab")  # Too short
        assert not generator.validate("")
        assert not generator.validate("user name")  # Space
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试用户名唯一性"""
        from dataforge.generators.basic.username import UsernameGenerator

        generator_factory.registry.register("username", UsernameGenerator)

        config = GeneratorConfig(generator_type="username", parameters={})
        generator = generator_factory.create_generator(config)
        usernames = generator.generate_batch(50)

        # Should have high uniqueness
        unique_usernames = set(usernames)
        assert len(unique_usernames) >= 45

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.basic.username import UsernameGenerator

        generator_factory.registry.register("username", UsernameGenerator)

        # Minimum length
        config = GeneratorConfig(
            generator_type="username", parameters={"min_length": 3, "max_length": 3}
        )
        generator = generator_factory.create_generator(config)
        username = generator.generate_single()
        assert len(username) == 3
