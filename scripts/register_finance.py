#!/usr/bin/env python3
"""
手动注册金融类生成器
"""

# 手动导入finance模块以触发注册
# 现在检查注册
from dataforge.core.factory import default_registry

# 导入具体的金融生成器类

print("注册金融生成器后:")
print("=" * 50)

for name in default_registry.list_generators():
    generator_class = default_registry.get_generator_class(name)
    print(f"- {name}: {generator_class.__name__}")

# 检查特定金融生成器
finance_generators = [
    "crypto_address",
    "stock_code",
    "bank_account",
    "derivatives",
    "market_data",
    "financial_report",
]

print("\n检查金融生成器:")
print("=" * 30)
for name in finance_generators:
    registered = default_registry.is_registered(name)
    print(f"{name}: {'✓' if registered else '✗'}")
