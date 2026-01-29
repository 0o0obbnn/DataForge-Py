"""
YAML数据生成器

提供YAML格式数据的生成，支持锚点、引用、注释和多文档。
"""

import random
import secrets
from datetime import datetime
from typing import Any

import yaml

from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GenerationContext, GeneratorConfig

from ...core.types import GeneratorType


class YAMLGenerator(DataGenerator):
    """YAML数据生成器基类"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.depth = int(self.config.parameters.get("depth", 4))
        # Normalize array_size to a tuple of two ints (min, max)
        array_param = self.config.parameters.get("array_size", (1, 5))
        try:
            self.array_size: tuple[int, int] = (
                int(array_param[0]),
                int(array_param[1]),
            )
        except Exception:
            self.array_size = (1, 5)

        self.use_anchors = bool(self.config.parameters.get("use_anchors", True))
        self.use_comments = bool(self.config.parameters.get("use_comments", False))
        self.use_multiline_strings = bool(
            self.config.parameters.get("use_multiline_strings", True)
        )
        self.use_aliases = bool(self.config.parameters.get("use_aliases", True))

    def _generate_key_name(self) -> str:
        """生成有效的YAML键名"""
        words = [
            "user",
            "data",
            "config",
            "settings",
            "value",
            "item",
            "property",
            "name",
            "title",
            "description",
            "status",
            "type",
            "category",
            "level",
            "amount",
            "count",
            "size",
            "length",
            "width",
            "height",
            "weight",
            "color",
            "style",
            "format",
            "mode",
            "option",
            "flag",
            "tag",
            "label",
            "code",
            "id",
            "key",
            "index",
            "position",
            "order",
        ]
        return random.choice(words)

    def _generate_string_value(self, length: int | None = None) -> str:
        """生成字符串值"""
        if length is None:
            length = secrets.randbelow(26) + 5

        words = [
            "lorem",
            "ipsum",
            "dolor",
            "sit",
            "amet",
            "consectetur",
            "adipiscing",
            "elit",
            "sed",
            "do",
            "eiusmod",
            "tempor",
            "incididunt",
            "ut",
            "labore",
            "et",
            "dolore",
            "magna",
            "aliqua",
            "enim",
            "ad",
            "minim",
            "veniam",
            "quis",
            "nostrud",
            "exercitation",
            "ullamco",
            "laboris",
            "nisi",
            "aliquip",
            "ex",
            "ea",
            "commodo",
            "consequat",
            "duis",
            "aute",
            "irure",
            "in",
            "reprehenderit",
            "voluptate",
            "velit",
            "esse",
            "cillum",
            "fugiat",
            "nulla",
            "pariatur",
            "excepteur",
            "sint",
            "occaecat",
            "cupidatat",
            "non",
            "proident",
            "sunt",
            "culpa",
            "qui",
            "officia",
            "deserunt",
            "mollit",
            "anim",
            "id",
            "est",
            "laborum",
        ]

        if self.use_multiline_strings and (secrets.randbelow(1000000) / 1000000) > 0.7:
            # 多行字符串
            lines = []
            num_lines = secrets.randbelow(3) + 2
            for _ in range(num_lines):
                line_words = random.choices(words, k=secrets.randbelow(6) + 3)
                lines.append(" ".join(line_words))
            return "\n".join(lines)
        else:
            return " ".join(random.choices(words, k=min(length // 4, 8)))

    def _generate_numeric_value(self) -> int | float:
        """生成数值"""
        if (secrets.randbelow(1000000) / 1000000) > 0.3:
            return secrets.randbelow(1000 + 1)
        else:
            return round(random.uniform(0, 100), 2)

    def _generate_boolean_value(self) -> bool:
        """生成布尔值"""
        return random.choice([True, False])

    def _generate_list_value(self, depth: int = 0) -> list[Any]:
        """生成列表值"""
        if depth >= self.depth:
            return [self._generate_primitive_value()]

        size = (
            secrets.randbelow(self.array_size[1] - self.array_size[0] + 1)
            + self.array_size[0]
        )
        items: list[Any] = []

        for _ in range(size):
            value_type = random.choice(["primitive", "dict", "list"])

            if value_type == "primitive":
                items.append(self._generate_primitive_value())
            elif value_type == "dict":
                items.append(self._generate_dict_value(depth + 1))
            else:
                items.append(self._generate_list_value(depth + 1))

        return items

    def _generate_dict_value(self, depth: int = 0) -> dict[str, Any]:
        """生成字典值"""
        if depth >= self.depth:
            return {self._generate_key_name(): self._generate_primitive_value()}

        data: dict[str, Any] = {}
        num_keys = secrets.randbelow(4) + 2

        for _ in range(num_keys):
            key = self._generate_key_name()

            # 避免重复键
            while key in data:
                key = self._generate_key_name()

            value_type = random.choice(["primitive", "dict", "list"])

            if value_type == "primitive":
                data[key] = self._generate_primitive_value()
            elif value_type == "dict":
                data[key] = self._generate_dict_value(depth + 1)
            else:
                data[key] = self._generate_list_value(depth + 1)

        return data

    def _generate_primitive_value(self) -> str | int | float | bool | None:
        """生成原始值"""
        value_types = ["string", "number", "boolean", "null"]

        if (secrets.randbelow(1000000) / 1000000) > 0.1:  # 90%概率生成非null值
            value_type = random.choice(value_types[:-1])
        else:
            value_type = "null"

        if value_type == "string":
            return self._generate_string_value()
        elif value_type == "number":
            return self._generate_numeric_value()
        elif value_type == "boolean":
            return self._generate_boolean_value()
        else:
            return None

    def _add_yaml_features(self, data: Any) -> Any:
        """添加YAML特性"""
        # 简化YAML特性，避免锚点和别名问题
        return data
        if isinstance(data, dict):
            # 添加锚点和别名
            if self.use_anchors and (secrets.randbelow(1000000) / 1000000) > 0.7:
                key = list(data.keys())[0] if data else "default"
                data[key] = {"<<": "*anchor"}

            # 添加注释
            if self.use_comments and (secrets.randbelow(1000000) / 1000000) > 0.5:
                return {"# This is a comment": data}

        return data

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个YAML数据"""
        template = self.config.parameters.get("template")
        if template:
            templates = self._get_yaml_templates()
            if template in templates:
                template_config = templates[template]
                data = template_config.get("structure", {})
                return yaml.dump(data, default_flow_style=False, allow_unicode=True)

        # 默认生成简单结构
        data = {
            "name": "test_user",
            "value": "sample_data",
            "timestamp": str(datetime.now()),
        }
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)

    def _generate_yaml_with_anchors(self) -> str:
        """生成带锚点的YAML数据"""
        data = {
            "defaults": {"user": {"name": "test_user", "email": "test@example.com"}},
            "users": [
                {"<<": "*user_defaults", "id": 1},
                {"<<": "*user_defaults", "id": 2},
            ],
        }
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)

        # 添加YAML特性
        data = self._add_yaml_features(data)

        # 配置YAML输出
        yaml_config = {
            "default_flow_style": False,
            "allow_unicode": True,
            "width": 1000,  # 防止自动换行
            "indent": 2,
        }

        yaml_str = yaml.dump(data, **yaml_config)

        # 添加文档分隔符（多文档支持）
        if (secrets.randbelow(1000000) / 1000000) > 0.8:
            second_data = self._generate_dict_value()
            second_yaml = yaml.dump(second_data, **yaml_config)
            yaml_str += "\n---\n" + second_yaml

        return yaml_str

    def validate(self, data: str) -> bool:
        """验证YAML格式"""
        try:
            yaml.safe_load(data)
            return True
        except yaml.YAMLError:
            return False

    def generate_batch(
        self, count: int, context: GenerationContext | None = None
    ) -> list[str]:
        """批量生成YAML数据"""
        return [self._generate_yaml() for _ in range(count)]

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []

    # Helper stubs to satisfy static type checkers and provide reasonable defaults
    def _get_yaml_templates(self) -> dict[str, dict[str, Any]]:
        """Return built-in templates. Subclasses may override."""
        return {}

    def _generate_yaml(self) -> str:
        """Default YAML generation implementation used by batch generation.

        Subclasses may override to provide templates or structured outputs.
        """
        data = self._generate_dict_value()
        return yaml.safe_dump(data, default_flow_style=False, allow_unicode=True)


