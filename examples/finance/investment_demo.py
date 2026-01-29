#!/usr/bin/env python3
"""
DataForge 金融生成器示例 - 投资相关

这个文件展示了DataForge项目中投资相关生成器的使用方法，包括：
- 股票代码 (stock_code)
- 基金代码 (fund_code)
- 债券代码 (bond_code)
- 期货代码 (future_code)
- 投资组合数据

作者: DataForge Team
日期: 2025-11-10
"""

import json
import os
import re
import sys

# 设置环境
sys.path.insert(0, ".")
os.environ["JWT_SECRET_KEY"] = "test-secret-key"

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

    # 演示股票代码生成
    print_subsection("股票代码生成器 (stock_code)")
    try:
        config = GeneratorConfig("stock_code", {}, count=5)
        generator_class = default_registry.get_generator_class("stock_code")
        if generator_class is None:
            raise Exception("Stock code generator not found in registry")
        generator = generator_class(config)
        stock_codes = generator.generate_batch(5)

        for i, stock_code in enumerate(stock_codes, 1):
            print(f"  示例 {i}: {stock_code}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 演示基金代码生成
    print_subsection("基金代码生成器 (fund_code)")
    try:
        config = GeneratorConfig("fund_code", {}, count=5)
        generator_class = default_registry.get_generator_class("fund_code")
        if generator_class is None:
            raise Exception("Fund code generator not found in registry")
        generator = generator_class(config)
        fund_codes = generator.generate_batch(5)

        for i, fund_code in enumerate(fund_codes, 1):
            print(f"  示例 {i}: {fund_code}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 演示债券代码生成
    print_subsection("债券代码生成器 (bond_code)")
    try:
        config = GeneratorConfig("bond_code", {}, count=5)
        generator_class = default_registry.get_generator_class("bond_code")
        if generator_class is None:
            raise Exception("Bond code generator not found in registry")
        generator = generator_class(config)
        bond_codes = generator.generate_batch(5)

        for i, bond_code in enumerate(bond_codes, 1):
            print(f"  示例 {i}: {bond_code}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 演示期货代码生成
    print_subsection("期货代码生成器 (future_code)")
    try:
        config = GeneratorConfig("future_code", {}, count=5)
        generator_class = default_registry.get_generator_class("future_code")
        if generator_class is None:
            raise Exception("Future code generator not found in registry")
        generator = generator_class(config)
        future_codes = generator.generate_batch(5)

        for i, future_code in enumerate(future_codes, 1):
            print(f"  示例 {i}: {future_code}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")


def parameter_configuration():
    """参数配置示例"""
    print_section("2. 参数配置示例")

    # 股票代码生成器参数配置
    print_subsection("股票代码生成器 - 市场配置")
    try:
        # 尝试不同的市场配置
        configs = [
            {},  # 默认配置
            {"market": "shanghai"},  # 上海证券交易所
            {"market": "shenzhen"},  # 深圳证券交易所
            {"market": "nasdaq"},  # 纳斯达克
            {"market": "nyse"},  # 纽约证券交易所
        ]

        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig("stock_code", params, count=3)
            generator_class = default_registry.get_generator_class("stock_code")
            if generator_class is None:
                raise Exception("Stock code generator not found in registry")
            generator = generator_class(config)
            stock_codes = generator.generate_batch(3)

            for j, stock_code in enumerate(stock_codes, 1):
                print(f"    结果 {j}: {stock_code}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 基金代码生成器参数配置
    print_subsection("基金代码生成器 - 基金类型配置")
    try:
        configs = [
            {},  # 默认配置
            {"fund_type": "stock"},  # 股票型基金
            {"fund_type": "bond"},  # 债券型基金
            {"fund_type": "mixed"},  # 混合型基金
            {"fund_type": "money_market"},  # 货币市场基金
        ]

        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig("fund_code", params, count=3)
            generator_class = default_registry.get_generator_class("fund_code")
            if generator_class is None:
                raise Exception("Fund code generator not found in registry")
            generator = generator_class(config)
            fund_codes = generator.generate_batch(3)

            for j, fund_code in enumerate(fund_codes, 1):
                print(f"    结果 {j}: {fund_code}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")


def batch_generation():
    """批量生成示例"""
    print_section("3. 批量生成示例")

    # 批量生成投资组合
    print_subsection("批量生成投资组合")
    try:
        investment_generators = ["stock_code", "fund_code", "bond_code", "future_code"]
        batch_size = 5

        print(f"  生成 {batch_size} 个投资组合:")
        print("  " + "-" * 100)
        print("  序号 | 股票代码  | 基金代码    | 债券代码    | 期货代码")
        print("  " + "-" * 100)

        for i in range(batch_size):
            investment_info = []

            # 生成投资信息
            for generator_name in investment_generators:
                try:
                    config = GeneratorConfig(generator_name, {}, count=1)
                    generator_class = default_registry.get_generator_class(
                        generator_name
                    )
                    if generator_class is None:
                        investment_info.append("N/A")
                    else:
                        generator = generator_class(config)
                        result = generator.generate_single()
                        investment_info.append(str(result))
                except:
                    investment_info.append("N/A")

            # 格式化输出
            stock = investment_info[0][:10].ljust(10)
            fund = investment_info[1][:12].ljust(12)
            bond = investment_info[2][:12].ljust(12)
            future = investment_info[3][:12].ljust(12)

            print(f"  {i+1:2d}    | {stock} | {fund} | {bond} | {future}")

        print("  " + "-" * 100)

    except Exception as e:
        print(f"  ❌ 批量生成失败: {e}")


def validation_examples():
    """数据验证示例"""
    print_section("4. 数据验证示例")

    # 验证股票代码格式
    print_subsection("股票代码格式验证")
    try:
        config = GeneratorConfig("stock_code", {}, count=5)
        generator_class = default_registry.get_generator_class("stock_code")
        if generator_class is None:
            raise Exception("Stock code generator not found in registry")
        generator = generator_class(config)
        stock_codes = generator.generate_batch(5)

        print("  生成的股票代码:")
        # 简单的股票代码验证
        stock_pattern = re.compile(r"^[A-Z]{1,6}\d{4,6}$")

        for i, stock_code in enumerate(stock_codes, 1):
            print(f"    {i}. {stock_code}")

            # 验证股票代码格式
            is_valid = bool(stock_pattern.match(stock_code))
            print(f"       格式验证: {'✅ 有效' if is_valid else '❌ 无效'}")

            # 验证股票代码长度
            length_valid = 6 <= len(stock_code) <= 12
            print(
                f"       长度验证: {'✅ 有效' if length_valid else '❌ 无效'} (长度: {len(stock_code)})"
            )

    except Exception as e:
        print(f"  ❌ 股票代码验证失败: {e}")

    # 验证基金代码格式
    print_subsection("基金代码格式验证")
    try:
        config = GeneratorConfig("fund_code", {}, count=5)
        generator_class = default_registry.get_generator_class("fund_code")
        if generator_class is None:
            raise Exception("Fund code generator not found in registry")
        generator = generator_class(config)
        fund_codes = generator.generate_batch(5)

        print("  生成的基金代码:")
        fund_pattern = re.compile(r"^[A-Z]{2}\d{4}$")

        for i, fund_code in enumerate(fund_codes, 1):
            print(f"    {i}. {fund_code}")

            # 验证基金代码格式
            is_valid = bool(fund_pattern.match(fund_code))
            print(f"       格式验证: {'✅ 有效' if is_valid else '❌ 无效'}")

    except Exception as e:
        print(f"  ❌ 基金代码验证失败: {e}")


def error_handling():
    """错误处理示例"""
    print_section("5. 错误处理示例")

    # 处理不存在的市场
    print_subsection("处理不存在的市场")
    try:
        config = GeneratorConfig("stock_code", {"market": "不存在的市场"}, count=1)
        generator_class = default_registry.get_generator_class("stock_code")
        if generator_class is None:
            raise Exception("Stock code generator not found in registry")
        generator = generator_class(config)
        stock_code = generator.generate_single()
        print(f"  生成的股票代码: {stock_code}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效市场错误: {type(e).__name__}")

    # 处理无效的基金类型
    print_subsection("处理无效的基金类型")
    try:
        config = GeneratorConfig("fund_code", {"fund_type": "不存在的类型"}, count=1)
        generator_class = default_registry.get_generator_class("fund_code")
        if generator_class is None:
            raise Exception("Fund code generator not found in registry")
        generator = generator_class(config)
        fund_code = generator.generate_single()
        print(f"  生成的基金代码: {fund_code}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效基金类型错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print_section("6. 最佳实践示例")

    # 实践1: 生成关联的投资组合
    print_subsection("实践1: 生成关联的投资组合")
    try:
        # 生成一个投资者的投资组合
        investment_portfolio = {}

        # 生成股票投资
        stock_config = GeneratorConfig("stock_code", {"market": "shanghai"}, count=3)
        stock_class = default_registry.get_generator_class("stock_code")
        if stock_class is None:
            raise Exception("Stock code generator not found in registry")
        stock_gen = stock_class(stock_config)
        investment_portfolio["stocks"] = stock_gen.generate_batch(3)

        # 生成基金投资
        fund_config = GeneratorConfig("fund_code", {"fund_type": "mixed"}, count=2)
        fund_class = default_registry.get_generator_class("fund_code")
        if fund_class is None:
            raise Exception("Fund code generator not found in registry")
        fund_gen = fund_class(fund_config)
        investment_portfolio["funds"] = fund_gen.generate_batch(2)

        print("  生成的投资组合:")
        for key, value in investment_portfolio.items():
            print(f"    {key}: {value}")

        print("\n  💡 建议：根据风险偏好配置不同类型的投资产品")

    except Exception as e:
        print(f"  ❌ 关联投资组合生成失败: {e}")

    # 实践2: 批量导出格式化数据
    print_subsection("实践2: 批量导出格式化数据")
    try:
        investment_data = []

        # 生成多个投资组合
        for i in range(3):
            record = {}

            # 生成投资信息
            for field in ["stock_code", "fund_code", "bond_code"]:
                config = GeneratorConfig(field, {}, count=1)
                generator_class = default_registry.get_generator_class(field)
                if generator_class is None:
                    raise Exception(f"{field} generator not found in registry")
                generator = generator_class(config)
                record[field] = generator.generate_single()

            # 添加投资者信息
            name_config = GeneratorConfig("name", {}, count=1)
            name_class = default_registry.get_generator_class("name")
            if name_class is None:
                raise Exception("Name generator not found in registry")
            name_gen = name_class(name_config)
            record["investor_name"] = name_gen.generate_single()

            # 添加投资金额
            record["investment_amount"] = f"{10000 + i * 5000}"

            investment_data.append(record)

        # 导出为JSON格式
        json_output = json.dumps(investment_data, ensure_ascii=False, indent=2)
        print("  JSON格式输出:")
        print(json_output)

    except Exception as e:
        print(f"  ❌ 格式化导出失败: {e}")


def investment_analysis_demo():
    """投资分析演示"""
    print_section("7. 投资分析演示")

    # 演示投资分析数据
    print_subsection("投资分析数据生成")
    try:
        # 生成投资分析报告
        analysis_data = []

        for i in range(3):
            analysis = {
                "portfolio_id": f"PORTFOLIO_{i+1:03d}",
                "total_value": 100000 + i * 25000,
                "stocks_value": 60000 + i * 15000,
                "funds_value": 30000 + i * 7500,
                "bonds_value": 10000 + i * 2500,
                "risk_level": ["低风险", "中风险", "高风险"][i],
                "expected_return": 0.05 + i * 0.02,
                "diversification_score": 0.7 + i * 0.1,
                "created_at": f"2025-11-10T{i+9:02d}:00:00",
            }
            analysis_data.append(analysis)

        print("  投资分析报告:")
        for analysis in analysis_data:
            print(f"\n  投资组合ID: {analysis['portfolio_id']}")
            print(f"    总价值: ¥{analysis['total_value']:,.0f}")
            print(f"    股票价值: ¥{analysis['stocks_value']:,.0f}")
            print(f"    基金价值: ¥{analysis['funds_value']:,.0f}")
            print(f"    债券价值: ¥{analysis['bonds_value']:,.0f}")
            print(f"    风险等级: {analysis['risk_level']}")
            print(f"    预期收益: {analysis['expected_return']:.1%}")
            print(f"    多样化评分: {analysis['diversification_score']:.1f}")

    except Exception as e:
        print(f"  ❌ 投资分析演示失败: {e}")


def main():
    """主函数，运行所有示例"""
    print("🎯 DataForge 金融生成器示例 - 投资相关")
    print("本示例展示了投资相关生成器的各种使用方法")

    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        investment_analysis_demo()

        print_section("✅ 示例演示完成")
        print("🎉 所有投资相关生成器示例已成功运行！")
        print("\n📚 相关文档:")
        print("  • 查看 examples/finance/crypto_demo.py 了解加密货币生成器")
        print("  • 查看 examples/finance/banking_demo.py 了解银行相关生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")

    except Exception as e:
        print(f"\n❌ 示例运行出现错误: {e}")
        print("请检查DataForge环境配置是否正确")


if __name__ == "__main__":
    main()
