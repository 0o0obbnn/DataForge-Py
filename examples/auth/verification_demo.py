"""
DataForge 验证码生成器示例
演示各种验证码生成器的使用方法
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

    # 会话ID生成器
    print("\n会话ID生成器 (session_id):")
    config = GeneratorConfig("session_id", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        session_id = generator.generate()
        print(f"  示例 {i+1}: {session_id}")


def parameter_configuration():
    """参数配置示例"""
    print("\n\n2. 参数配置示例")
    print("=" * 60)

    # 邮箱验证码 - 不同配置
    print("\n邮箱验证码生成器 - 配置选项:")
    email_configs = [
        {"length": 4, "type": "numeric"},
        {"length": 6, "type": "alphanumeric"},
        {"length": 8, "type": "alphabetic"},
        {"case": "upper"},
        {"case": "lower"},
        {"exclude_ambiguous": True},
        {"prefix": "CODE-"},
        {"suffix": "-END"},
    ]
    for i, params in enumerate(email_configs, 1):
        config = GeneratorConfig("email_verification", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # 短信验证码 - 不同配置
    print("\n短信验证码生成器 - 配置选项:")
    sms_configs = [
        {"length": 4, "type": "numeric"},
        {"length": 6, "type": "alphanumeric"},
        {"country_code": "+86"},
        {"country_code": "+1"},
        {"template": "Your code is: {}"},
        {"template": "Verification code: {}"},
    ]
    for i, params in enumerate(sms_configs, 1):
        config = GeneratorConfig("sms_verification", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # 会话ID - 不同配置
    print("\n会话ID生成器 - 配置选项:")
    session_configs = [
        {"length": 16},
        {"length": 32},
        {"format": "hex"},
        {"format": "base64"},
        {"prefix": "sess_"},
        {"separator": "-"},
    ]
    for i, params in enumerate(session_configs, 1):
        config = GeneratorConfig("session_id", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")


def batch_generation():
    """批量生成示例"""
    print("\n\n3. 批量生成示例")
    print("=" * 60)

    print("\n批量生成验证信息:")

    # 生成邮箱验证码
    email_config = GeneratorConfig(
        "email_verification", parameters={"length": 6, "type": "numeric"}
    )
    email_gen = default_factory.create_generator(email_config)

    # 生成短信验证码
    sms_config = GeneratorConfig(
        "sms_verification",
        parameters={"length": 6, "type": "numeric", "country_code": "+86"},
    )
    sms_gen = default_factory.create_generator(sms_config)

    # 生成会话ID
    session_config = GeneratorConfig(
        "session_id", parameters={"length": 32, "format": "hex"}
    )
    session_gen = default_factory.create_generator(session_config)

    # 生成5个验证信息
    verification_data = []
    for i in range(5):
        verification = {
            "email_code": email_gen.generate(),
            "sms_code": sms_gen.generate(),
            "session_id": session_gen.generate(),
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(minutes=10)).isoformat(),
            "attempts": 0,
            "max_attempts": 3,
        }
        verification_data.append(verification)

    # 打印验证信息
    print("-" * 100)
    print(f"{'邮箱验证码':<12} | {'短信验证码':<12} | {'会话ID':<35} | {'过期时间'}")
    print("-" * 100)
    for data in verification_data:
        email = data["email_code"]
        sms = data["sms_code"]
        session = (
            data["session_id"][:32] + ".."
            if len(data["session_id"]) > 35
            else data["session_id"]
        )
        expires = data["expires_at"][:19]
        print(f"{email:<12} | {sms:<12} | {session:<35} | {expires}")
    print("-" * 100)


def validation_examples():
    """数据验证示例"""
    print("\n\n4. 数据验证示例")
    print("=" * 60)

    # 邮箱验证码验证
    print("\n邮箱验证码格式验证:")
    config = GeneratorConfig("email_verification", parameters={"length": 6})
    generator = default_factory.create_generator(config)

    for i in range(3):
        code = generator.generate()
        is_valid = generator.validate(code)
        print(f"  {i+1}. {code}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度检查: {'✅ 符合' if len(code) == 6 else '❌ 不符合'}")
        print(f"     全数字: {'✅ 是' if code.isdigit() else '❌ 否'}")

    # 短信验证码验证
    print("\n短信验证码格式验证:")
    config = GeneratorConfig("sms_verification", parameters={"length": 6})
    generator = default_factory.create_generator(config)

    for i in range(3):
        code = generator.generate()
        is_valid = generator.validate(code)
        print(f"  {i+1}. {code}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度检查: {'✅ 符合' if len(code) == 6 else '❌ 不符合'}")

    # 会话ID验证
    print("\n会话ID格式验证:")
    config = GeneratorConfig("session_id", parameters={"length": 32})
    generator = default_factory.create_generator(config)

    for i in range(3):
        session_id = generator.generate()
        is_valid = generator.validate(session_id)
        print(f"  {i+1}. {session_id}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度检查: {'✅ 符合' if len(session_id) == 32 else '❌ 不符合'}")
        print(
            f"     十六进制: {'✅ 是' if all(c in '0123456789abcdefABCDEF' for c in session_id) else '❌ 否'}"
        )


def error_handling():
    """错误处理示例"""
    print("\n\n5. 错误处理示例")
    print("=" * 60)

    # 处理无效的验证码长度
    print("\n处理无效的验证码长度:")
    try:
        config = GeneratorConfig("email_verification", parameters={"length": -1})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的验证码: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效验证码长度错误: {type(e).__name__}")

    # 处理无效的验证码类型
    print("\n处理无效的验证码类型:")
    try:
        config = GeneratorConfig("email_verification", parameters={"type": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的验证码: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效验证码类型错误: {type(e).__name__}")

    # 处理无效的会话ID格式
    print("\n处理无效的会话ID格式:")
    try:
        config = GeneratorConfig("session_id", parameters={"format": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的会话ID: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效会话ID格式错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print("\n\n6. 最佳实践示例")
    print("=" * 60)

    # 实践1: 生成完整的验证系统配置
    print("\n实践1: 生成完整的验证系统配置")
    verification_config = {
        "email_settings": {
            "code_length": 6,
            "code_type": "numeric",
            "expiry_minutes": 10,
            "max_attempts": 3,
            "cooldown_minutes": 1,
            "template": "您的验证码是: {}",
            "subject": "验证码",
        },
        "sms_settings": {
            "code_length": 6,
            "code_type": "numeric",
            "expiry_minutes": 5,
            "max_attempts": 3,
            "cooldown_minutes": 1,
            "template": "【DataForge】您的验证码是: {}",
            "supported_countries": ["+86", "+1", "+44"],
        },
        "session_settings": {
            "id_length": 32,
            "id_format": "hex",
            "expiry_hours": 24,
            "max_sessions": 5,
            "cleanup_interval_hours": 1,
        },
    }

    print("  验证系统配置:")
    for key, value in verification_config.items():
        print(f"    {key}:")
        for sub_key, sub_value in value.items():
            print(f"      {sub_key}: {sub_value}")

    # 实践2: 批量导出验证数据
    print("\n实践2: 批量导出验证数据 (JSON格式)")
    verification_data = []

    for i in range(3):
        verification_record = {
            "user_id": f"user_{i+1:03d}",
            "email": f"user{i+1}@example.com",
            "phone": f"+1380013800{i+1:02d}",
            "verification": {
                "email_code": default_factory.create_generator(
                    GeneratorConfig("email_verification", parameters={"length": 6})
                ).generate(),
                "sms_code": default_factory.create_generator(
                    GeneratorConfig("sms_verification", parameters={"length": 6})
                ).generate(),
                "session_id": default_factory.create_generator(
                    GeneratorConfig(
                        "session_id", parameters={"length": 32, "format": "hex"}
                    )
                ).generate(),
            },
            "timestamps": {
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(minutes=10)).isoformat(),
                "last_attempt": None,
                "verified_at": None,
            },
            "status": {
                "is_verified": False,
                "attempts": 0,
                "max_attempts": 3,
                "is_locked": False,
            },
        }
        verification_data.append(verification_record)

    print("  JSON格式输出:")
    print(json.dumps(verification_data, ensure_ascii=False, indent=2))


def multi_channel_demo():
    """多渠道验证演示"""
    print("\n\n7. 多渠道验证演示")
    print("=" * 60)

    print("\n多渠道验证流程:")

    # 生成用户信息
    user_info = {
        "user_id": "user_001",
        "email": "john.doe@example.com",
        "phone": "+13800138000",
        "preferred_channels": ["email", "sms"],
    }

    print(f"  用户信息: {user_info}")

    # 为每个渠道生成验证码
    verification_codes = {}

    # 邮箱验证码
    email_config = GeneratorConfig(
        "email_verification",
        parameters={"length": 6, "type": "numeric", "prefix": "EMAIL-"},
    )
    email_gen = default_factory.create_generator(email_config)
    verification_codes["email"] = email_gen.generate()

    # 短信验证码
    sms_config = GeneratorConfig(
        "sms_verification",
        parameters={
            "length": 6,
            "type": "numeric",
            "prefix": "SMS-",
            "country_code": "+86",
        },
    )
    sms_gen = default_factory.create_generator(sms_config)
    verification_codes["sms"] = sms_gen.generate()

    # 生成会话ID
    session_config = GeneratorConfig(
        "session_id", parameters={"length": 32, "format": "hex", "prefix": "sess_"}
    )
    session_gen = default_factory.create_generator(session_config)
    session_id = session_gen.generate()

    print("\n  生成的验证码:")
    for channel, code in verification_codes.items():
        print(f"    {channel.upper()}: {code}")
    print(f"    会话ID: {session_id}")

    # 模拟验证过程
    print("\n  验证过程:")

    # 模拟用户输入验证码
    user_input_email = verification_codes["email"]
    user_input_sms = verification_codes["sms"]

    # 验证邮箱验证码
    email_valid = email_gen.validate(user_input_email)
    print(
        f"    邮箱验证码 '{user_input_email}': {'✅ 验证成功' if email_valid else '❌ 验证失败'}"
    )

    # 验证短信验证码
    sms_valid = sms_gen.validate(user_input_sms)
    print(
        f"    短信验证码 '{user_input_sms}': {'✅ 验证成功' if sms_valid else '❌ 验证失败'}"
    )

    # 验证会话ID
    session_valid = session_gen.validate(session_id)
    print(
        f"    会话ID '{session_id[:20]}...': {'✅ 验证成功' if session_valid else '❌ 验证失败'}"
    )

    # 生成验证结果
    verification_result = {
        "user_id": user_info["user_id"],
        "session_id": session_id,
        "verification_status": (
            "success" if email_valid and sms_valid and session_valid else "failed"
        ),
        "verified_channels": [],
        "timestamp": datetime.now().isoformat(),
    }

    if email_valid:
        verification_result["verified_channels"].append("email")
    if sms_valid:
        verification_result["verified_channels"].append("sms")

    print("\n  验证结果:")
    print(f"    状态: {verification_result['verification_status']}")
    print(f"    已验证渠道: {', '.join(verification_result['verified_channels'])}")
    print(f"    验证时间: {verification_result['timestamp']}")


def main():
    """主函数"""
    print("🎯 DataForge 验证码生成器示例")
    print("本示例展示了验证码相关生成器的各种使用方法\n")

    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        multi_channel_demo()

        print("\n" + "=" * 60)
        print("✅ 示例演示完成")
        print("=" * 60)
        print("🎉 所有验证码相关生成器示例已成功运行！")

        print("\n📚 相关文档:")
        print("  • 查看 examples/auth/token_demo.py 了解认证令牌相关生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")

    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
