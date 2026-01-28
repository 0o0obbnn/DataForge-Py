"""
优化姓名生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
@pytest.mark.skip(reason="NameOptimizedGenerator not implemented - advanced feature")
class TestNameOptimizedGenerator:
    """优化姓名生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个优化姓名"""
        from dataforge.generators.basic.name_optimized import NameOptimizedGenerator

        generator_factory.registry.register("name_optimized", NameOptimizedGenerator)

        config = GeneratorConfig(generator_type="name_optimized", parameters={})
        generator = generator_factory.create_generator(config)
        name = generator.generate_single()

        assert isinstance(name, str)
        assert 2 <= len(name) <= 4
        assert generator.validate(name)

    def test_generate_batch(self, generator_factory):
        """测试批量生成优化姓名"""
        from dataforge.generators.basic.name_optimized import NameOptimizedGenerator

        generator_factory.registry.register("name_optimized", NameOptimizedGenerator)

        config = GeneratorConfig(generator_type="name_optimized", parameters={})
        generator = generator_factory.create_generator(config)
        names = generator.generate_batch(10)

        assert len(names) == 10
        for name in names:
            assert isinstance(name, str)
            assert 2 <= len(name) <= 4

    def test_performance_optimization(self, generator_factory):
        """测试性能优化"""
        from dataforge.generators.basic.name_optimized import NameOptimizedGenerator

        generator_factory.registry.register("name_optimized", NameOptimizedGenerator)

        config = GeneratorConfig(generator_type="name_optimized", parameters={})
        generator = generator_factory.create_generator(config)

        # Should generate quickly
        import time

        start = time.time()
        names = generator.generate_batch(100)
        duration = time.time() - start

        assert len(names) == 100
        assert duration < 1.0  # Should be fast

    def test_with_cache(self, generator_factory):
        """测试缓存功能"""
        from dataforge.generators.basic.name_optimized import NameOptimizedGenerator

        generator_factory.registry.register("name_optimized", NameOptimizedGenerator)

        config = GeneratorConfig(
            generator_type="name_optimized", parameters={"use_cache": True}
        )
        generator = generator_factory.create_generator(config)
        name = generator.generate_single()

        assert isinstance(name, str)

    def test_male_name(self, generator_factory):
        """测试生成男性姓名"""
        from dataforge.generators.basic.name_optimized import NameOptimizedGenerator

        generator_factory.registry.register("name_optimized", NameOptimizedGenerator)

        config = GeneratorConfig(
            generator_type="name_optimized", parameters={"gender": "male"}
        )
        generator = generator_factory.create_generator(config)
        name = generator.generate_single()

        assert isinstance(name, str)
        assert 2 <= len(name) <= 4

    def test_female_name(self, generator_factory):
        """测试生成女性姓名"""
        from dataforge.generators.basic.name_optimized import NameOptimizedGenerator

        generator_factory.registry.register("name_optimized", NameOptimizedGenerator)

        config = GeneratorConfig(
            generator_type="name_optimized", parameters={"gender": "female"}
        )
        generator = generator_factory.create_generator(config)
        name = generator.generate_single()

        assert isinstance(name, str)
        assert 2 <= len(name) <= 4

    def test_validation(self, generator_factory):
        """测试姓名验证"""
        from dataforge.generators.basic.name_optimized import NameOptimizedGenerator

        generator_factory.registry.register("name_optimized", NameOptimizedGenerator)

        config = GeneratorConfig(generator_type="name_optimized", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid names
        assert generator.validate("张三")
        assert generator.validate("李四")

        # Invalid names
        assert not generator.validate("")
        assert not generator.validate("A")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试姓名唯一性"""
        from dataforge.generators.basic.name_optimized import NameOptimizedGenerator

        generator_factory.registry.register("name_optimized", NameOptimizedGenerator)

        config = GeneratorConfig(generator_type="name_optimized", parameters={})
        generator = generator_factory.create_generator(config)
        names = generator.generate_batch(50)

        # Should have variety
        unique_names = set(names)
        assert len(unique_names) > 20

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.basic.name_optimized import NameOptimizedGenerator

        generator_factory.registry.register("name_optimized", NameOptimizedGenerator)

        config = GeneratorConfig(generator_type="name_optimized", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            name = generator.generate_single()
            assert name is not None
            assert 2 <= len(name) <= 4
            assert all("\u4e00" <= char <= "\u9fff" for char in name)
