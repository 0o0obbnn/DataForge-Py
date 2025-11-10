"""
婚姻状况生成器集成测试
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from dataforge.generators.basic import (
    GenericMaritalStatusGenerator,
    MaritalStatusGenerator,
)


def test_integration():
    """测试婚姻状况生成器在系统中的集成使用"""
    print("=== 婚姻状况生成器集成测试 ===\n")

    # 测试1: 直接使用MaritalStatusGenerator
    print("1. 中国婚姻状况生成器:")
    china_gen = MaritalStatusGenerator({
        "region": "china",
        "include_age_factor": True
    })

    # 测试不同年龄
    test_contexts = [
        {"related_data": {"age": 22}},
        {"related_data": {"age": 35}},
        {"related_data": {"age": 50}},
    ]

    for ctx in test_contexts:
        age = ctx["related_data"]["age"]
        result = china_gen._generate_raw(type('MockContext', (), ctx)())
        print(f"   年龄 {age} 岁: {result}")

    # 测试2: 使用GenericMaritalStatusGenerator
    print("\n2. 通用婚姻状况生成器:")
    generic_gen = GenericMaritalStatusGenerator({
        "region": "international",
        "include_age_factor": False
    })

    # 生成多个样本
    results = []
    for _ in range(5):
        result = generic_gen._generate_raw(type('MockContext', (), {"related_data": {}})())
        results.append(result)

    print(f"   生成样本: {results}")

    # 测试3: 验证功能
    print("\n3. 验证功能:")
    test_values = ["未婚", "married", "divorced", "离异"]
    for val in test_values:
        valid_china = china_gen.validate(val)
        valid_generic = generic_gen.validate(val)
        print(f"   '{val}': 中国={valid_china}, 通用={valid_generic}")

    print("\n=== 集成测试完成 ===")

if __name__ == "__main__":
    test_integration()
