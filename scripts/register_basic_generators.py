#!/usr/bin/env python3
"""
DataForge 基础生成器注册模块
统一注册所有基础信息类生成器到默认注册表
"""

from dataforge.core.registry import GeneratorRegistry
from dataforge.generators.basic.age import ChineseAgeGenerator as AgeGenerator
from dataforge.generators.basic.bankcard import BankCardGenerator
from dataforge.generators.basic.email import ChineseEmailGenerator as EmailGenerator
from dataforge.generators.basic.idcard import IDCardGenerator
from dataforge.generators.basic.name import ChineseNameGenerator as NameGenerator
from dataforge.generators.basic.password import PasswordGenerator
from dataforge.generators.basic.phone import PhoneGenerator
from dataforge.generators.basic.username import UsernameGenerator


def register_basic_generators():
    """注册所有基础生成器"""
    registry = GeneratorRegistry()

    generators = {
        "username": UsernameGenerator,
        "password": PasswordGenerator,
        "email": EmailGenerator,
        "phone": PhoneGenerator,
        "name": NameGenerator,
        "age": AgeGenerator,
        "idcard": IDCardGenerator,
        "bankcard": BankCardGenerator,
    }

    for name, generator_class in generators.items():
        registry.register(name, generator_class)
        print(f"✅ 已注册: {name} -> {generator_class.__name__}")

    return registry


if __name__ == "__main__":
    print("🚀 DataForge 基础生成器注册")
    print("=" * 30)
    register_basic_generators()
    print("✨ 注册完成！")