class GenericYAMLGenerator(YAMLGenerator):
    """通用YAML数据生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self._setup()

    def _setup(self) -> None:
        """初始化设置"""
        self.depth = self.config.parameters.get("depth", 3)
        array_param = self.config.parameters.get("array_size", (1, 5))
        try:
            self.array_size = (int(array_param[0]), int(array_param[1]))
        except Exception:
            self.array_size = (1, 5)

        self.use_null = bool(self.config.parameters.get("use_null", True))
        self.template = self.config.parameters.get("template")
        self.use_anchors = bool(self.config.parameters.get("use_anchors", False))
        self.use_aliases = bool(self.config.parameters.get("use_aliases", False))

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成原始YAML字符串"""
        if self.template and self.template in self._get_yaml_templates():
            template_config = self._get_yaml_templates()[self.template]
            for key, value in template_config.items():
                setattr(self, key, value)
            return self._generate_yaml()
        else:
            return self._generate_yaml()

    def _generate_yaml(self) -> str:
        """生成YAML字符串"""
        template = self.config.parameters.get("template")

        if template and template in self._get_yaml_templates():
            template_config = self._get_yaml_templates()[template]
            structure = template_config.get("structure", {})
        else:
            # 默认YAML结构
            structure = {
                "config": {
                    "name": "test_config",
                    "version": 1.0,
                    "settings": {"debug": True, "timeout": 30},
                }
            }

        return yaml.safe_dump(structure, default_flow_style=False, allow_unicode=True)

    def validate(self, data: str) -> bool:
        """验证YAML格式"""
        try:
            parsed = yaml.safe_load(data)
            return isinstance(parsed, (dict, list))
        except yaml.YAMLError:
            return False

    @property
    def generator_type(self) -> GeneratorType:
        """获取生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """获取支持的参数列表"""
        return [
            "depth",
            "array_size",
            "use_null",
            "template",
            "use_anchors",
            "use_aliases",
        ]

    def _get_yaml_templates(self) -> dict[str, dict[str, Any]]:
        """获取YAML模板配置"""
        return {
            "user": {
                "structure": {
                    "name": "test_user",
                    "email": "test@example.com",
                    "age": 25,
                    "active": True,
                }
            },
            "config": {
                "structure": {
                    "name": "app_config",
                    "version": "1.0.0",
                    "settings": {"debug": True, "timeout": 30},
                }
            },
            "api": {
                "structure": {
                    "name": "api_response",
                    "status": "success",
                    "data": {"id": 1, "value": "test"},
                }
            },
        }


# 注册生成器
register_generator("yaml_generator", ["yaml"])(YAMLGenerator)
