"""
DataForge 简化 API 使用示例

演示如何使用新的 gen API 快速生成测试数据
"""

from dataforge import gen


def example_basic_usage():
    """基础用法：生成单个数据"""
    print("=" * 50)
    print("基础用法：生成单个数据")
    print("=" * 50)

    # 生成姓名
    name = gen.name()
    print(f"姓名: {name}")

    # 生成手机号
    phone = gen.phone()
    print(f"手机号: {phone}")

    # 生成邮箱
    email = gen.email()
    print(f"邮箱: {email}")

    # 生成身份证
    idcard = gen.idcard()
    print(f"身份证: {idcard}")

    # 生成银行卡号
    bankcard = gen.bankcard()
    print(f"银行卡号: {bankcard}")

    # 生成公司名称
    company = gen.company()
    print(f"公司名称: {company}")

    # 生成统一社会信用代码
    credit_code = gen.uscc()
    print(f"统一社会信用代码: {credit_code}")
    print()


def example_batch_generation():
    """批量生成数据"""
    print("=" * 50)
    print("批量生成数据")
    print("=" * 50)

    # 生成10个姓名
    names = gen.name(count=10)
    print(f"生成10个姓名: {names[:3]}... (共{len(names)}个)")

    # 生成5个手机号
    phones = gen.phone(count=5)
    print(f"生成5个手机号: {phones}")

    print()


def example_with_parameters():
    """带参数生成数据"""
    print("=" * 50)
    print("带参数生成数据")
    print("=" * 50)

    # 生成北京地区身份证
    idcard_beijing = gen.idcard(region="北京")
    print(f"北京身份证: {idcard_beijing}")

    # 生成男性身份证
    idcard_male = gen.idcard(gender="MALE")
    print(f"男性身份证: {idcard_male}")

    # 生成中国移动手机号
    phone_mobile = gen.phone(operator="MOBILE")
    print(f"中国移动号码: {phone_mobile}")

    # 生成工商银行卡号
    bankcard_icbc = gen.bankcard(bank="ICBC")
    print(f"工商银行卡号: {bankcard_icbc}")

    print()


def example_combined():
    """组合参数：批量+参数"""
    print("=" * 50)
    print("组合参数：批量生成+自定义参数")
    print("=" * 50)

    # 批量生成北京女性身份证
    idcards = gen.idcard(region="北京", gender="FEMALE", count=3)
    print("北京女性身份证 (3个):")
    for i, idcard in enumerate(idcards, 1):
        print(f"  {i}. {idcard}")

    # 批量生成中国移动手机号
    phones = gen.phone(operator="MOBILE", count=5)
    print("\n中国移动手机号 (5个):")
    for i, phone in enumerate(phones, 1):
        print(f"  {i}. {phone}")

    print()


def example_user_profile():
    """实战案例：生成用户资料"""
    print("=" * 50)
    print("实战案例：生成完整用户资料")
    print("=" * 50)

    # 生成5个用户资料
    for i in range(5):
        user = {
            "name": gen.name(),
            "gender": gen.gender(),
            "age": gen.age(),
            "phone": gen.phone(operator="MOBILE"),
            "email": gen.email(),
            "idcard": gen.idcard(),
            "address": gen.address(),
        }

        print(f"\n用户 #{i + 1}:")
        print(f"  姓名: {user['name']}")
        print(f"  性别: {user['gender']}")
        print(f"  年龄: {user['age']}")
        print(f"  手机: {user['phone']}")
        print(f"  邮箱: {user['email']}")
        print(f"  身份证: {user['idcard']}")
        print(f"  地址: {user['address']}")

    print()


def example_help_and_discovery():
    """帮助和发现功能"""
    print("=" * 50)
    print("帮助和发现功能")
    print("=" * 50)

    # 查看所有可用生成器
    generators = gen.list_generators()
    print(f"可用生成器总数: {generators}")
    print(f"可用生成器总数: {len(generators)}")
    print(f"前10个生成器: {generators[:10]}")

    # 检查生成器是否可用
    print(f"\n'name' 生成器是否可用? {gen.is_available('name')}")
    print(f"'invalid_gen' 生成器是否可用? {gen.is_available('invalid_gen')}")

    # 获取帮助信息
    print("\nDataForge 简介:")
    print(gen)

    print()


def example_error_handling():
    """错误处理示例"""
    print("=" * 50)
    print("错误处理示例")
    print("=" * 50)

    # 尝试调用不存在的生成器
    try:
        gen.invalid_generator()
    except AttributeError as e:
        print(f"❌ 错误: {e}")

    # 拼写错误会得到友好提示
    try:
        gen.namee()  # name 拼写错误
    except AttributeError as e:
        print(f"\n❌ 拼写错误: {e}")

    print()


def example_comparison():
    """新旧 API 对比"""
    print("=" * 50)
    print("新旧 API 对比")
    print("=" * 50)

    # 新 API（简洁）
    print("✅ 新 API（推荐）:")
    print("from dataforge import gen")
    print("names = gen.name(count=5)")
    names_new = gen.name(count=5)
    print(f"结果: {names_new}\n")

    # 旧 API（仍然可用）
    print("🔧 旧 API（仍然可用）:")
    print("from dataforge import default_factory, GeneratorConfig")
    print("config = GeneratorConfig(generator_type='name', parameters={})")
    print("generator = default_factory.create_generator(config)")
    print("names = generator.generate_batch(5)")

    from dataforge import GeneratorConfig, default_factory

    config = GeneratorConfig(generator_type="name", parameters={})
    generator = default_factory.create_generator(config)
    names_old = generator.generate_batch(5)
    print(f"结果: {names_old}")

    print("\n💡 两种方式都可以用，新 API 更简洁，旧 API 更灵活！")
    print()


if __name__ == "__main__":
    print("\n" + "🚀 DataForge 简化 API 使用示例".center(50, "="))
    print()

    try:
        example_basic_usage()
        example_batch_generation()
        example_with_parameters()
        example_combined()
        example_user_profile()
        example_help_and_discovery()
        example_error_handling()
        example_comparison()

        print("=" * 50)
        print("✅ 所有示例运行完成！".center(50))
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback

        traceback.print_exc()
