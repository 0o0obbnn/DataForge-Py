#!/usr/bin/env python3
"""比较注册的生成器和测试期望的生成器"""

import sys
import os
sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

from dataforge.core.factory import default_registry

def main():
    # 获取实际注册的生成器
    registered = set(default_registry.list_generators())
    
    # 定义测试中的核心生成器（从test_all_generators.py复制）
    core_generators = [
        "idcard", "bankcard", "phone", "name", "age", "gender", 
        "address", "license_plate", "company_name", "email",
        "advanced_timestamp", "datetime_range", "logistics"
    ]
    
    # 计算期望的生成器（模拟test_all_generators.py的逻辑）
    expected = set()
    for gen in core_generators:
        if gen in registered:
            expected.add(gen)
    
    # 添加其他已注册的生成器
    for gen in registered:
        if gen not in expected:
            expected.add(gen)
    
    print(f'实际注册的生成器数量: {len(registered)}')
    print(f'测试期望的生成器数量: {len(expected)}')
    
    # 检查差异
    missing = expected - registered
    extra = registered - expected
    
    print(f'\n差异分析:')
    print(f'期望但未注册: {len(missing)}个')
    if missing:
        for gen in sorted(missing):
            print(f'  - {gen}')
    
    print(f'注册但未期望: {len(extra)}个')
    if extra:
        for gen in sorted(extra):
            print(f'  - {gen}')
    
    # 检查核心生成器的注册情况
    print(f'\n核心生成器注册状态:')
    for gen in core_generators:
        status = '✅' if gen in registered else '❌'
        print(f'  {status} {gen}')
    
    # 统计未注册的核心生成器
    missing_core = [gen for gen in core_generators if gen not in registered]
    if missing_core:
        print(f'\n⚠️ 未注册的核心生成器: {len(missing_core)}个')
        for gen in missing_core:
            print(f'  - {gen}')
    else:
        print(f'\n✅ 所有核心生成器都已注册')

if __name__ == "__main__":
    main()