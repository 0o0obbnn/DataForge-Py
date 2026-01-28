"""测试账号认证类生成器。

验证用户名、密码、邮箱验证码、短信验证码生成器的功能。
"""

from dataforge.core.generator import GeneratorConfig
from dataforge.generators.auth.email_verification import EmailVerificationGenerator
from dataforge.generators.basic.password import PasswordGenerator
from dataforge.generators.basic.username import UsernameGenerator
from dataforge.generators.auth.sms_verification import SMSVerificationGenerator


def test_username_generator():
    """测试用户名生成器。"""
    print("=== 测试用户名生成器 ===")

    # 测试默认配置
    config = GeneratorConfig("username", {})
    generator = UsernameGenerator(config)
    username = generator.generate()
    print(f"默认用户名: {username}")
    print(f"验证结果: {generator.validate(username)}")

    # 测试自定义配置
    custom_configs = [
        {"length": 10, "format": "alpha"},
        {"length": 8, "format": "email_style"},
        {"length": 12, "format": "social", "use_underscore": True},
        {"prefix": "user", "suffix": "2024", "length": 8},
    ]

    for params in custom_configs:
        config = GeneratorConfig("username", params)
        generator = UsernameGenerator(config)
        username = generator.generate()
        print(f"配置 {params} -> 用户名: {username}")
        print(f"验证结果: {generator.validate(username)}")

    print()


def test_password_generator():
    """测试密码生成器。"""
    print("=== 测试密码生成器 ===")

    # 测试不同复杂度
    complexity_configs = [
        {"complexity": "simple", "length": 8},
        {"complexity": "medium", "length": 10},
        {"complexity": "strong", "length": 12},
        {
            "complexity": "custom",
            "length": 16,
            "use_uppercase": True,
            "use_lowercase": True,
            "use_digits": True,
            "use_special": True,
        },
    ]

    for params in complexity_configs:
        config = GeneratorConfig("password", params)
        generator = PasswordGenerator(config)
        password = generator.generate()
        print(f"配置 {params} -> 密码: {password}")
        print(f"验证结果: {generator.validate(password)}")

    print()


def test_email_verification_generator():
    """测试邮箱验证码生成器。"""
    print("=== 测试邮箱验证码生成器 ===")

    # 测试不同格式
    format_configs = [
        {"length": 6, "format": "numeric"},
        {"length": 8, "format": "alpha"},
        {"length": 10, "format": "alphanumeric"},
        {"length": 6, "format": "mixed"},
    ]

    for params in format_configs:
        config = GeneratorConfig("email_verification", params)
        generator = EmailVerificationGenerator(config)
        code = generator.generate()
        expiry_info = generator.get_expiry_info()
        print(f"配置 {params} -> 验证码: {code}")
        print(f"验证结果: {generator.validate(code)}")
        print(f"过期信息: {expiry_info}")

    print()


def test_sms_verification_generator():
    """测试短信验证码生成器。"""
    print("=== 测试短信验证码生成器 ===")

    # 测试不同场景
    scenario_configs = [
        {"scenario": "general", "length": 6},
        {"scenario": "banking", "length": 6},
        {"scenario": "login", "length": 4},
        {"scenario": "register", "length": 6},
        {"scenario": "transaction", "length": 6},
    ]

    for params in scenario_configs:
        config = GeneratorConfig("sms_verification", params)
        generator = SMSVerificationGenerator(config)
        code = generator.generate()
        sms_template = generator.get_sms_template()
        expiry_info = generator.get_expiry_info()
        print(f"配置 {params} -> 验证码: {code}")
        print(f"短信模板: {sms_template}")
        print(f"过期信息: {expiry_info}")
        print(f"验证结果: {generator.validate(code)}")

    print()


def test_batch_generation():
    """测试批量生成功能。"""
    print("=== 测试批量生成 ===")

    # 测试用户名批量生成
    config = GeneratorConfig(
        "username", {"length": 8, "format": "alpha_numeric"}, count=5
    )
    generator = UsernameGenerator(config)
    usernames = generator.generate_batch(5)
    print(f"批量生成用户名: {usernames}")

    # 测试密码批量生成
    config = GeneratorConfig(
        "password", {"complexity": "strong", "length": 12}, count=3
    )
    generator = PasswordGenerator(config)
    passwords = generator.generate_batch(3)
    print(f"批量生成密码: {passwords}")

    print()


def main():
    """主测试函数。"""
    try:
        test_username_generator()
        test_password_generator()
        test_email_verification_generator()
        test_sms_verification_generator()
        test_batch_generation()

        print("✅ 所有账号认证类生成器测试通过！")

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
