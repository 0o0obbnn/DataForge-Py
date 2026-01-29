"""
单生成器性能测试
"""

import time

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.performance
class TestSingleGeneratorPerformance:
    """单生成器性能测试类"""

    def test_name_generator_performance(self):
        """测试姓名生成器性能"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        config = GeneratorConfig("name", {})
        generator = factory.create_generator(config)

        # 预热
        for _ in range(10):
            generator.generate_single()

        # 性能测试
        start_time = time.time()
        iterations = 1000
        for _ in range(iterations):
            generator.generate_single()
        end_time = time.time()

        elapsed = end_time - start_time
        avg_time = elapsed / iterations * 1000  # 转换为毫秒

        print("\n姓名生成器性能:")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  平均时间: {avg_time:.3f}毫秒/次")
        print(f"  吞吐量: {iterations/elapsed:.0f}次/秒")

        # 性能断言：平均每次生成应该小于10ms
        assert avg_time < 10, f"性能不达标: {avg_time:.3f}ms > 10ms"

    def test_age_generator_performance(self):
        """测试年龄生成器性能"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.age import AgeGenerator

        registry.register("age", AgeGenerator)

        config = GeneratorConfig("age", {})
        generator = factory.create_generator(config)

        # 预热
        for _ in range(10):
            generator.generate_single()

        # 性能测试
        start_time = time.time()
        iterations = 10000
        for _ in range(iterations):
            generator.generate_single()
        end_time = time.time()

        elapsed = end_time - start_time
        avg_time = elapsed / iterations * 1000

        print("\n年龄生成器性能:")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  平均时间: {avg_time:.3f}毫秒/次")
        print(f"  吞吐量: {iterations/elapsed:.0f}次/秒")

        # 数字生成应该非常快
        assert avg_time < 1, f"性能不达标: {avg_time:.3f}ms > 1ms"

    def test_email_generator_performance(self):
        """测试邮箱生成器性能"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.contact.email import EmailGenerator

        registry.register("email", EmailGenerator)

        config = GeneratorConfig("email", {})
        generator = factory.create_generator(config)

        # 预热
        for _ in range(10):
            generator.generate_single()

        # 性能测试
        start_time = time.time()
        iterations = 1000
        for _ in range(iterations):
            generator.generate_single()
        end_time = time.time()

        elapsed = end_time - start_time
        avg_time = elapsed / iterations * 1000

        print("\n邮箱生成器性能:")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  平均时间: {avg_time:.3f}毫秒/次")
        print(f"  吞吐量: {iterations/elapsed:.0f}次/秒")

        assert avg_time < 10, f"性能不达标: {avg_time:.3f}ms > 10ms"

    def test_id_generator_performance(self):
        """测试身份证生成器性能"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.identifier.id import IDGenerator

        registry.register("id", IDGenerator)

        config = GeneratorConfig("id", {})
        generator = factory.create_generator(config)

        # 预热
        for _ in range(10):
            generator.generate_single()

        # 性能测试
        start_time = time.time()
        iterations = 1000
        for _ in range(iterations):
            generator.generate_single()
        end_time = time.time()

        elapsed = end_time - start_time
        avg_time = elapsed / iterations * 1000

        print("\n身份证生成器性能:")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  平均时间: {avg_time:.3f}毫秒/次")
        print(f"  吞吐量: {iterations/elapsed:.0f}次/秒")

        assert avg_time < 10, f"性能不达标: {avg_time:.3f}ms > 10ms"

    def test_address_generator_performance(self):
        """测试地址生成器性能"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.address import AddressGenerator

        registry.register("address", AddressGenerator)

        config = GeneratorConfig("address", {})
        generator = factory.create_generator(config)

        # 预热
        for _ in range(10):
            generator.generate_single()

        # 性能测试
        start_time = time.time()
        iterations = 1000
        for _ in range(iterations):
            generator.generate_single()
        end_time = time.time()

        elapsed = end_time - start_time
        avg_time = elapsed / iterations * 1000

        print("\n地址生成器性能:")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  平均时间: {avg_time:.3f}毫秒/次")
        print(f"  吞吐量: {iterations/elapsed:.0f}次/秒")

        assert avg_time < 15, f"性能不达标: {avg_time:.3f}ms > 15ms"

    def test_uuid_generator_performance(self):
        """测试UUID生成器性能"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.uuid import UUIDGenerator

        registry.register("uuid", UUIDGenerator)

        config = GeneratorConfig("uuid", {})
        generator = factory.create_generator(config)

        # 预热
        for _ in range(10):
            generator.generate_single()

        # 性能测试
        start_time = time.time()
        iterations = 10000
        for _ in range(iterations):
            generator.generate_single()
        end_time = time.time()

        elapsed = end_time - start_time
        avg_time = elapsed / iterations * 1000

        print("\nUUID生成器性能:")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  平均时间: {avg_time:.3f}毫秒/次")
        print(f"  吞吐量: {iterations/elapsed:.0f}次/秒")

        # UUID生成应该非常快
        assert avg_time < 1, f"性能不达标: {avg_time:.3f}ms > 1ms"

    def test_phone_generator_performance(self):
        """测试手机号生成器性能"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.contact.phone import PhoneGenerator

        registry.register("phone", PhoneGenerator)

        config = GeneratorConfig("phone", {})
        generator = factory.create_generator(config)

        # 预热
        for _ in range(10):
            generator.generate_single()

        # 性能测试
        start_time = time.time()
        iterations = 1000
        for _ in range(iterations):
            generator.generate_single()
        end_time = time.time()

        elapsed = end_time - start_time
        avg_time = elapsed / iterations * 1000

        print("\n手机号生成器性能:")
        print(f"  总时间: {elapsed:.3f}秒")
        print(f"  平均时间: {avg_time:.3f}毫秒/次")
        print(f"  吞吐量: {iterations/elapsed:.0f}次/秒")

        assert avg_time < 10, f"性能不达标: {avg_time:.3f}ms > 10ms"
