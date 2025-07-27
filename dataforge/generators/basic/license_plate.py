"""
车牌号生成器
"""
import random
import string
from typing import Optional, List
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator


class LicensePlateGenerator(ValidatedDataGenerator[str]):
    """中国车牌号生成器"""
    
    def _setup(self) -> None:
        self.plate_type = self.parameters.get('type', 'BOTH')  # FUEL, NEW_ENERGY, BOTH
        self.province = self.parameters.get('province', None)  # 省份简称
        self.city = self.parameters.get('city', None)  # 城市字母代码
        self.include_io = self.parameters.get('include_io', False)  # 是否包含I和O
        self.valid = self.parameters.get('valid', True)  # 是否保证符合基本格式规则
        
        # 省份简称映射
        self.provinces = {
            '京': '北京', '津': '天津', '冀': '河北', '晋': '山西', '蒙': '内蒙古',
            '辽': '辽宁', '吉': '吉林', '黑': '黑龙江', '沪': '上海', '苏': '江苏',
            '浙': '浙江', '皖': '安徽', '闽': '福建', '赣': '江西', '鲁': '山东',
            '豫': '河南', '鄂': '湖北', '湘': '湖南', '粤': '广东', '桂': '广西',
            '琼': '海南', '渝': '重庆', '川': '四川', '贵': '贵州', '云': '云南',
            '藏': '西藏', '陕': '陕西', '甘': '甘肃', '青': '青海', '宁': '宁夏',
            '新': '新疆'
        }
        
        # 城市代码字母
        self.city_codes = list('ABCDEFGHJKLMNPQRSTUVWXYZ')  # 默认不包含I和O
        if self.include_io:
            self.city_codes.extend(['I', 'O'])
        
        # 车牌字符（不包含I和O）
        self.plate_chars = list('ABCDEFGHJKLMNPQRSTUVWXYZ0123456789')
        if self.include_io:
            self.plate_chars.extend(['I', 'O'])
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始车牌号"""
        if self.plate_type == 'NEW_ENERGY':
            return self._generate_new_energy_plate()
        elif self.plate_type == 'FUEL':
            return self._generate_fuel_plate()
        else:  # BOTH
            if random.random() < 0.2:  # 20%概率生成新能源车牌
                return self._generate_new_energy_plate()
            else:
                return self._generate_fuel_plate()
    
    def _generate_fuel_plate(self) -> str:
        """生成燃油车牌号（7位）"""
        # 选择省份简称
        if self.province and self.province in self.provinces:
            province_code = self.province
        else:
            province_code = random.choice(list(self.provinces.keys()))
        
        # 选择城市代码
        if self.city and self.city in self.city_codes:
            city_code = self.city
        else:
            city_code = random.choice(self.city_codes)
        
        # 生成5位字母数字组合
        plate_suffix = ''.join(random.choices(self.plate_chars, k=5))
        
        return f"{province_code}{city_code}{plate_suffix}"
    
    def _generate_new_energy_plate(self) -> str:
        """生成新能源车牌号（8位，绿牌）"""
        # 选择省份简称
        if self.province and self.province in self.provinces:
            province_code = self.province
        else:
            province_code = random.choice(list(self.provinces.keys()))
        
        # 选择城市代码
        if self.city and self.city in self.city_codes:
            city_code = self.city
        else:
            city_code = random.choice(self.city_codes)
        
        # 新能源车牌以D或F开头
        new_energy_prefix = random.choice(['D', 'F'])
        
        # 生成5位字母数字组合
        plate_suffix = ''.join(random.choices(self.plate_chars, k=5))
        
        return f"{province_code}{city_code}{new_energy_prefix}{plate_suffix}"
    
    def validate(self, data: str) -> bool:
        """校验车牌号"""
        if not isinstance(data, str):
            return False
        
        # 基本长度检查
        if len(data) not in [7, 8]:
            return False
        
        # 检查第一位是否为中文省份简称
        if data[0] not in self.provinces:
            return False
        
        # 检查第二位是否为字母
        if not data[1].isalpha() or data[1] not in self.city_codes:
            return False
        
        # 检查后续字符
        if len(data) == 7:  # 燃油车牌
            # 后5位应该是字母或数字
            for char in data[2:]:
                if char not in self.plate_chars:
                    return False
        elif len(data) == 8:  # 新能源车牌
            # 第3位应该是D或F
            if data[2] not in ['D', 'F']:
                return False
            # 后5位应该是字母或数字
            for char in data[3:]:
                if char not in self.plate_chars:
                    return False
        
        return True
    
    def get_plate_info(self, plate: str) -> dict:
        """获取车牌信息"""
        if not self.validate(plate):
            return {'valid': False, 'error': '无效车牌号'}
        
        result = {
            'valid': True,
            'plate': plate,
            'province_code': plate[0],
            'province_name': self.provinces.get(plate[0], '未知'),
            'city_code': plate[1],
            'type': 'new_energy' if len(plate) == 8 else 'fuel',
            'length': len(plate)
        }
        
        if len(plate) == 8:
            result['new_energy_prefix'] = plate[2]
            result['suffix'] = plate[3:]
        else:
            result['suffix'] = plate[2:]
        
        return result
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['type', 'province', 'city', 'include_io', 'valid']


@register_generator('license_plate', ['plate', '车牌号', '车牌'])
class ChineseLicensePlateGenerator(LicensePlateGenerator):
    """中国车牌号生成器注册版本"""
    pass