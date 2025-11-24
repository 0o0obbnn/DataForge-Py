"""
DataForge 数值生成器示例
演示各种数值相关生成器的使用方法
"""

import os
import sys
import json
import math
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dataforge import GeneratorConfig, default_factory


def basic_usage():
    """基础用法示例"""
    print("1. 基础用法示例")
    print("=" * 60)
    
    # 整数生成器
    print("\n整数生成器 (integer):")
    config = GeneratorConfig("integer", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        num = generator.generate()
        print(f"  示例 {i+1}: {num}")
    
    # 数字生成器（可用作浮点数）
    print("\n数字生成器 (number):")
    config = GeneratorConfig("number", parameters={"type": "float"})
    generator = default_factory.create_generator(config)
    for i in range(3):
        num = generator.generate()
        print(f"  示例 {i+1}: {num}")
    
    # 小数生成器
    print("\n小数生成器 (decimal):")
    config = GeneratorConfig("decimal", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        num = generator.generate()
        print(f"  示例 {i+1}: {num}")
    
    # 百分比生成器
    print("\n百分比生成器 (percentage):")
    config = GeneratorConfig("percentage", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        percent = generator.generate()
        print(f"  示例 {i+1}: {percent}")
    
    # 科学计数法生成器
    print("\n科学计数法生成器 (scientific):")
    config = GeneratorConfig("scientific", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        scientific = generator.generate()
        print(f"  示例 {i+1}: {scientific}")


def parameter_configuration():
    """参数配置示例"""
    print("\n\n2. 参数配置示例")
    print("=" * 60)
    
    # 整数 - 不同范围
    print("\n整数生成器 - 范围配置:")
    int_configs = [
        {"min": 0, "max": 10},
        {"min": 100, "max": 200},
        {"min": -50, "max": 50},
        {"min": 1000, "max": 2000}
    ]
    for i, params in enumerate(int_configs, 1):
        config = GeneratorConfig("integer", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 数字生成器（浮点数） - 不同精度
    print("\n数字生成器（浮点数） - 精度配置:")
    float_configs = [
        {"type": "float", "min": 0.0, "max": 1.0},
        {"type": "float", "min": -100.0, "max": 100.0},
        {"type": "float", "decimal_places": 2},
        {"type": "float", "decimal_places": 4},
        {"type": "float", "decimal_places": 6}
    ]
    for i, params in enumerate(float_configs, 1):
        config = GeneratorConfig("number", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 小数 - 不同小数位数
    print("\n小数生成器 - 小数位数配置:")
    decimal_configs = [
        {"min": 0, "max": 100, "decimal_places": 2},
        {"min": 0, "max": 1000, "decimal_places": 3},
        {"min": -100, "max": 100, "decimal_places": 4},
        {"decimal_places": 1},
        {"decimal_places": 5}
    ]
    for i, params in enumerate(decimal_configs, 1):
        config = GeneratorConfig("decimal", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 百分比 - 不同范围
    print("\n百分比生成器 - 范围配置:")
    percent_configs = [
        {"min": 0, "max": 100},
        {"min": 0, "max": 1},
        {"min": -50, "max": 50},
        {"precision": 1},
        {"precision": 3}
    ]
    for i, params in enumerate(percent_configs, 1):
        config = GeneratorConfig("percentage", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 科学计数法 - 不同指数范围
    print("\n科学计数法生成器 - 指数范围配置:")
    scientific_configs = [
        {"min_exponent": -5, "max_exponent": 5},
        {"min_exponent": -10, "max_exponent": 10},
        {"precision": 2},
        {"precision": 4},
        {"precision": 6}
    ]
    for i, params in enumerate(scientific_configs, 1):
        config = GeneratorConfig("scientific", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")


def batch_generation():
    """批量生成示例"""
    print("\n\n3. 批量生成示例")
    print("=" * 60)
    
    print("\n批量生成数值数据:")
    
    # 生成整数
    int_config = GeneratorConfig("integer", parameters={"min": 1, "max": 100})
    int_gen = default_factory.create_generator(int_config)
    
    # 生成浮点数
    float_config = GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 1.0, "decimal_places": 3})
    float_gen = default_factory.create_generator(float_config)
    
    # 生成小数
    decimal_config = GeneratorConfig("decimal", parameters={"min": 0, "max": 1000, "decimal_places": 2})
    decimal_gen = default_factory.create_generator(decimal_config)
    
    # 生成百分比
    percent_config = GeneratorConfig("percentage", parameters={"min": 0, "max": 100, "precision": 1})
    percent_gen = default_factory.create_generator(percent_config)
    
    # 生成科学计数法
    scientific_config = GeneratorConfig("scientific", parameters={"precision": 4})
    scientific_gen = default_factory.create_generator(scientific_config)
    
    # 生成5条数值数据
    numeric_data = []
    for i in range(5):
        data = {
            "id": i + 1,
            "integer": int_gen.generate(),
            "float": float_gen.generate(),
            "decimal": decimal_gen.generate(),
            "percentage": percent_gen.generate(),
            "scientific": scientific_gen.generate(),
            "created_at": datetime.now().isoformat()
        }
        numeric_data.append(data)
    
    # 打印数值数据
    print("-" * 100)
    print(f"{'ID':<4} | {'整数':<8} | {'浮点数':<10} | {'小数':<12} | {'百分比':<10} | {'科学计数法'}")
    print("-" * 100)
    for data in numeric_data:
        print(f"{data['id']:<4} | {data['integer']:<8} | {data['float']:<10} | {data['decimal']:<12} | {data['percentage']:<10} | {data['scientific']}")
    print("-" * 100)


def validation_examples():
    """数据验证示例"""
    print("\n\n4. 数据验证示例")
    print("=" * 60)
    
    # 整数验证
    print("\n整数格式验证:")
    config = GeneratorConfig("integer", parameters={"min": 1, "max": 100})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        num = generator.generate()
        is_valid = generator.validate(num)
        in_range = 1 <= num <= 100
        print(f"  {i+1}. {num}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     范围检查: {'✅ 在范围内' if in_range else '❌ 超出范围'}")
    
    # 浮点数验证
    print("\n浮点数格式验证:")
    config = GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 1.0})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        num = generator.generate()
        is_valid = generator.validate(num)
        in_range = 0.0 <= num <= 1.0
        print(f"  {i+1}. {num}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     范围检查: {'✅ 在范围内' if in_range else '❌ 超出范围'}")
    
    # 小数验证
    print("\n小数格式验证:")
    config = GeneratorConfig("decimal", parameters={"min": 0, "max": 100, "decimal_places": 2})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        num = generator.generate()
        is_valid = generator.validate(num)
        in_range = 0 <= num <= 100
        decimal_places = len(str(num).split('.')[-1]) if '.' in str(num) else 0
        correct_places = decimal_places <= 2
        print(f"  {i+1}. {num}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     范围检查: {'✅ 在范围内' if in_range else '❌ 超出范围'}")
        print(f"     小数位数: {decimal_places} (≤2: {'✅' if correct_places else '❌'})")
    
    # 百分比验证
    print("\n百分比格式验证:")
    config = GeneratorConfig("percentage", parameters={"min": 0, "max": 100})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        percent = generator.generate()
        is_valid = generator.validate(percent)
        try:
            value = float(percent.rstrip('%'))
            in_range = 0 <= value <= 100
        except:
            in_range = False
        print(f"  {i+1}. {percent}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     范围检查: {'✅ 在范围内' if in_range else '❌ 超出范围'}")
    
    # 科学计数法验证
    print("\n科学计数法格式验证:")
    config = GeneratorConfig("scientific", parameters={"precision": 4})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        scientific = generator.generate()
        is_valid = generator.validate(scientific)
        has_e = 'e' in scientific.lower()
        print(f"  {i+1}. {scientific}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     科学计数法: {'✅ 是' if has_e else '❌ 否'}")


def error_handling():
    """错误处理示例"""
    print("\n\n5. 错误处理示例")
    print("=" * 60)
    
    # 处理无效的整数范围
    print("\n处理无效的整数范围:")
    try:
        config = GeneratorConfig("integer", parameters={"min": 100, "max": 50})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的整数: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效整数范围错误: {type(e).__name__}")
    
    # 处理无效的浮点数精度
    print("\n处理无效的浮点数精度:")
    try:
        config = GeneratorConfig("number", parameters={"type": "float", "decimal_places": -1})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的浮点数: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效浮点数精度错误: {type(e).__name__}")
    
    # 处理无效的小数位数
    print("\n处理无效的小数位数:")
    try:
        config = GeneratorConfig("decimal", parameters={"decimal_places": -1})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的小数: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效小数位数错误: {type(e).__name__}")
    
    # 处理无效的百分比范围
    print("\n处理无效的百分比范围:")
    try:
        config = GeneratorConfig("percentage", parameters={"min": 200, "max": 100})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的百分比: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效百分比范围错误: {type(e).__name__}")
    
    # 处理无效的科学计数法精度
    print("\n处理无效的科学计数法精度:")
    try:
        config = GeneratorConfig("scientific", parameters={"precision": -1})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的科学计数法: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效科学计数法精度错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print("\n\n6. 最佳实践示例")
    print("=" * 60)
    
    # 实践1: 生成完整的数值配置
    print("\n实践1: 生成完整的数值配置")
    numeric_config = {
        "integer_settings": {
            "default_range": {"min": 0, "max": 100},
            "max_range": {"min": -1000000, "max": 1000000},
            "allow_custom_range": True
        },
        "float_settings": {
            "default_range": {"min": 0.0, "max": 1.0},
            "default_precision": 6,
            "max_precision": 15,
            "allow_custom_precision": True
        },
        "decimal_settings": {
            "default_range": {"min": 0, "max": 100},
            "default_decimal_places": 2,
            "max_decimal_places": 10,
            "allow_custom_places": True
        },
        "percentage_settings": {
            "default_range": {"min": 0, "max": 100},
            "default_precision": 2,
            "allow_custom_range": True
        },
        "scientific_settings": {
            "default_precision": 6,
            "min_exponent": -20,
            "max_exponent": 20,
            "allow_custom_exponent": True
        }
    }
    
    print("  数值配置:")
    for key, value in numeric_config.items():
        print(f"    {key}:")
        for sub_key, sub_value in value.items():
            if isinstance(sub_value, dict):
                print(f"      {sub_key}: {sub_value}")
            else:
                print(f"      {sub_key}: {sub_value}")
    
    # 实践2: 批量导出数值数据
    print("\n实践2: 批量导出数值数据 (JSON格式)")
    numeric_data = []
    
    for i in range(3):
        numeric_record = {
            "record_id": f"numeric_{i+1:03d}",
            "measurements": {
                "temperature": default_factory.create_generator(
                    GeneratorConfig("number", parameters={"type": "float", "min": -50.0, "max": 50.0, "decimal_places": 1})
                ).generate(),
                "humidity": default_factory.create_generator(
                    GeneratorConfig("percentage", parameters={"min": 0, "max": 100, "precision": 1})
                ).generate(),
                "pressure": default_factory.create_generator(
                    GeneratorConfig("decimal", parameters={"min": 900, "max": 1100, "decimal_places": 2})
                ).generate(),
                "wind_speed": default_factory.create_generator(
                    GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 100.0, "decimal_places": 2})
                ).generate()
            },
            "statistics": {
                "count": default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 1, "max": 1000})
                ).generate(),
                "mean": default_factory.create_generator(
                    GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 100.0, "decimal_places": 3})
                ).generate(),
                "median": default_factory.create_generator(
                    GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 100.0, "decimal_places": 3})
                ).generate(),
                "std_dev": default_factory.create_generator(
                    GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 50.0, "decimal_places": 3})
                ).generate()
            },
            "financial": {
                "price": default_factory.create_generator(
                    GeneratorConfig("decimal", parameters={"min": 0.01, "max": 10000.0, "decimal_places": 2})
                ).generate(),
                "change": default_factory.create_generator(
                    GeneratorConfig("number", parameters={"type": "float", "min": -100.0, "max": 100.0, "decimal_places": 2})
                ).generate(),
                "change_percent": default_factory.create_generator(
                    GeneratorConfig("percentage", parameters={"min": -100, "max": 100, "precision": 2})
                ).generate(),
                "volume": default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 1000, "max": 10000000})
                ).generate()
            },
            "scientific": {
                "atomic_mass": default_factory.create_generator(
                    GeneratorConfig("scientific", parameters={"precision": 6})
                ).generate(),
                "planetary_distance": default_factory.create_generator(
                    GeneratorConfig("scientific", parameters={"min_exponent": 6, "max_exponent": 12, "precision": 4})
                ).generate(),
                "quantum_energy": default_factory.create_generator(
                    GeneratorConfig("scientific", parameters={"min_exponent": -20, "max_exponent": -10, "precision": 3})
                ).generate()
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator_version": "1.0.0",
                "data_purpose": "testing",
                "quality_score": 0.95
            }
        }
        numeric_data.append(numeric_record)
    
    print("  JSON格式输出:")
    print(json.dumps(numeric_data, ensure_ascii=False, indent=2))


