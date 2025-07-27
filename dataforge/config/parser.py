"""
配置解析器
"""
import yaml
import json
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from pydantic import BaseModel, ValidationError
from ..core.generator import GeneratorConfig
from ..core.factory import default_registry


class ConfigSchema(BaseModel):
    """配置文件模式定义"""
    generator_type: str
    count: int = 1
    validate: bool = True
    unique: bool = False
    parameters: Dict[str, Any] = {}
    related_fields: Optional[List[str]] = None


class MultiConfigSchema(BaseModel):
    """多生成器配置模式"""
    generators: List[ConfigSchema]
    output: Optional[Dict[str, Any]] = None
    global_settings: Optional[Dict[str, Any]] = None


class ConfigParser:
    """配置文件解析器"""
    
    def parse_config(self, config_data: Dict[str, Any]) -> List[GeneratorConfig]:
        """解析配置数据"""
        configs = []
        
        try:
            # 支持单个生成器配置
            if 'generator_type' in config_data:
                schema = ConfigSchema(**config_data)
                config = self._parse_single_config(schema.dict())
                configs.append(config)
            # 支持多个生成器配置
            elif 'generators' in config_data:
                multi_schema = MultiConfigSchema(**config_data)
                for gen_config in multi_schema.generators:
                    config = self._parse_single_config(gen_config.dict())
                    configs.append(config)
            else:
                raise ValueError("配置文件格式错误：必须包含 'generator_type' 或 'generators' 字段")
        except ValidationError as e:
            raise ValueError(f"配置验证失败: {e}")
        
        return configs
    
    def _parse_single_config(self, config_data: Dict[str, Any]) -> GeneratorConfig:
        """解析单个生成器配置"""
        if 'generator_type' not in config_data:
            raise ValueError("配置中必须包含 'generator_type' 字段")
        
        generator_type = config_data['generator_type']
        
        # 验证生成器类型是否已注册
        if not default_registry.is_registered(generator_type):
            available_generators = default_registry.list_generators()
            raise ValueError(f"未知的生成器类型: {generator_type}. 可用的生成器: {', '.join(available_generators)}")
        
        # 验证参数
        parameters = config_data.get('parameters', {})
        self._validate_generator_parameters(generator_type, parameters)
        
        return GeneratorConfig(
            generator_type=generator_type,
            parameters=parameters,
            count=config_data.get('count', 1),
            validate=config_data.get('validate', True),
            unique=config_data.get('unique', False),
            related_fields=config_data.get('related_fields', None)
        )
    
    def create_template_config(self, generator_types: List[str]) -> Dict[str, Any]:
        """创建配置模板"""
        if len(generator_types) == 1:
            return {
                "generator_type": generator_types[0],
                "count": 10,
                "validate": True,
                "unique": False,
                "parameters": self._get_default_parameters(generator_types[0])
            }
        else:
            generators = []
            for gen_type in generator_types:
                generators.append({
                    "generator_type": gen_type,
                    "count": 10,
                    "validate": True,
                    "unique": False,
                    "parameters": self._get_default_parameters(gen_type)
                })
            
            return {
                "generators": generators,
                "output": {
                    "format": "json",
                    "file": "output.json",
                    "pretty": True
                }
            }
    
    def _get_default_parameters(self, generator_type: str) -> Dict[str, Any]:
        """获取生成器的默认参数"""
        defaults = {
            'idcard': {
                'region': 'ANY',
                'gender': 'ANY',
                'birth_date_range': ['1980-01-01', '2000-12-31'],
                'valid': True
            },
            'bankcard': {
                'type': 'BOTH',
                'issuer': 'ANY',
                'bank': 'ANY',
                'length': 16,
                'valid': True
            },
            'phone': {
                'region': 'CN',
                'operator': 'ANY',
                'prefix': None,
                'valid': True
            },
            'name': {
                'type': 'BOTH',
                'gender': 'ANY',
                'surname_file': None,
                'givenname_file': None
            }
        }
        
        return defaults.get(generator_type, {})
    
    def save_config(self, config_data: Dict[str, Any], file_path: str, format_type: str = 'yaml'):
        """保存配置到文件"""
        path = Path(file_path)
        
        with open(path, 'w', encoding='utf-8') as f:
            if format_type.lower() == 'yaml':
                yaml.dump(config_data, f, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
            else:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    def _validate_generator_parameters(self, generator_type: str, parameters: Dict[str, Any]) -> None:
        """验证生成器参数"""
        try:
            # 创建临时配置来检查参数有效性
            temp_config = GeneratorConfig(generator_type=generator_type, parameters={})
            generator_class = default_registry.get_generator_class(generator_type)
            
            if generator_class:
                temp_generator = generator_class(temp_config)
                supported_params = getattr(temp_generator, 'supported_parameters', [])
                
                # 检查未知参数
                unknown_params = set(parameters.keys()) - set(supported_params)
                if unknown_params:
                    print(f"Warning: Unknown parameters for {generator_type}: {', '.join(unknown_params)}")
        except Exception:
            # 如果验证失败，只记录警告而不中断
            pass
    
    def validate_config(self, config_data: Dict[str, Any]) -> List[str]:
        """验证配置文件"""
        errors = []
        
        try:
            self.parse_config(config_data)
        except Exception as e:
            errors.append(str(e))
        
        return errors
    
    def load_config_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """加载配置文件"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"配置文件不存在: {file_path}")
        
        if not path.is_file():
            raise ValueError(f"路径不是文件: {file_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix.lower() in ['.yaml', '.yml']:
                    return yaml.safe_load(f)
                elif path.suffix.lower() == '.json':
                    return json.load(f)
                else:
                    # 尝试根据内容判断格式
                    content = f.read()
                    f.seek(0)
                    
                    try:
                        return yaml.safe_load(content)
                    except yaml.YAMLError:
                        try:
                            return json.loads(content)
                        except json.JSONDecodeError:
                            raise ValueError(f"无法解析配置文件格式: {file_path}")
        except Exception as e:
            raise ValueError(f"读取配置文件失败: {e}")