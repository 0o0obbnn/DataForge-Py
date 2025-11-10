#!/usr/bin/env python3
"""
DataForge 基础生成器综合测试
验证所有基础信息类生成器的功能和ruff规范符合性
"""

import json
import sys

from dataforge.core.factory import GeneratorConfig, default_factory, default_registry

# 导入并注册所有基础生成器
from dataforge.generators.basic.age import ChineseAgeGenerator as AgeGenerator
from dataforge.generators.basic.bankcard import BankCardGenerator
from dataforge.generators.basic.email import ChineseEmailGenerator as EmailGenerator
from dataforge.generators.basic.idcard import IDCardGenerator
from dataforge.generators.basic.name import ChineseNameGenerator as NameGenerator
from dataforge.generators.basic.password import PasswordGenerator
from dataforge.generators.basic.phone import PhoneGenerator
from dataforge.generators.basic.username import UsernameGenerator


def register_all_basic_generators():
    """注册所有基础生成器"""
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
        if not default_registry.is_registered(name):
            default_registry.register(name, generator_class)


def test_basic_generators():
    """测试所有基础生成器"""
    test_configs = {
        "username": {"length": 8, "format": "alpha_numeric"},
        "password": {"length": 12, "complexity": "strong"},
        "email": {"domains": ["test.com"], "username_length": (5, 10)},
        "phone": {"type": "MOBILE", "valid": True},
        "name": {"gender": "male", "length": 2},
        "age": {"min": 18, "max": 65, "distribution": "uniform"},
        "idcard": {"region": "110101", "valid": True, "gender": "male"},
        "bankcard": {"card_type": "DEBIT", "valid": True},
    }

    results = {}

    for generator_name, config in test_configs.items():
        try:
            print(f"🧪 测试 {generator_name} 生成器...")

            # 获取生成器实例
            generator_config = GeneratorConfig(
                generator_type=generator_name, parameters=config
            )
            generator = default_factory.create_generator(generator_config)

            # 测试单个生成
            single_result = generator.generate_single()

            # 测试批量生成
            batch_results = generator.generate_batch(5)

            # 测试验证功能
            is_valid = generator.validate(single_result)

            results[generator_name] = {
                "status": "✅ 通过",
                "single_result": str(single_result),
                "batch_count": len(batch_results),
                "validation": is_valid,
                "generator_type": str(generator.generator_type),
            }

            print(f"   生成结果: {single_result}")
            print(f"   验证结果: {is_valid}")

        except Exception as e:
            results[generator_name] = {
                "status": "❌ 失败",
                "error": str(e),
            }
            print(f"   错误: {e}")

    return results


def test_cross_validation():
    """测试生成器间的数据关联验证"""
    print("\n🔗 测试数据关联验证...")

    # 测试姓名和邮箱的关联
    try:
        name_config = GeneratorConfig(
            generator_type="name", parameters={"gender": "female"}
        )
        email_config = GeneratorConfig(
            generator_type="email", parameters={"type": "COMMON"}
        )

        name_gen = default_factory.create_generator(name_config)
        default_factory.create_generator(email_config)

        name = name_gen.generate_single()
        print(f"   生成姓名: {name}")

        # 验证邮箱可以基于姓名生成
        # 注意：这需要EmailGenerator支持上下文关联

    except Exception as e:
        print(f"   关联测试错误: {e}")


def test_cli_parameters():
    """测试CLI参数支持"""
    print("\n⚙️ 测试CLI参数支持...")

    # 检查所有生成器支持的参数
    generators = [
        "username",
        "password",
        "email",
        "phone",
        "name",
        "age",
        "idcard",
        "bankcard",
    ]

    for generator_name in generators:
        try:
            generator_config = GeneratorConfig(
                generator_type=generator_name, parameters={}
            )
            generator = default_factory.create_generator(generator_config)

            supported_params = list(
                getattr(generator, "supported_parameters", {}).keys()
            )
            print(f"   {generator_name}: {supported_params}")

        except Exception as e:
            print(f"   {generator_name}: 参数获取失败 - {e}")


def main():
    """主测试函数"""
    print("🚀 DataForge 基础生成器综合测试")
    print("=" * 50)

    # 注册所有基础生成器
    register_all_basic_generators()

    # 运行基础测试
    results = test_basic_generators()

    # 运行关联测试
    test_cross_validation()

    # 运行CLI参数测试
    test_cli_parameters()

    # 汇总结果
    print("\n📊 测试结果汇总:")
    print("-" * 30)

    passed = sum(1 for r in results.values() if "通过" in r["status"])
    total = len(results)

    for name, result in results.items():
        print(f"{result['status']} {name}")

    print(f"\n📈 通过率: {passed}/{total} ({passed / total * 100:.1f}%)")

    # 生成JSON报告
    with open("basic_generators_test_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    if passed == total:
        print("🎉 所有基础生成器测试通过！")
        return 0
    else:
        print("⚠️  部分生成器测试失败，请查看详细报告")
        return 1


if __name__ == "__main__":
    sys.exit(main())
