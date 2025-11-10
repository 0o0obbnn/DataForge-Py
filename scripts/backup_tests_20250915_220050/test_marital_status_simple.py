"""
婚姻状况生成器简单功能测试
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import random

from dataforge.generators.basic.marital_status import MaritalStatusGenerator


class MockConfig:
    """模拟配置类"""
    def __init__(self, parameters=None):
        self.parameters = parameters or {}

def test_marital_status_generator():
    """测试婚姻状况生成器"""
    print("=== 婚姻状况生成器功能测试 ===\n")

    # 测试1: 中国婚姻状况
    print("1. 中国婚姻状况测试:")
    config_china = {"region": "china", "include_age_factor": True}
    generator_china = MaritalStatusGenerator(config_china)

    # 验证选项
    options = generator_china._get_marital_status_options()
    print(f"   中国选项: {options}")

    # 测试不同年龄段的权重
    test_ages = [18, 25, 35, 45, 55]
    for age in test_ages:
        weights = generator_china._age_based_weights(age)
        print(f"   年龄 {age} 岁权重: {weights}")

    # 测试生成
    print("\n   生成示例:")
    for age in [20, 30, 40]:
        mock_context = type('MockContext', (), {
            'related_data': {'age': age}
        })()
        result = generator_china._generate_raw(mock_context)
        print(f"   年龄 {age} 岁: {result}")

    # 测试2: 国际婚姻状况
    print("\n2. 国际婚姻状况测试:")
    config_us = MockConfig({
        "region": "us",
        "include_age_factor": False
    })
    generator_us = MaritalStatusGenerator(config_us)

    options_us = generator_us._get_marital_status_options()
    print(f"   国际选项: {options_us}")

    # 测试验证功能
    print("\n3. 验证功能测试:")
    test_values = ["未婚", "已婚", "离异", "invalid", "married"]
    for val in test_values:
        is_valid_china = generator_china.validate(val)
        is_valid_us = generator_us.validate(val)
        print(f"   '{val}': 中国={is_valid_china}, 国际={is_valid_us}")

    # 测试4: 批量生成
    print("\n4. 批量生成测试:")
    results = []
    for _ in range(10):
        mock_context = type('MockContext', (), {
            'related_data': {'age': random.randint(20, 60)}
        })()
        result = generator_china._generate_raw(mock_context)
        results.append(result)

    # 统计分布
    stats = {}
    for r in results:
        stats[r] = stats.get(r, 0) + 1
    print(f"   生成分布: {stats}")

    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_marital_status_generator()
