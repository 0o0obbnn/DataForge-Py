#!/usr/bin/env python3
"""
测试核心算法的正确性
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataforge.core.factory import default_factory
from dataforge.core.generator import GeneratorConfig, GenerationContext

def test_idcard_algorithm():
    """测试身份证校验算法"""
    print("=== 测试身份证校验算法 ===")
    
    # 创建身份证生成器
    config = GeneratorConfig(
        generator_type='idcard',
        parameters={'valid': True}
    )
    generator = default_factory.create_generator(config)
    
    # 生成一些身份证并测试校验
    for i in range(5):
        idcard = generator.generate()
        is_valid = generator.validate(idcard)
        print(f"身份证: {idcard}, 校验结果: {is_valid}")
        
        # 手动验证校验位
        if len(idcard) == 18 and idcard[:17].isdigit():
            weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
            total = sum(int(idcard[j]) * weights[j] for j in range(17))
            expected_check = check_codes[total % 11]
            actual_check = idcard[17]
            manual_valid = expected_check == actual_check
            print(f"  手动校验: {manual_valid}, 期望: {expected_check}, 实际: {actual_check}")
    print()

def test_bankcard_algorithm():
    """测试银行卡Luhn算法"""
    print("=== 测试银行卡Luhn算法 ===")
    
    # 创建银行卡生成器
    config = GeneratorConfig(
        generator_type='bankcard',
        parameters={'valid': True}
    )
    generator = default_factory.create_generator(config)
    
    # 生成一些银行卡并测试校验
    for i in range(5):
        bankcard = generator.generate()
        is_valid = generator.validate(bankcard)
        print(f"银行卡: {bankcard}, 校验结果: {is_valid}")
        
        # 手动验证Luhn算法
        if bankcard.isdigit():
            manual_valid = manual_luhn_validate(bankcard)
            print(f"  手动Luhn校验: {manual_valid}")
    print()

def manual_luhn_validate(card_number: str) -> bool:
    """手动实现Luhn算法验证"""
    total = 0
    reverse_digits = card_number[::-1]
    
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # 偶数位置（从0开始）
            n *= 2
            if n > 9:
                n -= 9
        total += n
    
    return total % 10 == 0

def test_known_cards():
    """测试已知的银行卡号"""
    print("=== 测试已知银行卡号 ===")
    
    # 已知有效的银行卡号（测试用）
    known_valid_cards = [
        "4111111111111111",  # VISA测试卡号
        "5555555555554444",  # MasterCard测试卡号
        "378282246310005",   # AMEX测试卡号
    ]
    
    config = GeneratorConfig(
        generator_type='bankcard',
        parameters={'valid': True}
    )
    generator = default_factory.create_generator(config)
    
    for card in known_valid_cards:
        is_valid = generator.validate(card)
        manual_valid = manual_luhn_validate(card)
        print(f"卡号: {card}")
        print(f"  生成器校验: {is_valid}")
        print(f"  手动校验: {manual_valid}")
    print()

def test_age_idcard_relation():
    """测试年龄-身份证关联"""
    print("=== 测试年龄-身份证关联 ===")
    
    from datetime import datetime
    
    configs = [
        GeneratorConfig(generator_type='age', parameters={'min': 25, 'max': 35}),
        GeneratorConfig(generator_type='idcard', parameters={})
    ]
    
    print("生成5条关联记录并检查年龄匹配:")
    for i in range(5):
        context = GenerationContext()
        result = default_factory.generate_batch_with_relations(configs, context)
        
        age = result.get('age', 0)
        idcard = result.get('idcard', '')
        
        if len(idcard) == 18 and idcard[:17].isdigit():
            birth_year = int(idcard[6:10])
            current_year = datetime.now().year
            expected_age = current_year - birth_year
            match = age == expected_age
            print(f"记录{i+1}: 年龄={age}, 身份证年份={birth_year}, 期望年龄={expected_age}, 匹配={match}")
        else:
            print(f"记录{i+1}: 无效身份证 {idcard}")
    print()

def main():
    """主测试函数"""
    print("DataForge 核心算法测试")
    print("=" * 50)
    
    try:
        test_idcard_algorithm()
        test_bankcard_algorithm()
        test_known_cards()
        test_age_idcard_relation()
        
        print("所有算法测试完成！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())