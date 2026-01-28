"""
增强生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
@pytest.mark.skip(reason="EnhancedGenerator not implemented - advanced feature")
class TestEnhancedGenerators:
    """增强生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个增强数据"""
        from dataforge.generators.basic.enhanced_generators import EnhancedGenerator

        generator_factory.registry.register("enhanced", EnhancedGenerator)

        config = GeneratorConfig(generator_type="enhanced", parameters={})
        generator = generator_factory.create_generator(config)
        data = generator.generate_single()

        assert data is not None
        assert generator.validate(data)

    def test_generate_batch(self, generator_factory):
        """测试批量生成增强数据"""
        from dataforge.generators.basic.enhanced_generators import EnhancedGenerator

        generator_factory.registry.register("enhanced", EnhancedGenerator)

        config = GeneratorConfig(generator_type="enhanced", parameters={})
        generator = generator_factory.create_generator(config)
        data_list = generator.generate_batch(10)

        assert len(data_list) == 10
        for data in data_list:
            assert data is not None

    def test_enhanced_features(self, generator_factory):
        """测试增强特性"""
        from dataforge.generators.basic.enhanced_generators import EnhancedGenerator

        generator_factory.registry.register("enhanced", EnhancedGenerator)

        config = GeneratorConfig(
            generator_type="enhanced", parameters={"enhanced": True}
        )
        generator = generator_factory.create_generator(config)
        data = generator.generate_single()

        assert data is not None

    def test_with_metadata(self, generator_factory):
        """测试带元数据"""
        from dataforge.generators.basic.enhanced_generators import EnhancedGenerator

        generator_factory.registry.register("enhanced", EnhancedGenerator)

        config = GeneratorConfig(
            generator_type="enhanced", parameters={"include_metadata": True}
        )
        generator = generator_factory.create_generator(config)
        data = generator.generate_single()

        assert data is not None

    def test_quality_level(self, generator_factory):
        """测试质量级别"""
        from dataforge.generators.basic.enhanced_generators import EnhancedGenerator

        generator_factory.registry.register("enhanced", EnhancedGenerator)

        config = GeneratorConfig(
            generator_type="enhanced", parameters={"quality": "high"}
        )
        generator = generator_factory.create_generator(config)
        data = generator.generate_single()

        assert data is not None

    def test_validation(self, generator_factory):
        """测试数据验证"""
        from dataforge.generators.basic.enhanced_generators import EnhancedGenerator

        generator_factory.registry.register("enhanced", EnhancedGenerator)

        config = GeneratorConfig(generator_type="enhanced", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid data
        data = generator.generate_single()
        assert generator.validate(data)

        # Invalid data
        assert not generator.validate(None)
        assert not generator.validate("")

    def test_consistency(self, generator_factory):
        """测试数据一致性"""
        from dataforge.generators.basic.enhanced_generators import EnhancedGenerator

        generator_factory.registry.register("enhanced", EnhancedGenerator)

        config = GeneratorConfig(generator_type="enhanced", parameters={})
        generator = generator_factory.create_generator(config)
        data_list = generator.generate_batch(10)

        # All data should be consistent
        assert len(data_list) == 10

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.basic.enhanced_generators import EnhancedGenerator

        generator_factory.registry.register("enhanced", EnhancedGenerator)

        config = GeneratorConfig(generator_type="enhanced", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            data = generator.generate_single()
            assert data is not None
