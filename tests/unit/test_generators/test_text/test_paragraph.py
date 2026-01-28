"""
段落生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestParagraphGenerator:
    """段落生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个段落"""
        from dataforge.generators.text.paragraph import ParagraphGenerator

        generator_factory.registry.register("paragraph", ParagraphGenerator)

        config = GeneratorConfig(generator_type="paragraph", parameters={})
        generator = generator_factory.create_generator(config)
        paragraph = generator.generate_single()

        assert isinstance(paragraph, str)
        assert len(paragraph) > 20
        assert generator.validate(paragraph)

    def test_generate_batch(self, generator_factory):
        """测试批量生成段落"""
        from dataforge.generators.text.paragraph import ParagraphGenerator

        generator_factory.registry.register("paragraph", ParagraphGenerator)

        config = GeneratorConfig(generator_type="paragraph", parameters={})
        generator = generator_factory.create_generator(config)
        paragraphs = generator.generate_batch(5)

        assert len(paragraphs) == 5
        for paragraph in paragraphs:
            assert isinstance(paragraph, str)
            assert len(paragraph) > 20

    def test_sentence_count(self, generator_factory):
        """测试句子数量"""
        from dataforge.generators.text.paragraph import ParagraphGenerator

        generator_factory.registry.register("paragraph", ParagraphGenerator)

        config = GeneratorConfig(
            generator_type="paragraph", parameters={"sentences": 5}
        )
        generator = generator_factory.create_generator(config)
        paragraph = generator.generate_single()

        assert len(paragraph) > 50

    def test_chinese_paragraph(self, generator_factory):
        """测试中文段落"""
        from dataforge.generators.text.paragraph import ParagraphGenerator

        generator_factory.registry.register("paragraph", ParagraphGenerator)

        config = GeneratorConfig(
            generator_type="paragraph", parameters={"language": "zh"}
        )
        generator = generator_factory.create_generator(config)
        paragraph = generator.generate_single()

        assert isinstance(paragraph, str)
        assert len(paragraph) > 20

    def test_validation(self, generator_factory):
        """测试段落验证"""
        from dataforge.generators.text.paragraph import ParagraphGenerator

        generator_factory.registry.register("paragraph", ParagraphGenerator)

        config = GeneratorConfig(generator_type="paragraph", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid paragraph
        paragraph = generator.generate_single()
        assert generator.validate(paragraph)

        # Invalid paragraph
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_variety(self, generator_factory):
        """测试段落多样性"""
        from dataforge.generators.text.paragraph import ParagraphGenerator

        generator_factory.registry.register("paragraph", ParagraphGenerator)

        config = GeneratorConfig(generator_type="paragraph", parameters={})
        generator = generator_factory.create_generator(config)
        paragraphs = generator.generate_batch(10)

        # Should have variety
        unique_paragraphs = set(paragraphs)
        assert len(unique_paragraphs) > 5
