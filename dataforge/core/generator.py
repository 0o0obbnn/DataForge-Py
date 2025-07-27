"""
DataForge核心生成器接口和基类
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum


T = TypeVar('T')


class GeneratorType(Enum):
    """生成器类型枚举"""
    BASIC_INFO = "basic_info"
    IDENTIFIER = "identifier"
    CONTACT = "contact"
    NETWORK = "network"
    TEXT = "text"
    STRUCTURED = "structured"
    NUMERIC = "numeric"
    DATETIME = "datetime"
    SECURITY = "security"
    MEDIA = "media"
    ENUM = "enum"
    SPECIAL = "special"


@dataclass
class GeneratorConfig:
    """生成器配置类"""
    generator_type: str
    parameters: Dict[str, Any]
    count: int = 1
    validate: bool = True
    unique: bool = False
    related_fields: Optional[Dict[str, str]] = None


@dataclass
class GenerationContext:
    """数据生成上下文"""
    config: Optional[GeneratorConfig] = None
    related_data: Optional[Dict[str, Any]] = None
    batch_id: Optional[str] = None
    index: Optional[int] = None


class DataGenerator(ABC, Generic[T]):
    """数据生成器抽象基类"""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.parameters = config.parameters
        self._setup()
    
    @abstractmethod
    def _setup(self) -> None:
        """初始化设置，子类实现具体逻辑"""
        pass
    
    @abstractmethod
    def generate_single(self, context: Optional[GenerationContext] = None) -> T:
        """生成单个数据项"""
        pass
    
    def generate_batch(self, count: int, context: Optional[GenerationContext] = None) -> List[T]:
        """生成批量数据"""
        results = []
        for i in range(count):
            if context:
                context.index = i
            data = self.generate_single(context)
            
            # 如果需要唯一性校验
            if self.config.unique and data in results:
                # 重试生成，最多尝试3次
                retry_count = 0
                while data in results and retry_count < 3:
                    data = self.generate_single(context)
                    retry_count += 1
                    
            results.append(data)
        return results
    
    def generate(self, context: Optional[GenerationContext] = None) -> T:
        """生成单个数据项（便捷方法）"""
        return self.generate_single(context)
    
    @abstractmethod
    def validate(self, data: T) -> bool:
        """数据校验"""
        pass
    
    @property
    @abstractmethod
    def generator_type(self) -> GeneratorType:
        """获取生成器类型"""
        pass
    
    @property
    @abstractmethod
    def supported_parameters(self) -> List[str]:
        """获取支持的参数列表"""
        pass


class ValidatedDataGenerator(DataGenerator[T]):
    """带校验的数据生成器基类"""
    
    def generate_single(self, context: Optional[GenerationContext] = None) -> T:
        """生成单个数据项并校验"""
        data = self._generate_raw(context)
        
        if self.config.validate and not self.validate(data):
            if self.config.parameters.get('valid', True):
                # 如果要求生成有效数据但校验失败，重试
                retry_count = 0
                while not self.validate(data) and retry_count < 5:
                    data = self._generate_raw(context)
                    retry_count += 1
        
        return data
    
    @abstractmethod
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> T:
        """生成原始数据，子类实现"""
        pass


class RelatedDataGenerator(DataGenerator[T]):
    """支持关联数据的生成器基类"""
    
    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.related_fields = config.related_fields or {}
    
    def generate_single(self, context: Optional[GenerationContext] = None) -> T:
        """根据关联数据生成单个数据项"""
        related_data = None
        if context and context.related_data:
            related_data = {
                field: context.related_data.get(related_field)
                for field, related_field in self.related_fields.items()
                if related_field in context.related_data
            }
        
        return self._generate_with_relations(related_data, context)
    
    @abstractmethod
    def _generate_with_relations(
        self, 
        related_data: Optional[Dict[str, Any]], 
        context: Optional[GenerationContext] = None
    ) -> T:
        """根据关联数据生成数据"""
        pass