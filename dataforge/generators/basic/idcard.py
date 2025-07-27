"""
身份证号码生成器
"""
import random
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator
from ...core.validator import CustomValidator


class IDCardGenerator(ValidatedDataGenerator[str]):
    """中国身份证号码生成器"""
    
    # 身份证校验位计算的权重
    ID_WEIGHTS = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    ID_CHECK_CODES = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    
    # 地区代码映射（简化版，实际应从resources加载）
    REGION_CODES = {
        '北京': ['110000', '110100'],
        '上海': ['310000', '310100'], 
        '广东': ['440000', '440100', '440300', '440600'],
        '浙江': ['330000', '330100', '330200', '330300'],
        '江苏': ['320000', '320100', '320200', '320300'],
    }
    
    def _setup(self) -> None:
        self.region = self.parameters.get('region')
        self.birth_date_range = self.parameters.get('birth_date_range', ('1980-01-01', '2000-12-31'))
        self.gender = self.parameters.get('gender', 'ANY')  # MALE, FEMALE, ANY
        self.valid = self.parameters.get('valid', True)
        
        # 解析日期范围
        if isinstance(self.birth_date_range, tuple):
            start_str, end_str = self.birth_date_range
            self.start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
            self.end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
        else:
            # 默认范围
            self.start_date = date(1980, 1, 1)
            self.end_date = date(2000, 12, 31)
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始身份证号码"""
        if not self.valid:
            return self._generate_invalid_idcard()
        
        # 1. 地区代码（6位）
        region_code = self._get_region_code()
        
        # 2. 出生日期（8位）
        birth_date = self._get_random_birth_date(context)
        birth_str = birth_date.strftime('%Y%m%d')
        
        # 3. 顺序码（3位）
        sequence_code = self._get_sequence_code()
        
        # 4. 校验位（1位）
        id_17 = region_code + birth_str + sequence_code
        check_digit = self._calculate_check_digit(id_17)
        
        return id_17 + check_digit
    
    def _get_region_code(self) -> str:
        """获取地区代码"""
        if self.region:
            if self.region in self.REGION_CODES:
                return random.choice(self.REGION_CODES[self.region])[:6].ljust(6, '0')
            elif len(self.region) == 6 and self.region.isdigit():
                return self.region
        
        # 随机选择地区
        all_codes = []
        for codes in self.REGION_CODES.values():
            all_codes.extend(codes)
        return random.choice(all_codes)[:6].ljust(6, '0')
    
    def _get_random_birth_date(self, context: Optional[GenerationContext] = None) -> date:
        """获取随机出生日期"""
        # 如果有关联的年龄数据，使用它来计算出生日期
        if context and context.related_data and 'age' in context.related_data:
            age = context.related_data['age']
            current_year = datetime.now().year
            birth_year = current_year - age
            return date(birth_year, random.randint(1, 12), random.randint(1, 28))
        
        # 随机生成日期
        start_timestamp = self.start_date.toordinal()
        end_timestamp = self.end_date.toordinal()
        random_timestamp = random.randint(start_timestamp, end_timestamp)
        return date.fromordinal(random_timestamp)
    
    def _get_sequence_code(self) -> str:
        """获取顺序码（决定性别）"""
        # 前两位随机
        first_two = f"{random.randint(0, 99):02d}"
        
        # 第三位决定性别（奇数男，偶数女）
        if self.gender == 'MALE':
            third_digit = random.choice([1, 3, 5, 7, 9])
        elif self.gender == 'FEMALE':
            third_digit = random.choice([0, 2, 4, 6, 8])
        else:
            third_digit = random.randint(0, 9)
        
        return first_two + str(third_digit)
    
    def _calculate_check_digit(self, id_17: str) -> str:
        """计算校验位"""
        total = sum(int(id_17[i]) * self.ID_WEIGHTS[i] for i in range(17))
        return self.ID_CHECK_CODES[total % 11]
    
    def _generate_invalid_idcard(self) -> str:
        """生成无效身份证号码"""
        # 随机选择一种无效方式
        invalid_type = random.choice(['wrong_length', 'wrong_check', 'invalid_date', 'wrong_format'])
        
        if invalid_type == 'wrong_length':
            return ''.join([str(random.randint(0, 9)) for _ in range(random.choice([15, 16, 19, 20]))])
        elif invalid_type == 'wrong_check':
            # 生成正确格式但校验位错误的身份证
            valid_id = self._generate_raw(None)
            wrong_check = random.choice([c for c in self.ID_CHECK_CODES if c != valid_id[-1]])
            return valid_id[:-1] + wrong_check
        elif invalid_type == 'invalid_date':
            # 无效日期
            region_code = self._get_region_code()
            invalid_date = f"{random.randint(1900, 2030)}{random.randint(13, 15):02d}{random.randint(32, 35):02d}"
            sequence_code = self._get_sequence_code()
            id_17 = region_code + invalid_date + sequence_code
            return id_17 + self._calculate_check_digit(id_17)
        else:  # wrong_format
            # 包含字母的身份证
            id_with_letters = ''.join([
                random.choice('0123456789ABCDEF') for _ in range(18)
            ])
            return id_with_letters
    
    def validate(self, data: str) -> bool:
        """校验身份证号码"""
        if not isinstance(data, str) or len(data) != 18:
            return False
        
        # 检查前17位是否为数字
        if not data[:17].isdigit():
            return False
        
        # 检查最后一位校验位
        if data[17] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X']:
            return False
        
        # 校验位计算
        calculated_check = self._calculate_check_digit(data[:17])
        return calculated_check == data[17]
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['region', 'birth_date_range', 'gender', 'valid']


@register_generator('idcard', ['identity_card', 'id_card', '身份证'])
class ChineseIDCardGenerator(IDCardGenerator):
    """中国身份证号码生成器注册版本"""
    pass