"""
手机号码生成器
"""
import random
from typing import Optional, Dict, Any, List
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator


class PhoneGenerator(ValidatedDataGenerator[str]):
    """中国手机号码生成器"""
    
    # 中国三大运营商号段
    CHINA_MOBILE_PREFIXES = [
        '134', '135', '136', '137', '138', '139',  # 2G
        '147', '150', '151', '152', '157', '158', '159',  # 3G
        '172', '178', '182', '183', '184', '187', '188',  # 4G
        '195', '197', '198'  # 5G
    ]
    
    CHINA_UNICOM_PREFIXES = [
        '130', '131', '132',  # 2G
        '155', '156', '166',  # 3G
        '171', '175', '176', '185', '186',  # 4G
        '196'  # 5G
    ]
    
    CHINA_TELECOM_PREFIXES = [
        '133', '149', '153', '173', '174', '177', '180', '181', '189', '191', '193', '199'
    ]
    
    # 虚拟运营商号段
    VIRTUAL_PREFIXES = [
        '170', '171'  # 虚拟运营商
    ]
    
    def _setup(self) -> None:
        self.region = self.parameters.get('region', 'CN')
        self.prefix = self.parameters.get('prefix', None)  # 指定前缀列表
        self.valid = self.parameters.get('valid', True)
        self.operator = self.parameters.get('operator', 'ANY')  # MOBILE, UNICOM, TELECOM, VIRTUAL, ANY
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始手机号码"""
        if not self.valid:
            return self._generate_invalid_phone()
        
        # 1. 选择前缀
        prefix = self._select_prefix()
        
        # 2. 生成后8位
        suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        
        return prefix + suffix
    
    def _select_prefix(self) -> str:
        """选择号码前缀"""
        if self.prefix:
            # 使用指定的前缀列表
            if isinstance(self.prefix, list):
                return random.choice(self.prefix)
            else:
                return str(self.prefix)
        
        # 根据运营商选择前缀
        if self.operator == 'MOBILE':
            return random.choice(self.CHINA_MOBILE_PREFIXES)
        elif self.operator == 'UNICOM':
            return random.choice(self.CHINA_UNICOM_PREFIXES)
        elif self.operator == 'TELECOM':
            return random.choice(self.CHINA_TELECOM_PREFIXES)
        elif self.operator == 'VIRTUAL':
            return random.choice(self.VIRTUAL_PREFIXES)
        else:
            # 随机选择所有前缀
            all_prefixes = (self.CHINA_MOBILE_PREFIXES + 
                          self.CHINA_UNICOM_PREFIXES + 
                          self.CHINA_TELECOM_PREFIXES)
            return random.choice(all_prefixes)
    
    def _generate_invalid_phone(self) -> str:
        """生成无效手机号码"""
        invalid_type = random.choice(['wrong_length', 'wrong_prefix', 'wrong_format'])
        
        if invalid_type == 'wrong_length':
            # 错误长度
            wrong_length = random.choice([9, 10, 12, 13])
            return ''.join([str(random.randint(0, 9)) for _ in range(wrong_length)])
        elif invalid_type == 'wrong_prefix':
            # 错误前缀（不是有效的手机号段）
            invalid_prefixes = ['120', '121', '122', '100', '101', '102']
            prefix = random.choice(invalid_prefixes)
            suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            return prefix + suffix
        else:  # wrong_format
            # 包含字母或特殊字符
            invalid_phone = ''.join([
                random.choice('0123456789ABCDEF-() ') for _ in range(11)
            ])
            return invalid_phone
    
    def validate(self, data: str) -> bool:
        """校验手机号码"""
        if not isinstance(data, str):
            return False
        
        # 移除空格、连字符等格式字符
        clean_phone = data.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # 检查长度
        if len(clean_phone) != 11:
            return False
        
        # 检查是否全为数字
        if not clean_phone.isdigit():
            return False
        
        # 检查前缀是否有效
        prefix = clean_phone[:3]
        all_valid_prefixes = (self.CHINA_MOBILE_PREFIXES + 
                            self.CHINA_UNICOM_PREFIXES + 
                            self.CHINA_TELECOM_PREFIXES + 
                            self.VIRTUAL_PREFIXES)
        
        return prefix in all_valid_prefixes
    
    def get_operator_info(self, phone: str) -> Dict[str, str]:
        """获取手机号运营商信息"""
        if not self.validate(phone):
            return {'operator': 'UNKNOWN', 'type': 'INVALID'}
        
        prefix = phone[:3]
        
        if prefix in self.CHINA_MOBILE_PREFIXES:
            return {'operator': 'CHINA_MOBILE', 'name': '中国移动'}
        elif prefix in self.CHINA_UNICOM_PREFIXES:
            return {'operator': 'CHINA_UNICOM', 'name': '中国联通'}
        elif prefix in self.CHINA_TELECOM_PREFIXES:
            return {'operator': 'CHINA_TELECOM', 'name': '中国电信'}
        elif prefix in self.VIRTUAL_PREFIXES:
            return {'operator': 'VIRTUAL', 'name': '虚拟运营商'}
        else:
            return {'operator': 'UNKNOWN', 'name': '未知'}
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['region', 'prefix', 'valid', 'operator']


@register_generator('phone', ['mobile', 'cellphone', '手机号'])
class ChinesePhoneGenerator(PhoneGenerator):
    """中国手机号码生成器注册版本"""
    pass