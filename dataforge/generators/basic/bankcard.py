"""
银行卡号生成器
"""
import random
from typing import Optional, Dict, Any, List
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator


class BankCardGenerator(ValidatedDataGenerator[str]):
    """银行卡号生成器（支持Luhn算法校验）"""
    
    # BIN码数据库（简化版）
    BIN_DATABASE = {
        # 中国银行卡BIN码
        'ICBC': ['622202', '622200', '621558', '621559'],  # 工商银行
        'CCB': ['436742', '622700', '621700', '621068'],   # 建设银行
        'CMB': ['621286', '621483', '621485', '621486'],   # 招商银行
        'ABC': ['622848', '622849', '621672', '621673'],   # 农业银行
        'BOC': ['621661', '621662', '456351', '601382'],   # 中国银行
        
        # 国际卡组织BIN码
        'VISA': ['4'],
        'MASTERCARD': ['5'],
        'UNIONPAY': ['62'],
        'JCB': ['35'],
    }
    
    def _setup(self) -> None:
        self.card_type = self.parameters.get('type', 'BOTH')  # DEBIT, CREDIT, BOTH
        self.issuer = self.parameters.get('issuer', 'ANY')    # VISA, MC, UNIONPAY, 具体银行, ANY
        self.bank = self.parameters.get('bank', 'ANY')        # 具体银行代码
        self.length = self.parameters.get('length', 16)       # 卡号长度
        self.valid = self.parameters.get('valid', True)       # 是否符合Luhn算法
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始银行卡号"""
        if not self.valid:
            return self._generate_invalid_card()
        
        # 1. 选择BIN码
        bin_code = self._select_bin_code()
        
        # 2. 确定卡号长度
        target_length = self._determine_length(bin_code)
        
        # 3. 生成主体号码（除最后一位校验位）
        main_digits = self._generate_main_digits(bin_code, target_length - 1)
        
        # 4. 计算Luhn校验位
        check_digit = self._calculate_luhn_check_digit(main_digits)
        
        return main_digits + str(check_digit)
    
    def _select_bin_code(self) -> str:
        """选择BIN码"""
        if self.bank != 'ANY' and self.bank in self.BIN_DATABASE:
            return random.choice(self.BIN_DATABASE[self.bank])
        
        if self.issuer != 'ANY' and self.issuer in self.BIN_DATABASE:
            return random.choice(self.BIN_DATABASE[self.issuer])
        
        # 默认选择中国银行卡
        chinese_banks = ['ICBC', 'CCB', 'CMB', 'ABC', 'BOC']
        bank = random.choice(chinese_banks)
        return random.choice(self.BIN_DATABASE[bank])
    
    def _determine_length(self, bin_code: str) -> int:
        """确定卡号长度"""
        if self.length:
            return self.length
        
        # 根据BIN码确定默认长度
        if bin_code.startswith('4') or bin_code.startswith('5'):  # VISA/MC
            return 16
        elif bin_code.startswith('62'):  # 银联
            return 19
        elif bin_code.startswith('35'):  # JCB
            return 16
        else:
            return 16  # 默认16位
    
    def _generate_main_digits(self, bin_code: str, total_length: int) -> str:
        """生成主体数字（不含校验位）"""
        remaining_length = total_length - len(bin_code)
        random_digits = ''.join([str(random.randint(0, 9)) for _ in range(remaining_length)])
        return bin_code + random_digits
    
    def _calculate_luhn_check_digit(self, digits: str) -> int:
        """计算Luhn算法校验位"""
        # Luhn算法：从右到左，奇数位置不变，偶数位置*2，如果结果>9则减9
        total = 0
        for i, digit in enumerate(reversed(digits)):
            n = int(digit)
            if i % 2 == 1:  # 偶数位置（从0开始计数）
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        
        # 计算使总和为10的倍数的数字
        return (10 - (total % 10)) % 10
    
    def _generate_invalid_card(self) -> str:
        """生成无效银行卡号"""
        invalid_type = random.choice(['wrong_length', 'wrong_luhn', 'wrong_format'])
        
        if invalid_type == 'wrong_length':
            # 错误长度
            wrong_length = random.choice([12, 13, 14, 15, 17, 18, 20, 21])
            return ''.join([str(random.randint(0, 9)) for _ in range(wrong_length)])
        elif invalid_type == 'wrong_luhn':
            # 正确格式但Luhn校验错误
            valid_card = self._generate_raw(None)
            # 修改最后一位为错误的校验位
            wrong_check = (int(valid_card[-1]) + random.randint(1, 9)) % 10
            return valid_card[:-1] + str(wrong_check)
        else:  # wrong_format
            # 包含字母或特殊字符
            length = random.choice([16, 19])
            invalid_card = ''.join([
                random.choice('0123456789ABCDEF-/') for _ in range(length)
            ])
            return invalid_card
    
    def validate(self, data: str) -> bool:
        """使用Luhn算法校验银行卡号"""
        if not isinstance(data, str):
            return False
        
        # 移除空格和连字符
        clean_data = data.replace(' ', '').replace('-', '')
        
        # 检查是否全为数字
        if not clean_data.isdigit():
            return False
        
        # 检查长度
        if len(clean_data) < 13 or len(clean_data) > 19:
            return False
        
        # Luhn算法校验
        return self._luhn_validate(clean_data)
    
    def _luhn_validate(self, card_number: str) -> bool:
        """Luhn算法校验"""
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
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['type', 'issuer', 'bank', 'length', 'valid']


@register_generator('bankcard', ['credit_card', 'debit_card', '银行卡'])
class ChineseBankCardGenerator(BankCardGenerator):
    """中国银行卡号生成器注册版本"""
    pass