#!/usr/bin/env python3
"""直接运行集成测试"""

import sys
sys.path.append('.')

from dataforge.core.factory import default_registry, default_factory
from dataforge.core.generator import GeneratorConfig

def test_all_generators_registered():
    """验证所有预期生成器都已注册"""
    print("=== 测试生成器注册 ===")
    
    # 获取所有已注册的生成器
    registered = default_registry.list_generators()
    print(f"已注册生成器数量: {len(registered)}")
    
    # 定义核心生成器
    core_generators = [
        "idcard", "bankcard", "phone", "name", "age", "gender", 
        "address", "license_plate", "company_name", "email",
        "advanced_timestamp", "datetime_range", "logistics"
    ]
    
    # 检查核心生成器是否注册
    missing = []
    found = []
    for gen in core_generators:
        if default_registry.is_registered(gen):
            found.append(gen)
        else:
            missing.append(gen)
    
    print(f"核心生成器找到: {len(found)}")
    print(f"核心生成器缺失: {len(missing)}")
    
    if missing:
        print(f"缺失的生成器: {missing}")
        return False
    
    print("✅ 所有核心生成器都已注册")
    return True

def test_generator_instantiation():
    """测试生成器实例化"""
    print("\n=== 测试生成器实例化 ===")
    
    registered = default_registry.list_generators()
    failed = []
    success = 0
    
    for gen_name in registered:
        try:
            config = GeneratorConfig(
                generator_type=gen_name,
                parameters={},
                count=1,
                validate=False,
            )
            generator = default_factory.create_generator(config)
            if generator is not None:
                success += 1
            else:
                failed.append((gen_name, "Factory returned None"))
        except Exception as e:
            failed.append((gen_name, str(e)))
    
    print(f"成功实例化: {success}")
    print(f"失败实例化: {len(failed)}")
    
    if failed:
        print("失败的生成器:")
        for name, error in failed[:5]:  # 只显示前5个
            print(f"  - {name}: {error}")
        if len(failed) > 5:
            print(f"  ... 还有 {len(failed) - 5} 个失败")
        return False
    
    print("✅ 所有生成器实例化成功")
    return True

def test_basic_functionality():
    """测试基本功能"""
    print("\n=== 测试基本功能 ===")
    
    registered = default_registry.list_generators()
    failed = []
    success = 0
    
    for gen_name in registered[:10]:  # 只测试前10个
        try:
            config = GeneratorConfig(
                generator_type=gen_name,
                parameters={},
                count=1,
                validate=True,
            )
            generator = default_factory.create_generator(config)
            
            # 生成数据
            data = generator.generate_single()
            
            if data is None:
                failed.append((gen_name, "generate_single() returned None"))
                continue
            
            # 验证数据
            is_valid = generator.validate(data)
            if not is_valid:
                failed.append((gen_name, f"Validation failed: {data}"))
            else:
                success += 1
                
        except NotImplementedError:
            # 跳过未实现的生成器
            continue
        except Exception as e:
            failed.append((gen_name, f"Error: {str(e)}"))
    
    print(f"测试的生成器: {min(10, len(registered))}")
    print(f"功能正常: {success}")
    print(f"功能异常: {len(failed)}")
    
    if failed:
        print("异常的生成器:")
        for name, error in failed:
            print(f"  - {name}: {error}")
        return False
    
    print("✅ 测试的生成器功能正常")
    return True

def main():
    """主测试函数"""
    print("开始集成测试...\n")
    
    results = []
    results.append(test_all_generators_registered())
    results.append(test_generator_instantiation())
    results.append(test_basic_functionality())
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n=== 测试总结 ===")
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有集成测试通过!")
        return True
    else:
        print("❌ 部分集成测试失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)