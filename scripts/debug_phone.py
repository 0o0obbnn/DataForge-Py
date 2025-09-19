#!/usr/bin/env python3
"""
调试手机号生成器问题
"""

from dataforge.core.factory import default_factory
from dataforge.core.generator import GeneratorConfig


def test_phone_generator():
    """测试手机号生成器"""
    print("=== 测试手机号生成器 ===")

    config = GeneratorConfig(generator_type="phone", parameters={})
    generator = default_factory.create_generator(config)

    print(f"Generator class: {type(generator).__name__}")
    print(f"Generator module: {type(generator).__module__}")

    print("\n生成的手机号:")
    for i in range(5):
        phone = generator.generate()
        print(
            f'Phone {i + 1}: "{phone}", Length: {len(phone)}, Is digit: {phone.isdigit()}'
        )
        print(f"Validation result: {generator.validate(phone)}")


if __name__ == "__main__":
    test_phone_generator()
