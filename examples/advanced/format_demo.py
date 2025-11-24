"""
DataForge 格式化生成器示例
演示各种格式化、特殊字符等生成器的使用方法
"""

import os
import sys
import json
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dataforge import GeneratorConfig, default_factory


def basic_usage():
    """基础用法示例"""
    print("1. 基础用法示例")
    print("=" * 60)
    
    # 特殊字符生成器
    print("\n特殊字符生成器 (special_chars):")
    config = GeneratorConfig("special_chars", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        chars = generator.generate()
        print(f"  示例 {i+1}: {chars}")
    
    # Unicode符号生成器
    print("\nUnicode符号生成器 (unicode_symbols):")
    config = GeneratorConfig("unicode_symbols", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        symbols = generator.generate()
        print(f"  示例 {i+1}: {symbols}")
    
    # 布尔值生成器
    print("\n布尔值生成器 (boolean):")
    config = GeneratorConfig("boolean", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        boolean = generator.generate()
        print(f"  示例 {i+1}: {boolean}")
    
    # 百分比生成器
    print("\n百分比生成器 (percentage):")
    config = GeneratorConfig("percentage", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        percentage = generator.generate()
        print(f"  示例 {i+1}: {percentage}")
    
    # 科学计数法生成器
    print("\n科学计数法生成器 (scientific):")
    config = GeneratorConfig("scientific", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        scientific = generator.generate()
        print(f"  {i+1}: {scientific}")


def parameter_configuration():
    """参数配置示例"""
    print("\n\n2. 参数配置示例")
    print("=" * 60)
    
    # 特殊字符 - 不同类型
    print("\n特殊字符生成器 - 类型配置:")
    char_configs = [
        {"type": "punctuation"},
        {"type": "mathematical"},
        {"type": "currency"},
        {"type": "arrows"},
        {"type": "brackets"},
        {"type": "quotes"}
    ]
    for i, params in enumerate(char_configs, 1):
        config = GeneratorConfig("special_chars", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # Unicode符号 - 不同类别
    print("\nUnicode符号生成器 - 类别配置:")
    symbol_configs = [
        {"category": "arrows"},
        {"category": "mathematical"},
        {"category": "currency"},
        {"category": "emoticons"},
        {"category": "geometric"},
        {"category": "dingbats"}
    ]
    for i, params in enumerate(symbol_configs, 1):
        config = GeneratorConfig("unicode_symbols", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 布尔值 - 概率配置
    print("\n布尔值生成器 - 概率配置:")
    bool_configs = [
        {"true_probability": 0.8},
        {"true_probability": 0.2},
        {"true_probability": 0.5},
        {"true_probability": 0.0},
        {"true_probability": 1.0}
    ]
    for i, params in enumerate(bool_configs, 1):
        config = GeneratorConfig("boolean", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 百分比 - 范围配置
    print("\n百分比生成器 - 范围配置:")
    percent_configs = [
        {"min": 0, "max": 100},
        {"min": 0, "max": 1},
        {"min": -50, "max": 50},
        {"min": 0, "max": 1000},
        {"precision": 2},
        {"precision": 4}
    ]
    for i, params in enumerate(percent_configs, 1):
        config = GeneratorConfig("percentage", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 科学计数法 - 精度配置
    print("\n科学计数法生成器 - 精度配置:")
    scientific_configs = [
        {"precision": 2},
        {"precision": 4},
        {"precision": 6},
        {"min_exponent": -10, "max_exponent": 10},
        {"min_exponent": -5, "max_exponent": 5},
        {"min_exponent": 0, "max_exponent": 5}
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
    
    print("\n批量生成格式化数据:")
    
    # 生成特殊字符
    char_config = GeneratorConfig("special_chars", parameters={
        "type": "mixed",
        "count": 10
    })
    char_gen = default_factory.create_generator(char_config)
    
    # 生成Unicode符号
    symbol_config = GeneratorConfig("unicode_symbols", parameters={
        "category": "mixed",
        "count": 10
    })
    symbol_gen = default_factory.create_generator(symbol_config)
    
    # 生成布尔值序列
    bool_config = GeneratorConfig("boolean", parameters={
        "true_probability": 0.6
    })
    bool_gen = default_factory.create_generator(bool_config)
    
    # 生成百分比序列
    percent_config = GeneratorConfig("percentage", parameters={
        "min": 0,
        "max": 100,
        "precision": 1
    })
    percent_gen = default_factory.create_generator(percent_config)
    
    # 生成5个格式化数据集
    format_data = []
    for i in range(5):
        data = {
            "special_chars": char_gen.generate(),
            "unicode_symbols": symbol_gen.generate(),
            "boolean": bool_gen.generate(),
            "percentage": percent_gen.generate(),
            "scientific": default_factory.create_generator(
                GeneratorConfig("scientific", parameters={"precision": 3})
            ).generate(),
            "created_at": datetime.now().isoformat(),
            "data_id": f"FD_{i+1:03d}"
        }
        format_data.append(data)
    
    # 打印格式化数据
    print("-" * 100)
    print(f"{'ID':<6} | {'特殊字符':<15} | {'Unicode符号':<15} | {'布尔值':<8} | {'百分比':<10} | {'科学计数法'}")
    print("-" * 100)
    for data in format_data:
        special = data['special_chars'][:13] + ".." if len(data['special_chars']) > 15 else data['special_chars']
        unicode = data['unicode_symbols'][:13] + ".." if len(data['unicode_symbols']) > 15 else data['unicode_symbols']
        boolean = str(data['boolean'])
        percentage = data['percentage']
        scientific = data['scientific']
        data_id = data['data_id']
        print(f"{data_id:<6} | {special:<15} | {unicode:<15} | {boolean:<8} | {percentage:<10} | {scientific}")
    print("-" * 100)


def validation_examples():
    """数据验证示例"""
    print("\n\n4. 数据验证示例")
    print("=" * 60)
    
    # 特殊字符验证
    print("\n特殊字符格式验证:")
    config = GeneratorConfig("special_chars", parameters={"type": "punctuation"})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        chars = generator.generate()
        is_valid = generator.validate(chars)
        print(f"  {i+1}. {chars}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '无效'}")
        print(f"     长度: {len(chars)}")
    
    # Unicode符号验证
    print("\nUnicode符号格式验证:")
    config = GeneratorConfig("unicode_symbols", parameters={"category": "emoticons"})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        symbols = generator.generate()
        is_valid = generator.validate(symbols)
        print(f"  {i+1}. {symbols}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '无效'}")
        print(f"     长度: {len(symbols)}")
    
    # 百分比验证
    print("\n百分比格式验证:")
    config = GeneratorConfig("percentage", parameters={"min": 0, "max": 100})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        percentage = generator.generate()
        is_valid = generator.validate(percentage)
        print(f"  {i+1}. {percentage}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '无效'}")
        try:
            value = float(percentage.rstrip('%'))
            in_range = 0 <= value <= 100
            print(f"     范围检查: {'✅ 在范围内' if in_range else '❌ 超出范围'}")
        except:
            print(f"     数值转换: ❌ 无法转换为数字")
    
    # 科学计数法验证
    print("\n科学计数法格式验证:")
    config = GeneratorConfig("scientific", parameters={"precision": 4})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        scientific = generator.generate()
        is_valid = generator.validate(scientific)
        print(f"  {i+1}. {scientific}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '无效'}")
        # 检查是否包含'E'（科学计数法标识符）
        has_e = 'e' in scientific.lower()
        print(f"     科学计数法: {'✅ 是' if has_e else '❌ 否'}")
        print(f"     包含数字: {'✅ 是' if any(c.isdigit() for c in scientific) else '❌ 否'}")


def error_handling():
    """错误处理示例"""
    print("\n\n5. 错误处理示例")
    print("=" * 60)
    
    # 处理无效的字符类型
    print("\n处理无效的字符类型:")
    try:
        config = GeneratorConfig("special_chars", parameters={"type": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的特殊字符: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效字符类型错误: {type(e).__name__}")
    
    # 处理无效的Unicode类别
    print("\n处理无效的Unicode类别:")
    try:
        config = GeneratorConfig("unicode_symbols", parameters={"category": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的Unicode符号: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效Unicode类别错误: {type(e).__name__}")
    
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
    
    # 实践1: 生成完整的格式化系统配置
    print("\n实践1: 生成完整的格式化系统配置")
    format_config = {
        "character_settings": {
            "special_chars": {
                "supported_types": ["punctuation", "mathematical", "currency", "arrows", "brackets", "quotes"],
                "default_count": 10,
                "max_count": 100,
                "exclude_similar": True
            },
            "unicode_symbols": {
                "supported_categories": ["arrows", "mathematical", "currency", "emoticons", "geometric", "dingbats"],
                "default_category": "mixed",
                "default_count": 10,
                "max_count": 50
            }
        },
        "number_settings": {
            "boolean": {
                "default_true_probability": 0.5,
                "allow_custom_probability": True
            },
            "percentage": {
                "default_range": [0, 100],
                "default_precision": 2,
                "allow_custom_range": True
            },
            "scientific": {
                "default_precision": 6,
                "min_exponent": -10,
                "max_exponent": 10,
                "allow_custom_range": True
            }
        },
        "validation_rules": {
            "max_length": 100,
            "allow_empty": False,
            "custom_validation": True
        }
    }
    
    print("  格式化系统配置:")
    for key, value in format_config.items():
        print(f"    {key}:")
        for sub_key, sub_value in value.items():
            print(f"      {sub_key}: {sub_value}")
    
    # 实践2: 批量导出格式化数据
    print("\n实践2: 批量导出格式化数据 (JSON格式)")
    format_data = []
    
    for i in range(3):
        format_record = {
            "record_id": f"format_{i+1:03d}",
            "characters": {
                "punctuation": default_factory.create_generator(
                    GeneratorConfig("special_chars", parameters={"type": "punctuation", "count": 5})
                ).generate(),
                "mathematical": default_factory.create_generator(
                    GeneratorConfig("special_chars", parameters={"type": "mathematical", "count": 5})
                ).generate(),
                "currency": default_factory.create_generator(
                    GeneratorConfig("special_chars", parameters={"type": "currency", "count": 5})
                ).generate()
            },
            "symbols": {
                "arrows": default_factory.create_generator(
                    GeneratorConfig("unicode_symbols", parameters={"category": "arrows", "count": 3})
                ).generate(),
                "mathematical": default_factory.create_generator(
                    GeneratorConfig("unicode_symbols", parameters={"category": "mathematical", "count": 3})
                ).generate(),
                "emoticons": default_factory.create_generator(
                    GeneratorConfig("unicode_symbols", parameters={"category": "emoticons", "count": 3})
                ).generate()
            },
            "numbers": {
                "boolean_sequence": [
                    default_factory.create_generator(
                        GeneratorConfig("boolean", parameters={"true_probability": 0.7})
                    ).generate() for _ in range(5)
                ],
                "percentages": [
                    default_factory.create_generator(
                        GeneratorConfig("percentage", parameters={"min": 0, "max": 100, "precision": 1})
                    ).generate() for _ in range(5)
                ],
                "scientific_values": [
                    default_factory.create_generator(
                        GeneratorConfig("scientific", parameters={"precision": 4})
                    ).generate() for _ in range(5)
                ]
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator_version": "1.0.0",
                "data_purpose": "testing",
                "quality_score": 0.95
            }
        }
        format_data.append(format_record)
    
    print("  JSON格式输出:")
    print(json.dumps(format_data, ensure_ascii=False, indent=2))


def formatting_demo():
    """格式化演示"""
    print("\n\n7. 格式化演示")
    print("=" * 60)
    
    print("\n生成格式化演示数据:")
    
    # 生成密码强度指示器
    print("\n密码强度指示器:")
    strength_levels = [
        {"level": "weak", "chars": 8, "complexity": "low"},
        {"level": "medium", "chars": 12, "complexity": "medium"},
        {"level": "strong", "chars": 16, "complexity": "high"}
    ]
    
    for level_info in strength_levels:
        # 生成对应强度的密码
        password_config = GeneratorConfig("password", parameters={
            "length": level_info["chars"],
            "strength": level_info["complexity"]
        })
        password_gen = default_factory.create_generator(password_config)
        password = password_gen.generate()
        
        # 生成对应的特殊字符来装饰
        char_config = GeneratorConfig("special_chars", parameters={
            "type": "symbols",
            "count": 5
        })
        char_gen = default_factory.create_generator(char_config)
        symbols = char_gen.generate()
        
        print(f"    {level_info['level'].upper()} 密码:")
        print(f"      密码: {password}")
        print(f"      装饰: {symbols}")
        print(f"      复杂度: {level_info['complexity']}")
        print()
    
    # 生成数据格式化示例
    print("\n数据格式化示例:")
    
    # 生成示例数据
    sample_data = {
        "user_id": "user_001",
        "score": 85.67,
        "ratio": 0.75,
        "completion": 0.92
    }
    
    # 生成格式化字符串
    for key, value in sample_data.items():
        if isinstance(value, (int, float)):
            # 数字格式化
            if value >= 1000:
                formatted = f"{value:,}"
            elif value >= 1:
                formatted = f"{value:.2f}"
            else:
                formatted = f"{value:.2f}"
        elif isinstance(value, str):
            # 字符串格式化
            if len(value) > 20:
                formatted = f"{value[:17]}..."
            else:
                formatted = value
        else:
            formatted = str(value)
        
        print(f"    {key}: {formatted}")
    
    # 生成表格格式
    print("\n表格格式演示:")
    table_data = [
        {"name": "产品A", "price": 299.99, "stock": 150, "rating": 4.5},
        {"name": "产品B", "price": 199.99, "stock": 75, "rating": 4.2},
        {"name": "产品C", "price": 99.99, "stock": 200, "rating": 4.8}
    ]
    
    print("    产品名称    | 价格     | 库存  | 评分")
    print("    ----------|----------|------|------")
    for item in table_data:
        print(f"    {item['name']:<10} | {item['price']:>8.2f} | {item['stock']:>6} | {item['rating']:>5.1f}")
    
    # 生成进度条
    print("\n进度条演示:")
    progress_values = [0.1, 0.25, 0.5, 0.75, 0.9, 1.0]
    
    for progress in progress_values:
        bar_length = 30
        filled_length = int(bar_length * progress)
        empty_length = bar_length - filled_length
        bar = "█" * filled_length + "░" * empty_length
        percentage = f"{progress * 100:.0f}%"
        print(f"    [{bar}] {percentage}")
    
    # 生成状态指示器
    print("\n状态指示器演示:")
    statuses = [
        {"status": "success", "symbol": "✅", "color": "green"},
        {"status": "warning", "symbol": "⚠️", "color": "yellow"},
        {"status": "error", "symbol": "❌", "color": "red"},
        {"status": "info", "symbol": "ℹ️", "color": "blue"}
    ]
    
    for status_info in statuses:
        print(f"    {status_info['symbol']} {status_info['status']} ({status_info['color']})")


def main():
    """主函数"""
    print("🎯 DataForge 格式化生成器示例")
    print("本示例展示了格式化相关生成器的各种使用方法\n")
    
    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        formatting_demo()
        
        print("\n" + "=" * 60)
        print("✅ 示例演示完成")
        print("=" * 60)
        print("🎉 所有格式化相关生成器示例已成功运行！")
        
        print("\n📚 相关文档:")
        print("  • 查看 examples/advanced/security_demo.py 了解安全相关生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")
        
    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()