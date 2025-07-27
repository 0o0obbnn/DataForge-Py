"""
年龄生成器
"""
import random
from typing import Optional, List
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator


class AgeGenerator(ValidatedDataGenerator[int]):
    """年龄生成器"""
    
    def _setup(self) -> None:
        self.min_age = self.parameters.get('min', 18)
        self.max_age = self.parameters.get('max', 65)
        self.distribution = self.parameters.get('distribution', 'uniform')  # uniform, normal, realistic
        
        # 确保年龄范围合理
        if self.min_age < 0:
            self.min_age = 0
        if self.max_age > 120:
            self.max_age = 120
        if self.min_age >= self.max_age:
            self.min_age = 18
            self.max_age = 65
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> int:
        """生成原始年龄"""
        if self.distribution == 'normal':
            # 正态分布：集中在中间年龄段
            mean = (self.min_age + self.max_age) / 2
            std = (self.max_age - self.min_age) / 6  # 99.7%的值在3个标准差内
            age = int(random.normalvariate(mean, std))
            # 确保在范围内
            age = max(self.min_age, min(self.max_age, age))
            return age
        elif self.distribution == 'realistic':
            # 现实分布：模拟真实人口年龄分布
            return self._generate_realistic_age()
        else:
            # 均匀分布
            return random.randint(self.min_age, self.max_age)
    
    def _generate_realistic_age(self) -> int:
        """生成符合现实分布的年龄"""
        # 基于中国人口年龄分布的简化模型
        age_ranges = [
            (18, 25, 0.15),  # 青年
            (26, 35, 0.25),  # 青壮年
            (36, 45, 0.25),  # 中年
            (46, 55, 0.20),  # 中老年
            (56, 65, 0.15),  # 老年
        ]
        
        # 根据当前设置的min/max调整权重
        adjusted_ranges = []
        total_weight = 0
        
        for start, end, weight in age_ranges:
            # 计算与当前范围的交集
            overlap_start = max(start, self.min_age)
            overlap_end = min(end, self.max_age)
            
            if overlap_start <= overlap_end:
                # 根据重叠比例调整权重
                overlap_ratio = (overlap_end - overlap_start + 1) / (end - start + 1)
                adjusted_weight = weight * overlap_ratio
                adjusted_ranges.append((overlap_start, overlap_end, adjusted_weight))
                total_weight += adjusted_weight
        
        if not adjusted_ranges:
            # 如果没有重叠，回退到均匀分布
            return random.randint(self.min_age, self.max_age)
        
        # 随机选择年龄段
        rand_val = random.random() * total_weight
        cumulative_weight = 0
        
        for start, end, weight in adjusted_ranges:
            cumulative_weight += weight
            if rand_val <= cumulative_weight:
                return random.randint(start, end)
        
        # 备用方案
        return random.randint(self.min_age, self.max_age)
    
    def validate(self, data: int) -> bool:
        """校验年龄"""
        if not isinstance(data, int):
            return False
        
        return 0 <= data <= 120 and self.min_age <= data <= self.max_age
    
    def get_age_category(self, age: int) -> str:
        """获取年龄分类"""
        if age < 18:
            return "未成年"
        elif age < 25:
            return "青年"
        elif age < 35:
            return "青壮年"
        elif age < 45:
            return "中年"
        elif age < 55:
            return "中老年"
        elif age < 65:
            return "老年"
        else:
            return "高龄"
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.NUMERIC
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['min', 'max', 'distribution']


@register_generator('age', ['年龄'])
class ChineseAgeGenerator(AgeGenerator):
    """中文年龄生成器注册版本"""
    pass