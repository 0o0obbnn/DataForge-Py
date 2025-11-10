"""
婚姻状况生成器简单测试
"""

import random

from dataforge.generators.basic.marital_status import MaritalStatusGenerator


# 简单的测试运行
def test_marital_status():
    print("=== 婚姻状况生成器测试 ===")

    # 测试中国婚姻状况
    print("\n1. 中国婚姻状况测试:")
    generator = MaritalStatusGenerator(
        generator_type="marital_status",
        parameters={"region": "china", "include_age_factor": True}
    )

    # 测试不同年龄段的生成
    test_cases = [
        {"age": 18, "desc": "年轻人"},
        {"age": 30, "desc": "中年人"},
        {"age": 50, "desc": "老年人"},
    ]

    for case in test_cases:
        print(f"\n{case['desc']} ({case['age']}岁):")
        results = []
        for _ in range(10):
            # 模拟生成
            options = generator._get_marital_status_options()
            weights = generator._age_based_weights(case['age'])
            result = random.choices(options, weights=weights)[0]
            results.append(result)

        # 统计分布
        stats = {}
        for r in results:
            stats[r] = stats.get(r, 0) + 1

        print(f"  结果分布: {stats}")

    # 测试国际婚姻状况
    print("\n2. 国际婚姻状况测试:")
    generator_us = MaritalStatusGenerator(
        generator_type="marital_status",
        parameters={"region": "us", "include_age_factor": False}
    )

    options_us = generator_us._get_marital_status_options()
    print(f"  国际选项: {options_us}")

    # 测试验证功能
    print("\n3. 验证功能测试:")
    test_values = ["未婚", "已婚", "离异", "married", "invalid"]
    for val in test_values:
        is_valid = generator.validate(val)
        print(f"  '{val}': {'有效' if is_valid else '无效'}")

    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_marital_status()
