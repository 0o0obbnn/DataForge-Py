#!/usr/bin/env python3
"""测试生成器注册问题"""

print("=== 测试模块导入 ===")

# 测试直接导入 advanced 和 auth 模块
try:
    from dataforge.generators import advanced, auth
    print("SUCCESS: advanced 和 auth 模块导入成功")
except ImportError as e:
    print(f"ERROR: 导入失败 - {e}")

# 测试当前注册表状态
try:
    from dataforge.core.factory import default_registry
    print(f"\n当前注册的生成器数量: {len(default_registry._generators)}")
    
    # 按模块分组统计
    advanced_count = 0
    auth_count = 0
    other_count = 0
    
    print("\n已注册的生成器名称:")
    for name in sorted(default_registry._generators.keys()):
        print(f"  - {name}")
        if any(keyword in name for keyword in ['advanced', 'trading', 'datetime_range', 'media_file', 'sql_injection', 'xss_payload', 'user_behavior', 'analytics']):
            advanced_count += 1
        elif any(keyword in name for keyword in ['auth', 'token', 'email_verification', 'sms_verification', 'session_id']):
            auth_count += 1
        else:
            other_count += 1
    
    print(f"\n统计:")
    print(f"  - Advanced模块生成器: {advanced_count}")
    print(f"  - Auth模块生成器: {auth_count}")
    print(f"  - 其他模块生成器: {other_count}")
    
except Exception as e:
    print(f"ERROR: 获取注册表失败 - {e}")

# 测试手动导入 advanced 模块
print("\n=== 测试手动导入 advanced 模块 ===")
try:
    import dataforge.generators.advanced
    print("SUCCESS: 手动导入 advanced 模块成功")
    
    # 再次检查注册表
    from dataforge.core.factory import default_registry
    print(f"手动导入后注册的生成器数量: {len(default_registry._generators)}")
    
except Exception as e:
    print(f"ERROR: 手动导入 advanced 失败 - {e}")

# 测试手动导入 auth 模块
print("\n=== 测试手动导入 auth 模块 ===")
try:
    import dataforge.generators.auth
    print("SUCCESS: 手动导入 auth 模块成功")
    
    # 再次检查注册表
    from dataforge.core.factory import default_registry
    print(f"手动导入后注册的生成器数量: {len(default_registry._generators)}")
    
except Exception as e:
    print(f"ERROR: 手动导入 auth 失败 - {e}")