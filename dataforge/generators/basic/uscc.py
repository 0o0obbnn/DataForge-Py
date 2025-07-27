"""
统一社会信用代码生成器
"""
import random
from typing import Optional, Dict, Any, List
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator


class USCCGenerator(ValidatedDataGenerator[str]):
    """统一社会信用代码生成器（GB32100-2015标准）"""
    
    # 校验码字符集（不含I、O、S、V、Z）
    CHECK_CHARS = '0123456789ABCDEFGHJKLMNPQRTUWXY'
    
    # 加权因子
    WEIGHTS = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
    
    # 登记管理部门代码
    REGISTRATION_DEPT = {
        '1': '机构编制',  
        '5': '民政',
        '9': '工商',
        'Y': '其他'
    }
    
    # 机构类别代码
    ORGANIZATION_TYPE = {
        '1': '企业',
        '2': '个体工商户', 
        '3': '农民专业合作社',
        '9': '其他'
    }
    
    def _setup(self) -> None:
        self.region = self.parameters.get('region', None)  # 行政区划码
        self.dept_code = self.parameters.get('dept_code', '9')  # 默认工商部门
        self.org_type = self.parameters.get('org_type', '1')  # 默认企业
        self.valid = self.parameters.get('valid', True)
        
        # 加载地区代码数据
        self._load_region_data()
    
    def _load_region_data(self):
        """加载地区代码数据"""
        import json
        import os
        
        try:
            data_path = os.path.join(os.path.dirname(__file__), '../../data/chinese/regions.json')
            with open(data_path, 'r', encoding='utf-8') as f:
                regions_data = json.load(f)
            
            self.region_codes = []
            for province in regions_data['provinces']:
                self.region_codes.append(province['code'][:6])
                
            # 添加主要城市的区县代码
            for province_code, cities in regions_data['major_cities'].items():
                for city in cities:
                    for district in city.get('districts', []):
                        self.region_codes.append(district['code'])
                        
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果无法加载数据文件，使用默认地区代码
            self.region_codes = [
                '110000', '120000', '310000', '440000', '330000', 
                '320000', '370000', '410000', '420000', '510000'
            ]
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始统一社会信用代码"""
        if not self.valid:
            return self._generate_invalid_uscc()
        
        # 1. 登记管理部门代码（1位）
        dept_code = self.dept_code
        
        # 2. 机构类别代码（1位）
        org_type = self.org_type
        
        # 3. 行政区划代码（6位）
        if self.region and len(self.region) == 6 and self.region.isdigit():
            region_code = self.region
        else:
            region_code = random.choice(self.region_codes)
        
        # 4. 主体标识码（9位）- 随机生成
        subject_code = self._generate_subject_code()
        
        # 5. 校验码（1位）
        code_17 = dept_code + org_type + region_code + subject_code
        check_code = self._calculate_check_code(code_17)
        
        return code_17 + check_code
    
    def _generate_subject_code(self) -> str:
        """生成主体标识码（9位）"""
        # 使用0-9和A-Z（除I、O、S、V、Z）
        chars = '0123456789ABCDEFGHJKLMNPQRTUWXY'
        return ''.join([random.choice(chars) for _ in range(9)])
    
    def _calculate_check_code(self, code_17: str) -> str:
        """计算校验码"""
        total = 0
        for i, char in enumerate(code_17):
            if char.isdigit():
                value = int(char)
            else:
                # A=10, B=11, ..., Y=33 (跳过I、O、S、V、Z)
                value = self.CHECK_CHARS.index(char)
            total += value * self.WEIGHTS[i]
        
        remainder = total % 31
        if remainder == 0:
            return '0'
        else:
            return self.CHECK_CHARS[31 - remainder]
    
    def _generate_invalid_uscc(self) -> str:
        """生成无效统一社会信用代码"""
        invalid_type = random.choice(['wrong_length', 'wrong_check', 'invalid_chars', 'wrong_format'])
        
        if invalid_type == 'wrong_length':
            # 错误长度
            wrong_length = random.choice([15, 16, 17, 19, 20])
            return ''.join([random.choice(self.CHECK_CHARS) for _ in range(wrong_length)])
        elif invalid_type == 'wrong_check':
            # 正确格式但校验码错误
            valid_uscc = self._generate_raw(None)
            wrong_chars = [c for c in self.CHECK_CHARS if c != valid_uscc[-1]]
            return valid_uscc[:-1] + random.choice(wrong_chars)
        elif invalid_type == 'invalid_chars':
            # 包含非法字符（I、O、S、V、Z）
            invalid_chars = 'IOSVZ'
            valid_uscc = self._generate_raw(None)
            # 随机替换一个字符为非法字符
            pos = random.randint(0, 17)
            return valid_uscc[:pos] + random.choice(invalid_chars) + valid_uscc[pos+1:]
        else:  # wrong_format
            # 格式完全错误
            return ''.join([random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(18)])
    
    def validate(self, data: str) -> bool:
        """校验统一社会信用代码"""
        if not isinstance(data, str) or len(data) != 18:
            return False
        
        # 检查字符集
        for char in data:
            if char not in self.CHECK_CHARS:
                return False
        
        # 检查登记管理部门代码
        if data[0] not in self.REGISTRATION_DEPT:
            return False
        
        # 检查机构类别代码
        if data[1] not in self.ORGANIZATION_TYPE:
            return False
        
        # 检查行政区划代码（前6位应该是数字）
        if not data[2:8].isdigit():
            return False
        
        # 校验码检查
        calculated_check = self._calculate_check_code(data[:17])
        return calculated_check == data[17]
    
    def get_uscc_info(self, uscc: str) -> Dict[str, str]:
        """获取统一社会信用代码信息"""
        if not self.validate(uscc):
            return {'error': '无效的统一社会信用代码'}
        
        return {
            'registration_dept': self.REGISTRATION_DEPT.get(uscc[0], '未知'),
            'org_type': self.ORGANIZATION_TYPE.get(uscc[1], '未知'),
            'region_code': uscc[2:8],
            'subject_code': uscc[8:17],
            'check_code': uscc[17]
        }
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['region', 'dept_code', 'org_type', 'valid']


@register_generator('uscc', ['unified_social_credit_code', '统一社会信用代码'])
class ChineseUSCCGenerator(USCCGenerator):
    """中国统一社会信用代码生成器注册版本"""
    pass