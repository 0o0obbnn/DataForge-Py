#!/usr/bin/env python3
"""
DataForge 金融生成器示例 - 银行相关

这个文件展示了DataForge项目中银行相关生成器的使用方法，包括：
- 银行卡号 (bankcard)
- 银行账户 (bank_account)
- 金融衍生品 (derivatives)
- 市场数据 (market_data)
- 金融报告 (financial_report)

作者: DataForge Team
日期: 2025-11-10
"""

import json
import os
import re
import sys

# 设置环境
sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

from dataforge.core.factory import default_registry
from dataforge.core.generator import GeneratorConfig


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_subsection(title: str):
    """打印子章节标题"""
    print(f"\n{'─'*40}")
    print(f"  {title}")
    print(f"{'─'*40}")


def basic_usage():
    """基础用法示例"""
    print_section("1. 基础用法示例")

    # 演示银行卡号生成
    print_subsection("银行卡号生成器 (bankcard)")
    try:
        config = GeneratorConfig('bankcard', {}, count=3)
        generator_class = default_registry.get_generator_class('bankcard')
        if generator_class is None:
            raise Exception("Bankcard generator not found in registry")
        generator = generator_class(config)
        bankcards = generator.generate_batch(3)

        for i, bankcard in enumerate(bankcards, 1):
            print(f"  示例 {i}: {bankcard}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 演示银行账户生成
    print_subsection("银行账户生成器 (bank_account)")
    try:
        config = GeneratorConfig('bank_account', {}, count=3)
        generator_class = default_registry.get_generator_class('bank_account')
        if generator_class is None:
            raise Exception("Bank account generator not found in registry")
        generator = generator_class(config)
        accounts = generator.generate_batch(3)

        for i, account in enumerate(accounts, 1):
            print(f"  示例 {i}: {account}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 演示市场数据生成
    print_subsection("市场数据生成器 (market_data)")
    try:
        config = GeneratorConfig('market_data', {}, count=3)
        generator_class = default_registry.get_generator_class('market_data')
        if generator_class is None:
            raise Exception("Market data generator not found in registry")
        generator = generator_class(config)
        market_data = generator.generate_batch(3)

        for i, data in enumerate(market_data, 1):
            print(f"  示例 {i}: {data}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")


def parameter_configuration():
    """参数配置示例"""
    print_section("2. 参数配置示例")

    # 银行卡号生成器参数配置
    print_subsection("银行卡号生成器 - 银行类型配置")
    try:
        # 尝试不同的银行类型配置
        configs = [
            {},  # 默认配置
            {"bank_type": "icbc"},  # 工商银行
            {"bank_type": "ccb"},   # 建设银行
            {"bank_type": "abc"},   # 农业银行
        ]

        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig('bankcard', params, count=2)
            generator_class = default_registry.get_generator_class('bankcard')
            if generator_class is None:
                raise Exception("Bankcard generator not found in registry")
            generator = generator_class(config)
            bankcards = generator.generate_batch(2)

            for j, bankcard in enumerate(bankcards, 1):
                print(f"    结果 {j}: {bankcard}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 银行账户生成器参数配置
    print_subsection("银行账户生成器 - 账户类型配置")
    try:
        configs = [
            {},  # 默认配置
            {"account_type": "savings"},  # 储蓄账户
            {"account_type": "checking"},  # 支票账户
            {"account_type": "credit"},     # 信用账户
        ]

        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig('bank_account', params, count=2)
            generator_class = default_registry.get_generator_class('bank_account')
            if generator_class is None:
                raise Exception("Bank account generator not found in registry")
            generator = generator_class(config)
            accounts = generator.generate_batch(2)

            for j, account in enumerate(accounts, 1):
                print(f"    结果 {j}: {account}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")


def batch_generation():
    """批量生成示例"""
    print_section("3. 批量生成示例")

    # 批量生成完整银行信息
    print_subsection("批量生成完整银行信息")
    try:
        banking_generators = ['bankcard', 'bank_account', 'derivatives']
        batch_size = 5

        print(f"  生成 {batch_size} 个人的银行信息:")
        print("  " + "-" * 100)
        print("  序号 | 银行卡号        | 银行账户        | 衍生品")
        print("  " + "-" * 100)

        for i in range(batch_size):
            banking_info = []

            # 生成银行信息
            for generator_name in banking_generators:
                try:
                    config = GeneratorConfig(generator_name, {}, count=1)
                    generator_class = default_registry.get_generator_class(generator_name)
                    if generator_class is None:
                        banking_info.append("N/A")
                    else:
                        generator = generator_class(config)
                        result = generator.generate_single()
                        banking_info.append(str(result))
                except:
                    banking_info.append("N/A")

            # 格式化输出
            bankcard = banking_info[0][:16].ljust(16)
            account = banking_info[1][:16].ljust(16)
            derivatives = banking_info[2][:60].ljust(60)

            print(f"  {i+1:2d}    | {bankcard} | {account} | {derivatives}")

        print("  " + "-" * 100)

    except Exception as e:
        print(f"  ❌ 批量生成失败: {e}")


def validation_examples():
    """数据验证示例"""
    print_section("4. 数据验证示例")

    # 验证银行卡号格式
    print_subsection("银行卡号格式验证")
    try:
        config = GeneratorConfig('bankcard', {}, count=5)
        generator_class = default_registry.get_generator_class('bankcard')
        if generator_class is None:
            raise Exception("Bankcard generator not found in registry")
        generator = generator_class(config)
        bankcards = generator.generate_batch(5)

        print("  生成的银行卡号:")
        # 简单的银行卡号验证（16-19位数字）
        bankcard_pattern = re.compile(r'^\d{16,19}$')

        for i, bankcard in enumerate(bankcards, 1):
            print(f"    {i}. {bankcard}")

            # 验证银行卡号格式
            is_valid = bool(bankcard_pattern.match(bankcard))
            print(f"       格式验证: {'✅ 有效' if is_valid else '❌ 无效'}")

            # 验证Luhn算法（如果有的话）
            try:
                luhn_valid = generator.validate(bankcard)
                print(f"       Luhn验证: {'✅ 通过' if luhn_valid else '❌ 未通过'}")
            except:
                print("       Luhn验证: ⚠️ 无法验证")

    except Exception as e:
        print(f"  ❌ 银行卡验证失败: {e}")


def error_handling():
    """错误处理示例"""
    print_section("5. 错误处理示例")

    # 处理不存在的银行类型
    print_subsection("处理不存在的银行类型")
    try:
        config = GeneratorConfig('bankcard', {"bank_type": "不存在的银行"}, count=1)
        generator_class = default_registry.get_generator_class('bankcard')
        if generator_class is None:
            raise Exception("Bankcard generator not found in registry")
        generator = generator_class(config)
        bankcard = generator.generate_single()
        print(f"  生成的银行卡号: {bankcard}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效银行类型错误: {type(e).__name__}")

    # 处理无效的账户类型
    print_subsection("处理无效的账户类型")
    try:
        config = GeneratorConfig('bank_account', {"account_type": "不存在的账户"}, count=1)
        generator_class = default_registry.get_generator_class('bank_account')
        if generator_class is None:
            raise Exception("Bank account generator not found in registry")
        generator = generator_class(config)
        account = generator.generate_single()
        print(f"  生成的银行账户: {account}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效账户类型错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print_section("6. 最佳实践示例")

    # 实践1: 生成关联的银行信息
    print_subsection("实践1: 生成关联的银行信息")
    try:
        # 生成一个客户的完整银行信息
        customer_banking = {}

        # 生成银行卡信息
        bankcard_config = GeneratorConfig('bankcard', {"bank_type": "icbc"}, count=1)
        bankcard_class = default_registry.get_generator_class('bankcard')
        if bankcard_class is None:
            raise Exception("Bankcard generator not found in registry")
        bankcard_gen = bankcard_class(bankcard_config)
        customer_banking['bankcard'] = bankcard_gen.generate_single()

        # 生成关联的银行账户
        account_config = GeneratorConfig('bank_account', {"account_type": "savings"}, count=1)
        account_class = default_registry.get_generator_class('bank_account')
        if account_class is None:
            raise Exception("Bank account generator not found in registry")
        account_gen = account_class(account_config)
        customer_banking['bank_account'] = account_gen.generate_single()

        print("  生成的客户银行信息:")
        for key, value in customer_banking.items():
            print(f"    {key}: {value}")

        print("\n  💡 建议：使用相同银行的卡和账户生成更真实的数据")

    except Exception as e:
        print(f"  ❌ 关联银行信息生成失败: {e}")

    # 实践2: 批量导出格式化数据
    print_subsection("实践2: 批量导出格式化数据")
    try:
        banking_data = []

        # 生成多条银行信息
        for i in range(3):
            record = {}

            # 生成银行信息
            for field in ['bankcard', 'bank_account', 'derivatives']:
                config = GeneratorConfig(field, {}, count=1)
                generator_class = default_registry.get_generator_class(field)
                if generator_class is None:
                    raise Exception(f"{field} generator not found in registry")
                generator = generator_class(config)
                record[field] = generator.generate_single()

            # 添加客户信息
            name_config = GeneratorConfig('name', {}, count=1)
            name_class = default_registry.get_generator_class('name')
            if name_class is None:
                raise Exception("Name generator not found in registry")
            name_gen = name_class(name_config)
            record['customer_name'] = name_gen.generate_single()

            banking_data.append(record)

        # 导出为JSON格式
        json_output = json.dumps(banking_data, ensure_ascii=False, indent=2)
        print("  JSON格式输出:")
        print(json_output)

    except Exception as e:
        print(f"  ❌ 格式化导出失败: {e}")


def financial_instruments_demo():
    """金融工具演示"""
    print_section("7. 金融工具演示")

    # 演示各种金融工具
    print_subsection("金融工具生成")
    try:
        financial_generators = ['derivatives', 'market_data', 'financial_report']

        for gen_name in financial_generators:
            try:
                config = GeneratorConfig(gen_name, {}, count=2)
                generator_class = default_registry.get_generator_class(gen_name)
                if generator_class is None:
                    raise Exception(f"{gen_name} generator not found in registry")
                generator = generator_class(config)
                results = generator.generate_batch(2)

                print(f"\n  {gen_name}:")
                for i, result in enumerate(results, 1):
                    print(f"    示例 {i}: {result}")
            except Exception as e:
                print(f"  ❌ {gen_name} 生成失败: {e}")

    except Exception as e:
        print(f"  ❌ 金融工具演示失败: {e}")


def main():
    """主函数，运行所有示例"""
    print("🎯 DataForge 金融生成器示例 - 银行相关")
    print("本示例展示了银行相关生成器的各种使用方法")

    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        financial_instruments_demo()

        print_section("✅ 示例演示完成")
        print("🎉 所有银行相关生成器示例已成功运行！")
        print("\n📚 相关文档:")
        print("  • 查看 examples/finance/investment_demo.py 了解投资相关生成器")
        print("  • 查看 examples/finance/crypto_demo.py 了解加密货币生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")

    except Exception as e:
        print(f"\n❌ 示例运行出现错误: {e}")
        print("请检查DataForge环境配置是否正确")


if __name__ == "__main__":
    main()
