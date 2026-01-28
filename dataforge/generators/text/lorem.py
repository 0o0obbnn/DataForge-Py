"""Lorem Ipsum文本生成器"""

import random

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorType,
)


class LoremGenerator(DataGenerator):
    """Lorem Ipsum文本生成器"""

    LOREM_WORDS = [
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

    def _setup(self) -> None:
        """初始化设置"""
        pass

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        """生成Lorem Ipsum文本"""
        word_count = self.parameters.get("word_count", 10)
        words = [random.choice(self.LOREM_WORDS) for _ in range(word_count)]
        text = " ".join(words)
        return text.capitalize() + "."

    def validate(self, data: str) -> bool:
        """验证文本"""
        return isinstance(data, str) and len(data) > 0

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.TEXT

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["word_count"]


register_generator("lorem")(LoremGenerator)
