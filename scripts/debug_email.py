#!/usr/bin/env python3
"""调试邮件生成器问题"""

from dataforge.core.factory import default_factory
from dataforge.core.generator import GeneratorConfig


def debug_email_generator():
    print("=== 调试邮件生成器 ===")

    # 测试默认配置
    print("\n1. 默认配置:")
    config_default = GeneratorConfig(generator_type="email", parameters={})
    generator_default = default_factory.create_generator(config_default)
    for i in range(3):
        email = generator_default.generate()
        print(f"  {i + 1}: {email} (valid: {generator_default.validate(email)})")

    # 测试自定义域名（字符串）
    print("\n2. 自定义域名（字符串）:")
    config_custom = GeneratorConfig(
        generator_type="email", parameters={"domains": "test.com", "valid": True}
    )
    generator_custom = default_factory.create_generator(config_custom)
    for i in range(5):
        email = generator_custom.generate()
        valid = generator_custom.validate(email)
        ends_with_test = email.endswith("@test.com")
        print(
            f"  {i + 1}: {email} (valid: {valid}, ends with @test.com: {ends_with_test})"
        )

    # 检查生成器参数
    print("\n3. 生成器参数:")
    print(f"   生成器类型: {type(generator_custom)}")
    print(f"   生成器属性: {dir(generator_custom)}")
    print(f"   parameters中的domains: {generator_custom.parameters.get('domains')}")
    print(f"   parameters中的valid: {generator_custom.parameters.get('valid')}")

    # 测试自定义域名（列表）
    print("\n4. 自定义域名（列表）:")
    config_list = GeneratorConfig(
        generator_type="email", parameters={"domains": ["test.com", "example.com"]}
    )
    generator_list = default_factory.create_generator(config_list)
    for i in range(3):
        email = generator_list.generate()
        valid = generator_list.validate(email)
        print(f"  {i + 1}: {email} (valid: {valid})")


if __name__ == "__main__":
    debug_email_generator()
