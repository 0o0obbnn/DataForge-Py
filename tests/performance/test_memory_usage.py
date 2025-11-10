"""
内存使用测试
"""

import sys

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.performance
class TestMemoryUsage:
    """内存使用测试类"""

    def test_single_generator_memory(self):
        """测试单个生成器内存使用"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        config = GeneratorConfig("name", {})
        generator = factory.create_generator(config)
        
        # 生成数据
        names = [generator.generate_single() for _ in range(1000)]
        
        # 估算内存使用
        total_size = sum(sys.getsizeof(name) for name in names)
        avg_size = total_size / len(names)
        
        print(f"\n单个生成器内存使用:")
        print(f"  生成数量: {len(names)}")
        print(f"  总内存: {total_size/1024:.2f} KB")
        print(f"  平均每条: {avg_size:.2f} bytes")
        
        assert total_size < 1024 * 1024  # 应该小于1MB

    def test_batch_generation_memory(self):
        """测试批量生成内存使用"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        config = GeneratorConfig("name", {})
        generator = factory.create_generator(config)
        
        # 批量生成
        batch_size = 10000
        names = generator.generate_batch(batch_size)
        
        # 估算内存使用
        total_size = sum(sys.getsizeof(name) for name in names)
        avg_size = total_size / len(names)
        
        print(f"\n批量生成内存使用:")
        print(f"  批量大小: {batch_size}")
        print(f"  总内存: {total_size/1024:.2f} KB")
        print(f"  平均每条: {avg_size:.2f} bytes")
        
        assert total_size < 10 * 1024 * 1024  # 应该小于10MB

    def test_multiple_generators_memory(self):
        """测试多生成器内存使用"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        
        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        
        # 创建多个生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "gender": factory.create_generator(GeneratorConfig("gender", {})),
        }
        
        # 生成数据
        profiles = []
        for _ in range(1000):
            profile = {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
                "gender": generators["gender"].generate_single(),
            }
            profiles.append(profile)
        
        # 估算内存使用
        total_size = sum(sys.getsizeof(str(p)) for p in profiles)
        avg_size = total_size / len(profiles)
        
        print(f"\n多生成器内存使用:")
        print(f"  生成数量: {len(profiles)}")
        print(f"  总内存: {total_size/1024:.2f} KB")
        print(f"  平均每条: {avg_size:.2f} bytes")

    def test_large_batch_memory(self):
        """测试大批量内存使用"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.age import AgeGenerator
        registry.register("age", AgeGenerator)
        
        config = GeneratorConfig("age", {})
        generator = factory.create_generator(config)
        
        # 测试不同批量大小
        batch_sizes = [1000, 5000, 10000]
        
        for batch_size in batch_sizes:
            ages = generator.generate_batch(batch_size)
            total_size = sum(sys.getsizeof(age) for age in ages)
            
            print(f"\n批量大小 {batch_size}:")
            print(f"  总内存: {total_size/1024:.2f} KB")
            print(f"  平均每条: {total_size/batch_size:.2f} bytes")

    def test_generator_instance_memory(self):
        """测试生成器实例内存"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        config = GeneratorConfig("name", {})
        
        # 创建多个生成器实例
        generators = [factory.create_generator(config) for _ in range(100)]
        
        # 估算生成器实例内存
        total_size = sum(sys.getsizeof(gen) for gen in generators)
        avg_size = total_size / len(generators)
        
        print(f"\n生成器实例内存:")
        print(f"  实例数量: {len(generators)}")
        print(f"  总内存: {total_size/1024:.2f} KB")
        print(f"  平均每个: {avg_size:.2f} bytes")
