"""
DataForge 文本生成器示例
演示各种文本相关生成器的使用方法
"""

import json
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dataforge import GeneratorConfig, default_factory


def basic_usage():
    """基础用法示例"""
    print("1. 基础用法示例")
    print("=" * 60)

    # 字符串生成器
    print("\n字符串生成器 (string):")
    config = GeneratorConfig("string", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        text = generator.generate()
        print(f"  示例 {i+1}: {text}")

    # 布尔值生成器
    print("\n布尔值生成器 (boolean):")
    config = GeneratorConfig("boolean", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        boolean = generator.generate()
        print(f"  示例 {i+1}: {boolean}")

    # 枚举生成器
    print("\n枚举生成器 (enum):")
    config = GeneratorConfig(
        "enum", parameters={"options": ["选项1", "选项2", "选项3"]}
    )
    generator = default_factory.create_generator(config)
    for i in range(3):
        enum_val = generator.generate()
        print(f"  示例 {i+1}: {enum_val}")

    # 中文文本生成器
    print("\n中文文本生成器 (chinese_text):")
    config = GeneratorConfig("chinese_text", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        chinese = generator.generate()
        print(f"  示例 {i+1}: {chinese}")

    # 英文文本生成器
    print("\n英文文本生成器 (english_text):")
    config = GeneratorConfig("english_text", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        english = generator.generate()
        print(f"  示例 {i+1}: {english}")


def parameter_configuration():
    """参数配置示例"""
    print("\n\n2. 参数配置示例")
    print("=" * 60)

    # 字符串 - 不同长度和类型
    print("\n字符串生成器 - 长度和类型配置:")
    string_configs = [
        {"length": 5},
        {"length": 10},
        {"length": 20},
        {"type": "alphabetic"},
        {"type": "numeric"},
        {"type": "alphanumeric"},
        {"type": "mixed"},
    ]
    for i, params in enumerate(string_configs, 1):
        config = GeneratorConfig("string", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # 布尔值 - 不同概率
    print("\n布尔值生成器 - 概率配置:")
    bool_configs = [
        {"true_probability": 0.8},
        {"true_probability": 0.2},
        {"true_probability": 0.5},
        {"true_probability": 0.0},
        {"true_probability": 1.0},
    ]
    for i, params in enumerate(bool_configs, 1):
        config = GeneratorConfig("boolean", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # 枚举 - 不同选项
    print("\n枚举生成器 - 选项配置:")
    enum_configs = [
        {"options": ["红色", "绿色", "蓝色"]},
        {"options": ["小", "中", "大"]},
        {"options": ["低", "中", "高"]},
        {"options": ["北京", "上海", "广州", "深圳"]},
        {"options": ["优秀", "良好", "及格", "不及格"]},
    ]
    for i, params in enumerate(enum_configs, 1):
        config = GeneratorConfig("enum", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # 中文文本 - 不同长度
    print("\n中文文本生成器 - 长度配置:")
    chinese_configs = [
        {"length": 10},
        {"length": 50},
        {"length": 100},
        {"type": "sentence"},
        {"type": "paragraph"},
    ]
    for i, params in enumerate(chinese_configs, 1):
        config = GeneratorConfig("chinese_text", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result[:50]}{'...' if len(result) > 50 else ''}")

    # 英文文本 - 不同长度
    print("\n英文文本生成器 - 长度配置:")
    english_configs = [
        {"length": 10},
        {"length": 50},
        {"length": 100},
        {"type": "sentence"},
        {"type": "paragraph"},
    ]
    for i, params in enumerate(english_configs, 1):
        config = GeneratorConfig("english_text", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result[:50]}{'...' if len(result) > 50 else ''}")


def batch_generation():
    """批量生成示例"""
    print("\n\n3. 批量生成示例")
    print("=" * 60)

    print("\n批量生成文本数据:")

    # 生成字符串
    string_config = GeneratorConfig(
        "string", parameters={"length": 10, "type": "alphanumeric"}
    )
    string_gen = default_factory.create_generator(string_config)

    # 生成布尔值序列
    bool_config = GeneratorConfig("boolean", parameters={"true_probability": 0.6})
    bool_gen = default_factory.create_generator(bool_config)

    # 生成枚举值
    enum_config = GeneratorConfig(
        "enum", parameters={"options": ["产品A", "产品B", "产品C"]}
    )
    enum_gen = default_factory.create_generator(enum_config)

    # 生成中文文本
    chinese_config = GeneratorConfig("chinese_text", parameters={"length": 50})
    chinese_gen = default_factory.create_generator(chinese_config)

    # 生成英文文本
    english_config = GeneratorConfig("english_text", parameters={"length": 50})
    english_gen = default_factory.create_generator(english_config)

    # 生成5条文本数据
    text_data = []
    for i in range(5):
        data = {
            "id": i + 1,
            "string": string_gen.generate(),
            "boolean": bool_gen.generate(),
            "enum": enum_gen.generate(),
            "chinese_text": chinese_gen.generate(),
            "english_text": english_gen.generate(),
            "created_at": datetime.now().isoformat(),
        }
        text_data.append(data)

    # 打印文本数据
    print("-" * 100)
    print(
        f"{'ID':<4} | {'字符串':<12} | {'布尔值':<8} | {'枚举':<8} | {'中文文本':<25} | {'英文文本':<25}"
    )
    print("-" * 100)
    for data in text_data:
        chinese = (
            data["chinese_text"][:23] + ".."
            if len(data["chinese_text"]) > 25
            else data["chinese_text"]
        )
        english = (
            data["english_text"][:23] + ".."
            if len(data["english_text"]) > 25
            else data["english_text"]
        )
        print(
            f"{data['id']:<4} | {data['string']:<12} | {str(data['boolean']):<8} | {data['enum']:<8} | {chinese:<25} | {english:<25}"
        )
    print("-" * 100)


def validation_examples():
    """数据验证示例"""
    print("\n\n4. 数据验证示例")
    print("=" * 60)

    # 字符串验证
    print("\n字符串格式验证:")
    config = GeneratorConfig(
        "string", parameters={"length": 10, "type": "alphanumeric"}
    )
    generator = default_factory.create_generator(config)

    for i in range(3):
        text = generator.generate()
        is_valid = generator.validate(text)
        print(f"  {i+1}. {text}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(text)}")

    # 布尔值验证
    print("\n布尔值格式验证:")
    config = GeneratorConfig("boolean", parameters={"true_probability": 0.7})
    generator = default_factory.create_generator(config)

    for i in range(3):
        boolean = generator.generate()
        is_valid = generator.validate(boolean)
        print(f"  {i+1}. {boolean}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     类型: {type(boolean).__name__}")

    # 枚举验证
    print("\n枚举格式验证:")
    config = GeneratorConfig("enum", parameters={"options": ["红色", "绿色", "蓝色"]})
    generator = default_factory.create_generator(config)

    for i in range(3):
        enum_val = generator.generate()
        is_valid = generator.validate(enum_val)
        print(f"  {i+1}. {enum_val}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        valid_colors = ["红色", "绿色", "蓝色"]
        print(f"     在选项中: {'✅ 是' if enum_val in valid_colors else '❌ 否'}")

    # 中文文本验证
    print("\n中文文本格式验证:")
    config = GeneratorConfig("chinese_text", parameters={"length": 50})
    generator = default_factory.create_generator(config)

    for i in range(3):
        chinese = generator.generate()
        is_valid = generator.validate(chinese)
        print(f"  {i+1}. {chinese[:30]}{'...' if len(chinese) > 30 else ''}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(chinese)}")

    # 英文文本验证
    print("\n英文文本格式验证:")
    config = GeneratorConfig("english_text", parameters={"length": 50})
    generator = default_factory.create_generator(config)

    for i in range(3):
        english = generator.generate()
        is_valid = generator.validate(english)
        print(f"  {i+1}. {english[:30]}{'...' if len(english) > 30 else ''}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(english)}")


def error_handling():
    """错误处理示例"""
    print("\n\n5. 错误处理示例")
    print("=" * 60)

    # 处理无效的字符串长度
    print("\n处理无效的字符串长度:")
    try:
        config = GeneratorConfig("string", parameters={"length": -1})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的字符串: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效字符串长度错误: {type(e).__name__}")

    # 处理无效的布尔值概率
    print("\n处理无效的布尔值概率:")
    try:
        config = GeneratorConfig("boolean", parameters={"true_probability": 1.5})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的布尔值: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效布尔值概率错误: {type(e).__name__}")

    # 处理空的枚举选项
    print("\n处理空的枚举选项:")
    try:
        config = GeneratorConfig("enum", parameters={"options": []})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的枚举值: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了空枚举选项错误: {type(e).__name__}")

    # 处理无效的文本长度
    print("\n处理无效的文本长度:")
    try:
        config = GeneratorConfig("chinese_text", parameters={"length": -1})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的中文文本: {result[:30]}...")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效文本长度错误: {type(e).__name__}")

    # 处理无效的文本类型
    print("\n处理无效的文本类型:")
    try:
        config = GeneratorConfig("english_text", parameters={"type": "invalid_type"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的英文文本: {result[:30]}...")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效文本类型错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print("\n\n6. 最佳实践示例")
    print("=" * 60)

    # 实践1: 生成完整的文本配置
    print("\n实践1: 生成完整的文本配置")
    text_config = {
        "string_settings": {
            "supported_types": ["alphabetic", "numeric", "alphanumeric", "mixed"],
            "default_length": 10,
            "max_length": 100,
            "case_sensitive": True,
        },
        "boolean_settings": {
            "default_true_probability": 0.5,
            "allow_custom_probability": True,
        },
        "enum_settings": {
            "max_options": 10,
            "min_options": 2,
            "allow_duplicates": False,
        },
        "text_settings": {
            "chinese": {
                "default_length": 50,
                "supported_types": ["sentence", "paragraph", "article"],
                "encoding": "utf-8",
            },
            "english": {
                "default_length": 50,
                "supported_types": ["sentence", "paragraph", "article"],
                "encoding": "utf-8",
            },
        },
    }

    print("  文本配置:")
    for key, value in text_config.items():
        print(f"    {key}:")
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict):
                    print(f"      {sub_key}:")
                    for sub_sub_key, sub_sub_value in sub_value.items():
                        print(f"        {sub_sub_key}: {sub_sub_value}")
                else:
                    print(f"      {sub_key}: {sub_value}")
        else:
            print(f"      {key}: {value}")

    # 实践2: 批量导出文本数据
    print("\n实践2: 批量导出文本数据 (JSON格式)")
    text_data = []

    for i in range(3):
        text_record = {
            "record_id": f"text_{i+1:03d}",
            "strings": {
                "alphabetic": default_factory.create_generator(
                    GeneratorConfig(
                        "string", parameters={"length": 15, "type": "alphabetic"}
                    )
                ).generate(),
                "numeric": default_factory.create_generator(
                    GeneratorConfig(
                        "string", parameters={"length": 10, "type": "numeric"}
                    )
                ).generate(),
                "alphanumeric": default_factory.create_generator(
                    GeneratorConfig(
                        "string", parameters={"length": 12, "type": "alphanumeric"}
                    )
                ).generate(),
            },
            "flags": {
                "enabled": default_factory.create_generator(
                    GeneratorConfig("boolean", parameters={"true_probability": 0.7})
                ).generate(),
                "verified": default_factory.create_generator(
                    GeneratorConfig("boolean", parameters={"true_probability": 0.8})
                ).generate(),
                "active": default_factory.create_generator(
                    GeneratorConfig("boolean", parameters={"true_probability": 0.6})
                ).generate(),
            },
            "categories": {
                "priority": default_factory.create_generator(
                    GeneratorConfig("enum", parameters={"options": ["高", "中", "低"]})
                ).generate(),
                "status": default_factory.create_generator(
                    GeneratorConfig(
                        "enum",
                        parameters={"options": ["新建", "处理中", "已完成", "已关闭"]},
                    )
                ).generate(),
                "type": default_factory.create_generator(
                    GeneratorConfig(
                        "enum", parameters={"options": ["任务", "缺陷", "改进", "功能"]}
                    )
                ).generate(),
            },
            "content": {
                "chinese_title": default_factory.create_generator(
                    GeneratorConfig(
                        "chinese_text", parameters={"length": 20, "type": "sentence"}
                    )
                ).generate(),
                "chinese_body": default_factory.create_generator(
                    GeneratorConfig(
                        "chinese_text", parameters={"length": 100, "type": "paragraph"}
                    )
                ).generate(),
                "english_title": default_factory.create_generator(
                    GeneratorConfig(
                        "english_text", parameters={"length": 20, "type": "sentence"}
                    )
                ).generate(),
                "english_body": default_factory.create_generator(
                    GeneratorConfig(
                        "english_text", parameters={"length": 100, "type": "paragraph"}
                    )
                ).generate(),
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator_version": "1.0.0",
                "data_purpose": "testing",
                "quality_score": 0.95,
            },
        }
        text_data.append(text_record)

    print("  JSON格式输出:")
    print(json.dumps(text_data, ensure_ascii=False, indent=2))


def text_demo():
    """文本演示"""
    print("\n\n7. 文本演示")
    print("=" * 60)

    print("\n生成文章内容演示:")

    # 生成中文文章
    print("\n中文文章:")
    chinese_article = {
        "title": default_factory.create_generator(
            GeneratorConfig(
                "chinese_text", parameters={"length": 30, "type": "sentence"}
            )
        ).generate(),
        "author": default_factory.create_generator(
            GeneratorConfig("string", parameters={"length": 8, "type": "alphabetic"})
        ).generate(),
        "category": default_factory.create_generator(
            GeneratorConfig(
                "enum", parameters={"options": ["科技", "财经", "体育", "娱乐", "教育"]}
            )
        ).generate(),
        "content": default_factory.create_generator(
            GeneratorConfig(
                "chinese_text", parameters={"length": 200, "type": "paragraph"}
            )
        ).generate(),
        "tags": [
            default_factory.create_generator(
                GeneratorConfig("chinese_text", parameters={"length": 5})
            ).generate()
            for _ in range(3)
        ],
    }

    print(f"  标题: {chinese_article['title']}")
    print(f"  作者: {chinese_article['author']}")
    print(f"  分类: {chinese_article['category']}")
    print(f"  内容: {chinese_article['content'][:100]}...")
    print(f"  标签: {', '.join(chinese_article['tags'])}")

    # 生成英文文章
    print("\n英文文章:")
    english_article = {
        "title": default_factory.create_generator(
            GeneratorConfig(
                "english_text", parameters={"length": 30, "type": "sentence"}
            )
        ).generate(),
        "author": default_factory.create_generator(
            GeneratorConfig("string", parameters={"length": 8, "type": "alphabetic"})
        ).generate(),
        "category": default_factory.create_generator(
            GeneratorConfig(
                "enum",
                parameters={
                    "options": [
                        "Technology",
                        "Finance",
                        "Sports",
                        "Entertainment",
                        "Education",
                    ]
                },
            )
        ).generate(),
        "content": default_factory.create_generator(
            GeneratorConfig(
                "english_text", parameters={"length": 200, "type": "paragraph"}
            )
        ).generate(),
        "tags": [
            default_factory.create_generator(
                GeneratorConfig("english_text", parameters={"length": 5})
            ).generate()
            for _ in range(3)
        ],
    }

    print(f"  Title: {english_article['title']}")
    print(f"  Author: {english_article['author']}")
    print(f"  Category: {english_article['category']}")
    print(f"  Content: {english_article['content'][:100]}...")
    print(f"  Tags: {', '.join(english_article['tags'])}")

    # 生成产品描述
    print("\n产品描述演示:")

    products = []
    for i in range(3):
        product = {
            "product_id": default_factory.create_generator(
                GeneratorConfig(
                    "string",
                    parameters={"length": 8, "type": "alphanumeric", "prefix": "PROD_"},
                )
            ).generate(),
            "name": default_factory.create_generator(
                GeneratorConfig(
                    "chinese_text", parameters={"length": 15, "type": "sentence"}
                )
            ).generate(),
            "description": default_factory.create_generator(
                GeneratorConfig(
                    "chinese_text", parameters={"length": 80, "type": "paragraph"}
                )
            ).generate(),
            "features": [
                default_factory.create_generator(
                    GeneratorConfig("chinese_text", parameters={"length": 20})
                ).generate()
                for _ in range(3)
            ],
            "in_stock": default_factory.create_generator(
                GeneratorConfig("boolean", parameters={"true_probability": 0.8})
            ).generate(),
            "rating": default_factory.create_generator(
                GeneratorConfig(
                    "enum", parameters={"options": ["1星", "2星", "3星", "4星", "5星"]}
                )
            ).generate(),
        }
        products.append(product)

    print("  产品列表:")
    for product in products:
        print(f"    ID: {product['product_id']}")
        print(f"    名称: {product['name']}")
        print(f"    描述: {product['description'][:50]}...")
        print(f"    特点: {', '.join(product['features'])}")
        print(f"    库存: {'有货' if product['in_stock'] else '缺货'}")
        print(f"    评分: {product['rating']}")
        print()

    # 生成用户评论
    print("\n用户评论演示:")

    comments = []
    for i in range(3):
        comment = {
            "comment_id": default_factory.create_generator(
                GeneratorConfig(
                    "string",
                    parameters={
                        "length": 10,
                        "type": "alphanumeric",
                        "prefix": "COMM_",
                    },
                )
            ).generate(),
            "user_name": default_factory.create_generator(
                GeneratorConfig(
                    "string", parameters={"length": 8, "type": "alphabetic"}
                )
            ).generate(),
            "content": default_factory.create_generator(
                GeneratorConfig(
                    "chinese_text", parameters={"length": 60, "type": "paragraph"}
                )
            ).generate(),
            "rating": default_factory.create_generator(
                GeneratorConfig(
                    "enum", parameters={"options": ["好评", "中评", "差评"]}
                )
            ).generate(),
            "verified": default_factory.create_generator(
                GeneratorConfig("boolean", parameters={"true_probability": 0.6})
            ).generate(),
            "created_at": datetime.now().isoformat(),
        }
        comments.append(comment)

    print("  评论列表:")
    for comment in comments:
        print(f"    ID: {comment['comment_id']}")
        print(f"    用户: {comment['user_name']}")
        print(f"    内容: {comment['content'][:40]}...")
        print(f"    评价: {comment['rating']}")
        print(f"    已验证: {'是' if comment['verified'] else '否'}")
        print(f"    时间: {comment['created_at'][:19]}")
        print()


def main():
    """主函数"""
    print("📝 DataForge 文本生成器示例")
    print("本示例展示了文本相关生成器的各种使用方法\n")

    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        text_demo()

        print("\n" + "=" * 60)
        print("✅ 示例演示完成")
        print("=" * 60)
        print("🎉 所有文本相关生成器示例已成功运行！")

        print("\n📚 相关文档:")
        print("  • 查看 examples/numeric/numeric_demo.py 了解数值相关生成器")
        print("  • 查看 examples/identifier/identifier_demo.py 了解标识符相关生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")

    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
