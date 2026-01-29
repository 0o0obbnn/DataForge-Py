"""
DataForge 企业信息生成器示例
演示如何生成企业名称和统一社会信用代码
"""

import json
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dataforge import GeneratorConfig, default_factory


def basic_company_generation():
    """基础企业信息生成"""
    print("1. 基础企业信息生成")
    print("=" * 80)

    # 生成企业名称
    print("\n生成企业名称:")
    company_name_config = GeneratorConfig("company_name", parameters={})
    company_name_gen = default_factory.create_generator(company_name_config)

    for i in range(5):
        company_name = company_name_gen.generate()
        print(f"  {i+1}. {company_name}")

    # 生成统一社会信用代码
    print("\n生成统一社会信用代码 (USCC):")
    uscc_config = GeneratorConfig("uscc", parameters={"type": "enterprise"})
    uscc_gen = default_factory.create_generator(uscc_config)

    for i in range(5):
        uscc = uscc_gen.generate()
        print(f"  {i+1}. {uscc}")


def company_name_with_parameters():
    """带参数的企业名称生成"""
    print("\n\n2. 带参数的企业名称生成")
    print("=" * 80)

    # 不同行业的企业名称
    print("\n按行业生成企业名称:")
    industries = ["IT", "FINANCE", "RETAIL", "MANUFACTURING", "EDUCATION"]

    for industry in industries:
        config = GeneratorConfig("company_name", parameters={"industry": industry})
        generator = default_factory.create_generator(config)
        company_name = generator.generate()
        print(f"  {industry:15} -> {company_name}")

    # 不同类型的企业名称
    print("\n按类型生成企业名称:")
    company_types = ["CO_LTD", "GROUP", "INSTITUTE", "TECH", "TRADING"]

    for comp_type in company_types:
        config = GeneratorConfig("company_name", parameters={"type": comp_type})
        generator = default_factory.create_generator(config)
        company_name = generator.generate()
        print(f"  {comp_type:15} -> {company_name}")

    # 带地区前缀的企业名称
    print("\n带地区前缀的企业名称:")
    config = GeneratorConfig("company_name", parameters={"prefix_region": True})
    generator = default_factory.create_generator(config)

    for i in range(5):
        company_name = generator.generate()
        print(f"  {i+1}. {company_name}")

    # 英文企业名称
    print("\n英文企业名称:")
    config = GeneratorConfig("company_name", parameters={"language": "english"})
    generator = default_factory.create_generator(config)

    for i in range(5):
        company_name = generator.generate()
        print(f"  {i+1}. {company_name}")


def uscc_with_parameters():
    """带参数的统一社会信用代码生成"""
    print("\n\n3. 带参数的统一社会信用代码生成")
    print("=" * 80)

    # 不同类型的USCC
    print("\n按类型生成统一社会信用代码:")
    uscc_types = [
        ("enterprise", "企业"),
        ("individual", "个体工商户"),
        ("organization", "社会组织"),
        ("government", "政府机关"),
    ]

    for uscc_type, description in uscc_types:
        config = GeneratorConfig("uscc", parameters={"type": uscc_type})
        generator = default_factory.create_generator(config)
        uscc = generator.generate()
        print(f"  {description:12} ({uscc_type:12}) -> {uscc}")


def complete_company_profile():
    """生成完整的企业档案"""
    print("\n\n4. 生成完整的企业档案")
    print("=" * 80)

    print("\n生成5家企业的完整信息:\n")

    # 配置生成器
    company_name_gen = default_factory.create_generator(
        GeneratorConfig("company_name", parameters={"prefix_region": True})
    )
    uscc_gen = default_factory.create_generator(
        GeneratorConfig("uscc", parameters={"type": "enterprise"})
    )
    org_code_gen = default_factory.create_generator(
        GeneratorConfig("org_code", parameters={})
    )
    business_num_gen = default_factory.create_generator(
        GeneratorConfig("business_number", parameters={})
    )

    companies = []
    for i in range(5):
        company = {
            "序号": i + 1,
            "企业名称": company_name_gen.generate(),
            "统一社会信用代码": uscc_gen.generate(),
            "组织机构代码": org_code_gen.generate(),
            "工商注册号": business_num_gen.generate(),
            "注册日期": datetime.now().strftime("%Y-%m-%d"),
            "企业状态": "正常",
        }
        companies.append(company)

    # 打印表格
    print("-" * 120)
    print(
        f"{'序号':<4} | {'企业名称':<30} | {'统一社会信用代码':<20} | {'组织机构代码':<12} | {'工商注册号':<18}"
    )
    print("-" * 120)

    for company in companies:
        name = (
            company["企业名称"][:28] + ".."
            if len(company["企业名称"]) > 30
            else company["企业名称"]
        )
        print(
            f"{company['序号']:<4} | {name:<30} | {company['统一社会信用代码']:<20} | "
            f"{company['组织机构代码']:<12} | {company['工商注册号']:<18}"
        )

    print("-" * 120)

    return companies


