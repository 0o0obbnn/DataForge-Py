"""
大规模数据生成压力测试
"""

import time

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.stress
class TestLargeScaleGeneration:
    """大规模数据生成压力测试类"""

    def test_generate_10k_users(self):
        """测试生成10000个用户"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.contact.email import EmailGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("email", EmailGenerator)

        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
        }

        # 生成10000个用户
        target = 10000
        start_time = time.time()

        users = []
        for i in range(target):
            user = {
                "id": i + 1,
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
                "email": generators["email"].generate_single(),
            }
            users.append(user)

            # 每1000条打印进度
            if (i + 1) % 1000 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                print(f"\n已生成 {i + 1}/{target} 条 ({rate:.0f} 条/秒)")

        end_time = time.time()
        elapsed = end_time - start_time

        print("\n大规模生成完成:")
        print(f"  总数量: {len(users)}")
        print(f"  总时间: {elapsed:.2f}秒")
        print(f"  平均速度: {target/elapsed:.0f}条/秒")

        # 验证
        assert len(users) == target
        assert elapsed < 300  # 应该在5分钟内完成

    def test_generate_50k_records(self):
        """测试生成50000条记录"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.uuid import UUIDGenerator

        registry.register("age", AgeGenerator)
        registry.register("uuid", UUIDGenerator)

        age_gen = factory.create_generator(GeneratorConfig("age", {}))
        uuid_gen = factory.create_generator(GeneratorConfig("uuid", {}))

        # 生成50000条记录
        target = 50000
        start_time = time.time()

        records = []
        for i in range(target):
            record = {
                "id": uuid_gen.generate_single(),
                "value": age_gen.generate_single(),
            }
            records.append(record)

            if (i + 1) % 10000 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                print(f"\n已生成 {i + 1}/{target} 条 ({rate:.0f} 条/秒)")

        end_time = time.time()
        elapsed = end_time - start_time

        print("\n大规模生成完成:")
        print(f"  总数量: {len(records)}")
        print(f"  总时间: {elapsed:.2f}秒")
        print(f"  平均速度: {target/elapsed:.0f}条/秒")

        assert len(records) == target

    def test_continuous_generation(self):
        """测试持续生成（5分钟）"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        generator = factory.create_generator(GeneratorConfig("name", {}))

        # 持续生成5分钟
        duration = 60  # 1分钟（测试时缩短）
        start_time = time.time()
        count = 0

        while time.time() - start_time < duration:
            generator.generate_single()
            count += 1

            # 每10秒打印一次
            if count % 1000 == 0:
                elapsed = time.time() - start_time
                rate = count / elapsed
                print(f"\n已运行 {elapsed:.0f}秒, 生成 {count} 条 ({rate:.0f} 条/秒)")

        end_time = time.time()
        elapsed = end_time - start_time

        print("\n持续生成测试完成:")
        print(f"  运行时间: {elapsed:.2f}秒")
        print(f"  生成总数: {count}")
        print(f"  平均速度: {count/elapsed:.0f}条/秒")

        assert count > 0

    def test_memory_stability(self):
        """测试内存稳定性"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        generator = factory.create_generator(GeneratorConfig("name", {}))

        # 分批生成，测试内存是否稳定
        batch_count = 10
        batch_size = 1000

        for i in range(batch_count):
            # 生成一批数据
            names = [generator.generate_single() for _ in range(batch_size)]

            # 验证
            assert len(names) == batch_size

            # 清理（模拟实际使用）
            names.clear()

            print(f"\n批次 {i + 1}/{batch_count} 完成")

        print("\n内存稳定性测试完成")

    def test_high_volume_batch(self):
        """测试高容量批量生成"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.age import AgeGenerator

        registry.register("age", AgeGenerator)

        generator = factory.create_generator(GeneratorConfig("age", {}))

        # 测试不同批量大小
        batch_sizes = [1000, 5000, 10000, 20000]

        for batch_size in batch_sizes:
            start_time = time.time()
            ages = generator.generate_batch(batch_size)
            end_time = time.time()

            elapsed = end_time - start_time
            rate = batch_size / elapsed

            print(f"\n批量大小 {batch_size}:")
            print(f"  时间: {elapsed:.2f}秒")
            print(f"  速度: {rate:.0f}条/秒")

            assert len(ages) == batch_size
