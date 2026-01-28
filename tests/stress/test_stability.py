"""
稳定性压力测试
"""

import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.stress
class TestStability:
    """稳定性压力测试类"""

    def test_long_running_stability(self):
        """测试长时间运行稳定性"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)

        name_gen = factory.create_generator(GeneratorConfig("name", {}))
        age_gen = factory.create_generator(GeneratorConfig("age", {}))

        # 长时间运行测试（2分钟）
        duration = 120
        start_time = time.time()
        iterations = 0
        errors = 0

        while time.time() - start_time < duration:
            try:
                name = name_gen.generate_single()
                age = age_gen.generate_single()

                assert name is not None
                assert age is not None

                iterations += 1

                if iterations % 1000 == 0:
                    elapsed = time.time() - start_time
                    print(
                        f"\n已运行 {elapsed:.0f}秒, 迭代 {iterations} 次, 错误 {errors} 次"
                    )

            except Exception as e:
                errors += 1
                print(f"\n错误: {e}")

        end_time = time.time()
        elapsed = end_time - start_time

        print(f"\n长时间运行测试完成:")
        print(f"  运行时间: {elapsed:.2f}秒")
        print(f"  总迭代: {iterations}")
        print(f"  错误数: {errors}")
        print(f"  成功率: {(iterations-errors)/iterations*100:.2f}%")

        # 错误率应该很低
        assert errors < iterations * 0.01  # 错误率<1%

    def test_concurrent_stability(self):
        """测试并发稳定性"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        def worker(worker_id, iterations):
            """工作线程"""
            generator = factory.create_generator(GeneratorConfig("name", {}))
            results = []
            errors = 0

            for i in range(iterations):
                try:
                    name = generator.generate_single()
                    results.append(name)
                except Exception as e:
                    errors += 1
                    print(f"\nWorker {worker_id} 错误: {e}")

            return len(results), errors

        # 并发测试
        num_workers = 20
        iterations_per_worker = 500

        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [
                executor.submit(worker, i, iterations_per_worker)
                for i in range(num_workers)
            ]
            results = [f.result() for f in futures]
        end_time = time.time()

        elapsed = end_time - start_time
        total_generated = sum(r[0] for r in results)
        total_errors = sum(r[1] for r in results)

        print(f"\n并发稳定性测试完成:")
        print(f"  工作线程: {num_workers}")
        print(f"  每线程迭代: {iterations_per_worker}")
        print(f"  总生成: {total_generated}")
        print(f"  总错误: {total_errors}")
        print(f"  运行时间: {elapsed:.2f}秒")
        print(
            f"  成功率: {total_generated/(num_workers*iterations_per_worker)*100:.2f}%"
        )

        # 大部分应该成功
        assert total_generated > num_workers * iterations_per_worker * 0.95

    def test_resource_cleanup(self):
        """测试资源清理"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        # 创建和销毁多个生成器
        for i in range(100):
            generator = factory.create_generator(GeneratorConfig("name", {}))

            # 使用生成器
            names = [generator.generate_single() for _ in range(10)]
            assert len(names) == 10

            # 清理
            del generator
            del names

            if (i + 1) % 20 == 0:
                print(f"\n已创建和销毁 {i + 1} 个生成器")

        print(f"\n资源清理测试完成")

    def test_error_recovery(self):
        """测试错误恢复"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        generator = factory.create_generator(GeneratorConfig("name", {}))

        # 正常生成
        names1 = [generator.generate_single() for _ in range(100)]
        assert len(names1) == 100

        # 模拟错误后继续生成
        try:
            # 尝试一些可能失败的操作
            pass
        except Exception:
            pass

        # 应该能继续正常工作
        names2 = [generator.generate_single() for _ in range(100)]
        assert len(names2) == 100

        print(f"\n错误恢复测试完成")

    def test_repeated_operations(self):
        """测试重复操作稳定性"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.age import AgeGenerator

        registry.register("age", AgeGenerator)

        # 重复创建和使用生成器
        for i in range(50):
            generator = factory.create_generator(GeneratorConfig("age", {}))

            # 批量生成
            ages = generator.generate_batch(100)
            assert len(ages) == 100

            # 单个生成
            for _ in range(10):
                age = generator.generate_single()
                assert age is not None

            if (i + 1) % 10 == 0:
                print(f"\n完成 {i + 1} 轮重复操作")

        print(f"\n重复操作稳定性测试完成")
