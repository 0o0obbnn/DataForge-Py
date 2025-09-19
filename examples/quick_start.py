"""
简单的使用示例
演示如何快速使用ChineseDataGenerator
"""

from chinese_data_generator import ChineseDataGenerator

def quick_start():
    """快速开始示例"""
    print("快速开始 - ChineseDataGenerator")
    print("=" * 40)
    
    # 创建生成器实例
    generator = ChineseDataGenerator()
    
    # 生成基本信息
    print("\n基本信息生成:")
    print(f"姓名: {generator.generate_name()}")
    print(f"身份证: {generator.generate_idcard()}")
    print(f"手机号: {generator.generate_phone()}")
    print(f"座机号: {generator.generate_landline()}")
    
    # 生成企业信息
    print("\n企业信息生成:")
    print(f"公司名称: {generator.generate_company_name()}")
    print(f"统一社会信用代码: {generator.generate_uscc()}")
    
    # 生成完整档案
    print("\n完整个人档案:")
    profile = generator.generate_person_profile(gender='male', region='北京')
    for key, value in profile.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    quick_start()