def validation_examples():
    """数据验证示例"""
    print("\n\n5. 数据验证示例")
    print("=" * 80)

    # 验证企业名称
    print("\n验证企业名称格式:")
    company_name_gen = default_factory.create_generator(
        GeneratorConfig("company_name", parameters={})
    )

    for i in range(3):
        company_name = company_name_gen.generate()
        is_valid = company_name_gen.validate(company_name)
        print(f"  {i+1}. {company_name}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(company_name)} 字符")

    # 验证统一社会信用代码
    print("\n验证统一社会信用代码格式:")
    uscc_gen = default_factory.create_generator(
        GeneratorConfig("uscc", parameters={"type": "enterprise"})
    )

    for i in range(3):
        uscc = uscc_gen.generate()
        is_valid = uscc_gen.validate(uscc)
        print(f"  {i+1}. {uscc}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度: {len(uscc)} 字符")


def export_to_json():
    """导出为JSON格式"""
    print("\n\n6. 导出企业数据为JSON格式")
    print("=" * 80)

    # 配置生成器
    company_name_gen = default_factory.create_generator(
        GeneratorConfig("company_name", parameters={"prefix_region": True})
    )
    uscc_gen = default_factory.create_generator(
        GeneratorConfig("uscc", parameters={"type": "enterprise"})
    )
    org_code_gen = default_factory.create_generator(
        GeneratorConfig("org_code", parameters={})
    )

    # 生成企业数据
    companies_data = []
    for i in range(3):
        company = {
            "company_id": f"COMP{i+1:04d}",
            "basic_info": {
                "name": company_name_gen.generate(),
                "uscc": uscc_gen.generate(),
                "organization_code": org_code_gen.generate(),
                "registration_date": datetime.now().strftime("%Y-%m-%d"),
                "status": "active",
            },
            "business_info": {
                "industry": ["科技", "金融", "制造"][i % 3],
                "business_scope": "技术开发、技术咨询、技术服务",
                "registered_capital": f"{(i+1) * 1000}万元人民币",
            },
            "contact_info": {
                "address": f"北京市海淀区中关村大街{(i+1)*100}号",
                "postal_code": "100000",
                "phone": f"010-{8000+i}{5000+i:04d}",
                "email": f"contact@company{i+1}.com",
            },
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "data_source": "DataForge Generator",
                "version": "1.0.0",
            },
        }
        companies_data.append(company)

    # 输出JSON
    print("\nJSON格式输出:")
    print(json.dumps(companies_data, ensure_ascii=False, indent=2))

    return companies_data


def export_to_csv():
    """导出为CSV格式"""
    print("\n\n7. 导出企业数据为CSV格式")
    print("=" * 80)

    # 配置生成器
    company_name_gen = default_factory.create_generator(
        GeneratorConfig("company_name", parameters={"prefix_region": True})
    )
    uscc_gen = default_factory.create_generator(
        GeneratorConfig("uscc", parameters={"type": "enterprise"})
    )

    # 生成CSV数据
    print("\nCSV格式输出:")
    print("序号,企业名称,统一社会信用代码,注册日期,企业状态")

    for i in range(10):
        company_name = company_name_gen.generate()
        uscc = uscc_gen.generate()
        reg_date = datetime.now().strftime("%Y-%m-%d")
        status = "正常"
        print(f"{i+1},{company_name},{uscc},{reg_date},{status}")


def batch_generation_demo():
    """批量生成演示"""
    print("\n\n8. 批量生成企业信息")
    print("=" * 80)

    print("\n快速生成100家企业信息...")

    # 配置生成器
    company_name_gen = default_factory.create_generator(
        GeneratorConfig("company_name", parameters={"prefix_region": True})
    )
    uscc_gen = default_factory.create_generator(
        GeneratorConfig("uscc", parameters={"type": "enterprise"})
    )

    # 批量生成
    companies = []
    for i in range(100):
        company = {
            "id": i + 1,
            "name": company_name_gen.generate(),
            "uscc": uscc_gen.generate(),
        }
        companies.append(company)

    print(f"✅ 成功生成 {len(companies)} 家企业信息")

    # 显示前10条和后10条
    print("\n前10条记录:")
    for company in companies[:10]:
        print(f"  {company['id']:3d}. {company['name'][:35]:<35} | {company['uscc']}")

    print("\n...")

    print("\n后10条记录:")
    for company in companies[-10:]:
        print(f"  {company['id']:3d}. {company['name'][:35]:<35} | {company['uscc']}")

    # 统计信息
    print("\n统计信息:")
    print(f"  总数: {len(companies)} 家企业")
    print(
        f"  平均企业名称长度: {sum(len(c['name']) for c in companies) / len(companies):.1f} 字符"
    )
    print(f"  USCC长度: {len(companies[0]['uscc'])} 字符 (统一)")


