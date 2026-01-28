"""句子生成器"""

import random

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorType,
)


class SentenceGenerator(DataGenerator):
    """句子生成器"""

    WORDS = [
        "the",
        "quick",
        "brown",
        "fox",
        "jumps",
        "over",
        "lazy",
        "dog",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
        "up",
        "about",
        "into",
        "through",
        "after",
        "before",
        "under",
        "over",
        "between",
        "among",
        "during",
    ]

    def _setup(self) -> None:
        """初始化设置"""
        pass

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        """生成句子"""
        word_count = self.parameters.get("word_count", random.randint(5, 15))
        words = [random.choice(self.WORDS) for _ in range(word_count)]
        sentence = " ".join(words)
        return sentence.capitalize() + "."

    def validate(self, data: str) -> bool:
        """验证句子"""
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


register_generator("sentence")(SentenceGenerator)
