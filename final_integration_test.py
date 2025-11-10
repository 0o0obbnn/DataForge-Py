#!/usr/bin/env python3
"""最终集成测试 - 验证所有修复"""

import sys
from dataforge import default_factory, GeneratorConfig

def comprehensive_test():
    """全面的生成器测试"""
    print("🚀 开始最终集成测试...")
    
    # 测试用例：包含各种类型的生成器
    test_cases = [
        # 基础信息
        ("name", {}, "姓名"),
        ("company_name", {}, "公司名称"),
        ("address", {}, "地址"),
        ("age", {}, "年龄"),
        ("gender", {}, "性别"),
        
        # 联系方式
        ("phone", {}, "电话号码"),
        ("email", {}, "电子邮件"),
        
        # 身份标识
        ("idcard", {}, "身份证"),
        ("bankcard", {}, "银行卡"),
        ("generic_uuid", {}, "UUID"),
        ("generic_ulid", {}, "ULID"),
        
        # 物流信息
        ("generic_waybill", {}, "运单信息"),
        ("generic_tracking_number", {}, "跟踪号码"),
        
        # 教育职业
        ("education", {}, "教育程度"),
        ("occupation", {}, "职业"),
        
        # 数值类型
        ("integer", {"min": 1, "max": 100}, "整数"),
        ("decimal", {"min": 1.0, "max": 100.0}, "小数"),
        ("currency", {}, "货币"),
        ("percentage", {}, "百分比"),
        
        # 文本类型
        ("string", {"length": 10}, "字符串"),
        ("chinese_text", {"length": 20}, "中文文本"),
        ("english_text", {"length": 15}, "英文文本"),
        ("long_text", {"paragraphs": 2}, "长文本"),
        
        # 其他
        ("boolean", {}, "布尔值"),
        ("enum", {"values": ["A", "B", "C"]}, "枚举值"),
    ]
    
    success_count = 0
    failed_cases = []
    
    for generator_name, params, description in test_cases:
        try:
            config = GeneratorConfig(
                generator_type=generator_name,
                parameters=params
            )
            
            generator = default_factory.create_generator(config)
            result = generator.generate()
            
            print(f"✅ {description} ({generator_name}): {result}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ {description} ({generator_name}): {e}")
            failed_cases.append(generator_name)
    
    print(f"\n📊 测试结果统计:")
    print(f"总测试数: {len(test_cases)}")
    print(f"成功: {success_count}")
    print(f"失败: {len(failed_cases)}")
    print(f"成功率: {success_count/len(test_cases)*100:.1f}%")
    
    if failed_cases:
        print(f"\n❌ 失败的生成器: {failed_cases}")
    else:
        print(f"\n🎉 所有测试通过！生成器模块导入问题已完全解决！")
    
    # 显示注册表信息
    from dataforge import default_registry
    generators = default_registry._generators
    print(f"\n📋 注册表包含 {len(generators)} 个生成器")
    
    return len(failed_cases) == 0

if __name__ == "__main__":
    success = comprehensive_test()
    sys.exit(0 if success else 1)