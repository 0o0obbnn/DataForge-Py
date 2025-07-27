#!/usr/bin/env python3
"""
测试数据关联性管理系统
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataforge.core.factory import default_factory
from dataforge.core.generator import GeneratorConfig, GenerationContext
from dataforge.core.relations import default_relation_manager
import json

def test_single_generator():
    """测试单个字段生成"""
    print("=== 测试单个字段生成 ===")
    
    # 测试身份证生成
    config = GeneratorConfig(
        generator_type='idcard',
        parameters={'region': '110000', 'gender': 'MALE'}
    )
    
    generator = default_factory.create_generator(config)
    idcard = generator.generate()
    print(f"生成的身份证: {idcard}")
    print(f"校验结果: {generator.validate(idcard)}")
    print()

def test_relation_derivation():
    """测试关联推导"""
    print("=== 测试关联推导 ===")
    
    # 配置身份证和年龄生成器
    configs = [
        GeneratorConfig(generator_type='idcard', parameters={'region': '110000'}),
        GeneratorConfig(generator_type='age', parameters={})
    ]
    
    # 使用关联生成
    context = GenerationContext()
    result = default_factory.generate_batch_with_relations(configs, context)
    
    print(f"生成结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 验证关联性：从身份证推导的年龄应该匹配
    if 'idcard' in result and 'age' in result:
        idcard = result['idcard']
        age = result['age']
        if len(idcard) == 18 and idcard[:17].isdigit():
            birth_year = int(idcard[6:10])
            from datetime import datetime
            expected_age = datetime.now().year - birth_year
            print(f"身份证出生年份: {birth_year}")
            print(f"预期年龄: {expected_age}")
            print(f"生成年龄: {age}")
            print(f"年龄匹配: {age == expected_age}")
    print()

def test_gender_name_relation():
    """测试性别-姓名关联"""
    print("=== 测试性别-姓名关联 ===")
    
    # 配置身份证、性别和姓名生成器
    configs = [
        GeneratorConfig(generator_type='idcard', parameters={'gender': 'FEMALE'}),
        GeneratorConfig(generator_type='name', parameters={})
    ]
    
    context = GenerationContext()
    result = default_factory.generate_batch_with_relations(configs, context)
    
    print(f"生成结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 检查性别关联
    if 'idcard' in result:
        idcard = result['idcard']
        if len(idcard) == 18:
            gender_digit = int(idcard[16])
            gender = 'MALE' if gender_digit % 2 == 1 else 'FEMALE'
            print(f"身份证性别: {gender}")
    print()

def test_complex_relations():
    """测试复杂关联"""
    print("=== 测试复杂关联 ===")
    
    # 配置多个相关字段
    configs = [
        GeneratorConfig(generator_type='idcard', parameters={'region': '440000'}),
        GeneratorConfig(generator_type='name', parameters={}),
        GeneratorConfig(generator_type='address', parameters={'province': '广东省'})
    ]
    
    # 生成多条记录
    print("生成5条关联记录:")
    for i in range(5):
        context = GenerationContext()
        result = default_factory.generate_batch_with_relations(configs, context)
        print(f"记录 {i+1}: {json.dumps(result, ensure_ascii=False)}")
    print()

def test_dependency_ordering():
    """测试依赖排序"""
    print("=== 测试依赖排序 ===")
    
    # 测试字段依赖顺序
    field_names = ['name', 'idcard', 'age', 'address']
    ordered_fields = default_relation_manager.get_relation_dependencies(field_names)
    
    print(f"原始字段顺序: {field_names}")
    print(f"依赖排序后: {ordered_fields}")
    print()

def test_manual_relations():
    """测试手动添加关联规则"""
    print("=== 测试手动关联规则 ===")
    
    # 添加自定义关联规则
    from dataforge.core.relations import RelationRule
    
    def custom_age_to_name(age, context):
        """根据年龄约束姓名生成"""
        if age < 30:
            return {'type': 'modern'}  # 现代化名字
        else:
            return {'type': 'traditional'}  # 传统名字
    
    custom_rule = RelationRule(
        source_field='age',
        target_field='name',
        relation_type='constrain',
        rule_func=custom_age_to_name,
        priority=15
    )
    
    default_relation_manager.add_relation_rule(custom_rule)
    
    # 测试自定义规则
    configs = [
        GeneratorConfig(generator_type='age', parameters={'min': 35, 'max': 50}),
        GeneratorConfig(generator_type='name', parameters={})
    ]
    
    context = GenerationContext()
    result = default_factory.generate_batch_with_relations(configs, context)
    
    print(f"高年龄组结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print()

def main():
    """主测试函数"""
    print("DataForge 数据关联性管理系统测试")
    print("=" * 50)
    
    try:
        test_single_generator()
        test_relation_derivation()
        test_gender_name_relation()
        test_complex_relations()
        test_dependency_ordering()
        test_manual_relations()
        
        print("所有测试完成！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())