def numeric_demo():
    """数值演示"""
    print("\n\n7. 数值演示")
    print("=" * 60)
    
    print("\n生成统计数据演示:")
    
    # 生成统计报告
    print("\n统计报告:")
    stats_report = {
        "report_id": default_factory.create_generator(
            GeneratorConfig("string", parameters={"length": 8, "type": "alphanumeric", "prefix": "STAT_"})
        ).generate(),
        "sample_size": default_factory.create_generator(
            GeneratorConfig("integer", parameters={"min": 100, "max": 10000})
        ).generate(),
        "metrics": {
            "mean": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 100.0, "decimal_places": 3})
            ).generate(),
            "median": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 100.0, "decimal_places": 3})
            ).generate(),
            "mode": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 100.0, "decimal_places": 3})
            ).generate(),
            "std_dev": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 50.0, "decimal_places": 3})
            ).generate(),
            "variance": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 2500.0, "decimal_places": 3})
            ).generate(),
            "skewness": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": -5.0, "max": 5.0, "decimal_places": 3})
            ).generate(),
            "kurtosis": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": -5.0, "max": 10.0, "decimal_places": 3})
            ).generate()
        },
        "percentiles": {
            "p25": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 100.0, "decimal_places": 3})
            ).generate(),
            "p50": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 100.0, "decimal_places": 3})
            ).generate(),
            "p75": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 100.0, "decimal_places": 3})
            ).generate(),
            "p90": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 100.0, "decimal_places": 3})
            ).generate(),
            "p95": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 100.0, "decimal_places": 3})
            ).generate(),
            "p99": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 100.0, "decimal_places": 3})
            ).generate()
        }
    }
    
    print(f"  报告ID: {stats_report['report_id']}")
    print(f"  样本大小: {stats_report['sample_size']}")
    print("  指标:")
    for key, value in stats_report['metrics'].items():
        print(f"    {key}: {value}")
    print("  百分位数:")
    for key, value in stats_report['percentiles'].items():
        print(f"    {key}: {value}")
    
    # 生成财务数据
    print("\n财务数据演示:")
    
    stocks = []
    for i in range(3):
        stock = {
            "symbol": default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 4, "type": "alphabetic", "prefix": "STK_"})
            ).generate(),
            "price": default_factory.create_generator(
                GeneratorConfig("decimal", parameters={"min": 10.0, "max": 1000.0, "decimal_places": 2})
            ).generate(),
            "change": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": -50.0, "max": 50.0, "decimal_places": 2})
            ).generate(),
            "change_percent": default_factory.create_generator(
                GeneratorConfig("percentage", parameters={"min": -20, "max": 20, "precision": 2})
            ).generate(),
            "volume": default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 10000, "max": 10000000})
            ).generate(),
            "market_cap": default_factory.create_generator(
                GeneratorConfig("scientific", parameters={"min_exponent": 9, "max_exponent": 12, "precision": 4})
            ).generate(),
            "pe_ratio": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 5.0, "max": 100.0, "decimal_places": 2})
            ).generate(),
            "dividend_yield": default_factory.create_generator(
                GeneratorConfig("percentage", parameters={"min": 0, "max": 10, "precision": 2})
            ).generate()
        }
        stocks.append(stock)
    
    print("  股票列表:")
    for stock in stocks:
        print(f"    代码: {stock['symbol']}")
        print(f"    价格: ${stock['price']}")
        print(f"    涨跌: {stock['change']:+.2f} ({stock['change_percent']})")
        print(f"    成交量: {stock['volume']:,}")
        print(f"    市值: ${stock['market_cap']}")
        print(f"    市盈率: {stock['pe_ratio']}")
        print(f"    股息率: {stock['dividend_yield']}")
        print()
    
    # 生成科学数据
    print("\n科学数据演示:")
    
    experiments = []
    for i in range(3):
        experiment = {
            "experiment_id": default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 8, "type": "alphanumeric", "prefix": "EXP_"})
            ).generate(),
            "measurements": {
                "temperature": default_factory.create_generator(
                    GeneratorConfig("number", parameters={"type": "float", "min": -273.15, "max": 5000.0, "decimal_places": 2})
                ).generate(),
                "pressure": default_factory.create_generator(
                    GeneratorConfig("scientific", parameters={"min_exponent": -1, "max_exponent": 9, "precision": 4})
                ).generate(),
                "concentration": default_factory.create_generator(
                    GeneratorConfig("scientific", parameters={"min_exponent": -10, "max_exponent": 0, "precision": 6})
                ).generate(),
                "ph": default_factory.create_generator(
                    GeneratorConfig("number", parameters={"type": "float", "min": 0.0, "max": 14.0, "decimal_places": 2})
                ).generate(),
                "viscosity": default_factory.create_generator(
                    GeneratorConfig("number", parameters={"type": "float", "min": 0.001, "max": 10000.0, "decimal_places": 4})
                ).generate(),
                "density": default_factory.create_generator(
                    GeneratorConfig("number", parameters={"type": "float", "min": 0.1, "max": 50.0, "decimal_places": 3})
                ).generate()
            },
            "uncertainty": {
                "temperature_err": default_factory.create_generator(
                    GeneratorConfig("number", parameters={"type": "float", "min": 0.01, "max": 10.0, "decimal_places": 3})
                ).generate(),
                "pressure_err": default_factory.create_generator(
                    GeneratorConfig("number", parameters={"type": "float", "min": 0.001, "max": 100.0, "decimal_places": 3})
                ).generate(),
                "concentration_err": default_factory.create_generator(
                    GeneratorConfig("scientific", parameters={"min_exponent": -12, "max_exponent": -2, "precision": 3})
                ).generate()
            },
            "timestamp": datetime.now().isoformat()
        }
        experiments.append(experiment)
    
    print("  实验数据:")
    for exp in experiments:
        print(f"    实验ID: {exp['experiment_id']}")
        print("    测量值:")
        for key, value in exp['measurements'].items():
            print(f"      {key}: {value}")
        print("    不确定度:")
        for key, value in exp['uncertainty'].items():
            print(f"      {key}: ±{value}")
        print(f"    时间戳: {exp['timestamp'][:19]}")
        print()
    
    # 生成性能指标
    print("\n性能指标演示:")
    
    performance_metrics = {
        "response_time": {
            "min": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 10.0, "max": 100.0, "decimal_places": 2})
            ).generate(),
            "max": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 1000.0, "max": 10000.0, "decimal_places": 2})
            ).generate(),
            "mean": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 100.0, "max": 1000.0, "decimal_places": 2})
            ).generate(),
            "p95": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 500.0, "max": 5000.0, "decimal_places": 2})
            ).generate(),
            "p99": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 1000.0, "max": 10000.0, "decimal_places": 2})
            ).generate()
        },
        "throughput": {
            "requests_per_second": default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 100, "max": 10000})
            ).generate(),
            "bytes_per_second": default_factory.create_generator(
                GeneratorConfig("scientific", parameters={"min_exponent": 6, "max_exponent": 9, "precision": 3})
            ).generate(),
            "concurrent_users": default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 10, "max": 1000})
            ).generate()
        },
        "error_rates": {
            "error_rate": default_factory.create_generator(
                GeneratorConfig("percentage", parameters={"min": 0, "max": 5, "precision": 3})
            ).generate(),
            "timeout_rate": default_factory.create_generator(
                GeneratorConfig("percentage", parameters={"min": 0, "max": 2, "precision": 3})
            ).generate(),
            "failure_rate": default_factory.create_generator(
                GeneratorConfig("percentage", parameters={"min": 0, "max": 1, "precision": 3})
            ).generate()
        },
        "resource_usage": {
            "cpu_usage": default_factory.create_generator(
                GeneratorConfig("percentage", parameters={"min": 10, "max": 90, "precision": 1})
            ).generate(),
            "memory_usage": default_factory.create_generator(
                GeneratorConfig("percentage", parameters={"min": 20, "max": 80, "precision": 1})
            ).generate(),
            "disk_usage": default_factory.create_generator(
                GeneratorConfig("percentage", parameters={"min": 30, "max": 70, "precision": 1})
            ).generate(),
            "network_usage": default_factory.create_generator(
                GeneratorConfig("number", parameters={"type": "float", "min": 1.0, "max": 1000.0, "decimal_places": 2})
            ).generate()
        }
    }
    
    print("  响应时间 (ms):")
    for key, value in performance_metrics['response_time'].items():
        print(f"    {key}: {value}")
    
    print("  吞吐量:")
    for key, value in performance_metrics['throughput'].items():
        if key == "bytes_per_second":
            print(f"    {key}: {value} bytes/s")
        else:
            print(f"    {key}: {value}")
    
    print("  错误率:")
    for key, value in performance_metrics['error_rates'].items():
        print(f"    {key}: {value}")
    
    print("  资源使用率:")
    for key, value in performance_metrics['resource_usage'].items():
        unit = "%" if "usage" in key else "Mbps"
        print(f"    {key}: {value} {unit}")


def main():
    """主函数"""
    print("🔢 DataForge 数值生成器示例")
    print("本示例展示了数值相关生成器的各种使用方法\n")
    
    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        numeric_demo()
        
        print("\n" + "=" * 60)
        print("✅ 示例演示完成")
        print("=" * 60)
        print("🎉 所有数值相关生成器示例已成功运行！")
        
        print("\n📚 相关文档:")
        print("  • 查看 examples/identifier/identifier_demo.py 了解标识符相关生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")
        
    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()