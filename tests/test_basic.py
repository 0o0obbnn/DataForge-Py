"""
DataForge核心功能测试
"""
import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dataforge.core.generator import GeneratorConfig
from dataforge.core.factory import default_factory
from dataforge.generators.basic.idcard import IDCardGenerator
from dataforge.generators.basic.bankcard import BankCardGenerator
from dataforge.generators.basic.phone import PhoneGenerator


class TestIDCardGenerator(unittest.TestCase):
    """身份证生成器测试"""
    
    def setUp(self):
        self.config = GeneratorConfig(
            generator_type='idcard',
            parameters={
                'region': '北京',
                'gender': 'MALE',
                'birth_date_range': ('1990-01-01', '2000-12-31'),
                'valid': True
            }
        )
        self.generator = IDCardGenerator(self.config)
    
    def test_generate_single(self):
        """测试生成单个身份证号"""
        id_card = self.generator.generate_single()
        
        # 基本格式检查
        self.assertIsInstance(id_card, str)
        self.assertEqual(len(id_card), 18)
        
        # 校验检查
        self.assertTrue(self.generator.validate(id_card))
    
    def test_generate_batch(self):
        """测试批量生成"""
        id_cards = self.generator.generate_batch(10)
        
        self.assertEqual(len(id_cards), 10)
        for id_card in id_cards:
            self.assertTrue(self.generator.validate(id_card))
    
    def test_gender_constraint(self):
        """测试性别约束"""
        # 测试男性身份证
        male_config = GeneratorConfig(
            generator_type='idcard',
            parameters={'gender': 'MALE'}
        )
        male_generator = IDCardGenerator(male_config)
        
        for _ in range(10):
            id_card = male_generator.generate_single()
            gender_digit = int(id_card[16])
            self.assertEqual(gender_digit % 2, 1)  # 奇数表示男性
    
    def test_invalid_generation(self):
        """测试无效数据生成"""
        invalid_config = GeneratorConfig(
            generator_type='idcard',
            parameters={'valid': False}
        )
        invalid_generator = IDCardGenerator(invalid_config)
        
        invalid_id = invalid_generator.generate_single()
        # 无效数据不应该通过校验
        self.assertFalse(invalid_generator.validate(invalid_id))


class TestBankCardGenerator(unittest.TestCase):
    """银行卡生成器测试"""
    
    def setUp(self):
        self.config = GeneratorConfig(
            generator_type='bankcard',
            parameters={'valid': True}
        )
        self.generator = BankCardGenerator(self.config)
    
    def test_generate_single(self):
        """测试生成单个银行卡号"""
        card = self.generator.generate_single()
        
        # 基本格式检查
        self.assertIsInstance(card, str)
        self.assertTrue(13 <= len(card) <= 19)
        self.assertTrue(card.isdigit())
        
        # Luhn算法校验
        self.assertTrue(self.generator.validate(card))
    
    def test_luhn_algorithm(self):
        """测试Luhn算法校验"""
        # 已知有效的测试卡号
        valid_cards = [
            '4111111111111111',  # Visa测试卡
            '5555555555554444',  # MasterCard测试卡
        ]
        
        for card in valid_cards:
            self.assertTrue(self.generator._luhn_validate(card))
        
        # 无效卡号
        invalid_cards = [
            '4111111111111112',  # 校验位错误
            '1234567890123456',  # 无效卡号
        ]
        
        for card in invalid_cards:
            self.assertFalse(self.generator._luhn_validate(card))
    
    def test_bank_specific_generation(self):
        """测试特定银行卡号生成"""
        icbc_config = GeneratorConfig(
            generator_type='bankcard',
            parameters={'bank': 'ICBC'}
        )
        icbc_generator = BankCardGenerator(icbc_config)
        
        card = icbc_generator.generate_single()
        # 检查是否以工商银行BIN码开头
        icbc_bins = ['622202', '622200', '621558', '621559']
        self.assertTrue(any(card.startswith(bin_code) for bin_code in icbc_bins))


class TestPhoneGenerator(unittest.TestCase):
    """手机号生成器测试"""
    
    def setUp(self):
        self.config = GeneratorConfig(
            generator_type='phone',
            parameters={'valid': True}
        )
        self.generator = PhoneGenerator(self.config)
    
    def test_generate_single(self):
        """测试生成单个手机号"""
        phone = self.generator.generate_single()
        
        # 基本格式检查
        self.assertIsInstance(phone, str)
        self.assertEqual(len(phone), 11)
        self.assertTrue(phone.isdigit())
        
        # 校验检查
        self.assertTrue(self.generator.validate(phone))
    
    def test_operator_specific_generation(self):
        """测试特定运营商手机号生成"""
        mobile_config = GeneratorConfig(
            generator_type='phone',
            parameters={'operator': 'MOBILE'}
        )
        mobile_generator = PhoneGenerator(mobile_config)
        
        phone = mobile_generator.generate_single()
        prefix = phone[:3]
        self.assertIn(prefix, mobile_generator.CHINA_MOBILE_PREFIXES)
    
    def test_operator_info(self):
        """测试运营商信息获取"""
        # 测试中国移动号段
        mobile_phone = '13800138000'
        if self.generator.validate(mobile_phone):
            info = self.generator.get_operator_info(mobile_phone)
            self.assertEqual(info['operator'], 'CHINA_MOBILE')


class TestGeneratorFactory(unittest.TestCase):
    """生成器工厂测试"""
    
    def test_create_generator(self):
        """测试创建生成器"""
        config = GeneratorConfig(
            generator_type='idcard',
            parameters={'region': '上海'}
        )
        
        generator = default_factory.create_generator(config)
        self.assertIsInstance(generator, IDCardGenerator)
    
    def test_unknown_generator(self):
        """测试创建未知生成器"""
        config = GeneratorConfig(
            generator_type='unknown_type',
            parameters={}
        )
        
        with self.assertRaises(ValueError):
            default_factory.create_generator(config)


class TestOutputFormatter(unittest.TestCase):
    """输出格式化器测试"""
    
    def setUp(self):
        from dataforge.output.formatter import OutputFormatter
        self.formatter = OutputFormatter()
        self.test_data = {
            'idcard': ['110101199001011234', '110101199001012345'],
            'phone': ['13800138000', '13800138001']
        }
    
    def test_json_format(self):
        """测试JSON格式化"""
        result = self.formatter.format(self.test_data, 'json')
        self.assertIsInstance(result, str)
        
        import json
        parsed = json.loads(result)
        self.assertEqual(parsed, self.test_data)
    
    def test_csv_format(self):
        """测试CSV格式化"""
        result = self.formatter.format(self.test_data, 'csv')
        self.assertIsInstance(result, str)
        self.assertIn('idcard', result)
        self.assertIn('phone', result)
    
    def test_xml_format(self):
        """测试XML格式化"""
        result = self.formatter.format(self.test_data, 'xml')
        self.assertIsInstance(result, str)
        self.assertIn('<dataforge_output>', result)
        self.assertIn('</dataforge_output>', result)


if __name__ == '__main__':
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestIDCardGenerator,
        TestBankCardGenerator,
        TestPhoneGenerator,
        TestGeneratorFactory,
        TestOutputFormatter
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 输出测试结果
    if result.wasSuccessful():
        print("\\n✓ 所有测试通过！")
    else:
        print(f"\\n✗ 测试失败: {len(result.failures)} 个失败, {len(result.errors)} 个错误")
        sys.exit(1)