#!/usr/bin/env python3
"""简单测试脚本"""

import sys
sys.path.append('.')

from dataforge.core.factory import default_registry
from dataforge.core.generator import GeneratorConfig
from dataforge.core.factory import default_factory

print("=== DataForge 集成测试 ===")

# 1. 检查注册表
registered = default_registry.list_generators()
print(f"已注册生成器数量: {len(registered)}")

# 2. 核心生成器检查
core_generators = ["bankcard", "phone", "name", "company_name", "generic_waybill"]
found_core = [g for g in core_generators if default_registry.is_registered(g)]
print(f"核心生成器找到: {len(found_core)}/{len(core_generators)}")
print(f"找到的核心生成器: {found_core}")

# 3. 测试几个关键生成器
test_generators = ["bankcard", "company_name", "generic_waybill"]
success_count = 0

for gen_name in test_generators:
    if not default_registry.is_registered(gen_name):
        print(f"⚠️ 生成器 {gen_name} 未注册")
        continue
        
    try:
        config = GeneratorConfig(generator_type=gen_name, parameters={})
        generator = default_factory.create_generator(config)
        data = generator.generate_single()
        valid = generator.validate(data)
        
        print(f"✅ {gen_name}: {type(data).__name__} -> 验证: {valid}")
        success_count += 1
    except Exception as e:
        print(f"❌ {gen_name}: 错误 - {e}")

print(f"\n测试结果: {success_count}/{len(test_generators)} 成功")

if success_count == len(test_generators):
    print("🎉 所有关键测试通过!")
else:
    print("⚠️ 部分测试失败")