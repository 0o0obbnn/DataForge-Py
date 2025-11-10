#!/usr/bin/env python3
"""使用正确的工厂模式测试生成器"""

import sys
from dataforge import default_factory, GeneratorConfig

def test_generator_with_factory(generator_name, parameters=None):
    """使用工厂模式测试生成器"""
    try:
        config = GeneratorConfig(
            generator_type=generator_name,
            parameters=parameters or {}
        )
        
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"✅ {generator_name} 生成成功: {result}")
        return True
    except Exception as e:
        print(f"❌ {generator_name} 生成失败: {e}")
        return False

def main():
    print("使用工厂模式测试生成器...")
    
    # 测试核心生成器
    test_cases = [
        ("bankcard", {}),
        ("company_name", {}),
        ("generic_waybill", {}),
        ("education", {}),
        ("generic_education", {}),
        ("address", {}),
        ("age", {}),
        ("name", {}),
        ("phone", {}),
        ("email", {}),
        ("integer", {"min": 1, "max": 100}),
        ("decimal", {"min": 1.0, "max": 100.0}),
        ("string", {"length": 10}),
    ]
    
    success_count = 0
    failed_generators = []
    
    for gen_name, params in test_cases:
        if test_generator_with_factory(gen_name, params):
            success_count += 1
        else:
            failed_generators.append(gen_name)
    
    print(f"\n工厂模式测试完成:")
    print(f"成功: {success_count}/{len(test_cases)}")
    print(f"失败生成器: {failed_generators}")
    
    # 测试注册表的生成器列表
    from dataforge import default_registry
    generators = default_registry._generators
    print(f"\n注册表中所有生成器 ({len(generators)} 个):")
    for name in sorted(generators.keys()):
        print(f"  - {name}")

if __name__ == "__main__":
    main()