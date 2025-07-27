#!/usr/bin/env python3
"""
测试身份证校验问题
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataforge.core.factory import default_factory
from dataforge.core.generator import GeneratorConfig

def test_idcard_validation():
    """测试身份证校验问题"""
    print("=== 测试身份证校验问题 ===")
    
    config = GeneratorConfig(
        generator_type='idcard',
        parameters={'valid': True}
    )
    generator = default_factory.create_generator(config)
    
    # 测试生成的身份证
    print("1. 测试生成的身份证:")
    for i in range(3):
        idcard = generator.generate()
        is_valid = generator.validate(idcard)
        print(f"   {idcard}: {is_valid}")
    
    # 测试固定的身份证号
    print("\n2. 测试固定的身份证号:")
    test_ids = [
        "110000199001010008",  # 这个应该是有效的吗？
        "110101199003071354",  # 手动生成一个
    ]
    
    for test_id in test_ids:
        is_valid = generator.validate(test_id)
        print(f"   {test_id}: {is_valid}")
        
        # 手动计算校验位
        if len(test_id) == 18:
            weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
            
            if test_id[:17].isdigit():
                total = sum(int(test_id[i]) * weights[i] for i in range(17))
                expected_check = check_codes[total % 11]
                actual_check = test_id[17]
                print(f"     手动校验: 期望={expected_check}, 实际={actual_check}, 匹配={expected_check == actual_check}")
            else:
                print(f"     前17位不全是数字")
    
    print()

def test_bankcard_validation():
    """测试银行卡校验问题"""
    print("=== 测试银行卡校验问题 ===")
    
    config = GeneratorConfig(
        generator_type='bankcard',
        parameters={'valid': True}
    )
    generator = default_factory.create_generator(config)
    
    print("1. 测试10个生成的银行卡:")
    valid_count = 0
    for i in range(10):
        bankcard = generator.generate()
        is_valid = generator.validate(bankcard)
        if is_valid:
            valid_count += 1
        print(f"   {i+1}. {bankcard}: {is_valid}")
    
    print(f"\n有效率: {valid_count}/10 = {valid_count/10*100:.1f}%")
    print()

if __name__ == '__main__':
    test_idcard_validation()
    test_bankcard_validation()