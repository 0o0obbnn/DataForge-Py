"""
DataForge 实用工具生成器示例
演示各种实用工具生成器的使用方法，包括JSON、XML、YAML、媒体文件等
"""

import json
import os
import sys
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dataforge import GeneratorConfig, default_factory


def basic_usage():
    """基础用法示例"""
    print("1. 基础用法示例")
    print("=" * 60)

    # JSON生成器
    print("\nJSON生成器 (json_generator):")
    config = GeneratorConfig("json_generator", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        json_data = generator.generate()
        print(f"  示例 {i+1}: {json_data}")

    # XML生成器
    print("\nXML生成器 (xml_generator):")
    config = GeneratorConfig("xml_generator", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        xml_data = generator.generate()
        # 只显示前100个字符
        display_xml = xml_data[:100] + "..." if len(xml_data) > 100 else xml_data
        print(f"  示例 {i+1}: {display_xml}")

    # YAML生成器
    print("\nYAML生成器 (yaml_generator):")
    config = GeneratorConfig("yaml_generator", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        yaml_data = generator.generate()
        # 只显示前100个字符
        display_yaml = yaml_data[:100] + "..." if len(yaml_data) > 100 else yaml_data
        print(f"  示例 {i+1}: {display_yaml}")

    # 媒体文件生成器
    print("\n媒体文件生成器 (media_file):")
    config = GeneratorConfig("media_file", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        media_data = generator.generate()
        print(f"  示例 {i+1}: {media_data}")


def parameter_configuration():
    """参数配置示例"""
    print("\n\n2. 参数配置示例")
    print("=" * 60)

    # JSON生成器 - 不同结构
    print("\nJSON生成器 - 结构配置:")
    json_configs = [
        {"structure": "simple", "depth": 1},
        {"structure": "nested", "depth": 3},
        {"structure": "array", "array_size": 5},
        {"structure": "mixed", "depth": 2, "array_size": 3}
    ]
    for i, params in enumerate(json_configs, 1):
        config = GeneratorConfig("json_generator", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        # 只显示前80个字符
        display_result = result[:80] + "..." if len(result) > 80 else result
        print(f"    结果: {display_result}")

    # XML生成器 - 不同标签和属性
    print("\nXML生成器 - 标签和属性配置:")
    xml_configs = [
        {"root_tag": "user", "include_attributes": True},
        {"root_tag": "product", "include_attributes": False},
        {"root_tag": "order", "include_attributes": True, "depth": 2},
        {"root_tag": "data", "include_cdata": True}
    ]
    for i, params in enumerate(xml_configs, 1):
        config = GeneratorConfig("xml_generator", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        # 只显示前80个字符
        display_result = result[:80] + "..." if len(result) > 80 else result
        print(f"    结果: {display_result}")

    # YAML生成器 - 不同格式
    print("\nYAML生成器 - 格式配置:")
    yaml_configs = [
        {"format": "simple", "depth": 1},
        {"format": "nested", "depth": 3},
        {"format": "array", "array_size": 3},
        {"format": "complex", "depth": 2, "include_lists": True}
    ]
    for i, params in enumerate(yaml_configs, 1):
        config = GeneratorConfig("yaml_generator", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        # 只显示前80个字符
        display_result = result[:80] + "..." if len(result) > 80 else result
        print(f"    结果: {display_result}")

    # 媒体文件生成器 - 不同文件类型
    print("\n媒体文件生成器 - 文件类型配置:")
    media_configs = [
        {"file_type": "image", "include_metadata": True},
        {"file_type": "video", "include_metadata": True},
        {"file_type": "audio", "include_metadata": False},
        {"file_type": "document", "include_metadata": True}
    ]
    for i, params in enumerate(media_configs, 1):
        config = GeneratorConfig("media_file", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")


def batch_generation():
    """批量生成示例"""
    print("\n\n3. 批量生成示例")
    print("=" * 60)

    print("\n批量生成实用工具数据:")

    # 创建生成器
    json_config = GeneratorConfig("json_generator", parameters={"structure": "mixed", "depth": 2})
    json_gen = default_factory.create_generator(json_config)

    xml_config = GeneratorConfig("xml_generator", parameters={"root_tag": "item", "include_attributes": True})
    xml_gen = default_factory.create_generator(xml_config)

    yaml_config = GeneratorConfig("yaml_generator", parameters={"format": "nested", "depth": 2})
    yaml_gen = default_factory.create_generator(yaml_config)

    media_config = GeneratorConfig("media_file", parameters={"include_metadata": True})
    media_gen = default_factory.create_generator(media_config)

    # 生成5条实用工具数据
    utility_data = []
    for i in range(5):
        data = {
            "id": f"UTIL_{i+1:03d}",
            "json_data": json_gen.generate(),
            "xml_data": xml_gen.generate(),
            "yaml_data": yaml_gen.generate(),
            "media_data": media_gen.generate(),
            "created_at": datetime.now().isoformat()
        }
        utility_data.append(data)

    # 打印实用工具数据
    print("-" * 120)
    print(f"{'ID':<8} | {'JSON数据':<30} | {'XML数据':<30} | {'YAML数据':<30} | {'媒体数据'}")
    print("-" * 120)
    for data in utility_data:
        json_short = data["json_data"][:28] + ".." if len(data["json_data"]) > 30 else data["json_data"]
        xml_short = data["xml_data"][:28] + ".." if len(data["xml_data"]) > 30 else data["xml_data"]
        yaml_short = data["yaml_data"][:28] + ".." if len(data["yaml_data"]) > 30 else data["yaml_data"]
        media_short = str(data["media_data"])[:38] + ".." if len(str(data["media_data"])) > 40 else str(data["media_data"])

        print(f"{data['id']:<8} | {json_short:<30} | {xml_short:<30} | {yaml_short:<30} | {media_short}")
    print("-" * 120)


def validation_examples():
    """数据验证示例"""
    print("\n\n4. 数据验证示例")
    print("=" * 60)

    # JSON验证
    print("\nJSON格式验证:")
    config = GeneratorConfig("json_generator", parameters={"structure": "simple"})
    generator = default_factory.create_generator(config)

    for i in range(3):
        json_str = generator.generate()
        is_valid = generator.validate(json_str)
        is_json = False
        try:
            json.loads(json_str)
            is_json = True
        except:
            pass
        print(f"  {i+1}. {json_str[:50]}...")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     JSON格式: {'✅ 是' if is_json else '❌ 否'}")

    # XML验证
    print("\nXML格式验证:")
    config = GeneratorConfig("xml_generator", parameters={"root_tag": "data"})
    generator = default_factory.create_generator(config)

    for i in range(3):
        xml_str = generator.generate()
        is_valid = generator.validate(xml_str)
        has_xml_tag = xml_str.strip().startswith('<') and xml_str.strip().endswith('>')
        print(f"  {i+1}. {xml_str[:50]}...")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     XML标签: {'✅ 是' if has_xml_tag else '❌ 否'}")

    # YAML验证
    print("\nYAML格式验证:")
    config = GeneratorConfig("yaml_generator", parameters={"format": "simple"})
    generator = default_factory.create_generator(config)

    for i in range(3):
        yaml_str = generator.generate()
        is_valid = generator.validate(yaml_str)
        has_yaml_structure = ':' in yaml_str or '-' in yaml_str
        print(f"  {i+1}. {yaml_str[:50]}...")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     YAML结构: {'✅ 是' if has_yaml_structure else '❌ 否'}")

    # 媒体文件验证
    print("\n媒体文件格式验证:")
    config = GeneratorConfig("media_file", parameters={"file_type": "image"})
    generator = default_factory.create_generator(config)

    for i in range(3):
        media_data = generator.generate()
        is_valid = generator.validate(media_data)
        has_file_extension = '.' in str(media_data)
        print(f"  {i+1}. {media_data}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     文件扩展名: {'✅ 有' if has_file_extension else '❌ 无'}")


def error_handling():
    """错误处理示例"""
    print("\n\n5. 错误处理示例")
    print("=" * 60)

    # 处理无效的JSON结构
    print("\n处理无效的JSON结构:")
    try:
        config = GeneratorConfig("json_generator", parameters={"structure": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的JSON: {result[:50]}...")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效JSON结构错误: {type(e).__name__}")

    # 处理无效的XML标签
    print("\n处理无效的XML标签:")
    try:
        config = GeneratorConfig("xml_generator", parameters={"root_tag": ""})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的XML: {result[:50]}...")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效XML标签错误: {type(e).__name__}")

    # 处理无效的YAML格式
    print("\n处理无效的YAML格式:")
    try:
        config = GeneratorConfig("yaml_generator", parameters={"format": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的YAML: {result[:50]}...")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效YAML格式错误: {type(e).__name__}")

    # 处理无效的媒体文件类型
    print("\n处理无效的媒体文件类型:")
    try:
        config = GeneratorConfig("media_file", parameters={"file_type": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的媒体文件: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效媒体文件类型错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print("\n\n6. 最佳实践示例")
    print("=" * 60)

    # 实践1: 生成完整的配置文件
    print("\n实践1: 生成完整的配置文件")

    # JSON配置文件
    json_config_gen = default_factory.create_generator(
        GeneratorConfig("json_generator", parameters={
            "structure": "nested",
            "depth": 3,
            "include_types": ["string", "number", "boolean", "array"]
        })
    )

    # XML配置文件
    xml_config_gen = default_factory.create_generator(
        GeneratorConfig("xml_generator", parameters={
            "root_tag": "configuration",
            "include_attributes": True,
            "include_cdata": True,
            "depth": 2
        })
    )

    # YAML配置文件
    yaml_config_gen = default_factory.create_generator(
        GeneratorConfig("yaml_generator", parameters={
            "format": "complex",
            "depth": 2,
            "include_lists": True,
            "include_mappings": True
        })
    )

    print("  配置文件示例:")
    print(f"    JSON配置: {json_config_gen.generate()[:80]}...")
    print(f"    XML配置: {xml_config_gen.generate()[:80]}...")
    print(f"    YAML配置: {yaml_config_gen.generate()[:80]}...")

    # 实践2: 批量导出媒体元数据
    print("\n实践2: 批量导出媒体元数据")

    media_types = ["image", "video", "audio", "document"]
    media_metadata = []

    for media_type in media_types:
        for i in range(3):
            media_gen = default_factory.create_generator(
                GeneratorConfig("media_file", parameters={
                    "file_type": media_type,
                    "include_metadata": True,
                    "include_thumbnails": True
                })
            )
            media_info = media_gen.generate()
            media_metadata.append({
                "type": media_type,
                "info": media_info,
                "generated_at": datetime.now().isoformat()
            })

    print("  媒体元数据:")
    for item in media_metadata[:6]:  # 只显示前6条
        print(f"    类型: {item['type']}")
        print(f"    信息: {item['info']}")
        print(f"    生成时间: {item['generated_at'][:19]}")
        print()

    # 实践3: 数据格式转换示例
    print("\n实践3: 数据格式转换示例")

    # 生成基础数据
    base_data = {
        "user_id": default_factory.create_generator(
            GeneratorConfig("uuid", parameters={"version": 4})
        ).generate(),
        "name": default_factory.create_generator(
            GeneratorConfig("name", parameters={})
        ).generate(),
        "email": default_factory.create_generator(
            GeneratorConfig("email", parameters={})
        ).generate(),
        "age": default_factory.create_generator(
            GeneratorConfig("age", parameters={})
        ).generate(),
        "active": default_factory.create_generator(
            GeneratorConfig("boolean", parameters={"true_probability": 0.7})
        ).generate()
    }

    # 转换为不同格式
    print("  原始数据:")
    print(json.dumps(base_data, ensure_ascii=False, indent=2))

    # 生成对应格式的示例
    json_example = default_factory.create_generator(
        GeneratorConfig("json_generator", parameters={"structure": "simple"})
    ).generate()

    xml_example = default_factory.create_generator(
        GeneratorConfig("xml_generator", parameters={"root_tag": "user"})
    ).generate()

    yaml_example = default_factory.create_generator(
        GeneratorConfig("yaml_generator", parameters={"format": "simple"})
    ).generate()

    print(f"\n  JSON格式示例:\n    {json_example[:100]}...")
    print(f"\n  XML格式示例:\n    {xml_example[:100]}...")
    print(f"\n  YAML格式示例:\n    {yaml_example[:100]}...")


def utility_demo():
    """实用工具演示"""
    print("\n\n7. 实用工具演示")
    print("=" * 60)

    print("\n生成复杂数据结构演示:")

    # 生成复杂的API响应数据
    print("\nAPI响应数据:")

    api_response = {
        "status": default_factory.create_generator(
            GeneratorConfig("enum", parameters={"options": ["success", "error", "pending"]})
        ).generate(),
        "code": default_factory.create_generator(
            GeneratorConfig("integer", parameters={"min": 200, "max": 599})
        ).generate(),
        "message": default_factory.create_generator(
            GeneratorConfig("chinese_text", parameters={"length": 30})
        ).generate(),
        "data": json.loads(default_factory.create_generator(
            GeneratorConfig("json_generator", parameters={"structure": "nested", "depth": 2})
        ).generate()),
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "request_id": default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 16, "type": "alphanumeric"})
            ).generate()
        }
    }

    print(f"  状态: {api_response['status']}")
    print(f"  代码: {api_response['code']}")
    print(f"  消息: {api_response['message']}")
    print(f"  数据键: {list(api_response['data'].keys()) if isinstance(api_response['data'], dict) else 'N/A'}")
    print(f"  请求ID: {api_response['metadata']['request_id']}")

    # 生成配置文件
    print("\n配置文件演示:")

    config_types = ["development", "testing", "production"]
    for config_type in config_types:
        config_content = default_factory.create_generator(
            GeneratorConfig("yaml_generator", parameters={
                "format": "complex",
                "depth": 3,
                "include_lists": True
            })
        ).generate()

        print(f"  {config_type.title()} 配置:")
        print(f"    {config_content[:80]}...")

    # 生成媒体库
    print("\n媒体库演示:")

    media_library = []
    media_categories = ["images", "videos", "audios", "documents"]

    for category in media_categories:
        for i in range(3):
            media_item = {
                "id": f"{category[: -1]}_{i+1:03d}",
                "category": category,
                "file_info": default_factory.create_generator(
                    GeneratorConfig("media_file", parameters={
                        "file_type": category[: -1],
                        "include_metadata": True
                    })
                ).generate(),
                "tags": [
                    default_factory.create_generator(
                        GeneratorConfig("string", parameters={"length": 6, "type": "alphabetic"})
                    ).generate()
                    for _ in range(3)
                ],
                "created_at": (datetime.now() - timedelta(days=i+1)).isoformat()
            }
            media_library.append(media_item)

    print("  媒体库内容:")
    for item in media_library[:6]:  # 只显示前6条
        print(f"    ID: {item['id']}")
        print(f"    类别: {item['category']}")
        print(f"    文件信息: {item['file_info']}")
        print(f"    标签: {', '.join(item['tags'])}")
        print(f"    创建时间: {item['created_at'][:10]}")
        print()

    # 生成数据交换格式
    print("数据交换格式演示:")

    # 创建示例数据
    sample_data = {
        "users": [
            {
                "id": default_factory.create_generator(
                    GeneratorConfig("uuid", parameters={"version": 4})
                ).generate(),
                "name": default_factory.create_generator(
                    GeneratorConfig("name", parameters={})
                ).generate(),
                "email": default_factory.create_generator(
                    GeneratorConfig("email", parameters={})
                ).generate()
            }
            for _ in range(2)
        ],
        "products": [
            {
                "id": default_factory.create_generator(
                    GeneratorConfig("string", parameters={"length": 8, "type": "alphanumeric"})
                ).generate(),
                "name": default_factory.create_generator(
                    GeneratorConfig("chinese_text", parameters={"length": 15})
                ).generate(),
                "price": default_factory.create_generator(
                    GeneratorConfig("decimal", parameters={"min": 10.0, "max": 1000.0, "decimal_places": 2})
                ).generate()
            }
            for _ in range(2)
        ]
    }

    # 转换为不同格式
    json_data = json.dumps(sample_data, ensure_ascii=False, indent=2)

    xml_data = default_factory.create_generator(
        GeneratorConfig("xml_generator", parameters={
            "root_tag": "data",
            "include_attributes": True
        })
    ).generate()

    yaml_data = default_factory.create_generator(
        GeneratorConfig("yaml_generator", parameters={
            "format": "complex",
            "depth": 2
        })
    ).generate()

    print(f"  JSON格式 ({len(json_data)} 字符):")
    print(f"    {json_data[:100]}...")

    print(f"\n  XML格式 ({len(xml_data)} 字符):")
    print(f"    {xml_data[:100]}...")

    print(f"\n  YAML格式 ({len(yaml_data)} 字符):")
    print(f"    {yaml_data[:100]}...")


def main():
    """主函数"""
    print("🛠️ DataForge 实用工具生成器示例")
    print("本示例展示了实用工具相关生成器的各种使用方法\n")

    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        utility_demo()

        print("\n" + "=" * 60)
        print("✅ 示例演示完成")
        print("=" * 60)
        print("🎉 所有实用工具生成器示例已成功运行！")

        print("\n📚 相关文档:")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")
        print("  • 查看 docs/api/ 了解API文档")

    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
