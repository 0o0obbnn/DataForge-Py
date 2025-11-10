"""
Lorem文本生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestLoremGenerator:
    """Lorem文本生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个Lorem文本"""
        from dataforge.generators.text.lorem import LoremGenerator
        generator_factory.registry.register("lorem", LoremGenerator)
        
        config = GeneratorConfig(
            generator_type="lorem",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        text = generator.generate_single()
        
        assert isinstance(text, str)
        assert len(text) > 0
        assert generator.validate(text)

    def test_generate_batch(self, generator_factory):
        """测试批量生成Lorem文本"""
        from dataforge.generators.text.lorem import LoremGenerator
        generator_factory.registry.register("lorem", LoremGenerator)
        
        config = GeneratorConfig(
            generator_type="lorem",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        texts = generator.generate_batch(10)
        
        assert len(texts) == 10
        for text in texts:
            assert isinstance(text, str)
            assert len(text) > 0

    def test_word_count(self, generator_factory):
        """测试单词数量"""
        from dataforge.generators.text.lorem import LoremGenerator
        generator_factory.registry.register("lorem", LoremGenerator)
        
        config = GeneratorConfig(
            generator_type="lorem",
            parameters={"words": 10}
        )
        generator = generator_factory.create_generator(config)
        text = generator.generate_single()
        
        word_count = len(text.split())
        assert 5 <= word_count <= 15  # Allow some flexibility

    def test_sentence_format(self, generator_factory):
        """测试句子格式"""
        from dataforge.generators.text.lorem import LoremGenerator
        generator_factory.registry.register("lorem", LoremGenerator)
        
        config = GeneratorConfig(
            generator_type="lorem",
            parameters={"format": "sentence"}
        )
        generator = generator_factory.create_generator(config)
        text = generator.generate_single()
        
        assert isinstance(text, str)
        assert len(text) > 10

    def test_paragraph_format(self, generator_factory):
        """测试段落格式"""
        from dataforge.generators.text.lorem import LoremGenerator
        generator_factory.registry.register("lorem", LoremGenerator)
        
        config = GeneratorConfig(
            generator_type="lorem",
            parameters={"format": "paragraph"}
        )
        generator = generator_factory.create_generator(config)
        text = generator.generate_single()
        
        assert isinstance(text, str)
        assert len(text) > 50

    def test_validation(self, generator_factory):
        """测试文本验证"""
        from dataforge.generators.text.lorem import LoremGenerator
        generator_factory.registry.register("lorem", LoremGenerator)
        
        config = GeneratorConfig(
            generator_type="lorem",
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
        from dataforge.generators.text.lorem import LoremGenerator
        generator_factory.registry.register("lorem", LoremGenerator)
        
        config = GeneratorConfig(
            generator_type="lorem",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        texts = generator.generate_batch(20)
        
        # Should have some variety
        unique_texts = set(texts)
        assert len(unique_texts) > 5
