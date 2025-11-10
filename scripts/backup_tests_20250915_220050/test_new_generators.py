#!/usr/bin/env python3
"""
测试新增的生成器
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataforge.core.factory import default_factory
from dataforge.core.generator import GeneratorConfig


def test_new_generators():
    """测试新增的生成器"""
    print("=== 测试新增的生成器 ===\n")

    # 测试配置
    test_configs = [
        {
            "name": "车牌号生成器",
            "type": "license_plate",
            "params": {},
            "test_params": [
                {"type": "FUEL"},
                {"type": "NEW_ENERGY"},
                {"province": "京", "city": "A"},
            ],
        },
        {
            "name": "企业名称生成器",
            "type": "company_name",
            "params": {},
            "test_params": [
                {"industry": "IT"},
                {"industry": "FINANCE", "type": "GROUP"},
                {"prefix_region": False},
            ],
        },
        {
            "name": "统一社会信用代码生成器",
            "type": "uscc",
            "params": {},
            "test_params": [{"region": "110000"}, {"valid": False}],
        },
        {
            "name": "组织机构代码生成器",
            "type": "organization_code",
            "params": {},
            "test_params": [{"valid": True}, {"valid": False}],
        },
        {
            "name": "LEI码生成器",
            "type": "lei",
            "params": {},
            "test_params": [{"valid": True}, {"valid": False}],
        },
    ]

    for config in test_configs:
        print(f"📋 测试 {config['name']}:")

        try:
            # 基本测试
            gen_config = GeneratorConfig(
                generator_type=config["type"], parameters=config["params"]
            )
            generator = default_factory.create_generator(gen_config)

            # 生成基本数据
            basic_data = generator.generate_batch(3)
            print(f"   基本生成: {basic_data}")

            # 测试不同参数
            for i, test_params in enumerate(config["test_params"]):
                test_config = GeneratorConfig(
                    generator_type=config["type"], parameters=test_params
                )
                test_generator = default_factory.create_generator(test_config)
                test_data = test_generator.generate_batch(2)
                print(f"   参数测试{i + 1} {test_params}: {test_data}")

                # 校验测试
                for data in test_data[:1]:  # 只测试第一个
                    is_valid = test_generator.validate(data)
                    print(f"     校验 '{data}': {'✓' if is_valid else '✗'}")

        except Exception as e:
            print(f"   ❌ 错误: {e}")

        print()

    print("🎉 新增生成器测试完成！")


def test_generator_info_methods():
    """测试生成器的信息解析方法"""
    print("\n=== 测试生成器信息解析方法 ===\n")

    test_cases = [
        {
            "name": "车牌号信息解析",
            "type": "license_plate",
            "data": "京A12345",
            "method": "get_plate_info",
        },
        {
            "name": "企业名称信息解析",
            "type": "company_name",
            "data": "北京华为科技有限公司",
            "method": "get_company_info",
        },
        {
            "name": "USCC信息解析",
            "type": "uscc",
            "params": {"valid": True},
            "method": "get_uscc_info",
        },
        {
            "name": "组织机构代码信息解析",
            "type": "organization_code",
            "params": {"valid": True},
            "method": "get_org_code_info",
        },
        {
            "name": "LEI码信息解析",
            "type": "lei",
            "params": {"valid": True},
            "method": "get_lei_info",
        },
    ]

    for case in test_cases:
        print(f"🔍 测试 {case['name']}:")

        try:
            config = GeneratorConfig(
                generator_type=case["type"], parameters=case.get("params", {})
            )
            generator = default_factory.create_generator(config)

            # 如果提供了测试数据，使用测试数据；否则生成新数据
            if "data" in case:
                test_data = case["data"]
            else:
                test_data = generator.generate()

            print(f"   测试数据: {test_data}")

            # 调用信息解析方法
            if hasattr(generator, case["method"]):
                info = getattr(generator, case["method"])(test_data)
                print("   解析结果:")
                for key, value in info.items():
                    print(f"     {key}: {value}")
            else:
                print(f"   ⚠️ 方法 {case['method']} 不存在")

        except Exception as e:
            print(f"   ❌ 错误: {e}")

        print()


if __name__ == "__main__":
    test_new_generators()
    test_generator_info_methods()
