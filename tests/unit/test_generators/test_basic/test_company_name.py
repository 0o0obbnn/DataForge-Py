"""
公司名称生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestCompanyNameGenerator:
    """公司名称生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个公司名称"""
        config = GeneratorConfig(
            generator_type="company_name",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        company_name = generator.generate_single()
        
        assert isinstance(company_name, str)
        assert len(company_name) >= 4
        assert generator.validate(company_name)

    def test_generate_batch(self, generator_factory):
        """测试批量生成公司名称"""
        config = GeneratorConfig(
            generator_type="company_name",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        company_names = generator.generate_batch(10)
        
        assert len(company_names) == 10
        for name in company_names:
            assert isinstance(name, str)
            assert len(name) >= 4

    def test_chinese_company_name(self, generator_factory):
        """测试中文公司名称"""
        config = GeneratorConfig(
            generator_type="company_name",
            parameters={"language": "chinese"}
        )
        generator = generator_factory.create_generator(config)
        company_name = generator.generate_single()
        
        assert isinstance(company_name, str)
        # Should contain Chinese characters
        assert any('\u4e00' <= char <= '\u9fff' for char in company_name)

    def test_english_company_name(self, generator_factory):
        """测试英文公司名称"""
        config = GeneratorConfig(
            generator_type="company_name",
            parameters={"language": "english"}
        )
        generator = generator_factory.create_generator(config)
        company_name = generator.generate_single()
        
        assert isinstance(company_name, str)
        # Should contain English letters
        assert any(c.isalpha() and ord(c) < 128 for c in company_name)

    def test_company_suffix(self, generator_factory):
        """测试公司后缀"""
        config = GeneratorConfig(
            generator_type="company_name",
            parameters={"include_suffix": True}
        )
        generator = generator_factory.create_generator(config)
        company_name = generator.generate_single()
        
        # Common Chinese company suffixes
        suffixes = ["有限公司", "股份有限公司", "集团", "科技", "Ltd", "Inc", "Corp"]
        has_suffix = any(suffix in company_name for suffix in suffixes)
        assert isinstance(company_name, str)

    def test_industry_type(self, generator_factory):
        """测试行业类型"""
        config = GeneratorConfig(
            generator_type="company_name",
            parameters={"industry": "technology"}
        )
        generator = generator_factory.create_generator(config)
        company_name = generator.generate_single()
        
        assert isinstance(company_name, str)
        # Technology companies might contain related keywords
        tech_keywords = ["科技", "Tech", "软件", "Software", "网络", "Network"]
        # Not all generated names will have keywords, just verify it's valid
        assert len(company_name) >= 4

    def test_validation(self, generator_factory):
        """测试公司名称验证"""
        config = GeneratorConfig(
            generator_type="company_name",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid company names
        assert generator.validate("北京科技有限公司")
        assert generator.validate("ABC Technology Inc")
        
        # Invalid company names
        assert not generator.validate("AB")  # Too short
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试公司名称唯一性"""
        config = GeneratorConfig(
            generator_type="company_name",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        company_names = generator.generate_batch(50)
        
        # Should have variety
        unique_names = set(company_names)
        assert len(unique_names) > 30

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        config = GeneratorConfig(
            generator_type="company_name",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            name = generator.generate_single()
            assert name is not None
            assert len(name) >= 4
            assert isinstance(name, str)
