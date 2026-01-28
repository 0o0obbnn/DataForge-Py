"""
DataForge 标识符生成器示例
演示各种标识符相关生成器的使用方法
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

    # UUID生成器
    print("\nUUID生成器 (uuid):")
    config = GeneratorConfig("uuid", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        uid = generator.generate()
        print(f"  示例 {i+1}: {uid}")

    # ULID生成器
    print("\nULID生成器 (ulid):")
    config = GeneratorConfig("ulid", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        ulid = generator.generate()
        print(f"  示例 {i+1}: {ulid}")

    # 银行卡生成器
    print("\n银行卡生成器 (bankcard):")
    config = GeneratorConfig("bankcard", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        card = generator.generate()
        print(f"  示例 {i+1}: {card}")

    # 护照生成器
    print("\n护照生成器 (passport):")
    config = GeneratorConfig("passport", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        passport = generator.generate()
        print(f"  示例 {i+1}: {passport}")

    # 身份证生成器
    print("\n身份证生成器 (idcard):")
    config = GeneratorConfig("idcard", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        idcard = generator.generate()
        print(f"  示例 {i+1}: {idcard}")


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

    # 银行卡 - 不同类型
    print("\n银行卡生成器 - 类型配置:")
    card_configs = [
        {"type": "visa"},
        {"type": "mastercard"},
        {"type": "amex"},
        {"type": "unionpay"}
    ]
    for i, params in enumerate(card_configs, 1):
        config = GeneratorConfig("bankcard", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # 护照 - 不同国家
    print("\n护照生成器 - 国家配置:")
    passport_configs = [
        {"country": "CN"},
        {"country": "US"},
        {"country": "UK"},
        {"country": "JP"}
    ]
    for i, params in enumerate(passport_configs, 1):
        config = GeneratorConfig("passport", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # 物流单号 - 不同公司
    print("\n物流单号生成器 - 公司配置:")
    tracking_configs = [
        {"company": "fedex"},
        {"company": "ups"},
        {"company": "dhl"},
        {"company": "ems"}
    ]
    for i, params in enumerate(tracking_configs, 1):
        config = GeneratorConfig("tracking_number", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # 统一社会信用代码 - 不同类型
    print("\n统一社会信用代码生成器 - 类型配置:")
    uscc_configs = [
        {"type": "enterprise"},
        {"type": "individual"},
        {"type": "organization"},
        {"type": "government"}
    ]
    for i, params in enumerate(uscc_configs, 1):
        config = GeneratorConfig("uscc", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")


def batch_generation():
    """批量生成示例"""
    print("\n\n3. 批量生成示例")
    print("=" * 60)

    print("\n批量生成标识符数据:")

    # 生成UUID
    uuid_config = GeneratorConfig("uuid", parameters={"version": 4})
    uuid_gen = default_factory.create_generator(uuid_config)

    # 生成ULID
    ulid_config = GeneratorConfig("ulid", parameters={})
    ulid_gen = default_factory.create_generator(ulid_config)

    # 生成银行卡
    card_config = GeneratorConfig("bankcard", parameters={"type": "visa"})
    card_gen = default_factory.create_generator(card_config)

    # 生成护照
    passport_config = GeneratorConfig("passport", parameters={"country": "CN"})
    passport_gen = default_factory.create_generator(passport_config)

    # 生成身份证
    idcard_config = GeneratorConfig("idcard", parameters={})
    idcard_gen = default_factory.create_generator(idcard_config)

    # 生成5条标识符数据
    identifier_data = []
    for i in range(5):
        data = {
            "id": i + 1,
            "uuid": uuid_gen.generate(),
            "ulid": ulid_gen.generate(),
            "bankcard": card_gen.generate(),
            "passport": passport_gen.generate(),
            "idcard": idcard_gen.generate(),
            "created_at": datetime.now().isoformat()
        }
        identifier_data.append(data)

    # 打印标识符数据
    print("-" * 100)
    print(f"{'ID':<4} | {'UUID':<36} | {'ULID':<26} | {'银行卡':<19} | {'护照':<18}")
    print("-" * 100)
    for data in identifier_data:
        uuid = data['uuid'][:34] + "..." if len(data['uuid']) > 36 else data['uuid']
        ulid = data['ulid'][:24] + "..." if len(data['ulid']) > 26 else data['ulid']
        card = data['bankcard'][:17] + "..." if len(data['bankcard']) > 19 else data['bankcard']
        passport = data['passport'][:16] + "..." if len(data['passport']) > 18 else data['passport']
        print(f"{data['id']:<4} | {uuid:<36} | {ulid:<26} | {card:<19} | {passport:<18}")
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

    # 银行卡验证
    print("\n银行卡格式验证:")
    config = GeneratorConfig("bankcard", parameters={"type": "visa"})
    generator = default_factory.create_generator(config)

    for i in range(3):
        card = generator.generate()
        is_valid = generator.validate(card)
        print(f"  {i+1}. {card}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(card)}")

    # 护照验证
    print("\n护照格式验证:")
    config = GeneratorConfig("passport", parameters={"country": "CN"})
    generator = default_factory.create_generator(config)

    for i in range(3):
        passport = generator.generate()
        is_valid = generator.validate(passport)
        print(f"  {i+1}. {passport}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(passport)}")

    # 身份证验证
    print("\n身份证格式验证:")
    config = GeneratorConfig("idcard", parameters={})
    generator = default_factory.create_generator(config)

    for i in range(3):
        idcard = generator.generate()
        is_valid = generator.validate(idcard)
        print(f"  {i+1}. {idcard}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(idcard)}")

    # 统一社会信用代码验证
    print("\n统一社会信用代码格式验证:")
    config = GeneratorConfig("uscc", parameters={"type": "enterprise"})
    generator = default_factory.create_generator(config)

    for i in range(3):
        uscc = generator.generate()
        is_valid = generator.validate(uscc)
        print(f"  {i+1}. {uscc}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(uscc)}")


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

    # 处理无效的银行卡类型
    print("\n处理无效的银行卡类型:")
    try:
        config = GeneratorConfig("bankcard", parameters={"type": "invalid_type"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的银行卡: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效银行卡类型错误: {type(e).__name__}")

    # 处理无效的护照国家
    print("\n处理无效的护照国家:")
    try:
        config = GeneratorConfig("passport", parameters={"country": "XX"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的护照: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效护照国家错误: {type(e).__name__}")

    # 处理无效的物流公司
    print("\n处理无效的物流公司:")
    try:
        config = GeneratorConfig("tracking_number", parameters={"company": "invalid_company"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的物流单号: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效物流公司错误: {type(e).__name__}")

    # 处理无效的USCC类型
    print("\n处理无效的USCC类型:")
    try:
        config = GeneratorConfig("uscc", parameters={"type": "invalid_type"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的USCC: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效USCC类型错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print("\n\n6. 最佳实践示例")
    print("=" * 60)

    # 实践1: 生成完整的标识符配置
    print("\n实践1: 生成完整的标识符配置")
    identifier_config = {
        "uuid_settings": {
            "supported_versions": [1, 4],
            "default_version": 4,
            "namespace_support": True
        },
        "ulid_settings": {
            "encoding": "base32",
            "time_length": 48,
            "random_length": 80
        },
        "bankcard_settings": {
            "supported_types": ["visa", "mastercard", "amex", "unionpay"],
            "default_type": "visa",
            "luhn_validation": True
        },
        "passport_settings": {
            "supported_countries": ["CN", "US", "UK", "JP", "DE", "FR"],
            "default_country": "CN",
            "mrz_support": True
        },
        "idcard_settings": {
            "supported_regions": ["CN", "US", "UK", "JP"],
            "default_region": "CN",
            "checksum_validation": True
        },
        "logistics_settings": {
            "supported_companies": ["fedex", "ups", "dhl", "ems", "sf_express"],
            "tracking_validation": True
        }
    }

    print("  标识符配置:")
    for key, value in identifier_config.items():
        print(f"    {key}:")
        for sub_key, sub_value in value.items():
            print(f"      {sub_key}: {sub_value}")

    # 实践2: 批量导出标识符数据
    print("\n实践2: 批量导出标识符数据 (JSON格式)")
    identifier_data = []

    for i in range(3):
        identifier_record = {
            "record_id": f"identifier_{i+1:03d}",
            "person_identifiers": {
                "uuid": default_factory.create_generator(
                    GeneratorConfig("uuid", parameters={"version": 4})
                ).generate(),
                "ulid": default_factory.create_generator(
                    GeneratorConfig("ulid", parameters={})
                ).generate(),
                "idcard": default_factory.create_generator(
                    GeneratorConfig("idcard", parameters={})
                ).generate(),
                "passport": default_factory.create_generator(
                    GeneratorConfig("passport", parameters={"country": "CN"})
                ).generate(),
                "driver_license": default_factory.create_generator(
                    GeneratorConfig("driver_license", parameters={})
                ).generate()
            },
            "financial_identifiers": {
                "bankcard": default_factory.create_generator(
                    GeneratorConfig("bankcard", parameters={"type": "visa"})
                ).generate(),
                "business_number": default_factory.create_generator(
                    GeneratorConfig("business_number", parameters={})
                ).generate(),
                "organization_code": default_factory.create_generator(
                    GeneratorConfig("org_code", parameters={})
                ).generate(),
                "uscc": default_factory.create_generator(
                    GeneratorConfig("uscc", parameters={"type": "enterprise"})
                ).generate()
            },
            "logistics_identifiers": {
                "tracking_number": default_factory.create_generator(
                    GeneratorConfig("tracking_number", parameters={"company": "fedex"})
                ).generate(),
                "waybill": default_factory.create_generator(
                    GeneratorConfig("waybill", parameters={"company": "ups"})
                ).generate()
            },
            "international_identifiers": {
                "visa": default_factory.create_generator(
                    GeneratorConfig("visa", parameters={"type": "tourist"})
                ).generate(),
                "lei_code": default_factory.create_generator(
                    GeneratorConfig("lei", parameters={})
                ).generate()
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator_version": "1.0.0",
                "data_purpose": "testing",
                "quality_score": 0.95
            }
        }
        identifier_data.append(identifier_record)

    print("  JSON格式输出:")
    print(json.dumps(identifier_data, ensure_ascii=False, indent=2))


def identifier_demo():
    """标识符演示"""
    print("\n\n7. 标识符演示")
    print("=" * 60)

    print("\n生成用户身份信息演示:")

    # 生成用户身份信息
    print("\n用户身份信息:")
    user_profiles = []
    for i in range(3):
        profile = {
            "user_id": default_factory.create_generator(
                GeneratorConfig("uuid", parameters={"version": 4})
            ).generate(),
            "session_id": default_factory.create_generator(
                GeneratorConfig("ulid", parameters={})
            ).generate(),
            "personal_info": {
                "idcard": default_factory.create_generator(
                    GeneratorConfig("idcard", parameters={})
                ).generate(),
                "passport": default_factory.create_generator(
                    GeneratorConfig("passport", parameters={"country": "CN"})
                ).generate(),
                "driver_license": default_factory.create_generator(
                    GeneratorConfig("driver_license", parameters={})
                ).generate()
            },
            "financial_info": {
                "bankcard": default_factory.create_generator(
                    GeneratorConfig("bankcard", parameters={"type": "visa"})
                ).generate(),
                "business_number": default_factory.create_generator(
                    GeneratorConfig("business_number", parameters={})
                ).generate(),
                "organization_code": default_factory.create_generator(
                    GeneratorConfig("org_code", parameters={})
                ).generate(),
                "uscc": default_factory.create_generator(
                    GeneratorConfig("uscc", parameters={"type": "enterprise"})
                ).generate()
            },
            "travel_info": {
                "visa": default_factory.create_generator(
                    GeneratorConfig("visa", parameters={"type": "tourist"})
                ).generate(),
                "lei_code": default_factory.create_generator(
                    GeneratorConfig("lei", parameters={})
                ).generate()
            },
            "timestamp": datetime.now().isoformat()
        }
        user_profiles.append(profile)

    print("  用户档案:")
    for profile in user_profiles:
        print(f"    用户ID: {profile['user_id']}")
        print(f"    会话ID: {profile['session_id']}")
        print("    个人信息:")
        for key, value in profile['personal_info'].items():
            display_value = str(value)[:10] + "..." if len(str(value)) > 10 else str(value)
            print(f"      {key}: {display_value}")
        print("    金融信息:")
        for key, value in profile['financial_info'].items():
            display_value = str(value)[:10] + "..." if len(str(value)) > 10 else str(value)
            print(f"      {key}: {display_value}")
        print("    旅行信息:")
        for key, value in profile['travel_info'].items():
            display_value = str(value)[:10] + "..." if len(str(value)) > 10 else str(value)
            print(f"      {key}: {display_value}")
        print(f"    时间戳: {profile['timestamp'][:19]}")
        print()

    # 生成物流追踪信息
    print("\n物流追踪信息演示:")

    shipments = []
    for i in range(3):
        shipment = {
            "shipment_id": default_factory.create_generator(
                GeneratorConfig("uuid", parameters={"version": 4})
            ).generate(),
            "tracking_info": {
                "tracking_number": default_factory.create_generator(
                    GeneratorConfig("tracking_number", parameters={"company": "fedex"})
                ).generate(),
                "waybill": default_factory.create_generator(
                    GeneratorConfig("waybill", parameters={"company": "ups"})
                ).generate(),
                "carrier": "FedEx",
                "status": "In Transit"
            },
            "sender": {
                "name": "Sender Name",
                "address": "123 Sender Street, City, Country",
                "phone": "+1234567890"
            },
            "recipient": {
                "name": "Recipient Name",
                "address": "456 Recipient Avenue, City, Country",
                "phone": "+0987654321"
            },
            "package_info": {
                "weight": "2.5 kg",
                "dimensions": "30x20x15 cm",
                "contents": "Electronics"
            },
            "timeline": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "location": "Origin Facility",
                    "status": "Package picked up"
                },
                {
                    "timestamp": (datetime.now().replace(hour=datetime.now().hour + 2)).isoformat(),
                    "location": "Transit Hub",
                    "status": "In transit"
                },
                {
                    "timestamp": (datetime.now().replace(hour=datetime.now().hour + 4)).isoformat(),
                    "location": "Destination Facility",
                    "status": "Out for delivery"
                }
            ]
        }
        shipments.append(shipment)

    print("  货运信息:")
    for shipment in shipments:
        print(f"    货运ID: {shipment['shipment_id']}")
        print("    追踪信息:")
        for key, value in shipment['tracking_info'].items():
            print(f"      {key}: {value}")
        print(f"    承运商: {shipment['tracking_info']['carrier']}")
        print(f"    状态: {shipment['tracking_info']['status']}")
        print(f"    发件人: {shipment['sender']['name']}")
        print(f"    收件人: {shipment['recipient']['name']}")
        print("    时间线:")
        for event in shipment['timeline']:
            print(f"      {event['timestamp'][:19]} - {event['location']}: {event['status']}")
        print()

    # 生成企业标识信息
    print("\n企业标识信息演示:")

    companies = []
    for i in range(3):
        company = {
            "company_id": default_factory.create_generator(
                GeneratorConfig("uuid", parameters={"version": 4})
            ).generate(),
            "business_info": {
                "business_number": default_factory.create_generator(
                    GeneratorConfig("business_number", parameters={})
                ).generate(),
                "organization_code": default_factory.create_generator(
                    GeneratorConfig("org_code", parameters={})
                ).generate(),
                "uscc": default_factory.create_generator(
                    GeneratorConfig("uscc", parameters={"type": "enterprise"})
                ).generate(),
                "lei_code": default_factory.create_generator(
                    GeneratorConfig("lei", parameters={})
                ).generate()
            },
            "company_details": {
                "name": f"Company {i+1}",
                "industry": ["Technology", "Finance", "Manufacturing"][i],
                "established": f"20{20 + i}",
                "employees": [100, 500, 1000][i]
            },
            "financial_info": {
                "bank_account": default_factory.create_generator(
                    GeneratorConfig("bankcard", parameters={"type": "unionpay"})
                ).generate(),
                "credit_rating": ["AAA", "AA", "A"][i],
                "annual_revenue": f"${(i+1) * 1000000:,}"
            },
            "registration_date": datetime.now().isoformat()
        }
        companies.append(company)

    print("  企业信息:")
    for company in companies:
        print(f"    企业ID: {company['company_id']}")
        print("    业务标识:")
        for key, value in company['business_info'].items():
            display_value = str(value)[:15] + "..." if len(str(value)) > 15 else str(value)
            print(f"      {key}: {display_value}")
        print("    企业详情:")
        for key, value in company['company_details'].items():
            print(f"      {key}: {value}")
        print("    财务信息:")
        for key, value in company['financial_info'].items():
            if key == "bank_account":
                display_value = str(value)[:10] + "..." if len(str(value)) > 10 else str(value)
                print(f"      {key}: {display_value}")
            else:
                print(f"      {key}: {value}")
        print(f"    注册日期: {company['registration_date'][:10]}")
        print()


def main():
    """主函数"""
    print("🆔 DataForge 标识符生成器示例")
    print("本示例展示了标识符相关生成器的各种使用方法\n")

    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        identifier_demo()

        print("\n" + "=" * 60)
        print("✅ 示例演示完成")
        print("=" * 60)
        print("🎉 所有标识符相关生成器示例已成功运行！")

        print("\n📚 相关文档:")
        print("  • 查看 examples/integration/integration_demo.py 了解集成示例")
        print("  • 查看 examples/utility/utility_demo.py 了解实用工具示例")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")

    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
