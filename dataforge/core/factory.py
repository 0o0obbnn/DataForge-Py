"""
Generator factory and registry system for DataForge
"""

import inspect
from typing import Dict, List, Optional, Type, Union, Any
from dataclasses import dataclass

from .generator import DataGenerator, GenerationContext


@dataclass
class GeneratorConfig:
    """Configuration for creating generators"""
    generator_type: str
    parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}


class GeneratorRegistry:
    """Registry for managing generator types"""
    
    def __init__(self):
        self._generators: Dict[str, Type[DataGenerator]] = {}
        self._aliases: Dict[str, str] = {}
    
    def register(self, name: str, generator_class: Type[DataGenerator], aliases: Optional[List[str]] = None):
        """Register a generator class"""
        if not issubclass(generator_class, DataGenerator):
            raise ValueError(f"Generator class must inherit from DataGenerator")
        
        self._generators[name] = generator_class
        
        # Register aliases
        if aliases:
            for alias in aliases:
                self._aliases[alias] = name
    
    def get(self, name: str) -> Optional[Type[DataGenerator]]:
        """Get generator class by name or alias"""
        # Check direct name first
        if name in self._generators:
            return self._generators[name]
        
        # Check aliases
        if name in self._aliases:
            actual_name = self._aliases[name]
            return self._generators[actual_name]
        
        return None
    
    def is_registered(self, name: str) -> bool:
        """Check if generator is registered"""
        return name in self._generators or name in self._aliases
    
    def list_generators(self) -> List[str]:
        """List all registered generator names"""
        return list(self._generators.keys())
    
    def list_aliases(self) -> Dict[str, str]:
        """List all aliases and their targets"""
        return self._aliases.copy()


class GeneratorFactory:
    """Factory for creating generator instances"""
    
    def __init__(self, registry: GeneratorRegistry):
        self.registry = registry
    
    def create_generator(self, config: GeneratorConfig) -> DataGenerator:
        """Create a generator instance from config"""
        generator_class = self.registry.get(config.generator_type)
        
        if generator_class is None:
            raise ValueError(f"Unknown generator type: {config.generator_type}")
        
        # Create instance with parameters
        return generator_class(config.parameters or {})
    
    def create_generator_simple(self, generator_type: str, **parameters) -> DataGenerator:
        """Create a generator with simple parameters"""
        config = GeneratorConfig(generator_type, parameters)
        return self.create_generator(config)


# Global registry and factory instances
default_registry = GeneratorRegistry()
default_factory = GeneratorFactory(default_registry)


# Decorator for registering generators
def register_generator(name: str, aliases: Optional[List[str]] = None):
    """Decorator to register a generator class"""
    def decorator(cls: Type[DataGenerator]):
        default_registry.register(name, cls, aliases)
        return cls
    return decorator


# Function-style registration for compatibility
def register_generator_func(name: str, generator_class: Type[DataGenerator], aliases: Optional[List[str]] = None):
    """Function-style generator registration"""
    default_registry.register(name, generator_class, aliases)
