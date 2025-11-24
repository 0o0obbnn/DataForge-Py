#!/usr/bin/env python3
"""
UUID生成器
"""

import uuid

from ...core.factory import register_generator
from ...core.generator import DataGenerator, GeneratorConfig
from ...core.types import GeneratorType


class UUIDGenerator(DataGenerator[str]):
    """生成UUID"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.version = self.config.parameters.get("version", 4)

    def generate_single(self, context=None) -> str:
        """生成单个UUID"""
        if self.version == 1:
            return str(uuid.uuid1())
        elif self.version == 3:
            # Requires namespace and name
            namespace = self.config.parameters.get("namespace", uuid.NAMESPACE_DNS)
            name = self.config.parameters.get("name", "dataforge.com")
            return str(uuid.uuid3(namespace, name))
        elif self.version == 5:
            # Requires namespace and name
            namespace = self.config.parameters.get("namespace", uuid.NAMESPACE_DNS)
            name = self.config.parameters.get("name", "dataforge.com")
            return str(uuid.uuid5(namespace, name))
        else:  # Default to version 4
            return str(uuid.uuid4())

    def validate(self, data: str) -> bool:
        """校验UUID"""
        if not isinstance(data, str):
            return False
        try:
            uuid.UUID(
                data, version=self.version if self.version in [1, 2, 3, 4, 5] else 4
            )
            return True
        except (ValueError, AttributeError):
            return False

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        return ["version", "namespace", "name"]


@register_generator("uuid")
class GenericUUIDGenerator(UUIDGenerator):
    """通用uuid生成器注册版本"""

    pass
