#!/usr/bin/env python3
"""
数据加载和缓存性能测试
"""
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataforge.core.cache import get_cache_stats, invalidate_cache
from dataforge.core.preloader import get_preload_stats, get_performance_stats, wait_for_data_preload
from dataforge.core.factory import default_factory
from dataforge.core.generator import GeneratorConfig


def test_cache_performance():
    """测试缓存性能"""
    print("=== 数据缓存和预加载性能测试 ===")
    
    # 1. 检查预加载状态
    print("1. 预加载状态:")
    preload_stats = get_preload_stats()
    print(f"   预加载完成: {preload_stats['is_preloaded']}")
    print(f"   正在预加载: {preload_stats['is_preloading']}")
    
    if preload_stats['is_preloading']:
        print("   等待预加载完成...")
        success = wait_for_data_preload(timeout=15.0)
        print(f"   预加载完成: {success}")
    
    print()
    
    # 2. 检查缓存状态
    print("2. 缓存状态:")
    cache_stats = get_cache_stats()
    print(f"   缓存文件数: {cache_stats['cache_size']}")
    print(f"   最大缓存数: {cache_stats['max_cache_size']}")
    print(f"   缓存生存时间: {cache_stats['cache_ttl']}秒")
    if cache_stats['cached_files']:
        print("   已缓存文件:")
        for file_path in cache_stats['cached_files']:
            print(f"     - {os.path.basename(file_path)}")
    print()
    
    # 3. 测试数据生成性能
    print("3. 数据生成性能测试:")
    
    generators_to_test = [
        ('name', '姓名生成器', {}),
        ('address', '地址生成器', {}),
        ('name', '姓名生成器（包含拼音）', {'include_pinyin': True}),
        ('address', '地址生成器（详细地址）', {'detail_level': 'FULL'}),
    ]
    
    for generator_type, desc, params in generators_to_test:
        print(f"   测试 {desc}:")
        
        # 第一次生成（可能需要加载数据）
        start_time = time.time()
        try:
            config = GeneratorConfig(generator_type=generator_type, parameters=params)
            generator = default_factory.create_generator(config)
            data = generator.generate_batch(10)
            first_time = time.time() - start_time
            print(f"     首次生成10条: {first_time*1000:.2f}ms")
        except Exception as e:
            print(f"     错误: {e}")
            continue
        
        # 第二次生成（应该使用缓存）
        start_time = time.time()
        try:
            config = GeneratorConfig(generator_type=generator_type, parameters=params)
            generator = default_factory.create_generator(config)
            data = generator.generate_batch(100)
            second_time = time.time() - start_time
            print(f"     缓存生成100条: {second_time*1000:.2f}ms")
            
            # 计算性能提升
            per_item_first = first_time / 10 * 1000
            per_item_second = second_time / 100 * 1000
            if per_item_first > 0:
                improvement = (per_item_first - per_item_second) / per_item_first * 100
                print(f"     单条数据性能提升: {improvement:.1f}%")
            
        except Exception as e:
            print(f"     错误: {e}")
        
        print()
    
    # 4. 压力测试
    print("4. 压力测试（生成大量数据）:")
    start_time = time.time()
    try:
        config = GeneratorConfig(generator_type='name', parameters={'include_pinyin': False})
        generator = default_factory.create_generator(config)
        data = generator.generate_batch(1000)
        batch_time = time.time() - start_time
        print(f"   批量生成1000条姓名: {batch_time*1000:.2f}ms")
        print(f"   平均每条: {batch_time/1000*1000:.3f}ms")
        print(f"   生成速度: {1000/batch_time:.0f}条/秒")
        
        # 显示部分生成的数据
        print("   样本数据:")
        for i, name in enumerate(data[:5]):
            print(f"     {i+1}. {name}")
        
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 5. 性能统计
    print("5. 性能统计:")
    perf_stats = get_performance_stats()
    if perf_stats['generation_count'] > 0:
        print(f"   总生成次数: {perf_stats['generation_count']}")
        print(f"   平均生成时间: {perf_stats['avg_generation_time_ms']:.2f}ms")
        print(f"   最短生成时间: {perf_stats['min_generation_time_ms']:.2f}ms")
        print(f"   最长生成时间: {perf_stats['max_generation_time_ms']:.2f}ms")
        print(f"   缓存命中率: {perf_stats['cache_hit_rate_percent']:.1f}%")
    else:
        print("   暂无性能数据")
    
    print()
    
    # 6. 测试缓存失效和重新加载
    print("6. 测试缓存失效:")
    print("   清空缓存...")
    invalidate_cache()
    
    cache_stats_after = get_cache_stats()
    print(f"   清空后缓存文件数: {cache_stats_after['cache_size']}")
    
    # 重新生成数据触发重新加载
    start_time = time.time()
    try:
        config = GeneratorConfig(generator_type='name', parameters={})
        generator = default_factory.create_generator(config)
        data = generator.generate_batch(5)
        reload_time = time.time() - start_time
        print(f"   重新加载后生成5条: {reload_time*1000:.2f}ms")
    except Exception as e:
        print(f"   错误: {e}")
    
    print("\n🎉 性能测试完成！")


def test_memory_usage():
    """测试内存使用情况"""
    print("\n=== 内存使用测试 ===")
    
    try:
        import psutil
        process = psutil.Process()
        
        # 获取当前内存使用
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        print(f"测试前内存使用: {memory_before:.2f} MB")
        
        # 生成大量数据
        print("生成大量数据...")
        for _ in range(10):
            config = GeneratorConfig(generator_type='name', parameters={})
            generator = default_factory.create_generator(config)
            data = generator.generate_batch(100)
        
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        print(f"测试后内存使用: {memory_after:.2f} MB")
        print(f"内存增长: {memory_after - memory_before:.2f} MB")
        
    except ImportError:
        print("psutil模块未安装，跳过内存测试")


if __name__ == "__main__":
    test_cache_performance()
    test_memory_usage()