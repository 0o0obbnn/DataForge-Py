"""
统一社会信用代码生成器
"""
import random
from typing import Optional, List
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator


class USCCGenerator(ValidatedDataGenerator[str]):
    """统一社会信用代码生成器 (GB32100-2015标准)"""
    
    def _setup(self) -> None:
        self.region = self.parameters.get('region', None)  # 行政区划码
        self.valid = self.parameters.get('valid', True)  # 是否保证生成有效代码
        
        # 登记管理部门码
        self.registration_departments = {
            '1': '机构编制',
            '5': '民政',
            '9': '工商',
            'Y': '其他'
        }
        
        # 机构类别码
        self.organization_types = {
            '1': '企业',
            '2': '个体工商户',
            '3': '农民专业合作社',
            '9': '其他'
        }
        
        # 常用行政区划码（部分）
        self.regions = {
            '110000': '北京市',
            '120000': '天津市',
            '130000': '河北省',
            '140000': '山西省',
            '150000': '内蒙古自治区',
            '210000': '辽宁省',
            '220000': '吉林省',
            '230000': '黑龙江省',
            '310000': '上海市',
            '320000': '江苏省',
            '330000': '浙江省',
            '340000': '安徽省',
            '350000': '福建省',
            '360000': '江西省',
            '370000': '山东省',
            '410000': '河南省',
            '420000': '湖北省',
            '430000': '湖南省',
            '440000': '广东省',
            '450000': '广西壮族自治区',
            '460000': '海南省',
            '500000': '重庆市',
            '510000': '四川省',
            '520000': '贵州省',
            '530000': '云南省',
            '540000': '西藏自治区',
            '610000': '陕西省',
            '620000': '甘肃省',
            '630000': '青海省',
            '640000': '宁夏回族自治区',
            '650000': '新疆维吾尔自治区'
        }
        
        # 校验码字符表（GB32100-2015标准）
        self.check_code_chars = '0123456789ABCDEFGHJKLMNPQRTUWXY'
        self.weight_factors = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始统一社会信用代码"""
        # 1. 登记管理部门码 (1位)
        dept_code = random.choice(list(self.registration_departments.keys()))
        
        # 2. 机构类别码 (1位)
        org_type = random.choice(list(self.organization_types.keys()))
        
        # 3. 行政区划码 (6位)
        if self.region and self.region in self.regions:
            region_code = self.region
        else:
            region_code = random.choice(list(self.regions.keys()))
        
        # 4. 主体标识码 (9位) - 随机生成
        entity_id = self._generate_entity_id()
        
        # 5. 校验码 (1位)
        code_without_check = dept_code + org_type + region_code + entity_id
        
        if self.valid:
            check_code = self._calculate_check_code(code_without_check)
        else:
            # 生成错误的校验码
            check_code = random.choice(self.check_code_chars)
            # 确保不是正确的校验码
            correct_check = self._calculate_check_code(code_without_check)
            while check_code == correct_check:
                check_code = random.choice(self.check_code_chars)
        
        return code_without_check + check_code
    
    def _generate_entity_id(self) -> str:
        """生成主体标识码 (9位)"""
        # 使用数字和字母（除I、O、S、V、Z）
        chars = '0123456789ABCDEFGHJKLMNPQRTUWXY'
        return ''.join(random.choices(chars, k=9))
    
    def _calculate_check_code(self, code_17: str) -> str:
        """计算校验码 (GB32100-2015标准)"""
        if len(code_17) != 17:
            raise ValueError("代码长度必须为17位")
        
        # 将字符转换为数值
        total = 0
        for i, char in enumerate(code_17):
            if char.isdigit():
                char_value = int(char)
            else:
                # 字母转换为数值
                char_value = self.check_code_chars.index(char)
            
            total += char_value * self.weight_factors[i]
        
        # 计算校验码
        remainder = total % 31
        check_index = (31 - remainder) % 31
        return self.check_code_chars[check_index]
    
    def validate(self, data: str) -> bool:
        """校验统一社会信用代码"""
        if not isinstance(data, str) or len(data) != 18:
            return False
        
        # 检查字符是否都在允许的字符集中
        for char in data:
            if char not in self.check_code_chars:
                return False
        
        # 检查登记管理部门码
        if data[0] not in self.registration_departments:
            return False
        
        # 检查机构类别码
        if data[1] not in self.organization_types:
            return False
        
        # 检查行政区划码（前6位数字）
        region_code = data[2:8]
        if not region_code.isdigit():
            return False
        
        # 校验码验证
        code_without_check = data[:17]
        expected_check = self._calculate_check_code(code_without_check)
        return data[17] == expected_check
    
    def get_uscc_info(self, uscc: str) -> dict:
        """解析统一社会信用代码信息"""
        if not self.validate(uscc):
            return {'valid': False, 'error': '无效的统一社会信用代码'}
        
        result = {
            'valid': True,
            'uscc': uscc,
            'registration_dept_code': uscc[0],
            'registration_dept_name': self.registration_departments.get(uscc[0], '未知'),
            'organization_type_code': uscc[1],
            'organization_type_name': self.organization_types.get(uscc[1], '未知'),
            'region_code': uscc[2:8],
            'region_name': self.regions.get(uscc[2:8], '未知地区'),
            'entity_id': uscc[8:17],
            'check_code': uscc[17]
        }
        
        return result
    
    def generate_with_info(self, context: Optional[GenerationContext] = None) -> dict:
        """生成统一社会信用代码并返回详细信息"""
        uscc = self._generate_raw(context)
        return self.get_uscc_info(uscc)
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.IDENTIFIER
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['region', 'valid']


@register_generator('uscc', ['unified_social_credit_code', '统一社会信用代码', '社会信用代码'])
class ChineseUSCCGenerator(USCCGenerator):
    """中国统一社会信用代码生成器注册版本"""
    pass