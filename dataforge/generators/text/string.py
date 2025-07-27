"""
文本生成器
"""
import random
import string
from typing import Optional, Dict, Any, List, Union
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator


class StringGenerator(ValidatedDataGenerator[str]):
    """字符串生成器"""
    
    # 预定义字符集
    CHAR_SETS = {
        'LETTERS': string.ascii_letters,
        'LOWERCASE': string.ascii_lowercase,
        'UPPERCASE': string.ascii_uppercase,
        'DIGITS': string.digits,
        'ALPHANUMERIC': string.ascii_letters + string.digits,
        'PRINTABLE': string.printable.replace('\n\r\t\v\f', ''),
        'PUNCTUATION': string.punctuation,
        'CHINESE': '的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严',
        'SPECIAL': '!@#$%^&*()_+-=[]{}|;:,.<>?'
    }
    
    def _setup(self) -> None:
        self.length = self.parameters.get('length', 10)
        self.min_length = self.parameters.get('min_length', None)
        self.max_length = self.parameters.get('max_length', None)
        self.charset = self.parameters.get('charset', 'ALPHANUMERIC')
        self.custom_charset = self.parameters.get('custom_charset', None)
        self.exclude_chars = self.parameters.get('exclude', [])
        self.must_include = self.parameters.get('must_include', [])  # 必须包含的字符类型
        self.case_style = self.parameters.get('case', 'MIXED')  # UPPER, LOWER, MIXED, TITLE
        self.allow_repeats = self.parameters.get('allow_repeats', True)
        self.format_pattern = self.parameters.get('format', None)  # 格式模式
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始字符串"""
        # 确定长度
        if self.min_length is not None and self.max_length is not None:
            length = random.randint(self.min_length, self.max_length)
        else:
            length = self.length
        
        # 如果有格式模式，使用模式生成
        if self.format_pattern:
            return self._generate_with_pattern()
        
        # 获取字符集
        chars = self._get_character_set()
        
        # 生成字符串
        if self.allow_repeats:
            result = ''.join(random.choices(chars, k=length))
        else:
            if length > len(chars):
                raise ValueError(f"无法生成长度为{length}的不重复字符串，可用字符只有{len(chars)}个")
            result = ''.join(random.sample(chars, length))
        
        # 确保包含必须的字符类型
        result = self._ensure_required_chars(result, chars)
        
        # 应用大小写样式
        result = self._apply_case_style(result)
        
        return result
    
    def _get_character_set(self) -> List[str]:
        """获取字符集"""
        if self.custom_charset:
            chars = list(self.custom_charset)
        else:
            chars = list(self.CHAR_SETS.get(self.charset.upper(), self.CHAR_SETS['ALPHANUMERIC']))
        
        # 排除指定字符
        chars = [c for c in chars if c not in self.exclude_chars]
        
        return chars
    
    def _ensure_required_chars(self, result: str, available_chars: List[str]) -> str:
        """确保包含必需的字符类型"""
        if not self.must_include:
            return result
        
        result_list = list(result)
        
        for requirement in self.must_include:
            req_chars = self.CHAR_SETS.get(requirement.upper(), [])
            req_chars = [c for c in req_chars if c in available_chars]
            
            if req_chars and not any(c in result for c in req_chars):
                # 替换一个随机位置的字符
                pos = random.randint(0, len(result_list) - 1)
                result_list[pos] = random.choice(req_chars)
        
        return ''.join(result_list)
    
    def _apply_case_style(self, text: str) -> str:
        """应用大小写样式"""
        if self.case_style.upper() == 'UPPER':
            return text.upper()
        elif self.case_style.upper() == 'LOWER':
            return text.lower()
        elif self.case_style.upper() == 'TITLE':
            return text.title()
        else:  # MIXED
            return text
    
    def _generate_with_pattern(self) -> str:
        """根据格式模式生成"""
        pattern = self.format_pattern
        result = ''
        
        for char in pattern:
            if char == '#':  # 数字
                result += random.choice(string.digits)
            elif char == '@':  # 字母
                result += random.choice(string.ascii_letters)
            elif char == '*':  # 任意字符
                result += random.choice(string.ascii_letters + string.digits)
            elif char == '?':  # 可选字符
                if random.random() < 0.5:
                    result += random.choice(string.ascii_letters)
            else:
                result += char
        
        return result
    
    def validate(self, data: str) -> bool:
        """校验字符串"""
        if not isinstance(data, str):
            return False
        
        # 检查长度
        if self.min_length is not None and len(data) < self.min_length:
            return False
        if self.max_length is not None and len(data) > self.max_length:
            return False
        if not (self.min_length or self.max_length) and len(data) != self.length:
            return False
        
        # 检查字符集
        valid_chars = set(self._get_character_set())
        if not all(c in valid_chars for c in data):
            return False
        
        # 检查重复限制
        if not self.allow_repeats and len(set(data)) != len(data):
            return False
        
        # 检查必须包含的字符类型
        for requirement in self.must_include:
            req_chars = set(self.CHAR_SETS.get(requirement.upper(), []))
            if not any(c in req_chars for c in data):
                return False
        
        return True
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return [
            'length', 'min_length', 'max_length', 'charset', 'custom_charset',
            'exclude', 'must_include', 'case', 'allow_repeats', 'format'
        ]


class BooleanGenerator(ValidatedDataGenerator[Union[bool, str]]):
    """布尔值生成器"""
    
    def _setup(self) -> None:
        self.true_ratio = self.parameters.get('true_ratio', 0.5)  # True的概率
        self.output_format = self.parameters.get('format', 'BOOLEAN')  # BOOLEAN, STRING, NUMERIC, CHINESE
        self.custom_values = self.parameters.get('custom_values', None)  # 自定义True/False值
        self.null_ratio = self.parameters.get('null_ratio', 0.0)  # null值的概率
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> Union[bool, str, None]:
        """生成原始布尔值"""
        # 处理null值
        if self.null_ratio > 0 and random.random() < self.null_ratio:
            return None
        
        # 生成布尔值
        bool_value = random.random() < self.true_ratio
        
        # 根据输出格式转换
        return self._format_output(bool_value)
    
    def _format_output(self, value: bool) -> Union[bool, str]:
        """格式化输出"""
        if self.custom_values:
            true_val, false_val = self.custom_values
            return true_val if value else false_val
        
        format_map = {
            'BOOLEAN': value,
            'STRING': 'true' if value else 'false',
            'STRING_UPPER': 'TRUE' if value else 'FALSE',
            'NUMERIC': 1 if value else 0,
            'CHINESE': '是' if value else '否',
            'YN': 'Y' if value else 'N',
            'YESNO': 'Yes' if value else 'No'
        }
        
        return format_map.get(self.output_format.upper(), value)
    
    def validate(self, data: Union[bool, str, int, None]) -> bool:
        """校验布尔值"""
        if data is None:
            return self.null_ratio > 0
        
        if self.custom_values:
            return data in self.custom_values
        
        valid_values = {
            'BOOLEAN': [True, False],
            'STRING': ['true', 'false'],
            'STRING_UPPER': ['TRUE', 'FALSE'],
            'NUMERIC': [1, 0],
            'CHINESE': ['是', '否'],
            'YN': ['Y', 'N'],
            'YESNO': ['Yes', 'No']
        }
        
        expected = valid_values.get(self.output_format.upper(), [True, False])
        return data in expected
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['true_ratio', 'format', 'custom_values', 'null_ratio']


class EnumGenerator(ValidatedDataGenerator[Any]):
    """枚举值生成器"""
    
    def _setup(self) -> None:
        self.values = self.parameters.get('values', ['A', 'B', 'C'])
        self.weights = self.parameters.get('weights', None)  # 权重
        self.allow_null = self.parameters.get('allow_null', False)
        self.null_ratio = self.parameters.get('null_ratio', 0.1)
        self.case_sensitive = self.parameters.get('case_sensitive', True)
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> Any:
        """生成原始枚举值"""
        # 处理null值
        if self.allow_null and random.random() < self.null_ratio:
            return None
        
        # 根据权重选择
        if self.weights and len(self.weights) == len(self.values):
            return random.choices(self.values, weights=self.weights)[0]
        else:
            return random.choice(self.values)
    
    def validate(self, data: Any) -> bool:
        """校验枚举值"""
        if data is None:
            return self.allow_null
        
        if self.case_sensitive:
            return data in self.values
        else:
            # 不区分大小写的比较
            if isinstance(data, str):
                return any(data.lower() == str(v).lower() for v in self.values)
            return data in self.values
    
    def get_value_distribution(self, sample_size: int = 1000) -> Dict[Any, float]:
        """获取值分布统计"""
        samples = [self.generate() for _ in range(sample_size)]
        distribution = {}
        
        for value in self.values:
            count = samples.count(value)
            distribution[value] = count / sample_size
        
        if self.allow_null:
            null_count = samples.count(None)
            distribution[None] = null_count / sample_size
        
        return distribution
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['values', 'weights', 'allow_null', 'null_ratio', 'case_sensitive']


@register_generator('string', ['str', 'text', '字符串'])
class GenericStringGenerator(StringGenerator):
    """通用字符串生成器注册版本"""
    pass


@register_generator('boolean', ['bool', '布尔'])
class GenericBooleanGenerator(BooleanGenerator):
    """通用布尔值生成器注册版本"""
    pass


@register_generator('enum', ['choice', '枚举'])
class GenericEnumGenerator(EnumGenerator):
    """通用枚举生成器注册版本"""
    pass