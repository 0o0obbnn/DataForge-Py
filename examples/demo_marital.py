"""
婚姻状况生成器演示脚本
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from dataforge.generators.basic import (
    GenericMaritalStatusGenerator,
    MaritalStatusGenerator,
)


def demo_marital_status():
    """演示婚姻状况生成器的使用"""
    print("=== DataForge 婚姻状况生成器演示 ===\n")

    # 1. 中国婚姻状况生成器演示
    print("1. 中国婚姻状况生成器")
    print("-" * 40)
    china_gen = MaritalStatusGenerator({
        "region": "china",
        "include_age_factor": True
    })

    print("支持的婚姻状况:")
    for status in china_gen._get_marital_status_options():
        print(f"  • {status}")

    print("\n按年龄生成示例:")
    age_samples = [18, 25, 35, 45, 55]
    for age in age_samples:
        class MockContext:
            def __init__(self, age):
                self.related_data = {"age": age}

        result = china_gen._generate_raw(MockContext(age))
        print(f"  年龄 {age} 岁: {result}")

    # 2. 国际婚姻状况生成器演示
    print("\n2. 国际婚姻状况生成器")
    print("-" * 40)
    intl_gen = MaritalStatusGenerator({
        "region": "us",
        "include_age_factor": False
    })

    print("支持的婚姻状况:")
    for status in intl_gen._get_marital_status_options():
        print(f"  • {status}")

    print("\n随机生成示例:")
    for i in range(5):
        result = intl_gen._generate_raw(type('MockContext', (), {'related_data': {}})())
        print(f"  样本 {i+1}: {result}")

    # 3. 通用婚姻状况生成器演示
    print("\n3. 通用婚姻状况生成器")
    print("-" * 40)
    generic_gen = GenericMaritalStatusGenerator({
        "region": "china"
    })

    print("批量生成示例 (带年龄关联):")
    ages = [22, 28, 32, 38, 42]
    for age in ages:
        class MockContext:
            def __init__(self, age):
                self.related_data = {"age": age}

        result = generic_gen._generate_raw(MockContext(age))
        print(f"  年龄 {age} 岁: {result}")

    # 4. 验证功能演示
    print("\n4. 验证功能演示")
    print("-" * 40)

    test_values = ["未婚", "已婚", "离异", "single", "married", "invalid"]
    print("中国验证器:")
    for val in test_values:
        valid = china_gen.validate(val)
        print(f"  '{val}': {'✓' if valid else '✗'}")

    print("\n国际验证器:")
    for val in test_values:
        valid = intl_gen.validate(val)
        print(f"  '{val}': {'✓' if valid else '✗'}")

    print("\n=== 演示完成 ===")

if __name__ == "__main__":
    demo_marital_status()
