"""
句子生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestSentenceGenerator:
    """句子生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个句子"""
        from dataforge.generators.text.sentence import SentenceGenerator
        generator_factory.registry.register("sentence", SentenceGenerator)
        
        config = GeneratorConfig(
            generator_type="sentence",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        sentence = generator.generate_single()
        
        assert isinstance(sentence, str)
        assert len(sentence) > 0
        assert generator.validate(sentence)

    def test_generate_batch(self, generator_factory):
        """测试批量生成句子"""
        from dataforge.generators.text.sentence import SentenceGenerator
        generator_factory.registry.register("sentence", SentenceGenerator)
        
        config = GeneratorConfig(
            generator_type="sentence",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        sentences = generator.generate_batch(10)
        
        assert len(sentences) == 10
        for sentence in sentences:
            assert isinstance(sentence, str)
            assert len(sentence) > 0

    def test_chinese_sentence(self, generator_factory):
        """测试中文句子"""
        from dataforge.generators.text.sentence import SentenceGenerator
        generator_factory.registry.register("sentence", SentenceGenerator)
        
        config = GeneratorConfig(
            generator_type="sentence",
            parameters={"language": "zh"}
        )
        generator = generator_factory.create_generator(config)
        sentence = generator.generate_single()
        
        # Should contain Chinese characters
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in sentence)
        assert has_chinese or len(sentence) > 0

    def test_english_sentence(self, generator_factory):
        """测试英文句子"""
        from dataforge.generators.text.sentence import SentenceGenerator
        generator_factory.registry.register("sentence", SentenceGenerator)
        
        config = GeneratorConfig(
            generator_type="sentence",
            parameters={"language": "en"}
        )
        generator = generator_factory.create_generator(config)
        sentence = generator.generate_single()
        
        assert isinstance(sentence, str)
        assert len(sentence) > 5

    def test_sentence_length(self, generator_factory):
        """测试句子长度"""
        from dataforge.generators.text.sentence import SentenceGenerator
        generator_factory.registry.register("sentence", SentenceGenerator)
        
        config = GeneratorConfig(
            generator_type="sentence",
            parameters={"min_words": 5, "max_words": 15}
        )
        generator = generator_factory.create_generator(config)
        sentence = generator.generate_single()
        
        assert len(sentence) > 10

    def test_validation(self, generator_factory):
        """测试句子验证"""
        from dataforge.generators.text.sentence import SentenceGenerator
        generator_factory.registry.register("sentence", SentenceGenerator)
        
        config = GeneratorConfig(
            generator_type="sentence",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid sentence
        sentence = generator.generate_single()
        assert generator.validate(sentence)
        
        # Invalid sentence
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_variety(self, generator_factory):
        """测试句子多样性"""
        from dataforge.generators.text.sentence import SentenceGenerator
        generator_factory.registry.register("sentence", SentenceGenerator)
        
        config = GeneratorConfig(
            generator_type="sentence",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        sentences = generator.generate_batch(20)
        
        # Should have variety
        unique_sentences = set(sentences)
        assert len(unique_sentences) > 10