def industry_specific_demo():
    """特定行业企业生成演示"""
    print("\n\n9. 特定行业企业生成演示")
    print("=" * 80)

    industries = {
        "IT": "信息技术",
        "FINANCE": "金融服务",
        "RETAIL": "零售贸易",
        "MANUFACTURING": "制造业",
        "EDUCATION": "教育培训",
    }

    uscc_gen = default_factory.create_generator(
        GeneratorConfig("uscc", parameters={"type": "enterprise"})
    )

    print("\n按行业生成企业信息:\n")

    for industry_code, industry_name in industries.items():
        print(f"{industry_name} ({industry_code}):")

        company_name_gen = default_factory.create_generator(
            GeneratorConfig(
                "company_name",
                parameters={"industry": industry_code, "prefix_region": True},
            )
        )

        for i in range(3):
            company_name = company_name_gen.generate()
            uscc = uscc_gen.generate()
            print(f"  {i+1}. {company_name:<40} | {uscc}")
        print()


def real_world_scenario():
    """真实场景应用示例"""
    print("\n\n10. 真实场景应用示例")
    print("=" * 80)

    print("\n场景：企业工商注册系统")
    print("-" * 80)

    # 模拟企业注册流程
    print("\n正在注册新企业...")

    # 生成企业基本信息
    company_name_gen = default_factory.create_generator(
        GeneratorConfig(
            "company_name", parameters={"industry": "IT", "prefix_region": True}
        )
    )
    uscc_gen = default_factory.create_generator(
        GeneratorConfig("uscc", parameters={"type": "enterprise"})
    )
    org_code_gen = default_factory.create_generator(
        GeneratorConfig("org_code", parameters={})
    )

    company_name = company_name_gen.generate()
    uscc = uscc_gen.generate()
    org_code = org_code_gen.generate()

    print("\n✅ 企业注册成功！")
    print("\n企业注册信息:")
    print(f"  企业名称: {company_name}")
    print(f"  统一社会信用代码: {uscc}")
    print(f"  组织机构代码: {org_code}")
    print(f"  注册日期: {datetime.now().strftime('%Y年%m月%d日')}")
    print("  企业类型: 有限责任公司")
    print("  登记机关: 北京市市场监督管理局")
    print("  企业状态: 存续（在营、开业、在册）")

    # 验证信息
    print("\n数据验证:")
    print(
        f"  企业名称格式: {'✅ 有效' if company_name_gen.validate(company_name) else '❌ 无效'}"
    )
    print(f"  USCC格式: {'✅ 有效' if uscc_gen.validate(uscc) else '❌ 无效'}")
    print(
        f"  组织机构代码格式: {'✅ 有效' if org_code_gen.validate(org_code) else '❌ 无效'}"
    )

    print("\n📋 企业证照已生成，可用于:")
    print("  • 开设银行账户")
    print("  • 税务登记")
    print("  • 社保登记")
    print("  • 公章刻制")
    print("  • 发票申领")


def main():
    """主函数"""
    print("🏢 DataForge 企业信息生成器示例")
    print("本示例展示如何生成企业名称和统一社会信用代码\n")

    try:
        # 运行所有示例
        basic_company_generation()
        company_name_with_parameters()
        uscc_with_parameters()
        complete_company_profile()
        validation_examples()
        export_to_json()
        export_to_csv()
        batch_generation_demo()
        industry_specific_demo()
        real_world_scenario()

        print("\n" + "=" * 80)
        print("✅ 示例演示完成")
        print("=" * 80)
        print("🎉 所有企业信息生成示例已成功运行！")

        print("\n📚 相关文档:")
        print("  • 查看 examples/identifier/identifier_demo.py 了解更多标识符生成")
        print("  • 查看 examples/basic/personal_info_demo.py 了解个人信息生成")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")

        print("\n💡 使用提示:")
        print("  • 企业名称支持参数: industry, type, prefix_region, language")
        print("  • USCC支持参数: type (enterprise/individual/organization/government)")
        print("  • 所有生成的数据都经过格式验证，确保符合规范")

    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
