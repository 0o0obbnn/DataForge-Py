#!/usr/bin/env python3
"""深入调试生成器装饰器执行问题"""

print("=== 检查装饰器导入和执行 ===")

# 检查装饰器是否正确导入
try:
    from dataforge.core.factory import register_generator, default_registry
    print("SUCCESS: register_generator 装饰器导入成功")
    print(f"装饰器对象: {register_generator}")
    print(f"默认注册表: {default_registry}")
except Exception as e:
    print(f"ERROR: 装饰器导入失败 - {e}")

# 尝试手动执行一个 advanced 模块的生成器注册
print("\n=== 手动测试 advanced 模块生成器注册 ===")

try:
    # 直接导入一个具体的生成器类
    from dataforge.generators.advanced.advanced_timestamp import AdvancedTimestampGenerator
    
    print(f"生成器类: {AdvancedTimestampGenerator}")
    print(f"是否有 _registered_name 属性: {hasattr(AdvancedTimestampGenerator, '_registered_name')}")
    
    # 手动注册
    register_generator("test_advanced_timestamp", ["test_timestamp"])(AdvancedTimestampGenerator)
    
    print(f"手动注册后的生成器数量: {len(default_registry._generators)}")
    print("最新注册的生成器:")
    for name in sorted(default_registry._generators.keys())[-5:]:
        print(f"  - {name}")
        
except Exception as e:
    print(f"ERROR: 手动注册失败 - {e}")
    import traceback
    traceback.print_exc()

# 检查 advanced 模块的具体导入问题
print("\n=== 检查 advanced 模块导入详情 ===")

try:
    import dataforge.generators.advanced.advanced_timestamp as at_module
    print(f"advanced_timestamp 模块: {at_module}")
    print(f"模块内容: {dir(at_module)}")
    
    # 检查是否有装饰器执行
    if hasattr(at_module, 'AdvancedTimestampGenerator'):
        gen_class = at_module.AdvancedTimestampGenerator
        print(f"生成器类: {gen_class}")
        print(f"是否有注册标记: {hasattr(gen_class, '_registered_name')}")
        if hasattr(gen_class, '_registered_name'):
            print(f"注册名称: {gen_class._registered_name}")
    else:
        print("ERROR: 找不到 AdvancedTimestampGenerator 类")
        
except Exception as e:
    print(f"ERROR: 检查 advanced_timestamp 模块失败 - {e}")
    import traceback
    traceback.print_exc()

# 测试直接导入整个 advanced 模块并检查装饰器执行
print("\n=== 测试完整 advanced 模块导入 ===")

try:
    # 清空注册表重新测试
    default_registry._generators.clear()
    default_registry._aliases.clear()
    print(f"清空后的注册表大小: {len(default_registry._generators)}")
    
    # 重新导入基础模块
    from dataforge.generators import basic
    print(f"导入 basic 模块后注册表大小: {len(default_registry._generators)}")
    
    # 导入 advanced 模块
    import dataforge.generators.advanced
    print(f"导入 advanced 模块后注册表大小: {len(default_registry._generators)}")
    
    # 检查 advanced 模块的具体文件
    import dataforge.generators.advanced.advanced_timestamp
    print(f"导入 advanced_timestamp 后注册表大小: {len(default_registry._generators)}")
    
except Exception as e:
    print(f"ERROR: 完整测试失败 - {e}")
    import traceback
    traceback.print_exc()