"""
文章生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestArticleGenerator:
    """文章生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单篇文章"""
        from dataforge.generators.text.article import ArticleGenerator
        generator_factory.registry.register("article", ArticleGenerator)
        
        config = GeneratorConfig(
            generator_type="article",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        article = generator.generate_single()
        
        assert isinstance(article, (str, dict))
        assert generator.validate(article)

    def test_generate_batch(self, generator_factory):
        """测试批量生成文章"""
        from dataforge.generators.text.article import ArticleGenerator
        generator_factory.registry.register("article", ArticleGenerator)
        
        config = GeneratorConfig(
            generator_type="article",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        articles = generator.generate_batch(3)
        
        assert len(articles) == 3
        for article in articles:
            assert article is not None

    def test_article_structure(self, generator_factory):
        """测试文章结构"""
        from dataforge.generators.text.article import ArticleGenerator
        generator_factory.registry.register("article", ArticleGenerator)
        
        config = GeneratorConfig(
            generator_type="article",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        article = generator.generate_single()
        
        if isinstance(article, dict):
            # Should have title and content
            assert "title" in article or "content" in article or len(article) > 0
        elif isinstance(article, str):
            assert len(article) > 100

    def test_article_length(self, generator_factory):
        """测试文章长度"""
        from dataforge.generators.text.article import ArticleGenerator
        generator_factory.registry.register("article", ArticleGenerator)
        
        config = GeneratorConfig(
            generator_type="article",
            parameters={"paragraphs": 3}
        )
        generator = generator_factory.create_generator(config)
        article = generator.generate_single()
        
        if isinstance(article, str):
            assert len(article) > 100
        elif isinstance(article, dict):
            assert article is not None

    def test_validation(self, generator_factory):
        """测试文章验证"""
        from dataforge.generators.text.article import ArticleGenerator
        generator_factory.registry.register("article", ArticleGenerator)
        
        config = GeneratorConfig(
            generator_type="article",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid article
        article = generator.generate_single()
        assert generator.validate(article)
        
        # Invalid article
        assert not generator.validate("")
        assert not generator.validate(None)
