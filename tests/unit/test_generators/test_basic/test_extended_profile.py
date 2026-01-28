"""
扩展档案生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
@pytest.mark.skip(reason="ExtendedProfileGenerator not implemented - advanced feature")
class TestExtendedProfileGenerator:
    """扩展档案生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个扩展档案"""
        from dataforge.generators.basic.extended_profile import ExtendedProfileGenerator

        generator_factory.registry.register(
            "extended_profile", ExtendedProfileGenerator
        )

        config = GeneratorConfig(generator_type="extended_profile", parameters={})
        generator = generator_factory.create_generator(config)
        profile = generator.generate_single()

        assert profile is not None
        assert generator.validate(profile)

    def test_generate_batch(self, generator_factory):
        """测试批量生成扩展档案"""
        from dataforge.generators.basic.extended_profile import ExtendedProfileGenerator

        generator_factory.registry.register(
            "extended_profile", ExtendedProfileGenerator
        )

        config = GeneratorConfig(generator_type="extended_profile", parameters={})
        generator = generator_factory.create_generator(config)
        profiles = generator.generate_batch(10)

        assert len(profiles) == 10
        for profile in profiles:
            assert profile is not None

    def test_complete_profile(self, generator_factory):
        """测试完整档案"""
        from dataforge.generators.basic.extended_profile import ExtendedProfileGenerator

        generator_factory.registry.register(
            "extended_profile", ExtendedProfileGenerator
        )

        config = GeneratorConfig(
            generator_type="extended_profile", parameters={"completeness": "full"}
        )
        generator = generator_factory.create_generator(config)
        profile = generator.generate_single()

        # Full profile should have multiple fields
        assert profile is not None

    def test_basic_profile(self, generator_factory):
        """测试基础档案"""
        from dataforge.generators.basic.extended_profile import ExtendedProfileGenerator

        generator_factory.registry.register(
            "extended_profile", ExtendedProfileGenerator
        )

        config = GeneratorConfig(
            generator_type="extended_profile", parameters={"completeness": "basic"}
        )
        generator = generator_factory.create_generator(config)
        profile = generator.generate_single()

        assert profile is not None

    def test_with_demographics(self, generator_factory):
        """测试带人口统计信息"""
        from dataforge.generators.basic.extended_profile import ExtendedProfileGenerator

        generator_factory.registry.register(
            "extended_profile", ExtendedProfileGenerator
        )

        config = GeneratorConfig(
            generator_type="extended_profile", parameters={"include_demographics": True}
        )
        generator = generator_factory.create_generator(config)
        profile = generator.generate_single()

        assert profile is not None

    def test_with_contact_info(self, generator_factory):
        """测试带联系信息"""
        from dataforge.generators.basic.extended_profile import ExtendedProfileGenerator

        generator_factory.registry.register(
            "extended_profile", ExtendedProfileGenerator
        )

        config = GeneratorConfig(
            generator_type="extended_profile", parameters={"include_contact": True}
        )
        generator = generator_factory.create_generator(config)
        profile = generator.generate_single()

        assert profile is not None

    def test_validation(self, generator_factory):
        """测试档案验证"""
        from dataforge.generators.basic.extended_profile import ExtendedProfileGenerator

        generator_factory.registry.register(
            "extended_profile", ExtendedProfileGenerator
        )

        config = GeneratorConfig(generator_type="extended_profile", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid profile
        profile = generator.generate_single()
        assert generator.validate(profile)

        # Invalid profiles
        assert not generator.validate(None)
        assert not generator.validate("")

    def test_consistency(self, generator_factory):
        """测试档案一致性"""
        from dataforge.generators.basic.extended_profile import ExtendedProfileGenerator

        generator_factory.registry.register(
            "extended_profile", ExtendedProfileGenerator
        )

        config = GeneratorConfig(generator_type="extended_profile", parameters={})
        generator = generator_factory.create_generator(config)
        profile = generator.generate_single()

        # Profile fields should be consistent
        assert profile is not None

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.basic.extended_profile import ExtendedProfileGenerator

        generator_factory.registry.register(
            "extended_profile", ExtendedProfileGenerator
        )

        config = GeneratorConfig(generator_type="extended_profile", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            profile = generator.generate_single()
            assert profile is not None
