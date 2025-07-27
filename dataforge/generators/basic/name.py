"""
姓名生成器
"""
import random
import json
import os
from typing import Optional, Dict, Any, List
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator
from ...core.cache import get_cached_data, get_data_file_path, LazyDataLoader


class NameGenerator(ValidatedDataGenerator[str]):
    """中文姓名生成器"""
    
    def _setup(self) -> None:
        self.name_type = self.parameters.get('type', 'BOTH')  # CN, EN, BOTH
        self.gender = self.parameters.get('gender', 'ANY')  # MALE, FEMALE, ANY
        self.surname_file = self.parameters.get('surname_file', None)
        self.givenname_file = self.parameters.get('givenname_file', None)
        self.include_pinyin = self.parameters.get('include_pinyin', False)
        self.compound_surname_ratio = self.parameters.get('compound_surname_ratio', 0.1)
        
        # 使用惰性加载器加载姓名数据
        self._setup_lazy_loaders()
    
    def _setup_lazy_loaders(self):
        """设置惰性数据加载器"""
        # 设置姓氏数据加载器
        surnames_path = self.surname_file or get_data_file_path('chinese/surnames.json')
        self._surnames_loader = LazyDataLoader(surnames_path)
        
        # 设置名字数据加载器
        givennames_path = self.givenname_file or get_data_file_path('chinese/givennames.json')
        self._givennames_loader = LazyDataLoader(givennames_path)
    
    @property
    def surnames_data(self):
        """获取姓氏数据（惰性加载）"""
        try:
            return self._surnames_loader.data
        except (FileNotFoundError, RuntimeError):
            return self._get_default_surnames_data()
    
    @property
    def givennames_data(self):
        """获取名字数据（惰性加载）"""
        try:
            return self._givennames_loader.data
        except (FileNotFoundError, RuntimeError):
            return self._get_default_givennames_data()
    
    def _load_name_data(self):
        """加载姓名数据"""
        try:
            # 加载姓氏数据
            surnames_path = self.surname_file or os.path.join(
                os.path.dirname(__file__), '../../data/chinese/surnames.json'
            )
            with open(surnames_path, 'r', encoding='utf-8') as f:
                surnames_data = json.load(f)
            
            self.common_surnames = surnames_data['common_surnames']
            self.rare_surnames = surnames_data.get('rare_surnames', [])
            
            # 加载名字数据
            givennames_path = self.givenname_file or os.path.join(
                os.path.dirname(__file__), '../../data/chinese/givennames.json'
            )
            with open(givennames_path, 'r', encoding='utf-8') as f:
                givennames_data = json.load(f)
            
            self.male_names = givennames_data['male_names']
            self.female_names = givennames_data['female_names']
            self.neutral_names = givennames_data['neutral_names']
            
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果无法加载数据文件，使用默认数据
            self._setup_default_data()
    
    def _setup_default_data(self):
        """设置默认姓名数据"""
        self.common_surnames = [
            {'surname': '王', 'pinyin': 'wang', 'frequency': 0.0693},
            {'surname': '李', 'pinyin': 'li', 'frequency': 0.0636},
            {'surname': '张', 'pinyin': 'zhang', 'frequency': 0.0626},
            {'surname': '刘', 'pinyin': 'liu', 'frequency': 0.0520},
            {'surname': '陈', 'pinyin': 'chen', 'frequency': 0.0451}
        ]
        
        self.rare_surnames = [
            {'surname': '欧阳', 'pinyin': 'ouyang', 'type': 'compound'},
            {'surname': '司马', 'pinyin': 'sima', 'type': 'compound'}
        ]
        
        self.male_names = {
            'single_char': ['伟', '强', '磊', '军', '洋'],
            'double_char': ['志强', '建国', '建华', '国强', '志华']
        }
        
        self.female_names = {
            'single_char': ['丽', '美', '红', '燕', '芳'],
            'double_char': ['淑华', '淑英', '淑芳', '淑娟', '淑敏']
        }
        
        self.neutral_names = {
            'single_char': ['嘉', '欣', '悦', '乐', '安'],
            'double_char': ['思琪', '思涵', '思萱', '思雅', '思洁']
        }
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始姓名"""
        if self.name_type == 'EN':
            return self._generate_english_name()
        elif self.name_type == 'CN':
            return self._generate_chinese_name(context)
        else:  # BOTH
            return self._generate_chinese_name(context) if random.random() < 0.8 else self._generate_english_name()
    
    def _generate_chinese_name(self, context: Optional[GenerationContext] = None) -> str:
        """生成中文姓名"""
        # 1. 选择姓氏
        surname_info = self._select_surname()
        surname = surname_info['surname']
        
        # 2. 确定性别（如果有关联数据）
        gender = self._determine_gender(context)
        
        # 3. 选择名字
        given_name = self._select_given_name(gender)
        
        # 4. 组合姓名
        full_name = surname + given_name
        
        # 5. 如果需要拼音
        if self.include_pinyin:
            surname_pinyin = surname_info['pinyin']
            # 简化处理，实际应该有完整的拼音库
            given_pinyin = self._get_pinyin_approximation(given_name)
            full_name = f"{full_name} ({surname_pinyin} {given_pinyin})"
        
        return full_name
    
    def _select_surname(self) -> Dict[str, Any]:
        """选择姓氏"""
        # 是否选择复姓
        rare_surnames = self.surnames_data.get('rare_surnames', [])
        if random.random() < self.compound_surname_ratio and rare_surnames:
            return random.choice(rare_surnames)
        
        # 根据频率加权选择常见姓氏
        surnames = self.surnames_data.get('common_surnames', [])
        if not surnames:
            return {'surname': '王', 'pinyin': 'wang', 'frequency': 1.0}
        
        weights = [s.get('frequency', 1.0) for s in surnames]
        return random.choices(surnames, weights=weights)[0]
    
    def _determine_gender(self, context: Optional[GenerationContext] = None) -> str:
        """确定性别"""
        # 如果有关联数据中的性别信息
        if context and context.related_data and 'gender' in context.related_data:
            related_gender = context.related_data['gender']
            if related_gender in ['MALE', 'FEMALE']:
                return related_gender
        
        # 如果参数指定了性别
        if self.gender in ['MALE', 'FEMALE']:
            return self.gender
        
        # 随机选择性别
        return random.choice(['MALE', 'FEMALE'])
    
    def _select_given_name(self, gender: str) -> str:
        """选择名字"""
        if gender == 'MALE':
            name_pool = self.givennames_data.get('male_names', [])
        elif gender == 'FEMALE':
            name_pool = self.givennames_data.get('female_names', [])
        else:
            # 随机选择男名、女名或中性名
            male_names = self.givennames_data.get('male_names', [])
            female_names = self.givennames_data.get('female_names', [])
            neutral_names = self.givennames_data.get('neutral_names', [])
            all_pools = [pool for pool in [male_names, female_names, neutral_names] if pool]
            name_pool = random.choice(all_pools) if all_pools else []
        
        if not name_pool:
            return '明'  # 默认名字
        
        # 兼容不同的数据格式
        if isinstance(name_pool, dict):
            # 如果是字典格式 {'single_char': [...], 'double_char': [...]}
            if random.random() < 0.3:  # 30%概率单字名
                names = name_pool.get('single_char', [])
            else:
                names = name_pool.get('double_char', [])
            return random.choice(names) if names else '明'
        else:
            # 如果是列表格式 [{'name': '...', 'pinyin': '...'}, ...]
            name_info = random.choice(name_pool)
            if isinstance(name_info, dict):
                return name_info.get('name', '明')
            else:
                return str(name_info)
    
    def _get_pinyin_approximation(self, name: str) -> str:
        """获取名字的拼音近似（简化实现）"""
        # 这里使用简化的拼音映射，实际应该使用专业的拼音库
        pinyin_map = {
            '伟': 'wei', '强': 'qiang', '磊': 'lei', '军': 'jun', '洋': 'yang',
            '丽': 'li', '美': 'mei', '红': 'hong', '燕': 'yan', '芳': 'fang',
            '嘉': 'jia', '欣': 'xin', '悦': 'yue', '乐': 'le', '安': 'an',
            '志': 'zhi', '建': 'jian', '国': 'guo', '华': 'hua', '淑': 'shu',
            '英': 'ying', '娟': 'juan', '敏': 'min', '思': 'si', '琪': 'qi',
            '涵': 'han', '萱': 'xuan', '雅': 'ya', '洁': 'jie'
        }
        
        pinyin_parts = []
        for char in name:
            pinyin_parts.append(pinyin_map.get(char, char.lower()))
        
        return ''.join(pinyin_parts)
    
    def _generate_english_name(self) -> str:
        """生成英文姓名"""
        first_names_male = [
            'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Charles',
            'Joseph', 'Thomas', 'Christopher', 'Daniel', 'Paul', 'Mark', 'Donald', 'Steven'
        ]
        
        first_names_female = [
            'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica',
            'Sarah', 'Karen', 'Nancy', 'Lisa', 'Betty', 'Helen', 'Sandra', 'Donna'
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas'
        ]
        
        # 选择性别对应的名字
        if self.gender == 'MALE':
            first_name = random.choice(first_names_male)
        elif self.gender == 'FEMALE':
            first_name = random.choice(first_names_female)
        else:
            all_first_names = first_names_male + first_names_female
            first_name = random.choice(all_first_names)
        
        last_name = random.choice(last_names)
        
        return f"{first_name} {last_name}"
    
    def validate(self, data: str) -> bool:
        """校验姓名"""
        if not isinstance(data, str) or len(data.strip()) == 0:
            return False
        
        # 移除拼音部分
        name = data.split('(')[0].strip()
        
        # 基本长度检查
        if len(name) < 2 or len(name) > 10:
            return False
        
        # 检查是否包含有效字符
        if ' ' in name:
            # 英文名检查
            parts = name.split()
            return len(parts) >= 2 and all(part.isalpha() for part in parts)
        else:
            # 中文名检查
            return all('\u4e00' <= char <= '\u9fff' for char in name)
    
    def analyze_name(self, name: str) -> Dict[str, Any]:
        """分析姓名信息"""
        result = {
            'original': name,
            'type': 'unknown',
            'surname': '',
            'given_name': '',
            'gender_tendency': 'unknown',
            'pinyin': ''
        }
        
        # 提取拼音
        if '(' in name and ')' in name:
            pinyin_part = name[name.find('(')+1:name.find(')')]
            result['pinyin'] = pinyin_part
            name = name.split('(')[0].strip()
        
        if ' ' in name:
            # 英文名
            result['type'] = 'english'
            parts = name.split()
            if len(parts) >= 2:
                result['given_name'] = parts[0]
                result['surname'] = ' '.join(parts[1:])
        else:
            # 中文名
            result['type'] = 'chinese'
            if len(name) >= 2:
                # 检查是否为复姓
                compound_surnames = [s['surname'] for s in self.rare_surnames]
                for compound in compound_surnames:
                    if name.startswith(compound):
                        result['surname'] = compound
                        result['given_name'] = name[len(compound):]
                        break
                else:
                    # 单字姓
                    result['surname'] = name[0]
                    result['given_name'] = name[1:]
        
        return result
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['type', 'gender', 'surname_file', 'givenname_file', 'include_pinyin', 'compound_surname_ratio']


@register_generator('name', ['fullname', '姓名'])
class ChineseNameGenerator(NameGenerator):
    """中文姓名生成器注册版本"""
    pass