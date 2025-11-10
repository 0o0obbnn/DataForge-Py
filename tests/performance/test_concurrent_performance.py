"""
并发性能测试
"""

import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.performance
class TestConcurrentPerformance:
    """并发性能测试类"""

    def test_concurrent_name_generation(self):
        """测试并发姓名生成"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        config = GeneratorConfig("name", {})
        
        def generate_names(n):
            generator = factory.create_generator(config)
            return [generator.generate_single() for _ in range(n)]
        
        # 并发测试
        num_threads = 10
        items_per_thread = 100
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(generate_names, items_per_thread) for _ in range(num_threads)]
            results = [f.result() for f in futures]
        end_time = time.time()
        
        elapsed = end_time - start_time
        total_items = num_threads * items_per_thread
        
        print(f"\n并发姓名生成性能:")
        print(f"  线程数: {num_threads}")
        print(f"  每线程生成: {items_per_thread}条")
        print(f"  总生成: {total_items}条")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  吞吐量: {total_items/elapsed:.0f}条/秒")
        
        assert len(results) == num_threads
        assert all(len(r) == items_per_thread for r in results)

    def test_concurrent_multiple_generators(self):
        """测试并发多生成器"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        
        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        
        def generate_profile(n):
            name_gen = factory.create_generator(GeneratorConfig("name", {}))
            age_gen = factory.create_generator(GeneratorConfig("age", {}))
            gender_gen = factory.create_generator(GeneratorConfig("gender", {}))
            
            profiles = []
            for _ in range(n):
                profile = {
                    "name": name_gen.generate_single(),
                    "age": age_gen.generate_single(),
                    "gender": gender_gen.generate_single(),
                }
                profiles.append(profile)
            return profiles
        
        # 并发测试
        num_threads = 10
        items_per_thread = 50
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(generate_profile, items_per_thread) for _ in range(num_threads)]
            results = [f.result() for f in futures]
        end_time = time.time()
        
        elapsed = end_time - start_time
        total_items = num_threads * items_per_thread
        
        print(f"\n并发多生成器性能:")
        print(f"  线程数: {num_threads}")
        print(f"  每线程生成: {items_per_thread}条")
        print(f"  总生成: {total_items}条")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  吞吐量: {total_items/elapsed:.0f}条/秒")
        
        assert len(results) == num_threads

    def test_concurrent_scalability(self):
        """测试并发可扩展性"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.age import AgeGenerator
        registry.register("age", AgeGenerator)
        
        config = GeneratorConfig("age", {})
        
        def generate_ages(n):
            generator = factory.create_generator(config)
            return [generator.generate_single() for _ in range(n)]
        
        # 测试不同线程数
        thread_counts = [1, 2, 5, 10]
        items_per_thread = 100
        
        for num_threads in thread_counts:
            start_time = time.time()
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [executor.submit(generate_ages, items_per_thread) for _ in range(num_threads)]
                results = [f.result() for f in futures]
            end_time = time.time()
            
            elapsed = end_time - start_time
            total_items = num_threads * items_per_thread
            throughput = total_items / elapsed
            
            print(f"\n线程数 {num_threads}:")
            print(f"  时间: {elapsed:.3f}秒")
            print(f"  吞吐量: {throughput:.0f}条/秒")

    def test_concurrent_id_generation(self):
        """测试并发身份证生成"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.identifier.id import IDGenerator
        registry.register("id", IDGenerator)
        
        config = GeneratorConfig("id", {})
        
        def generate_ids(n):
            generator = factory.create_generator(config)
            return [generator.generate_single() for _ in range(n)]
        
        # 并发测试
        num_threads = 10
        items_per_thread = 100
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(generate_ids, items_per_thread) for _ in range(num_threads)]
            results = [f.result() for f in futures]
        end_time = time.time()
        
        elapsed = end_time - start_time
        total_items = num_threads * items_per_thread
        
        print(f"\n并发身份证生成性能:")
        print(f"  线程数: {num_threads}")
        print(f"  每线程生成: {items_per_thread}条")
        print(f"  总生成: {total_items}条")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  吞吐量: {total_items/elapsed:.0f}条/秒")
        
        # 验证唯一性
        all_ids = [id for result in results for id in result]
        unique_ids = set(all_ids)
        print(f"  唯一性: {len(unique_ids)}/{len(all_ids)}")

    def test_concurrent_stress(self):
        """测试并发压力"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        config = GeneratorConfig("name", {})
        
        def generate_names(n):
            generator = factory.create_generator(config)
            return [generator.generate_single() for _ in range(n)]
        
        # 高并发测试
        num_threads = 50
        items_per_thread = 20
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(generate_names, items_per_thread) for _ in range(num_threads)]
            results = [f.result() for f in futures]
        end_time = time.time()
        
        elapsed = end_time - start_time
        total_items = num_threads * items_per_thread
        
        print(f"\n并发压力测试:")
        print(f"  线程数: {num_threads}")
        print(f"  每线程生成: {items_per_thread}条")
        print(f"  总生成: {total_items}条")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  吞吐量: {total_items/elapsed:.0f}条/秒")
        
        assert len(results) == num_threads
        assert all(len(r) == items_per_thread for r in results)
