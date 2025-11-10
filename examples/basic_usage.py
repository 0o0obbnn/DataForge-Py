"""
DataForge使用示例
"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dataforge import GeneratorConfig, default_factory
from dataforge.output.formatter import OutputFormatter


def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")

    # 生成身份证号
    config = GeneratorConfig(
        generator_type="idcard",
        parameters={
            "region": "北京",
            "gender": "MALE",
            "birth_date_range": ("1990-01-01", "2000-12-31"),
        },
    )

    generator = default_factory.create_generator(config)
    id_cards = generator.generate_batch(5)

    print("生成的身份证号:")
    for i, id_card in enumerate(id_cards, 1):
        print(f"  {i}. {id_card}")
        print(f"     校验结果: {'✓' if generator.validate(id_card) else '✗'}")

    print()


def example_bankcard_generation():
    """银行卡生成示例"""
    print("=== 银行卡生成示例 ===")

    config = GeneratorConfig(
        generator_type="bankcard",
        parameters={
            "bank": "ICBC",  # 工商银行
            "valid": True,
        },
    )

    generator = default_factory.create_generator(config)
    cards = generator.generate_batch(3)

    print("生成的银行卡号:")
    for i, card in enumerate(cards, 1):
        print(f"  {i}. {card}")
        print(f"     Luhn校验: {'✓' if generator.validate(card) else '✗'}")

    print()


def example_phone_generation():
    """手机号生成示例"""
    print("=== 手机号生成示例 ===")

    config = GeneratorConfig(
        generator_type="phone",
        parameters={
            "operator": "MOBILE",  # 中国移动
            "valid": True,
        },
    )

    generator = default_factory.create_generator(config)
    phones = generator.generate_batch(3)

    print("生成的手机号:")
    for i, phone in enumerate(phones, 1):
        print(f"  {i}. {phone}")
        operator_info = generator.get_operator_info(phone)
        print(f"     运营商: {operator_info.get('name', '未知')}")

    print()


def example_invalid_data():
    """无效数据生成示例"""
    print("=== 无效数据生成示例 ===")

    # 生成无效身份证号
    config = GeneratorConfig(generator_type="idcard", parameters={"valid": False})

    generator = default_factory.create_generator(config)
    invalid_ids = generator.generate_batch(3)

    print("生成的无效身份证号:")
    for i, id_card in enumerate(invalid_ids, 1):
        print(f"  {i}. {id_card}")
        print(
            f"     校验结果: {'✓' if generator.validate(id_card) else '✗ (预期无效)'}"
        )

    print()


def example_output_formatting():
    """输出格式化示例"""
    print("=== 输出格式化示例 ===")

    # 生成多种类型的数据
    data = {}

    # 身份证
    id_config = GeneratorConfig(generator_type="idcard", parameters={"region": "上海"})
    id_generator = default_factory.create_generator(id_config)
    data["idcard"] = id_generator.generate_batch(2)

    # 手机号
    phone_config = GeneratorConfig(
        generator_type="phone", parameters={"operator": "UNICOM"}
    )
    phone_generator = default_factory.create_generator(phone_config)
    data["phone"] = phone_generator.generate_batch(2)

    # 格式化输出
    formatter = OutputFormatter()

    print("JSON格式输出:")
    json_output = formatter.format(data, "json", pretty=True)
    print(json_output)

    print("\\nCSV格式输出:")
    csv_output = formatter.format(data, "csv")
    print(csv_output)

    print("\\nXML格式输出:")
    xml_output = formatter.format(data, "xml", pretty=True)
    print(xml_output[:500] + "..." if len(xml_output) > 500 else xml_output)


def example_config_file():
    """配置文件示例"""
    print("=== 配置文件示例 ===")

    from dataforge.config.parser import ConfigParser

    # 创建配置解析器
    parser = ConfigParser()

    # 示例配置
    config_data = {
        "generators": [
            {
                "generator_type": "idcard",
                "count": 5,
                "parameters": {
                    "region": "广东",
                    "gender": "FEMALE",
                    "birth_date_range": ["1985-01-01", "1995-12-31"],
                },
            },
            {
                "generator_type": "phone",
                "count": 5,
                "parameters": {"operator": "TELECOM"},
            },
        ]
    }

    # 解析配置
    configs = parser.parse_config(config_data)

    print("根据配置生成的数据:")
    results = {}
    for config in configs:
        generator = default_factory.create_generator(config)
        results[config.generator_type] = generator.generate_batch(config.count)

    # 输出结果
    formatter = OutputFormatter()
    output = formatter.format(results, "json", pretty=True)
    print(output)


def example_related_data():
    """关联数据生成示例"""
    print("=== 关联数据生成示例（概念演示）===")

    # 这里演示概念，实际的关联性需要更复杂的实现
    print("注意：完整的关联数据功能需要在正式版本中实现")

    # 生成身份证，然后根据身份证推断年龄
    id_config = GeneratorConfig(
        generator_type="idcard",
        parameters={"birth_date_range": ("1990-01-01", "1995-12-31")},
    )

    id_generator = default_factory.create_generator(id_config)
    id_cards = id_generator.generate_batch(3)

    print("生成的身份证号及推断信息:")
    for i, id_card in enumerate(id_cards, 1):
        # 从身份证号提取信息
        birth_year = int(id_card[6:10])
        gender_code = int(id_card[16])
        gender = "男" if gender_code % 2 == 1 else "女"
        current_year = 2024
        age = current_year - birth_year

        print(f"  {i}. {id_card}")
        print(f"     出生年份: {birth_year}")
        print(f"     性别: {gender}")
        print(f"     年龄: {age}岁")


if __name__ == "__main__":
    print("DataForge 使用示例\\n")

    try:
        example_basic_usage()
        example_bankcard_generation()
        example_phone_generation()
        example_invalid_data()
        example_output_formatting()
        example_config_file()
        example_related_data()

        print("\\n=== 示例运行完成 ===")
        print("更多用法请参考文档: https://dataforge.readthedocs.io/")

    except Exception as e:
        print(f"运行示例时发生错误: {e}")
        import traceback

        traceback.print_exc()
