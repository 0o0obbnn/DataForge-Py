"""
整数生成器
"""
import random
from decimal import Decimal
from typing import Optional, Dict, Any, List, Union
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator


class IntegerGenerator(ValidatedDataGenerator[int]):
    """整数生成器"""
    
    def _setup(self) -> None:
        self.min_value = self.parameters.get('min', 0)
        self.max_value = self.parameters.get('max', 100)
        self.allow_negative = self.parameters.get('allow_negative', True)
        self.allow_zero = self.parameters.get('allow_zero', True)
        self.distribution = self.parameters.get('distribution', 'UNIFORM')  # UNIFORM, NORMAL, EXPONENTIAL
        self.step = self.parameters.get('step', 1)  # 步长
        self.exclude_values = self.parameters.get('exclude', [])  # 排除的值
        self.weights = self.parameters.get('weights', None)  # 权重分布
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> int:
        """生成原始整数"""
        # 调整范围
        min_val, max_val = self._adjust_range()
        
        # 根据分布类型生成
        if self.distribution.upper() == 'NORMAL':
            value = self._generate_normal_distribution(min_val, max_val)
        elif self.distribution.upper() == 'EXPONENTIAL':
            value = self._generate_exponential_distribution(min_val, max_val)
        elif self.weights:
            value = self._generate_weighted_distribution(min_val, max_val)
        else:  # UNIFORM
            value = self._generate_uniform_distribution(min_val, max_val)
        
        # 应用步长
        if self.step != 1:
            value = (value // self.step) * self.step
        
        # 排除特定值
        if value in self.exclude_values:
            # 重新生成（最多尝试10次）
            for _ in range(10):
                value = self._generate_uniform_distribution(min_val, max_val)
                if self.step != 1:
                    value = (value // self.step) * self.step
                if value not in self.exclude_values:
                    break
        
        return value
    
    def _adjust_range(self) -> tuple[int, int]:
        """调整生成范围"""
        min_val = self.min_value
        max_val = self.max_value
        
        # 处理负数限制
        if not self.allow_negative:
            min_val = max(0, min_val)
        
        # 处理零值限制
        if not self.allow_zero:
            if min_val <= 0 <= max_val:
                if min_val == 0:
                    min_val = 1
                elif max_val == 0:
                    max_val = -1
        
        return min_val, max_val
    
    def _generate_uniform_distribution(self, min_val: int, max_val: int) -> int:
        """生成均匀分布的整数"""
        return random.randint(min_val, max_val)
    
    def _generate_normal_distribution(self, min_val: int, max_val: int) -> int:
        """生成正态分布的整数"""
        mean = (min_val + max_val) / 2
        # 标准差为范围的1/6，这样99.7%的值在范围内
        std_dev = (max_val - min_val) / 6
        
        # 生成正态分布值并裁剪到范围内
        value = random.normalvariate(mean, std_dev)
        value = max(min_val, min(max_val, int(round(value))))
        
        return value
    
    def _generate_exponential_distribution(self, min_val: int, max_val: int) -> int:
        """生成指数分布的整数"""
        # λ参数，控制分布形状
        lambda_param = 1.0
        
        # 生成[0,1)的指数分布值
        exp_value = random.expovariate(lambda_param)
        
        # 映射到指定范围
        range_size = max_val - min_val
        normalized = 1 - min(1.0, exp_value / 5.0)  # 截断并反转
        value = min_val + int(normalized * range_size)
        
        return min(max_val, max(min_val, value))
    
    def _generate_weighted_distribution(self, min_val: int, max_val: int) -> int:
        """生成加权分布的整数"""
        if not isinstance(self.weights, dict):
            return self._generate_uniform_distribution(min_val, max_val)
        
        # 构建值和权重列表
        values = []
        weights = []
        
        for value, weight in self.weights.items():
            if min_val <= value <= max_val:
                values.append(value)
                weights.append(weight)
        
        if not values:
            return self._generate_uniform_distribution(min_val, max_val)
        
        # 加权随机选择
        return random.choices(values, weights=weights)[0]
    
    def validate(self, data: int) -> bool:
        """校验整数"""
        if not isinstance(data, int):
            return False
        
        min_val, max_val = self._adjust_range()
        
        # 检查范围
        if not (min_val <= data <= max_val):
            return False
        
        # 检查步长
        if self.step != 1 and (data - min_val) % self.step != 0:
            return False
        
        # 检查排除值
        if data in self.exclude_values:
            return False
        
        return True
    
    def generate_sequence(self, count: int, sequence_type: str = 'RANDOM') -> List[int]:
        """生成整数序列"""
        if sequence_type.upper() == 'ASCENDING':
            return self._generate_ascending_sequence(count)
        elif sequence_type.upper() == 'DESCENDING':
            return self._generate_descending_sequence(count)
        elif sequence_type.upper() == 'ARITHMETIC':
            return self._generate_arithmetic_sequence(count)
        else:  # RANDOM
            return [self.generate() for _ in range(count)]
    
    def _generate_ascending_sequence(self, count: int) -> List[int]:
        """生成递增序列"""
        min_val, max_val = self._adjust_range()
        values = random.sample(range(min_val, max_val + 1), min(count, max_val - min_val + 1))
        return sorted(values)
    
    def _generate_descending_sequence(self, count: int) -> List[int]:
        """生成递减序列"""
        return list(reversed(self._generate_ascending_sequence(count)))
    
    def _generate_arithmetic_sequence(self, count: int) -> List[int]:
        """生成等差序列"""
        min_val, max_val = self._adjust_range()
        start = random.randint(min_val, max_val - count * self.step)
        return [start + i * self.step for i in range(count)]
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return [
            'min', 'max', 'allow_negative', 'allow_zero', 'distribution',
            'step', 'exclude', 'weights'
        ]


class DecimalGenerator(ValidatedDataGenerator[float]):
    """小数生成器"""
    
    def _setup(self) -> None:
        self.min_value = self.parameters.get('min', 0.0)
        self.max_value = self.parameters.get('max', 100.0)
        self.precision = self.parameters.get('precision', 2)  # 小数位数
        self.allow_negative = self.parameters.get('allow_negative', True)
        self.allow_zero = self.parameters.get('allow_zero', True)
        self.distribution = self.parameters.get('distribution', 'UNIFORM')
        self.scientific_notation = self.parameters.get('scientific_notation', False)
        self.use_decimal = self.parameters.get('use_decimal', False)  # 使用Decimal类型
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> Union[float, Decimal]:
        """生成原始小数"""
        # 调整范围
        min_val, max_val = self._adjust_range()
        
        # 根据分布类型生成
        if self.distribution.upper() == 'NORMAL':
            value = self._generate_normal_distribution(min_val, max_val)
        elif self.distribution.upper() == 'EXPONENTIAL':
            value = self._generate_exponential_distribution(min_val, max_val)
        else:  # UNIFORM
            value = random.uniform(min_val, max_val)
        
        # 应用精度
        value = round(value, self.precision)
        
        # 转换为Decimal类型（如果需要）
        if self.use_decimal:
            return Decimal(str(value))
        
        return value
    
    def _adjust_range(self) -> tuple[float, float]:
        """调整生成范围"""
        min_val = float(self.min_value)
        max_val = float(self.max_value)
        
        # 处理负数限制
        if not self.allow_negative:
            min_val = max(0.0, min_val)
        
        # 处理零值限制
        if not self.allow_zero:
            if min_val <= 0.0 <= max_val:
                if min_val == 0.0:
                    min_val = 10 ** (-self.precision)
                elif max_val == 0.0:
                    max_val = -(10 ** (-self.precision))
        
        return min_val, max_val
    
    def _generate_normal_distribution(self, min_val: float, max_val: float) -> float:
        """生成正态分布的小数"""
        mean = (min_val + max_val) / 2
        std_dev = (max_val - min_val) / 6
        
        value = random.normalvariate(mean, std_dev)
        return max(min_val, min(max_val, value))
    
    def _generate_exponential_distribution(self, min_val: float, max_val: float) -> float:
        """生成指数分布的小数"""
        lambda_param = 1.0
        exp_value = random.expovariate(lambda_param)
        
        range_size = max_val - min_val
        normalized = 1 - min(1.0, exp_value / 5.0)
        value = min_val + normalized * range_size
        
        return min(max_val, max(min_val, value))
    
    def validate(self, data: Union[float, Decimal]) -> bool:
        """校验小数"""
        if not isinstance(data, (float, Decimal, int)):
            return False
        
        value = float(data)
        min_val, max_val = self._adjust_range()
        
        # 检查范围
        if not (min_val <= value <= max_val):
            return False
        
        # 检查精度
        if self.precision >= 0:
            rounded_value = round(value, self.precision)
            if abs(value - rounded_value) > 1e-10:
                return False
        
        return True
    
    def format_output(self, value: Union[float, Decimal]) -> str:
        """格式化输出"""
        if self.scientific_notation:
            return f"{value:.{self.precision}e}"
        else:
            return f"{value:.{self.precision}f}"
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return [
            'min', 'max', 'precision', 'allow_negative', 'allow_zero',
            'distribution', 'scientific_notation', 'use_decimal'
        ]


class RandomNumberGenerator(ValidatedDataGenerator[str]):
    """随机数字串生成器"""
    
    def _setup(self) -> None:
        self.length = self.parameters.get('length', 10)
        self.min_length = self.parameters.get('min_length', None)
        self.max_length = self.parameters.get('max_length', None)
        self.leading_zeros = self.parameters.get('leading_zeros', True)
        self.allow_duplicates = self.parameters.get('allow_duplicates', True)
        self.format_pattern = self.parameters.get('format', None)  # 如 "###-###-###"
        self.exclude_digits = self.parameters.get('exclude_digits', [])
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始随机数字串"""
        # 确定长度
        if self.min_length is not None and self.max_length is not None:
            length = random.randint(self.min_length, self.max_length)
        else:
            length = self.length
        
        # 如果有格式模式，使用模式生成
        if self.format_pattern:
            return self._generate_with_pattern()
        
        # 生成数字串
        digits = self._get_available_digits()
        
        if not self.leading_zeros and length > 1:
            # 第一位不能是0
            first_digit = random.choice([d for d in digits if d != '0'])
            remaining_digits = ''.join(random.choices(digits, k=length-1))
            return first_digit + remaining_digits
        else:
            return ''.join(random.choices(digits, k=length))
    
    def _get_available_digits(self) -> List[str]:
        """获取可用的数字"""
        all_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        return [d for d in all_digits if d not in self.exclude_digits]
    
    def _generate_with_pattern(self) -> str:
        """根据格式模式生成"""
        pattern = self.format_pattern
        digits = self._get_available_digits()
        result = ''
        
        for char in pattern:
            if char == '#':
                result += random.choice(digits)
            else:
                result += char
        
        return result
    
    def validate(self, data: str) -> bool:
        """校验随机数字串"""
        if not isinstance(data, str):
            return False
        
        # 如果有格式模式，检查格式
        if self.format_pattern:
            return self._validate_pattern(data)
        
        # 检查是否只包含数字
        if not data.isdigit():
            return False
        
        # 检查长度
        if self.min_length is not None and len(data) < self.min_length:
            return False
        if self.max_length is not None and len(data) > self.max_length:
            return False
        if not (self.min_length or self.max_length) and len(data) != self.length:
            return False
        
        # 检查前导零
        if not self.leading_zeros and len(data) > 1 and data[0] == '0':
            return False
        
        # 检查排除的数字
        for digit in self.exclude_digits:
            if digit in data:
                return False
        
        return True
    
    def _validate_pattern(self, data: str) -> bool:
        """验证格式模式"""
        if len(data) != len(self.format_pattern):
            return False
        
        for i, (char, pattern_char) in enumerate(zip(data, self.format_pattern)):
            if pattern_char == '#':
                if not char.isdigit():
                    return False
                if char in self.exclude_digits:
                    return False
            else:
                if char != pattern_char:
                    return False
        
        return True
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return [
            'length', 'min_length', 'max_length', 'leading_zeros',
            'allow_duplicates', 'format', 'exclude_digits'
        ]


@register_generator('integer', ['int', '整数'])
class GenericIntegerGenerator(IntegerGenerator):
    """通用整数生成器注册版本"""
    pass


@register_generator('decimal', ['float', 'number', '小数'])
class GenericDecimalGenerator(DecimalGenerator):
    """通用小数生成器注册版本"""
    pass


@register_generator('random_number', ['random_digits', '随机数字'])
class GenericRandomNumberGenerator(RandomNumberGenerator):
    """随机数字串生成器注册版本"""
    pass