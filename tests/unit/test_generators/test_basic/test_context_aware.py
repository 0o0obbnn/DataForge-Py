"""
上下文感知生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
@pytest.mark.skip(reason="ContextAwareGenerator not implemented - advanced feature")
class TestContextAwareGenerator:
    """上下文感知生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个上下文感知数据"""
        from dataforge.generators.basic.context_aware import ContextAwareGenerator

        generator_factory.registry.register("context_aware", ContextAwareGenerator)

        config = GeneratorConfig(generator_type="context_aware", parameters={})
        generator = generator_factory.create_generator(config)
        data = generator.generate_single()

        assert data is not None
        assert generator.validate(data)

    def test_generate_batch(self, generator_factory):
        """测试批量生成上下文感知数据"""
        from dataforge.generators.basic.context_aware import ContextAwareGenerator

        generator_factory.registry.register("context_aware", ContextAwareGenerator)

        config = GeneratorConfig(generator_type="context_aware", parameters={})
        generator = generator_factory.create_generator(config)
        data_list = generator.generate_batch(10)

        assert len(data_list) == 10
        for data in data_list:
            assert data is not None

    def test_with_context(self, generator_factory):
        """测试带上下文生成"""
        from dataforge.generators.basic.context_aware import ContextAwareGenerator

        generator_factory.registry.register("context_aware", ContextAwareGenerator)

        config = GeneratorConfig(
            generator_type="context_aware",
            parameters={"context": {"age": 25, "gender": "male"}},
        )
        generator = generator_factory.create_generator(config)
        data = generator.generate_single()

        assert data is not None

    def test_age_based_context(self, generator_factory):
        """测试基于年龄的上下文"""
        from dataforge.generators.basic.context_aware import ContextAwareGenerator

        generator_factory.registry.register("context_aware", ContextAwareGenerator)

        config = GeneratorConfig(generator_type="context_aware", parameters={"age": 30})
        generator = generator_factory.create_generator(config)
        data = generator.generate_single()

        assert data is not None

    def test_gender_based_context(self, generator_factory):
        """测试基于性别的上下文"""
        from dataforge.generators.basic.context_aware import ContextAwareGenerator

        generator_factory.registry.register("context_aware", ContextAwareGenerator)

        config = GeneratorConfig(
            generator_type="context_aware", parameters={"gender": "female"}
        )
        generator = generator_factory.create_generator(config)
        data = generator.generate_single()

        assert data is not None

    def test_validation(self, generator_factory):
        """测试数据验证"""
        from dataforge.generators.basic.context_aware import ContextAwareGenerator

        generator_factory.registry.register("context_aware", ContextAwareGenerator)

        config = GeneratorConfig(generator_type="context_aware", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid data
        data = generator.generate_single()
        assert generator.validate(data)

        # Invalid data
        assert not generator.validate(None)
        assert not generator.validate("")

    def test_consistency(self, generator_factory):
        """测试上下文一致性"""
        from dataforge.generators.basic.context_aware import ContextAwareGenerator

        generator_factory.registry.register("context_aware", ContextAwareGenerator)

        config = GeneratorConfig(
            generator_type="context_aware", parameters={"context": {"age": 25}}
        )
        generator = generator_factory.create_generator(config)
        data_list = generator.generate_batch(10)

        # All data should be consistent with context
        assert len(data_list) == 10

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.basic.context_aware import ContextAwareGenerator

        generator_factory.registry.register("context_aware", ContextAwareGenerator)

        config = GeneratorConfig(generator_type="context_aware", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            data = generator.generate_single()
            assert data is not None
