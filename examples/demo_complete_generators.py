"""
示例脚本：演示DataForge框架的完整功能
"""

from dataforge.core.factory import default_factory, GeneratorConfig
from chinese_data_generator import ChineseDataGenerator
import json

def demo_core_framework():
    """演示核心框架使用"""
    print("=" * 60)
    print("DataForge核心框架演示")
    print("=" * 60)
    
    # 使用工厂模式创建生成器
    print("\n1. 使用工厂模式创建生成器")
    
    # 创建姓名生成器
    name_config = GeneratorConfig(
        generator_type="name",
        parameters={"gender": "male", "length": 2}
    )
    name_generator = default_factory.create_generator(name_config)
    print(f"男性姓名: {name_generator.generate()}")
    
    # 创建身份证生成器
    id_config = GeneratorConfig(
        generator_type="idcard",
        parameters={"region": "北京", "gender": "MALE"}
    )
    id_generator = default_factory.create_generator(id_config)
    print(f"北京男性身份证: {id_generator.generate()}")
    
    # 创建手机号生成器
    phone_config = GeneratorConfig(
        generator_type="phone",
        parameters={"carrier": "mobile"}
    )
    phone_generator = default_factory.create_generator(phone_config)
    print(f"中国移动号码: {phone_generator.generate()}")

def demo_chinese_generator():
    """演示中文数据生成器"""
    print("\n\n=" * 60)
    print("中文数据生成器演示")
    print("=" * 60)
    
    generator = ChineseDataGenerator()
    
    print("\n1. 基础信息生成")
    print(f"姓名: {generator.generate_name()}")
    print(f"身份证: {generator.generate_idcard()}")
    print(f"手机号: {generator.generate_phone()}")
    print(f"座机号: {generator.generate_landline()}")
    print(f"公司名称: {generator.generate_company_name()}")
    print(f"统一社会信用代码: {generator.generate_uscc()}")
    
    print("\n2. 参数化生成")
    print(f"女性姓名: {generator.generate_name('female')}")
    print(f"上海身份证: {generator.generate_idcard('FEMALE', '上海')}")
    print(f"中国联通号码: {generator.generate_phone('unicom')}")
    print(f"深圳座机: {generator.generate_landline('0755')}")
    print(f"科技公司: {generator.generate_company_name('tech', '北京')}")
    
    print("\n3. 完整档案生成")
    person = generator.generate_person_profile(
        gender='female',
        region='广东',
        carrier='telecom',
        area_code='020'
    )
    
    print("个人档案:")
    for key, value in person.items():
        print(f"  {key}: {value}")
    
    print("\n4. 企业档案生成")
    company = generator.generate_company_profile(
        company_type='finance',
        region='上海'
    )
    
    print("企业档案:")
    for key, value in company.items():
        print(f"  {key}: {value}")

def demo_batch_generation():
    """演示批量生成"""
    print("\n\n=" * 60)
    print("批量数据生成演示")
    print("=" * 60)
    
    generator = ChineseDataGenerator()
    
    print("\n1. 批量生成指定类型数据")
    batch_data = generator.generate_batch_data(
        data_types=['name', 'phone', 'idcard'],
        count=5,
        gender='male',
        region='北京'
    )
    
    for data_type, data_list in batch_data.items():
        print(f"\n{data_type}类型数据:")
        for i, data in enumerate(data_list, 1):
            print(f"  {i}. {data}")
    
    print("\n2. 混合数据生成")
    mixed_data = generator.generate_mixed_data(
        person_count=3,
        company_count=2,
        gender='female',
        region='江苏'
    )
    
    print("\n个人信息:")
    for person in mixed_data['个人信息']:
        print(f"  {person}")
    
    print("\n企业信息:")
    for company in mixed_data['企业信息']:
        print(f"  {company}")

def demo_data_validation():
    """演示数据验证"""
    print("\n\n=" * 60)
    print("数据验证演示")
    print("=" * 60)
    
    generator = ChineseDataGenerator()
    
    # 生成数据并验证
    test_data = {
        'name': generator.generate_name(),
        'idcard': generator.generate_idcard(),
        'phone': generator.generate_phone(),
        'company': generator.generate_company_name(),
        'uscc': generator.generate_uscc()
    }
    
    print("\n生成的数据及其验证结果:")
    for data_type, data in test_data.items():
        is_valid = generator.validate_data(data, data_type)
        status = "✓" if is_valid else "✗"
        print(f"  {status} {data_type}: {data} - {'有效' if is_valid else '无效'}")

def demo_custom_configuration():
    """演示自定义配置"""
    print("\n\n=" * 60)
    print("自定义配置演示")
    print("=" * 60)
    
    # 创建自定义配置的生成器
    custom_config = {
        'name': {'gender': 'female', 'length': 3},
        'idcard': {'region': '浙江', 'valid': True},
        'phone': {'carrier': 'unicom'},
        'landline': {'city': '杭州'},
        'company': {'type': 'tech', 'region': '杭州'},
        'uscc': {'org_type': 'enterprise', 'region': '浙江'}
    }
    
    custom_generator = ChineseDataGenerator(custom_config)
    
    print("\n使用自定义配置生成的数据:")
    print(f"3字女性姓名: {custom_generator.generate_name()}")
    print(f"浙江身份证: {custom_generator.generate_idcard()}")
    print(f"联通手机号: {custom_generator.generate_phone()}")
    print(f"杭州座机: {custom_generator.generate_landline()}")
    print(f"杭州科技公司: {custom_generator.generate_company_name()}")
    print(f"浙江企业信用代码: {custom_generator.generate_uscc()}")

def demo_export_formats():
    """演示不同导出格式"""
    print("\n\n=" * 60)
    print("数据导出格式演示")
    print("=" * 60)
    
    generator = ChineseDataGenerator()
    
    # 生成数据
    data = generator.generate_mixed_data(person_count=2, company_count=1)
    
    print("\n1. JSON格式输出:")
    json_output = json.dumps(data, ensure_ascii=False, indent=2)
    print(json_output)
    
    print("\n2. CSV格式数据（个人信息）:")
    print("序号,姓名,身份证号码,手机号码,座机号码")
    for person in data['个人信息']:
        csv_line = f"{person['序号']},{person['姓名']},{person['身份证号码']},{person['手机号码']},{person['座机号码']}"
        print(csv_line)
    
    print("\n3. 格式化输出:")
    for i, person in enumerate(data['个人信息'], 1):
        print(f"{i:2d}. {person['姓名']:8s} - {person['手机号码']} - {person['身份证号码']}")

def main():
    """主函数"""
    print("DataForge测试数据生成框架 - 完整功能演示")
    print("="*80)
    
    try:
        # 演示各种功能
        demo_core_framework()
        demo_chinese_generator()
        demo_batch_generation()
        demo_data_validation()
        demo_custom_configuration()
        demo_export_formats()
        
        print("\n\n=" * 60)
        print("演示完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
