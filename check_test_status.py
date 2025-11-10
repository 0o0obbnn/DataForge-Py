#!/usr/bin/env python3
"""检查当前测试状态"""

import sys
sys.path.append('.')

# 测试生成器检测
try:
    from tests.integration.test_all_generators import get_expected_generators
    expected = get_expected_generators()
    print(f"预期生成器数量: {len(expected)}")
    print(f"前10个生成器: {expected[:10]}")
except Exception as e:
    print(f"生成器检测失败: {e}")

# 测试注册表
try:
    from dataforge.core.factory import default_registry
    registered = default_registry.list_generators()
    print(f"注册表生成器数量: {len(registered)}")
    print(f"前10个注册生成器: {registered[:10]}")
except Exception as e:
    print(f"注册表检测失败: {e}")

# 测试核心功能
try:
    from dataforge.core.generator import GeneratorConfig
    config = GeneratorConfig('test', {'precision': 'MILLIS'})
    result = config.get('precision', 'default')
    print(f"GeneratorConfig.get() 测试: {result}")
except Exception as e:
    print(f"GeneratorConfig 测试失败: {e}")

# 测试物流生成器
try:
    from dataforge.generators.identifier.logistics import GenericWaybillGenerator
    from dataforge.core.generator import GeneratorConfig
    gen = GenericWaybillGenerator(GeneratorConfig('generic_waybill', {'carrier': 'SF'}))
    data = gen.generate_single()
    valid = gen.validate(data)
    print(f"GenericWaybillGenerator 测试: {data} -> {valid}")
except Exception as e:
    print(f"GenericWaybillGenerator 测试失败: {e}")

# 测试公司名称生成器
try:
    from dataforge.generators.basic.company_name import CompanyNameGenerator
    from dataforge.core.generator import GeneratorConfig
    gen = CompanyNameGenerator(GeneratorConfig('company_name', {'prefix_region': False}))
    
    # 测试多次生成确保长度
    short_names = []
    for _ in range(100):
        name = gen.generate_single()
        if len(name) < 4:
            short_names.append(name)
    
    print(f"CompanyNameGenerator 测试: 短名称数量 {len(short_names)}")
    if short_names:
        print(f"短名称示例: {short_names[:5]}")
except Exception as e:
    print(f"CompanyNameGenerator 测试失败: {e}")

print("\n测试状态检查完成!")