"""
地址生成器
"""
import random  # TODO: Convert to secrets
import secrets
import json
import os
from typing import Optional, Dict, Any, List

from ...core.types import GeneratorType
from ...core.generator import DataGenerator, GeneratorConfig, GenerationContext
from ...core.factory import register_generator
from ...core.cache import get_cached_data, get_data_file_path, LazyDataLoader

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary



class AddressGenerator(DataGenerator[str]):
    """中国地址生成器"""
    
    def _setup(self) -> None:
        self.country = self.parameters.get('country', 'CN')
        self.province = self.parameters.get('province', None)  # 省份名称或代码
        self.city = self.parameters.get('city', None)  # 城市名称或代码
        self.district = self.parameters.get('district', None)  # 区县名称或代码
        self.detail_level = self.parameters.get('detail_level', 'FULL')  # STREET, COMMUNITY, FULL
        self.include_zipcode = self.parameters.get('zipcode', True)
        
        # 使用惰性加载器加载地址数据
        self._setup_lazy_loader()
        # 确保地址组件被初始化
        self._load_address_data()
    
    def _setup_lazy_loader(self):
        """设置惰性数据加载器"""
        data_path = get_data_file_path('chinese/regions.json')
        self._regions_loader = LazyDataLoader(data_path)
    
    @property
    def regions_data(self):
        """获取地区数据（惰性加载）"""
        try:
            return self._regions_loader.data
        except (FileNotFoundError, RuntimeError):
            return self._get_default_regions_data()
    
    def _get_default_regions_data(self):
        """获取默认地区数据"""
        return {
            'provinces': [
                {'code': '110000', 'name': '北京市', 'short': '京'},
                {'code': '310000', 'name': '上海市', 'short': '沪'},
                {'code': '440000', 'name': '广东省', 'short': '粤'},
                {'code': '320000', 'name': '江苏省', 'short': '苏'},
                {'code': '330000', 'name': '浙江省', 'short': '浙'}
            ],
            'major_cities': {
                '110000': [{'name': '北京市', 'districts': ['朝阳区', '海淀区', '丰台区', '西城区', '东城区']}],
                '310000': [{'name': '上海市', 'districts': ['黄浦区', '徐汇区', '长宁区', '静安区', '普陀区']}],
                '440000': [
                    {'name': '广州市', 'districts': ['天河区', '越秀区', '荔湾区', '海珠区', '白云区']},
                    {'name': '深圳市', 'districts': ['南山区', '福田区', '罗湖区', '宝安区', '龙岗区']}
                ]
            },
            'street_types': ['路', '街', '巷', '大道', '大街', '胡同'],
            'building_types': ['号', '号楼', '单元', '室', '栋']
        }
    
    def _load_address_data(self):
        """加载地址数据（兼容性方法，现在使用惰性加载）"""
        # 预生成一些常用的地址组件
        self._generate_address_components()
        
        # 预生成一些常用的地址组件
        self._generate_address_components()
    
    def _generate_address_components(self):
        """生成地址组件"""
        # 街道名称
        self.street_names = [
            '人民', '解放', '建设', '中山', '胜利', '新华', '和平', '光明',
            '文化', '工业', '商业', '学院', '体育', '科技', '环城', '迎宾',
            '友谊', '团结', '青年', '少年', '儿童', '妇女', '老人', '军民',
            '东风', '西风', '南风', '北风', '春风', '秋风', '红旗', '五星',
            '八一', '国庆', '劳动', '青春', '希望', '未来', '梦想', '幸福'
        ]
        
        # 方位词
        self.directions = ['东', '西', '南', '北', '中', '内', '外', '上', '下', '前', '后']
        
        # 小区/社区名称
        self.community_names = [
            '花园', '公园', '家园', '苑', '庭', '城', '府', '轩', '阁', '居',
            '山庄', '别墅', '新村', '小区', '社区', '广场', '中心', '大厦',
            '新城', '名苑', '豪庭', '雅居', '华府', '盛世', '锦绣', '凤凰',
            '龙湖', '碧桂园', '万科', '恒大', '保利', '融创', '绿地', '华润'
        ]
        
        # 建筑单位
        self.building_units = ['栋', '幢', '座', '楼', '单元', '号楼']
        
        # 门牌号前缀
        self.address_prefixes = ['金', '银', '玉', '珠', '宝', '华', '富', '贵', '吉', '祥']
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始地址"""
        # 如果指定了city但没有指定province，需要先找到city所属的province
        if self.city and not self.province:
            province_info = self._find_province_by_city(self.city)
        else:
            # 1. 选择省份
            province_info = self._select_province()
        
        # 2. 选择城市和区县
        city_info, district_info = self._select_city_district(province_info)
        
        # 3. 生成详细地址
        detailed_address = self._generate_detailed_address()
        
        # 4. 组装完整地址
        full_address = self._assemble_address(
            province_info, city_info, district_info, detailed_address
        )
        
        return full_address
    
    def _find_province_by_city(self, city_name: str) -> Dict[str, str]:
        """根据城市名查找所属省份"""
        # 遍历所有省份的城市数据
        for province in self.regions_data['provinces']:
            province_code = province['code']
            cities_data = self.regions_data.get('major_cities', {}).get(province_code, [])
            
            for city in cities_data:
                if (city['name'] == city_name or 
                    city_name in city['name'] or
                    city['name'].startswith(city_name)):
                    return province
        
        # 如果找不到，返回随机省份
        return secrets.choice(self.regions_data['provinces'])
    
    def _select_province(self) -> Dict[str, str]:
        """选择省份"""
        if self.province:
            # 查找指定省份（支持模糊匹配）
            for province in self.regions_data['provinces']:
                if (province['name'] == self.province or 
                    province['code'] == self.province or
                    province['short'] == self.province or
                    self.province in province['name'] or
                    province['name'].startswith(self.province)):
                    return province
        
        # 随机选择省份
        return secrets.choice(self.regions_data['provinces'])
    
    def _select_city_district(self, province_info: Dict[str, str]) -> tuple:
        """选择城市和区县"""
        province_code = province_info['code']
        
        # 查找该省份的城市数据
        cities_data = self.regions_data.get('major_cities', {}).get(province_code, [])
        
        if not cities_data:
            # 如果没有具体城市数据，生成虚拟城市名
            city_info = {
                'name': f"{secrets.choice(self.street_names)}{secrets.choice(['市', '县', '区'])}",
                'code': f"{province_code[:4]}01"
            }
            district_info = {
                'name': f"{secrets.choice(self.street_names)}{secrets.choice(['区', '县', '镇'])}",
                'code': f"{city_info['code']}01",
                'zipcode': f"{random.randint(100000, 999999)}"
            }
            return city_info, district_info
        
        # 如果指定了城市，查找匹配的城市
        city_data = None
        if self.city:
            for city in cities_data:
                if (city['name'] == self.city or 
                    self.city in city['name'] or
                    city['name'].startswith(self.city)):
                    city_data = city
                    break
        
        # 如果没有找到指定城市或没有指定城市，随机选择
        if not city_data:
            city_data = secrets.choice(cities_data)
        city_info = {
            'name': city_data['name'],
            'code': city_data['code']
        }
        
        # 随机选择区县
        districts = city_data.get('districts', [])
        if districts:
            district_data = secrets.choice(districts)
            district_info = {
                'name': district_data['name'],
                'code': district_data['code'],
                'zipcode': district_data.get('zipcode', '000000')
            }
        else:
            # 生成虚拟区县
            district_info = {
                'name': f"{secrets.choice(self.street_names)}{secrets.choice(['区', '县'])}",
                'code': f"{city_info['code']}01",
                'zipcode': f"{random.randint(100000, 999999)}"
            }
        
        return city_info, district_info
    
    def _generate_detailed_address(self) -> Dict[str, str]:
        """生成详细地址"""
        result = {}
        
        if self.detail_level in ['STREET', 'COMMUNITY', 'FULL']:
            # 生成街道
            street_name = secrets.choice(self.street_names)
            direction = secrets.choice(self.directions) if (secrets.randbelow(1000000) / 1000000) < 0.3 else ''
            street_type = secrets.choice(self.regions_data.get('street_types', ['路', '街']))
            result['street'] = f"{direction}{street_name}{street_type}"
        
        if self.detail_level in ['COMMUNITY', 'FULL']:
            # 生成小区/社区
            prefix = secrets.choice(self.address_prefixes) if (secrets.randbelow(1000000) / 1000000) < 0.4 else ''
            community_name = secrets.choice(self.community_names)
            result['community'] = f"{prefix}{community_name}"
        
        if self.detail_level == 'FULL':
            # 生成门牌号
            building_num = random.randint(1, 999)
            building_unit = secrets.choice(self.building_units) if (secrets.randbelow(1000000) / 1000000) < 0.6 else ''
            
            unit_num = ''
            room_num = ''
            
            if (secrets.randbelow(1000000) / 1000000) < 0.7:  # 70%概率有单元号
                unit_num = f"{random.randint(1, 6)}单元"
            
            if (secrets.randbelow(1000000) / 1000000) < 0.8:  # 80%概率有房间号
                floor = random.randint(1, 30)
                room = random.randint(1, 8)
                room_num = f"{floor:02d}{room:02d}室"
            
            result['building'] = f"{building_num}{building_unit}"
            if unit_num:
                result['unit'] = unit_num
            if room_num:
                result['room'] = room_num
        
        return result
    
    def _assemble_address(self, province_info: Dict, city_info: Dict, 
                         district_info: Dict, detailed_address: Dict) -> str:
        """组装完整地址"""
        address_parts = []
        
        # 省份
        address_parts.append(province_info['name'])
        
        # 城市（如果不是直辖市）
        if province_info['name'] not in ['北京市', '上海市', '天津市', '重庆市']:
            address_parts.append(city_info['name'])
        
        # 区县
        address_parts.append(district_info['name'])
        
        # 街道
        if 'street' in detailed_address:
            address_parts.append(detailed_address['street'])
        
        # 小区/社区
        if 'community' in detailed_address:
            address_parts.append(detailed_address['community'])
        
        # 建筑信息
        building_parts = []
        if 'building' in detailed_address:
            building_parts.append(detailed_address['building'])
        if 'unit' in detailed_address:
            building_parts.append(detailed_address['unit'])
        if 'room' in detailed_address:
            building_parts.append(detailed_address['room'])
        
        if building_parts:
            address_parts.append(''.join(building_parts))
        
        # 组装地址
        full_address = ''.join(address_parts)
        
        # 添加邮编（如果需要）
        if self.include_zipcode:
            zipcode = district_info.get('zipcode', '000000')
            full_address = f"{full_address} ({zipcode})"
        
        return full_address
    
    def validate(self, data: str) -> bool:
        """校验地址"""
        if not isinstance(data, str) or len(data.strip()) == 0:
            return False
        
        # 基本长度检查
        if len(data) < 10 or len(data) > 200:
            return False
        
        # 检查是否包含基本的地址组件
        address_indicators = ['省', '市', '区', '县', '路', '街', '巷', '号', '室', '单元']
        has_indicator = any(indicator in data for indicator in address_indicators)
        
        return has_indicator
    
    def parse_address(self, address: str) -> Dict[str, Any]:
        """解析地址信息"""
        result = {
            'original': address,
            'province': '',
            'city': '',
            'district': '',
            'street': '',
            'community': '',
            'building': '',
            'zipcode': ''
        }
        
        # 提取邮编
        import re
        zipcode_match = re.search(r'\((\d{6})\)', address)
        if zipcode_match:
            result['zipcode'] = zipcode_match.group(1)
            address = address.replace(zipcode_match.group(0), '').strip()
        
        # 简单的地址解析（可以进一步优化）
        for province in self.regions_data['provinces']:
            if province['name'] in address:
                result['province'] = province['name']
                break
        
        return result
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['country', 'province', 'city', 'district', 'detail_level', 'zipcode']

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)



@register_generator('address', ['addr', '地址'])
class ChineseAddressGenerator(AddressGenerator):
    """中国地址生成器注册版本"""
    pass