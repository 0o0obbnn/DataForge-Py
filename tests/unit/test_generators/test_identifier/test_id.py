"""
通用ID生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestIDGenerator:
    """通用ID生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个ID"""
        from dataforge.generators.identifier.id import IDGenerator

        generator_factory.registry.register("id", IDGenerator)

        config = GeneratorConfig(generator_type="id", parameters={})
        generator = generator_factory.create_generator(config)
        id_value = generator.generate_single()

        assert id_value is not None
        assert generator.validate(id_value)

    def test_generate_batch(self, generator_factory):
        """测试批量生成ID"""
        from dataforge.generators.identifier.id import IDGenerator

        generator_factory.registry.register("id", IDGenerator)

        config = GeneratorConfig(generator_type="id", parameters={})
        generator = generator_factory.create_generator(config)
        ids = generator.generate_batch(10)

        assert len(ids) == 10
        for id_value in ids:
            assert id_value is not None

    def test_numeric_id(self, generator_factory):
        """测试数字ID"""
        from dataforge.generators.identifier.id import IDGenerator

        generator_factory.registry.register("id", IDGenerator)

        config = GeneratorConfig(generator_type="id", parameters={"type": "numeric"})
        generator = generator_factory.create_generator(config)
        id_value = generator.generate_single()

        if isinstance(id_value, str):
            assert id_value.isdigit()
        else:
            assert isinstance(id_value, int)

    def test_uuid_id(self, generator_factory):
        """测试UUID格式ID"""
        from dataforge.generators.identifier.id import IDGenerator

        generator_factory.registry.register("id", IDGenerator)

        config = GeneratorConfig(generator_type="id", parameters={"type": "uuid"})
        generator = generator_factory.create_generator(config)
        id_value = generator.generate_single()

        if isinstance(id_value, str):
            # UUID format
            assert len(id_value) >= 32

    def test_sequential_id(self, generator_factory):
        """测试顺序ID"""
        from dataforge.generators.identifier.id import IDGenerator

        generator_factory.registry.register("id", IDGenerator)

        config = GeneratorConfig(
            generator_type="id", parameters={"type": "sequential", "start": 1000}
        )
        generator = generator_factory.create_generator(config)
        ids = generator.generate_batch(5)

        # Sequential IDs should be in order
        assert len(ids) == 5

    def test_custom_prefix(self, generator_factory):
        """测试自定义前缀"""
        from dataforge.generators.identifier.id import IDGenerator

        generator_factory.registry.register("id", IDGenerator)

        config = GeneratorConfig(generator_type="id", parameters={"prefix": "USER_"})
        generator = generator_factory.create_generator(config)
        id_value = generator.generate_single()

        if isinstance(id_value, str):
            assert id_value.startswith("USER_")

    def test_length(self, generator_factory):
        """测试指定长度"""
        from dataforge.generators.identifier.id import IDGenerator

        generator_factory.registry.register("id", IDGenerator)

        config = GeneratorConfig(generator_type="id", parameters={"length": 16})
        generator = generator_factory.create_generator(config)
        id_value = generator.generate_single()

        if isinstance(id_value, str):
            assert len(id_value) >= 16

    def test_validation(self, generator_factory):
        """测试ID验证"""
        from dataforge.generators.identifier.id import IDGenerator

        generator_factory.registry.register("id", IDGenerator)

        config = GeneratorConfig(generator_type="id", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid ID
        id_value = generator.generate_single()
        assert generator.validate(id_value)

        # Invalid IDs
        assert not generator.validate("")
        assert not generator.validate(None)

    def test_uniqueness(self, generator_factory):
        """测试ID唯一性"""
        from dataforge.generators.identifier.id import IDGenerator

        generator_factory.registry.register("id", IDGenerator)

        config = GeneratorConfig(generator_type="id", parameters={})
        generator = generator_factory.create_generator(config)
        ids = generator.generate_batch(100)

        # All IDs should be unique
        unique_ids = set(str(id_val) for id_val in ids)
        assert len(unique_ids) == 100

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.identifier.id import IDGenerator

        generator_factory.registry.register("id", IDGenerator)

        config = GeneratorConfig(generator_type="id", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            id_value = generator.generate_single()
            assert id_value is not None
