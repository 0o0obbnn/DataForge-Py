from dataforge.core.factory import default_factory
from dataforge.core.generator import GenerationContext, GeneratorConfig
from dataforge.generators.contact.phone import GenericPhoneNumberGenerator


def test_phone_number_generation():
    """测试电话号码生成"""
    print("=== 测试电话号码生成 ===")

    # 测试不同号码类型
    for number_type in ["MOBILE", "LANDLINE", "TOLL_FREE", "MIXED"]:
        config = GeneratorConfig(
            generator_type="phone",
            parameters={
                "type": number_type,
                "format": "STANDARD",
                "region": "北京" if number_type == "LANDLINE" else None,
            },
        )
        generator = default_factory.create_generator(config)
        phone = generator.generate()
        print(f"生成的{number_type}号码: {phone}")
        print(f"校验结果: {generator.validate(phone)}")
        # 使用具体生成器类型来访问特定方法
        if isinstance(generator, GenericPhoneNumberGenerator):
            print(f"号码类型: {generator.get_number_type(phone)}")
        print()


def test_phone_number_formats():
    """测试电话号码格式"""
    print("=== 测试电话号码格式 ===")

    # 测试不同格式
    for format_type in ["STANDARD", "COMPACT", "INTERNATIONAL"]:
        config = GeneratorConfig(
            generator_type="phone", parameters={"type": "MOBILE", "format": format_type}
        )
        generator = default_factory.create_generator(config)
        phone = generator.generate()
        print(f"配置: {{'format': '{format_type}'}}")
        print(f"生成的号码: {phone}")
        print(f"校验结果: {generator.validate(phone)}")
        # 使用具体生成器类型来访问特定方法
        if isinstance(generator, GenericPhoneNumberGenerator):
            print(f"号码类型: {generator.get_number_type(phone)}")
        print()


def test_phone_number_relations():
    """测试电话号码关联"""
    print("=== 测试电话号码关联 ===")

    # 测试与身份证的关联
    configs = [
        GeneratorConfig(generator_type="idcard", parameters={"region": "440600"}),
        GeneratorConfig(generator_type="phone", parameters={"type": "MOBILE"}),
    ]

    context = GenerationContext()
    result = default_factory.generate_batch_with_relations(configs, context)
    print(f"生成结果: {result}")

    # 测试与地址的关联
    configs = [
        GeneratorConfig(generator_type="address", parameters={"province": "广东省"}),
        GeneratorConfig(generator_type="phone", parameters={"type": "LANDLINE"}),
    ]

    context = GenerationContext()
    result = default_factory.generate_batch_with_relations(configs, context)
    print(f"生成结果: {result}")

    # 测试与姓名的关联
    configs = [
        GeneratorConfig(generator_type="name", parameters={"gender": "MALE"}),
        GeneratorConfig(generator_type="phone", parameters={"type": "MOBILE"}),
    ]

    context = GenerationContext()
    result = default_factory.generate_batch_with_relations(configs, context)
    print(f"生成结果: {result}")
    print()


def test_phone_number_validation():
    """测试电话号码校验"""
    print("=== 测试电话号码校验 ===")

    # 测试有效号码
    valid_numbers = [
        "15 2099 3721",  # 有效手机号（标准格式）
        "010-65518443",  # 有效固定电话（标准格式）
        "4007 6279 4121",  # 有效400号码（标准格式）
        "1306930916",  # 有效手机号（紧凑格式）
        "0891748055",  # 有效固定电话（紧凑格式）
        "400679972722",  # 有效400号码（紧凑格式）
        "+86 18 6624 1822",  # 有效手机号（国际格式）
        "+86 028 85518443",  # 有效固定电话（国际格式）
        "+86 4007 6279 4121",  # 有效400号码（国际格式）
    ]

    print("测试有效号码:")
    for number in valid_numbers:
        print(f"号码: {number}")
        # 创建一个基础配置
        config = GeneratorConfig(generator_type="phone", parameters={})
        # 创建生成器实例
        generator = GenericPhoneNumberGenerator(config)
        # 直接使用具体实例的方法，无需设置number_type
        print(f"校验结果: {generator.validate(number)}")
        print(f"号码类型: {generator.get_number_type(number)}")
        print()

    # 测试无效号码
    invalid_numbers = [
        "12 2099 3721",  # 无效手机号（前缀不正确）
        "010-6551844312",  # 无效固定电话（号码过长）
        "4007 6279 412",  # 无效400号码（号码过短）
        "13069309160",  # 有效手机号但格式错误
        "089174805512",  # 有效固定电话但格式错误
        "4006799727221",  # 有效400号码但格式错误
        "+86 12 6624 1822",  # 无效手机号（国际格式）
        "+86 028 85518443123",  # 有效固定电话但号码过长（国际格式）
        "+86 4007 6279 412",  # 有效400号码但号码过短（国际格式）
    ]

    print("测试无效号码:")
    for number in invalid_numbers:
        print(f"号码: {number}")
        # 创建一个基础配置
        config = GeneratorConfig(generator_type="phone", parameters={})
        # 创建生成器实例
        generator = GenericPhoneNumberGenerator(config)
        # 直接使用具体实例的方法，无需设置number_type
        print(f"校验结果: {generator.validate(number)}")
        print(f"号码类型: {generator.get_number_type(number)}")
        print()
    print()


def test_phone_number_integration():
    """测试电话号码与其他数据的集成"""
    print("=== 测试电话号码与其他数据的集成 ===")

    # 测试与身份证的关联
    configs = [
        GeneratorConfig(generator_type="idcard", parameters={"region": "440600"}),
        GeneratorConfig(generator_type="phone", parameters={"type": "MOBILE"}),
    ]

    context = GenerationContext()
    result = default_factory.generate_batch_with_relations(configs, context)
    print(f"生成结果: {result}")

    # 测试与地址的关联
    configs = [
        GeneratorConfig(generator_type="address", parameters={"province": "广东省"}),
        GeneratorConfig(generator_type="phone", parameters={"type": "LANDLINE"}),
    ]

    context = GenerationContext()
    result = default_factory.generate_batch_with_relations(configs, context)
    print(f"生成结果: {result}")

    # 测试与姓名的关联
    configs = [
        GeneratorConfig(generator_type="name", parameters={"gender": "MALE"}),
        GeneratorConfig(generator_type="phone", parameters={"type": "MOBILE"}),
    ]

    context = GenerationContext()
    result = default_factory.generate_batch_with_relations(configs, context)
    print(f"生成结果: {result}")
    print()


def main():
    """主测试函数"""
    print("DataForge 电话号码生成器测试")
    print("=" * 50)
    print()

    test_phone_number_generation()
    test_phone_number_formats()
    test_phone_number_relations()
    test_phone_number_validation()
    test_phone_number_integration()

    print("所有测试完成！")


if __name__ == "__main__":
    main()
