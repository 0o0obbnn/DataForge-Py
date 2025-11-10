#!/usr/bin/env python3
"""检查注册表详细信息"""

try:
    from dataforge.core.factory import default_registry
    
    # 检查一些应该存在的生成器
    test_generators = [
        'chinese_organization_code',
        'generic_driver_license', 
        'generic_tracking_number',
        'advanced_timestamp',
        'sql_injection',
        'xss_payload',
        'user_behavior'
    ]
    
    print("=== 注册表详细信息 ===")
    for gen in test_generators:
        is_registered = default_registry.is_registered(gen)
        print(f"{gen}: {'已注册' if is_registered else '未注册'}")
        
        if is_registered:
            try:
                generator_class = default_registry.get_generator_class(gen)
                print(f"  类: {generator_class}")
            except Exception as e:
                print(f"  获取类失败: {e}")
    
    print(f"\n总注册生成器数: {len(default_registry.list_generators())}")
    print("所有已注册生成器:")
    for gen in sorted(default_registry.list_generators()):
        print(f"  - {gen}")
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()