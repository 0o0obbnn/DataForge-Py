"""
批量生成性能测试
"""

import time

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.performance
class TestBatchPerformance:
    """批量生成性能测试类"""

    def test_batch_name_generation(self):
        """测试批量姓名生成性能"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        config = GeneratorConfig("name", {})
        generator = factory.create_generator(config)
        
        # 预热
        generator.generate_batch(10)
        
        # 性能测试
        batch_size = 1000
        start_time = time.time()
        names = generator.generate_batch(batch_size)
        end_time = time.time()
        
        elapsed = end_time - start_time
        avg_time = elapsed / batch_size * 1000
        
        print(f"\n批量姓名生成性能 (批量大小: {batch_size}):")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  平均时间: {avg_time:.3f}毫秒/条")
        print(f"  吞吐量: {batch_size/elapsed:.0f}条/秒")
        
        assert len(names) == batch_size
        assert elapsed < 10, f"批量生成太慢: {elapsed:.3f}秒 > 10秒"

    def test_batch_profile_generation(self):
        """测试批量用户档案生成性能"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        
        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "gender": factory.create_generator(GeneratorConfig("gender", {})),
        }
        
        # 预热
        for _ in range(10):
            {k: g.generate_single() for k, g in generators.items()}
        
        # 性能测试
        batch_size = 1000
        start_time = time.time()
        profiles = []
        for _ in range(batch_size):
            profile = {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
                "gender": generators["gender"].generate_single(),
            }
            profiles.append(profile)
        end_time = time.time()
        
        elapsed = end_time - start_time
        avg_time = elapsed / batch_size * 1000
        
        print(f"\n批量用户档案生成性能 (批量大小: {batch_size}):")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  平均时间: {avg_time:.3f}毫秒/条")
        print(f"  吞吐量: {batch_size/elapsed:.0f}条/秒")
        
        assert len(profiles) == batch_size
        assert elapsed < 15, f"批量生成太慢: {elapsed:.3f}秒 > 15秒"

    def test_large_batch_generation(self):
        """测试大批量生成性能"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        config = GeneratorConfig("name", {})
        generator = factory.create_generator(config)
        
        # 测试不同批量大小
        batch_sizes = [100, 500, 1000, 5000]
        
        for batch_size in batch_sizes:
            start_time = time.time()
            names = generator.generate_batch(batch_size)
            end_time = time.time()
            
            elapsed = end_time - start_time
            throughput = batch_size / elapsed
            
            print(f"\n批量大小 {batch_size}:")
            print(f"  时间: {elapsed:.3f}秒")
            print(f"  吞吐量: {throughput:.0f}条/秒")
            
            assert len(names) == batch_size

    def test_batch_id_generation(self):
        """测试批量身份证生成性能"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.identifier.id import IDGenerator
        registry.register("id", IDGenerator)
        
        config = GeneratorConfig("id", {})
        generator = factory.create_generator(config)
        
        # 预热
        generator.generate_batch(10)
        
        # 性能测试
        batch_size = 1000
        start_time = time.time()
        ids = generator.generate_batch(batch_size)
        end_time = time.time()
        
        elapsed = end_time - start_time
        avg_time = elapsed / batch_size * 1000
        
        print(f"\n批量身份证生成性能 (批量大小: {batch_size}):")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  平均时间: {avg_time:.3f}毫秒/条")
        print(f"  吞吐量: {batch_size/elapsed:.0f}条/秒")
        
        assert len(ids) == batch_size
        assert elapsed < 10, f"批量生成太慢: {elapsed:.3f}秒 > 10秒"

    def test_batch_email_generation(self):
        """测试批量邮箱生成性能"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.contact.email import EmailGenerator
        registry.register("email", EmailGenerator)
        
        config = GeneratorConfig("email", {})
        generator = factory.create_generator(config)
        
        # 预热
        generator.generate_batch(10)
        
        # 性能测试
        batch_size = 1000
        start_time = time.time()
        emails = generator.generate_batch(batch_size)
        end_time = time.time()
        
        elapsed = end_time - start_time
        avg_time = elapsed / batch_size * 1000
        
        print(f"\n批量邮箱生成性能 (批量大小: {batch_size}):")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  平均时间: {avg_time:.3f}毫秒/条")
        print(f"  吞吐量: {batch_size/elapsed:.0f}条/秒")
        
        assert len(emails) == batch_size
        assert elapsed < 10, f"批量生成太慢: {elapsed:.3f}秒 > 10秒"

    def test_batch_generation_scalability(self):
        """测试批量生成可扩展性"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.age import AgeGenerator
        registry.register("age", AgeGenerator)
        
        config = GeneratorConfig("age", {})
        generator = factory.create_generator(config)
        
        # 测试线性扩展性
        batch_sizes = [100, 200, 500, 1000]
        times = []
        
        for batch_size in batch_sizes:
            start_time = time.time()
            generator.generate_batch(batch_size)
            end_time = time.time()
            elapsed = end_time - start_time
            times.append(elapsed)
            
            print(f"\n批量大小 {batch_size}: {elapsed:.3f}秒")
        
        # 验证时间增长是线性的（允许一些误差）
        # 时间应该大致成比例增长
        ratio_1 = times[1] / times[0]  # 200/100
        ratio_2 = times[2] / times[1]  # 500/200
        
        print(f"\n扩展性比率:")
        print(f"  200/100: {ratio_1:.2f}")
        print(f"  500/200: {ratio_2:.2f}")
