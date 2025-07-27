"""
生成器工厂和注册表
"""
from typing import Dict, Type, List, Optional, Any
from .generator import DataGenerator, GeneratorConfig, GeneratorType, GenerationContext
from .relations import default_relation_manager


class GeneratorRegistry:
    """生成器注册表"""
    
    def __init__(self):
        self._generators: Dict[str, Type[DataGenerator]] = {}
        self._aliases: Dict[str, str] = {}
    
    def register(self, name: str, generator_class: Type[DataGenerator], aliases: Optional[List[str]] = None):
        """注册生成器"""
        self._generators[name] = generator_class
        
        if aliases:
            for alias in aliases:
                self._aliases[alias] = name
    
    def get_generator_class(self, name: str) -> Optional[Type[DataGenerator]]:
        """获取生成器类"""
        # 先检查是否为别名
        actual_name = self._aliases.get(name, name)
        return self._generators.get(actual_name)
    
    def list_generators(self, generator_type: Optional[GeneratorType] = None) -> List[str]:
        """列出所有生成器"""
        if generator_type is None:
            return list(self._generators.keys())
        
        # 过滤指定类型的生成器
        result = []
        for name, generator_class in self._generators.items():
            try:
                # 实例化一个临时对象来检查类型
                temp_config = GeneratorConfig(generator_type=name, parameters={})
                temp_generator = generator_class(temp_config)
                if temp_generator.generator_type == generator_type:
                    result.append(name)
            except:
                pass
        return result
    
    def is_registered(self, name: str) -> bool:
        """检查生成器是否已注册"""
        actual_name = self._aliases.get(name, name) 
        return actual_name in self._generators


class GeneratorFactory:
    """生成器工厂"""
    
    def __init__(self, registry: GeneratorRegistry):
        self.registry = registry
    
    def create_generator(self, config: GeneratorConfig) -> DataGenerator:
        """创建生成器实例"""
        generator_class = self.registry.get_generator_class(config.generator_type)
        
        if generator_class is None:
            raise ValueError(f"Unknown generator type: {config.generator_type}")
        
        return generator_class(config)
    
    def create_generators_batch(self, configs: List[GeneratorConfig]) -> List[DataGenerator]:
        """批量创建生成器"""
        return [self.create_generator(config) for config in configs]
    
    def generate_batch_with_relations(self, configs: List[GeneratorConfig], 
                                    context: Optional[GenerationContext] = None) -> Dict[str, Any]:
        """批量生成数据并应用关联规则"""
        if context is None:
            context = GenerationContext()
        
        # 1. 获取字段依赖顺序
        field_names = [config.generator_type for config in configs]
        ordered_fields = default_relation_manager.get_relation_dependencies(field_names)
        
        # 2. 按顺序生成数据
        result_data = {}
        config_map = {config.generator_type: config for config in configs}
        
        for field_name in ordered_fields:
            if field_name in config_map:
                config = config_map[field_name]
                
                # 3. 应用关联规则更新配置
                result_data = default_relation_manager.apply_relations(
                    result_data, [config], context
                )
                
                # 4. 设置上下文关联数据
                if context.related_data is None:
                    context.related_data = {}
                context.related_data.update(result_data)
                
                # 5. 生成数据
                generator = self.create_generator(config)
                generated_value = generator.generate(context)
                result_data[field_name] = generated_value
                
                # 6. 更新上下文关联数据
                context.related_data[field_name] = generated_value
        
        return result_data


# 全局注册表实例
default_registry = GeneratorRegistry()
default_factory = GeneratorFactory(default_registry)


def register_generator(name: str, aliases: Optional[List[str]] = None):
    """生成器注册装饰器"""
    def decorator(generator_class: Type[DataGenerator]):
        default_registry.register(name, generator_class, aliases)
        return generator_class
    return decorator