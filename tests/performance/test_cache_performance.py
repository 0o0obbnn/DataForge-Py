#!/usr/bin/env python3
"""
DataForge 数据加载和缓存性能测试 (pytest风格)
"""

import os
import time

import pytest

from dataforge.core.cache import get_cache_stats, invalidate_cache
from dataforge.core.factory import GeneratorFactory
from dataforge.core.generator import GeneratorConfig
from dataforge.core.preloader import (
    get_preload_stats,
    wait_for_data_preload,
)


@pytest.mark.performance
def test_preloading_and_cache_status(capsys):
    """测试预加载和缓存状态的报告"""
    # 1. 检查预加载状态
    preload_stats = get_preload_stats()
    assert isinstance(preload_stats, dict)
    assert "is_preloaded" in preload_stats

    if preload_stats["is_preloading"]:
        wait_for_data_preload(timeout=20.0)
        preload_stats = get_preload_stats()
        assert preload_stats["is_preloaded"] is True

    # 2. 检查缓存状态
    cache_stats = get_cache_stats()
    assert isinstance(cache_stats, dict)
    assert "cache_size" in cache_stats

    with capsys.readouterr():
        print("\n--- Preload and Cache Status ---")
        print(f"Preloaded: {preload_stats['is_preloaded']}")
        print(f"Cache size: {cache_stats['cache_size']}")


@pytest.mark.performance
@pytest.mark.parametrize(
    "generator_type, params",
    [
        ("name", {}),
        ("address", {"detail_level": "FULL"}),
    ],
)
def test_generation_performance(
    generator_factory: GeneratorFactory, generator_type: str, params: dict, capsys
):
    """测试首次生成和缓存生成的性能差异"""
    invalidate_cache()  # Ensure a clean slate

    # 第一次生成 (应该会触发数据加载)
    start_time = time.time()
    config = GeneratorConfig(generator_type=generator_type, parameters=params)
    generator = generator_factory.create_generator(config)
    generator.generate_batch(10)
    first_time = time.time() - start_time

    # 第二次生成 (应该使用缓存)
    start_time = time.time()
    generator.generate_batch(100)
    second_time = time.time() - start_time

    with capsys.readouterr():
        print(f"\n--- Performance for {generator_type} ---")
        print(f"First generation (10 items): {first_time * 1000:.2f}ms")
        print(f"Cached generation (100 items): {second_time * 1000:.2f}ms")

        per_item_first_ms = (first_time / 10) * 1000
        per_item_second_ms = (second_time / 100) * 1000
        print(
            f"Per-item first: {per_item_first_ms:.3f}ms, cached: {per_item_second_ms:.3f}ms"
        )

    assert per_item_second_ms < per_item_first_ms


@pytest.mark.performance
def test_stress_generation(generator_factory: GeneratorFactory, capsys):
    """压力测试: 批量生成大量数据"""
    config = GeneratorConfig(generator_type="name", parameters={})
    generator = generator_factory.create_generator(config)

    start_time = time.time()
    batch_size = 2000
    generator.generate_batch(batch_size)
    total_time = time.time() - start_time

    with capsys.readouterr():
        print("\n--- Stress Test ---")
        print(f"Generated {batch_size} names in {total_time * 1000:.2f}ms")
        print(f"Speed: {batch_size / total_time:.0f} items/sec")

    assert total_time < 2  # Should be reasonably fast


@pytest.mark.performance
def test_memory_usage(generator_factory: GeneratorFactory, capsys):
    """测试生成大量数据时的内存使用情况"""
    try:
        import psutil
    except ImportError:
        pytest.skip("psutil is not installed, skipping memory test.")

    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)

    for _ in range(15):
        config = GeneratorConfig(generator_type="name", parameters={})
        generator = generator_factory.create_generator(config)
        generator.generate_batch(100)

    mem_after = process.memory_info().rss / (1024 * 1024)
    mem_growth = mem_after - mem_before

    with capsys.readouterr():
        print("\n--- Memory Usage Test ---")
        print(f"Memory before: {mem_before:.2f} MB")
        print(f"Memory after: {mem_after:.2f} MB")
        print(f"Memory growth: {mem_growth:.2f} MB")

    # Allow for some memory growth, but it should not be excessive
    assert mem_growth < 50
