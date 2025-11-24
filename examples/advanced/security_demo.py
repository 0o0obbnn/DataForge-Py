"""
DataForge 安全生成器示例
演示各种安全相关生成器的使用方法
"""

import os
import sys
import json
import hashlib
import secrets
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dataforge import GeneratorConfig, default_factory


def basic_usage():
    """基础用法示例"""
    print("1. 基础用法示例")
    print("=" * 60)
    
    # UUID生成器（用作唯一标识符）
    print("\nUUID生成器 (uuid):")
    config = GeneratorConfig("uuid", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        uid = generator.generate()
        print(f"  示例 {i+1}: {uid}")
    
    # 密码生成器
    print("\n密码生成器 (password):")
    config = GeneratorConfig("password", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        password = generator.generate()
        print(f"  示例 {i+1}: {password}")
    
    # 会话令牌生成器
    print("\n会话令牌生成器 (session_token):")
    config = GeneratorConfig("session_token", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        token = generator.generate()
        print(f"  示例 {i+1}: {token}")
    
    # 认证令牌生成器
    print("\n认证令牌生成器 (auth_token):")
    config = GeneratorConfig("auth_token", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        auth_token = generator.generate()
        print(f"  示例 {i+1}: {auth_token}")
    
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
    
    # UUID - 不同版本
    print("\nUUID生成器 - 版本配置:")
    uuid_configs = [
        {"version": 4},
        {"version": 1},
        {"namespace": "example.com"}
    ]
    for i, params in enumerate(uuid_configs, 1):
        config = GeneratorConfig("uuid", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 密码 - 不同强度
    print("\n密码生成器 - 强度配置:")
    password_configs = [
        {"length": 8, "strength": "weak"},
        {"length": 16, "strength": "medium"},
        {"length": 24, "strength": "strong"},
        {"include_symbols": True, "include_numbers": True}
    ]
    for i, params in enumerate(password_configs, 1):
        config = GeneratorConfig("password", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 会话令牌 - 不同长度
    print("\n会话令牌生成器 - 长度配置:")
    token_configs = [
        {"length": 16},
        {"length": 32},
        {"length": 64},
        {"prefix": "sess_"}
    ]
    for i, params in enumerate(token_configs, 1):
        config = GeneratorConfig("session_token", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 认证令牌 - 不同类型
    print("\n认证令牌生成器 - 类型配置:")
    auth_configs = [
        {"type": "bearer"},
        {"type": "basic"},
        {"type": "jwt"},
        {"length": 64, "prefix": "auth_"}
    ]
    for i, params in enumerate(auth_configs, 1):
        config = GeneratorConfig("auth_token", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 会话ID - 不同格式
    print("\n会话ID生成器 - 格式配置:")
    session_configs = [
        {"format": "hex"},
        {"format": "base64"},
        {"length": 32},
        {"prefix": "sid_"}
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
    
    print("\n批量生成安全凭证:")
    
    # 生成UUID
    uuid_config = GeneratorConfig("uuid", parameters={"version": 4})
    uuid_gen = default_factory.create_generator(uuid_config)
    
    # 生成密码
    password_config = GeneratorConfig("password", parameters={"length": 16, "strength": "strong"})
    password_gen = default_factory.create_generator(password_config)
    
    # 生成会话令牌
    session_config = GeneratorConfig("session_token", parameters={"length": 32, "prefix": "sess_"})
    session_gen = default_factory.create_generator(session_config)
    
    # 生成认证令牌
    auth_config = GeneratorConfig("auth_token", parameters={"type": "jwt", "length": 64})
    auth_gen = default_factory.create_generator(auth_config)
    
    # 生成会话ID
    sid_config = GeneratorConfig("session_id", parameters={"length": 32, "prefix": "sid_"})
    sid_gen = default_factory.create_generator(sid_config)
    
    # 生成5个安全凭证集
    credentials = []
    for i in range(5):
        credential = {
            "credential_id": f"CRED_{i+1:03d}",
            "user_uuid": uuid_gen.generate(),
            "password": password_gen.generate(),
            "session_token": session_gen.generate(),
            "auth_token": auth_gen.generate(),
            "session_id": sid_gen.generate(),
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now().replace(year=datetime.now().year + 1)).isoformat()
        }
        credentials.append(credential)
    
    # 打印凭证信息
    print("-" * 100)
    print(f"{'凭证ID':<10} | {'UUID':<25} | {'会话令牌':<25} | {'认证令牌':<25}")
    print("-" * 100)
    for cred in credentials:
        uid = cred['user_uuid'][:23] + "..." if len(cred['user_uuid']) > 25 else cred['user_uuid']
        session = cred['session_token'][:23] + "..." if len(cred['session_token']) > 25 else cred['session_token']
        auth = cred['auth_token'][:23] + "..." if len(cred['auth_token']) > 25 else cred['auth_token']
        cred_id = cred['credential_id']
        print(f"{cred_id:<10} | {uid:<25} | {session:<25} | {auth:<25}")
    print("-" * 100)


def validation_examples():
    """数据验证示例"""
    print("\n\n4. 数据验证示例")
    print("=" * 60)
    
    # UUID验证
    print("\nUUID格式验证:")
    config = GeneratorConfig("uuid", parameters={"version": 4})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        uid = generator.generate()
        is_valid = generator.validate(uid)
        print(f"  {i+1}. {uid}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(uid)}")
    
    # 密码验证
    print("\n密码格式验证:")
    config = GeneratorConfig("password", parameters={"length": 16, "strength": "strong"})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        password = generator.generate()
        is_valid = generator.validate(password)
        print(f"  {i+1}. {password}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(password)}")
    
    # 会话令牌验证
    print("\n会话令牌格式验证:")
    config = GeneratorConfig("session_token", parameters={"length": 32})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        token = generator.generate()
        is_valid = generator.validate(token)
        print(f"  {i+1}. {token}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(token)}")
    
    # 认证令牌验证
    print("\n认证令牌格式验证:")
    config = GeneratorConfig("auth_token", parameters={"type": "jwt"})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        auth_token = generator.generate()
        is_valid = generator.validate(auth_token)
        print(f"  {i+1}. {auth_token}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(auth_token)}")
    
    # 会话ID验证
    print("\n会话ID格式验证:")
    config = GeneratorConfig("session_id", parameters={"length": 32})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        session_id = generator.generate()
        is_valid = generator.validate(session_id)
        print(f"  {i+1}. {session_id}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(session_id)}")


def error_handling():
    """错误处理示例"""
    print("\n\n5. 错误处理示例")
    print("=" * 60)
    
    # 处理无效的UUID版本
    print("\n处理无效的UUID版本:")
    try:
        config = GeneratorConfig("uuid", parameters={"version": 99})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的UUID: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效UUID版本错误: {type(e).__name__}")
    
    # 处理无效的密码长度
    print("\n处理无效的密码长度:")
    try:
        config = GeneratorConfig("password", parameters={"length": -1})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的密码: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效密码长度错误: {type(e).__name__}")
    
    # 处理无效的令牌长度
    print("\n处理无效的令牌长度:")
    try:
        config = GeneratorConfig("session_token", parameters={"length": -1})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的会话令牌: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效令牌长度错误: {type(e).__name__}")
    
    # 处理无效的认证类型
    print("\n处理无效的认证类型:")
    try:
        config = GeneratorConfig("auth_token", parameters={"type": "invalid_type"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的认证令牌: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效认证类型错误: {type(e).__name__}")
    
    # 处理无效的会话ID格式
    print("\n处理无效的会话ID格式:")
    try:
        config = GeneratorConfig("session_id", parameters={"format": "invalid_format"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的会话ID: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效会话ID格式错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print("\n\n6. 最佳实践示例")
    print("=" * 60)
    
    # 实践1: 生成完整的安全配置
    print("\n实践1: 生成完整的安全配置")
    security_config = {
        "user_identity": {
            "user_uuid": default_factory.create_generator(
                GeneratorConfig("uuid", parameters={"version": 4})
            ).generate(),
            "session_uuid": default_factory.create_generator(
                GeneratorConfig("uuid", parameters={"version": 1})
            ).generate()
        },
        "authentication": {
            "password": default_factory.create_generator(
                GeneratorConfig("password", parameters={"length": 24, "strength": "strong"})
            ).generate(),
            "session_token": default_factory.create_generator(
                GeneratorConfig("session_token", parameters={"length": 64, "prefix": "sess_"})
            ).generate(),
            "auth_token": default_factory.create_generator(
                GeneratorConfig("auth_token", parameters={"type": "jwt", "length": 128})
            ).generate(),
            "session_id": default_factory.create_generator(
                GeneratorConfig("session_id", parameters={"length": 32, "prefix": "sid_"})
            ).generate()
        },
        "security_tokens": {
            "email_verification": default_factory.create_generator(
                GeneratorConfig("email_verification", parameters={"length": 6})
            ).generate(),
            "sms_verification": default_factory.create_generator(
                GeneratorConfig("sms_verification", parameters={"length": 6})
            ).generate()
        }
    }
    
    print("  安全配置:")
    for category, settings in security_config.items():
        print(f"    {category}:")
        for key, value in settings.items():
            if isinstance(value, dict):
                print(f"      {key}:")
                for sub_key, sub_value in value.items():
                    display_value = str(sub_value)[:30] + "..." if len(str(sub_value)) > 30 else str(sub_value)
                    print(f"        {sub_key}: {display_value}")
            else:
                display_value = str(value)[:30] + "..." if len(str(value)) > 30 else str(value)
                print(f"      {key}: {display_value}")
    
    # 实践2: 批量导出安全凭证
    print("\n实践2: 批量导出安全凭证 (JSON格式)")
    credentials_data = []
    
    for i in range(3):
        credential_data = {
            "credential_id": f"SEC_CRED_{i+1:03d}",
            "service": "example_service",
            "credentials": {
                "user_uuid": default_factory.create_generator(
                    GeneratorConfig("uuid", parameters={"version": 4})
                ).generate(),
                "password": default_factory.create_generator(
                    GeneratorConfig("password", parameters={"length": 20, "strength": "strong"})
                ).generate(),
                "session_token": default_factory.create_generator(
                    GeneratorConfig("session_token", parameters={"length": 64, "prefix": "tok_"})
                ).generate(),
                "auth_token": default_factory.create_generator(
                    GeneratorConfig("auth_token", parameters={"type": "jwt", "length": 128})
                ).generate(),
                "session_id": default_factory.create_generator(
                    GeneratorConfig("session_id", parameters={"length": 32, "prefix": "sid_"})
                ).generate()
            },
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now().replace(year=datetime.now().year + 1)).isoformat(),
                "last_rotated": datetime.now().isoformat(),
                "rotation_interval": "90 days",
                "permissions": ["read", "write", "admin"],
                "ip_restrictions": ["192.168.1.0/24", "10.0.0.0/8"],
                "rate_limit": "1000 requests/hour"
            }
        }
        credentials_data.append(credential_data)
    
    print("  JSON格式输出:")
    print(json.dumps(credentials_data, ensure_ascii=False, indent=2))


def security_demo():
    """安全演示"""
    print("\n\n7. 安全演示")
    print("=" * 60)
    
    print("\n密码哈希演示:")
    
    # 生成示例密码
    passwords = ["password123", "admin2023!", "user@secure", "MyStr0ngP@ss"]
    
    # 生成盐值（使用UUID作为盐值）
    salt_config = GeneratorConfig("uuid", parameters={"version": 4})
    salt_gen = default_factory.create_generator(salt_config)
    
    for password in passwords:
        salt = salt_gen.generate()
        # 模拟密码哈希（实际应用中应使用专门的密码哈希函数）
        hash_obj = hashlib.sha256()
        hash_obj.update((password + salt).encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        
        print(f"  密码: {password}")
        print(f"  盐值: {salt}")
        print(f"  哈希: {password_hash[:32]}...")
        print()
    
    # JWT令牌演示
    print("\nJWT令牌演示:")
    
    # 生成JWT密钥
    jwt_secret = default_factory.create_generator(
        GeneratorConfig("auth_token", parameters={"type": "jwt", "length": 64})
    ).generate()
    
    print(f"  JWT密钥: {jwt_secret}")
    
    # 模拟JWT载荷
    jwt_payload = {
        "sub": "user123",
        "name": "John Doe",
        "iat": int(datetime.now().timestamp()),
        "exp": int((datetime.now().replace(year=datetime.now().year + 1)).timestamp()),
        "roles": ["user", "admin"]
    }
    
    print(f"  JWT载荷: {json.dumps(jwt_payload, ensure_ascii=False, indent=4)}")
    
    # 会话令牌轮换演示
    print("\n会话令牌轮换演示:")
    
    # 生成多个会话令牌
    session_tokens = []
    for i in range(5):
        token = default_factory.create_generator(
            GeneratorConfig("session_token", parameters={"length": 64, "prefix": "sess_"})
        ).generate()
        session_tokens.append({
            "token_id": f"token_{i+1}",
            "session_token": token,
            "created_at": datetime.now().isoformat(),
            "status": "active" if i < 3 else "inactive"
        })
    
    print("  会话令牌列表:")
    for token_info in session_tokens:
        display_token = token_info['session_token'][:20] + "..." if len(token_info['session_token']) > 20 else token_info['session_token']
        print(f"    {token_info['token_id']}: {display_token} ({token_info['status']})")
    
    # 数字签名验证演示
    print("\n数字签名验证演示:")
    
    # 生成要签名的数据
    message = "This is a secure message"
    message_hash = hashlib.sha256(message.encode()).hexdigest()
    
    # 生成签名密钥（使用UUID作为密钥）
    sig_key = default_factory.create_generator(
        GeneratorConfig("uuid", parameters={"version": 4})
    ).generate()
    
    print(f"  原始消息: {message}")
    print(f"  消息哈希: {message_hash}")
    print(f"  签名密钥: {sig_key}")
    
    # 模拟签名过程
    signature_input = message_hash + sig_key
    signature = hashlib.sha256(signature_input.encode()).hexdigest()
    
    print(f"  数字签名: {signature[:32]}...")
    
    # 模拟验证过程
    verify_input = message_hash + sig_key
    verify_signature = hashlib.sha256(verify_input.encode()).hexdigest()
    
    is_valid = signature == verify_signature
    print(f"  验证结果: {'✅ 签名有效' if is_valid else '❌ 签名无效'}")
    
    # 安全证书演示
    print("\n安全证书演示:")
    
    # 生成证书信息
    certificate = {
        "certificate_id": default_factory.create_generator(
            GeneratorConfig("session_id", parameters={"length": 16, "prefix": "cert_"})
        ).generate(),
        "subject": "CN=example.com,O=Example Org,L=San Francisco,ST=CA,C=US",
        "issuer": "CN=Root CA,O=Root Authority,L=New York,ST=NY,C=US",
        "serial_number": secrets.randbelow(2**64),
        "not_before": datetime.now().isoformat(),
        "not_after": (datetime.now().replace(year=datetime.now().year + 2)).isoformat(),
        "public_key": default_factory.create_generator(
            GeneratorConfig("uuid", parameters={"version": 4})
        ).generate(),
        "signature_algorithm": "SHA256withRSA",
        "signature": default_factory.create_generator(
            GeneratorConfig("uuid", parameters={"version": 4})
        ).generate()
    }
    
    print("  证书信息:")
    for key, value in certificate.items():
        if isinstance(value, str) and len(value) > 50:
            display_value = value[:47] + "..."
        else:
            display_value = value
        print(f"    {key}: {display_value}")


def main():
    """主函数"""
    print("🔐 DataForge 安全生成器示例")
    print("本示例展示了安全相关生成器的各种使用方法\n")
    
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
        print("🎉 所有安全相关生成器示例已成功运行！")
        
        print("\n📚 相关文档:")
        print("  • 查看 examples/advanced/datetime_demo.py 了解时间相关生成器")
        print("  • 查看 examples/advanced/format_demo.py 了解格式化相关生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")
        
    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
