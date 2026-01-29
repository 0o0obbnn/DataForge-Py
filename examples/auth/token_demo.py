"""
DataForge 认证令牌生成器示例
演示各种认证令牌、验证码等生成器的使用方法
"""

import base64
import hashlib
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

    # 认证令牌生成器
    print("\n认证令牌生成器 (auth_token):")
    config = GeneratorConfig("auth_token", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        token = generator.generate()
        print(f"  示例 {i+1}: {token}")

    # 邮箱验证码生成器
    print("\n邮箱验证码生成器 (email_verification):")
    config = GeneratorConfig("email_verification", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        code = generator.generate()
        print(f"  示例 {i+1}: {code}")

    # 短信验证码生成器
    print("\n短信验证码生成器 (sms_verification):")
    config = GeneratorConfig("sms_verification", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        code = generator.generate()
        print(f"  示例 {i+1}: {code}")

    # 密码生成器
    print("\n密码生成器 (password):")
    config = GeneratorConfig("password", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        password = generator.generate()
        print(f"  示例 {i+1}: {password}")

    # 用户名生成器
    print("\n用户名生成器 (username):")
    config = GeneratorConfig("username", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        username = generator.generate()
        print(f"  示例 {i+1}: {username}")


def parameter_configuration():
    """参数配置示例"""
    print("\n\n2. 参数配置示例")
    print("=" * 60)

    # 认证令牌 - 不同类型
    print("\n认证令牌生成器 - 类型配置:")
    token_types = [
        {"type": "jwt"},
        {"type": "bearer"},
        {"type": "api_key"},
        {"type": "oauth"},
        {"length": 64},
        {"prefix": "Bearer"},
    ]
    for i, params in enumerate(token_types, 1):
        config = GeneratorConfig("auth_token", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # 验证码 - 不同长度和类型
    print("\n验证码生成器 - 长度配置:")
    code_configs = [
        {"length": 4, "type": "numeric"},
        {"length": 6, "type": "alphanumeric"},
        {"length": 8, "type": "mixed"},
        {"case": "upper"},
        {"exclude_ambiguous": True},
    ]
    for i, params in enumerate(code_configs, 1):
        config = GeneratorConfig("email_verification", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # 密码 - 不同强度
    print("\n密码生成器 - 强度配置:")
    password_configs = [
        {"length": 8, "strength": "weak"},
        {"length": 12, "strength": "medium"},
        {"length": 16, "strength": "strong"},
        {"include_symbols": True},
        {"exclude_similar": True},
    ]
    for i, params in enumerate(password_configs, 1):
        config = GeneratorConfig("password", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # 用户名 - 不同风格
    print("\n用户名生成器 - 风格配置:")
    username_styles = [
        {"style": "random"},
        {"style": "professional"},
        {"style": "gaming"},
        {"style": "email_based"},
        {"separator": "_"},
        {"include_numbers": True},
    ]
    for i, params in enumerate(username_styles, 1):
        config = GeneratorConfig("username", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")


def batch_generation():
    """批量生成示例"""
    print("\n\n3. 批量生成示例")
    print("=" * 60)

    print("\n批量生成用户认证信息:")

    # 生成认证令牌
    token_config = GeneratorConfig(
        "auth_token", parameters={"type": "jwt", "length": 32}
    )
    token_gen = default_factory.create_generator(token_config)

    # 生成邮箱验证码
    email_config = GeneratorConfig(
        "email_verification", parameters={"length": 6, "type": "numeric"}
    )
    email_gen = default_factory.create_generator(email_config)

    # 生成密码
    password_config = GeneratorConfig(
        "password",
        parameters={"length": 12, "strength": "medium", "include_symbols": True},
    )
    password_gen = default_factory.create_generator(password_config)

    # 生成用户名
    username_config = GeneratorConfig(
        "username", parameters={"style": "professional", "include_numbers": True}
    )
    username_gen = default_factory.create_generator(username_config)

    # 生成5个用户认证信息
    auth_users = []
    for i in range(5):
        user = {
            "username": username_gen.generate(),
            "password": password_gen.generate(),
            "auth_token": token_gen.generate(),
            "email_verification": email_gen.generate(),
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
        }
        auth_users.append(user)

    # 打印用户信息
    print("-" * 100)
    print(f"{'用户名':<20} | {'密码':<15} | {'令牌':<30} | {'验证码'}")
    print("-" * 100)
    for user in auth_users:
        username = (
            user["username"][:18] + ".."
            if len(user["username"]) > 20
            else user["username"]
        )
        password = (
            user["password"][:13] + ".."
            if len(user["password"]) > 15
            else user["password"]
        )
        token = (
            user["auth_token"][:28] + ".."
            if len(user["auth_token"]) > 30
            else user["auth_token"]
        )
        code = user["email_verification"]
        print(f"{username:<20} | {password:<15} | {token:<30} | {code}")
    print("-" * 100)


def validation_examples():
    """数据验证示例"""
    print("\n\n4. 数据验证示例")
    print("=" * 60)

    # 认证令牌验证
    print("\n认证令牌格式验证:")
    config = GeneratorConfig("auth_token", parameters={"type": "jwt"})
    generator = default_factory.create_generator(config)

    for i in range(3):
        token = generator.generate()
        is_valid = generator.validate(token)
        print(f"  {i+1}. {token}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     令牌长度: {len(token)}")

    # 验证码验证
    print("\n验证码格式验证:")
    config = GeneratorConfig("email_verification", parameters={"length": 6})
    generator = default_factory.create_generator(config)

    for i in range(3):
        code = generator.generate()
        is_valid = generator.validate(code)
        print(f"  {i+1}. {code}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度检查: {'✅ 符合' if len(code) == 6 else '❌ 不符合'}")

    # 密码强度验证
    print("\n密码强度验证:")
    config = GeneratorConfig(
        "password",
        parameters={"length": 12, "strength": "strong", "include_symbols": True},
    )
    generator = default_factory.create_generator(config)

    for i in range(3):
        password = generator.generate()
        is_valid = generator.validate(password)

        # 检查密码强度
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)

        print(f"  {i+1}. {password}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     包含大写: {'✅' if has_upper else '❌'}")
        print(f"     包含小写: {'✅' if has_lower else '❌'}")
        print(f"     包含数字: {'✅' if has_digit else '❌'}")
        print(f"     包含符号: {'✅' if has_symbol else '❌'}")


def error_handling():
    """错误处理示例"""
    print("\n\n5. 错误处理示例")
    print("=" * 60)

    # 处理无效的令牌类型
    print("\n处理无效的令牌类型:")
    try:
        config = GeneratorConfig("auth_token", parameters={"type": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的令牌: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效令牌类型错误: {type(e).__name__}")

    # 处理无效的验证码长度
    print("\n处理无效的验证码长度:")
    try:
        config = GeneratorConfig("email_verification", parameters={"length": -1})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的验证码: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效验证码长度错误: {type(e).__name__}")

    # 处理无效的密码强度
    print("\n处理无效的密码强度:")
    try:
        config = GeneratorConfig("password", parameters={"strength": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的密码: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效密码强度错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print("\n\n6. 最佳实践示例")
    print("=" * 60)

    # 实践1: 生成完整的认证系统配置
    print("\n实践1: 生成完整的认证系统配置")
    auth_config = {
        "jwt_secret": default_factory.create_generator(
            GeneratorConfig("auth_token", parameters={"type": "jwt", "length": 64})
        ).generate(),
        "api_key": default_factory.create_generator(
            GeneratorConfig("auth_token", parameters={"type": "api_key", "length": 32})
        ).generate(),
        "oauth_token": default_factory.create_generator(
            GeneratorConfig("auth_token", parameters={"type": "oauth", "length": 48})
        ).generate(),
        "password_policy": {
            "min_length": 8,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_digits": True,
            "require_symbols": True,
            "max_age_days": 90,
        },
        "verification_settings": {
            "email_code_length": 6,
            "sms_code_length": 6,
            "code_expiry_minutes": 10,
            "max_attempts": 3,
        },
    }

    print("  认证系统配置:")
    for key, value in auth_config.items():
        if isinstance(value, dict):
            print(f"    {key}:")
            for sub_key, sub_value in value.items():
                print(f"      {sub_key}: {sub_value}")
        else:
            display_value = (
                str(value)[:60] + "..." if len(str(value)) > 60 else str(value)
            )
            print(f"    {key}: {display_value}")

    # 实践2: 批量导出认证数据
    print("\n实践2: 批量导出认证数据 (JSON格式)")
    auth_data = []

    for i in range(3):
        user_auth = {
            "user_id": f"user_{i+1:03d}",
            "credentials": {
                "username": default_factory.create_generator(
                    GeneratorConfig("username", parameters={"style": "professional"})
                ).generate(),
                "password": default_factory.create_generator(
                    GeneratorConfig(
                        "password",
                        parameters={
                            "length": 16,
                            "strength": "strong",
                            "include_symbols": True,
                        },
                    )
                ).generate(),
                "email": f"user{i+1}@example.com",
            },
            "tokens": {
                "access_token": default_factory.create_generator(
                    GeneratorConfig(
                        "auth_token", parameters={"type": "bearer", "length": 32}
                    )
                ).generate(),
                "refresh_token": default_factory.create_generator(
                    GeneratorConfig(
                        "auth_token", parameters={"type": "jwt", "length": 64}
                    )
                ).generate(),
                "api_key": default_factory.create_generator(
                    GeneratorConfig(
                        "auth_token", parameters={"type": "api_key", "prefix": "sk_"}
                    )
                ).generate(),
            },
            "verification": {
                "email_code": default_factory.create_generator(
                    GeneratorConfig("email_verification", parameters={"length": 6})
                ).generate(),
                "phone_code": default_factory.create_generator(
                    GeneratorConfig("sms_verification", parameters={"length": 6})
                ).generate(),
            },
        }
        auth_data.append(user_auth)

    print("  JSON格式输出:")
    print(json.dumps(auth_data, ensure_ascii=False, indent=2))


def security_demo():
    """安全演示"""
    print("\n\n7. 安全演示")
    print("=" * 60)

    print("\n密码哈希演示:")

    # 生成密码
    password_config = GeneratorConfig(
        "password",
        parameters={"length": 12, "strength": "strong", "include_symbols": True},
    )
    password_gen = default_factory.create_generator(password_config)

    # 生成多个密码并展示哈希
    passwords = []
    for i in range(3):
        password = password_gen.generate()
        passwords.append(password)

        # 计算不同哈希
        md5_hash = hashlib.md5(password.encode()).hexdigest()
        sha256_hash = hashlib.sha256(password.encode()).hexdigest()

        print(f"\n  密码 {i+1}: {password}")
        print(f"    MD5: {md5_hash}")
        print(f"    SHA256: {sha256_hash[:32]}...")

    print("\n令牌安全演示:")

    # 生成不同类型的令牌
    token_types = ["jwt", "bearer", "api_key", "oauth"]
    for token_type in token_types:
        config = GeneratorConfig(
            "auth_token", parameters={"type": token_type, "length": 32}
        )
        generator = default_factory.create_generator(config)
        token = generator.generate()

        # 模拟Base64编码（实际应用中会更复杂）
        encoded = base64.b64encode(token.encode()).decode()

        print(f"\n  {token_type.upper()} 令牌:")
        print(f"    原始: {token[:32]}...")
        print(f"    编码: {encoded[:32]}...")

    print("\n验证码安全演示:")

    # 生成验证码并展示过期时间
    verification_config = GeneratorConfig(
        "email_verification", parameters={"length": 6, "type": "numeric"}
    )
    verification_gen = default_factory.create_generator(verification_config)

    for i in range(3):
        code = verification_gen.generate()
        expiry = datetime.now() + timedelta(minutes=10)

        print(f"\n  验证码 {i+1}: {code}")
        print(f"    过期时间: {expiry.strftime('%Y-%m-%d %H:%M:%S')}")
        print("    剩余时间: 10分钟")
        print("    安全提示: 请勿在不安全的渠道传输验证码")


def main():
    """主函数"""
    print("🎯 DataForge 认证令牌生成器示例")
    print("本示例展示了认证相关生成器的各种使用方法\n")

    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        security_demo()

        print("\n" + "=" * 60)
        print("✅ 示例演示完成")
        print("=" * 60)
        print("🎉 所有认证相关生成器示例已成功运行！")

        print("\n📚 相关文档:")
        print("  • 查看 examples/auth/verification_demo.py 了解验证码相关生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")

    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
