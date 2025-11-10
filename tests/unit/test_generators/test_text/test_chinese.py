"""
中文文本生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestChineseTextGenerator:
    """中文文本生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个中文文本"""
        from dataforge.generators.text.chinese import ChineseTextGenerator
        generator_factory.registry.register("chinese_text", ChineseTextGenerator)
        
        config = GeneratorConfig(
            generator_type="chinese_text",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        text = generator.generate_single()
        
        assert isinstance(text, str)
        assert len(text) > 0
        assert generator.validate(text)

    def test_generate_batch(self, generator_factory):
        """测试批量生成中文文本"""
        from dataforge.generators.text.chinese import ChineseTextGenerator
        generator_factory.registry.register("chinese_text", ChineseTextGenerator)
        
        config = GeneratorConfig(
            generator_type="chinese_text",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        texts = generator.generate_batch(10)
        
        assert len(texts) == 10
        for text in texts:
            assert isinstance(text, str)
            assert len(text) > 0

    def test_chinese_characters(self, generator_factory):
        """测试中文字符"""
        from dataforge.generators.text.chinese import ChineseTextGenerator
        generator_factory.registry.register("chinese_text", ChineseTextGenerator)
        
        config = GeneratorConfig(
            generator_type="chinese_text",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        text = generator.generate_single()
        
        # Should contain Chinese characters
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)
        assert has_chinese

    def test_text_length(self, generator_factory):
        """测试文本长度"""
        from dataforge.generators.text.chinese import ChineseTextGenerator
        generator_factory.registry.register("chinese_text", ChineseTextGenerator)
        
        config = GeneratorConfig(
            generator_type="chinese_text",
            parameters={"length": 50}
        )
        generator = generator_factory.create_generator(config)
        text = generator.generate_single()
        
        # Length may be approximate
        assert 30 <= len(text) <= 70

    def test_sentence_format(self, generator_factory):
        """测试句子格式"""
        from dataforge.generators.text.chinese import ChineseTextGenerator
        generator_factory.registry.register("chinese_text", ChineseTextGenerator)
        
        config = GeneratorConfig(
            generator_type="chinese_text",
            parameters={"format": "sentence"}
        )
        generator = generator_factory.create_generator(config)
        text = generator.generate_single()
        
        # Should be a sentence
        assert isinstance(text, str)
        assert len(text) > 5

    def test_paragraph_format(self, generator_factory):
        """测试段落格式"""
        from dataforge.generators.text.chinese import ChineseTextGenerator
        generator_factory.registry.register("chinese_text", ChineseTextGenerator)
        
        config = GeneratorConfig(
            generator_type="chinese_text",
            parameters={"format": "paragraph"}
        )
        generator = generator_factory.create_generator(config)
        text = generator.generate_single()
        
        # Should be a paragraph
        assert isinstance(text, str)
        assert len(text) > 20

    def test_validation(self, generator_factory):
        """测试文本验证"""
        from dataforge.generators.text.chinese import ChineseTextGenerator
        generator_factory.registry.register("chinese_text", ChineseTextGenerator)
        
        config = GeneratorConfig(
            generator_type="chinese_text",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid text
        text = generator.generate_single()
        assert generator.validate(text)
        
        # Invalid text
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_variety(self, generator_factory):
        """测试文本多样性"""
        from dataforge.generators.text.chinese import ChineseTextGenerator
        generator_factory.registry.register("chinese_text", ChineseTextGenerator)
        
        config = GeneratorConfig(
            generator_type="chinese_text",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        texts = generator.generate_batch(20)
        
        # Should have variety
        unique_texts = set(texts)
        assert len(unique_texts) > 10

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.text.chinese import ChineseTextGenerator
        generator_factory.registry.register("chinese_text", ChineseTextGenerator)
        
        config = GeneratorConfig(
            generator_type="chinese_text",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            text = generator.generate_single()
            assert text is not None
            assert len(text) > 0
            assert isinstance(text, str)
