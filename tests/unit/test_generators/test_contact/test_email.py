#!/usr/bin/env python3
"""
测试电子邮件生成器
"""

import sys

from dataforge.core.factory import default_factory
from dataforge.core.generator import GenerationContext, GeneratorConfig

# 导入电子邮件生成器


def test_email_generation():
    """测试电子邮件生成"""
    print("=== 测试电子邮件生成 ===")

    # 测试不同域名类型的电子邮件生成
    for domain_type in ["RANDOM", "REAL", "CUSTOM"]:
        if domain_type == "CUSTOM":
            config = GeneratorConfig(
                generator_type="email",
                parameters={
                    "domain_type": domain_type,
                    "domains": ["dataforge.cn", "test.dataforge.org"],
                },
            )
        else:
            config = GeneratorConfig(
                generator_type="email", parameters={"domain_type": domain_type}
            )

        generator = default_factory.create_generator(config)
        email = generator.generate()
        print(f"域名类型: {domain_type}")
        print(f"生成的电子邮件: {email}")
        print(f"校验结果: {generator.validate(email)}")
        print()

    # 测试包含中文字符的电子邮件生成
    config = GeneratorConfig(
        generator_type="email", parameters={"include_chinese": True}
    )

    generator = default_factory.create_generator(config)
    for _ in range(3):
        email = generator.generate()
        print(f"生成的中文电子邮件: {email}")
        print(f"校验结果: {generator.validate(email)}")
        print()


def test_email_relations():
    """测试电子邮件关联"""
    print("=== 测试电子邮件与其他数据的关联 ===")

    # 测试与身份证的关联
    configs = [
        GeneratorConfig(generator_type="idcard", parameters={"region": "440000"}),
        GeneratorConfig(generator_type="email", parameters={}),
    ]

    context = GenerationContext()
    result = default_factory.generate_batch_with_relations(configs, context)
    print(f"生成结果: {result}")
    print()

    # 测试与姓名的关联
    configs = [
        GeneratorConfig(generator_type="name", parameters={"gender": "MALE"}),
        GeneratorConfig(generator_type="email", parameters={}),
    ]

    context = GenerationContext()
    result = default_factory.generate_batch_with_relations(configs, context)
    print(f"生成结果: {result}")
    print()

    # 测试与地址的关联
    configs = [
        GeneratorConfig(generator_type="address", parameters={"province": "广东省"}),
        GeneratorConfig(generator_type="email", parameters={}),
    ]

    context = GenerationContext()
    result = default_factory.generate_batch_with_relations(configs, context)
    print(f"生成结果: {result}")
    print()


def main():
    """主测试函数"""
    print("DataForge 电子邮件生成器测试")
    print("=" * 50)

    test_email_generation()
    test_email_relations()

    print("所有测试完成！")
    return 0


if __name__ == "__main__":
    sys.exit(main())
