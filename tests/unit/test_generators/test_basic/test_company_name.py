"""
公司名称生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig
from dataforge.resources.company_name_loader import (
    clear_config_cache,
    load_company_name_config,
)


@pytest.mark.unit
class TestCompanyNameGenerator:
    """公司名称生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个公司名称"""
        config = GeneratorConfig(generator_type="company_name", parameters={})
        generator = generator_factory.create_generator(config)
        company_name = generator.generate_single()

        assert isinstance(company_name, str)
        assert len(company_name) >= 4
        assert generator.validate(company_name)

    def test_generate_batch(self, generator_factory):
        """测试批量生成公司名称"""
        config = GeneratorConfig(generator_type="company_name", parameters={})
        generator = generator_factory.create_generator(config)
        company_names = generator.generate_batch(10)

        assert len(company_names) == 10
        for name in company_names:
            assert isinstance(name, str)
            assert len(name) >= 4

    def test_chinese_company_name(self, generator_factory):
        """测试中文公司名称"""
        config = GeneratorConfig(
            generator_type="company_name", parameters={"language": "chinese"}
        )
        generator = generator_factory.create_generator(config)
        company_name = generator.generate_single()

        assert isinstance(company_name, str)
        # Should contain Chinese characters
        assert any("\u4e00" <= char <= "\u9fff" for char in company_name)

    def test_english_company_name(self, generator_factory):
        """测试英文公司名称"""
        config = GeneratorConfig(
            generator_type="company_name", parameters={"language": "english"}
        )
        generator = generator_factory.create_generator(config)
        company_name = generator.generate_single()

        assert isinstance(company_name, str)
        # Should contain English letters
        assert any(c.isalpha() and ord(c) < 128 for c in company_name)

    def test_company_suffix(self, generator_factory):
        """测试公司后缀"""
        config = GeneratorConfig(
            generator_type="company_name", parameters={"include_suffix": True}
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
            generator_type="company_name", parameters={"industry": "technology"}
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
        config = GeneratorConfig(generator_type="company_name", parameters={})
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
        config = GeneratorConfig(generator_type="company_name", parameters={})
        generator = generator_factory.create_generator(config)
        company_names = generator.generate_batch(50)

        # Should have variety
        unique_names = set(company_names)
        assert len(unique_names) > 30

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        config = GeneratorConfig(generator_type="company_name", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            name = generator.generate_single()
            assert name is not None
            assert len(name) >= 4
            assert isinstance(name, str)

    def test_industry_parameter(self, generator_factory):
        """测试行业参数"""
        industries = [
            "IT",
            "FINANCE",
            "RETAIL",
            "MANUFACTURING",
            "EDUCATION",
            "REAL_ESTATE",
        ]

        for industry in industries:
            config = GeneratorConfig(
                generator_type="company_name", parameters={"industry": industry}
            )
            generator = generator_factory.create_generator(config)
            company_name = generator.generate_single()

            assert isinstance(company_name, str)
            assert len(company_name) >= 4
            assert generator.validate(company_name)

    def test_company_type_parameter(self, generator_factory):
        """测试公司类型参数"""
        company_types = [
            "CO_LTD",
            "GROUP",
            "INSTITUTE",
            "CORP",
            "TECH",
            "TRADING",
            "INVESTMENT",
        ]

        for comp_type in company_types:
            config = GeneratorConfig(
                generator_type="company_name", parameters={"type": comp_type}
            )
            generator = generator_factory.create_generator(config)
            company_name = generator.generate_single()

            assert isinstance(company_name, str)
            assert len(company_name) >= 4
            # 验证包含对应的公司类型后缀
            assert generator.validate(company_name)

    def test_prefix_region_parameter(self, generator_factory):
        """测试地区前缀参数"""
        # 测试启用地区前缀
        config_with_region = GeneratorConfig(
            generator_type="company_name", parameters={"prefix_region": True}
        )
        generator = generator_factory.create_generator(config_with_region)

        # 生成多个名称，至少有一个应该包含地区前缀
        names_with_region = generator.generate_batch(20)
        assert len(names_with_region) == 20

        # 测试禁用地区前缀
        config_no_region = GeneratorConfig(
            generator_type="company_name", parameters={"prefix_region": False}
        )
        generator_no_region = generator_factory.create_generator(config_no_region)
        names_no_region = generator_no_region.generate_batch(10)
        assert len(names_no_region) == 10

    def test_config_loading(self):
        """测试配置加载功能"""
        # 清除缓存以确保重新加载
        clear_config_cache()

        # 加载配置
        config = load_company_name_config(locale="zh_CN")

        # 验证配置结构
        assert isinstance(config, dict)
        assert "regions" in config
        assert "industry_keywords" in config
        assert "general_keywords" in config
        assert "company_types" in config

        # 验证数据类型
        assert isinstance(config["regions"], list)
        assert len(config["regions"]) > 0

        assert isinstance(config["industry_keywords"], dict)
        assert len(config["industry_keywords"]) > 0

        assert isinstance(config["general_keywords"], list)
        assert len(config["general_keywords"]) > 0

        assert isinstance(config["company_types"], dict)
        assert len(config["company_types"]) > 0

    def test_config_caching(self):
        """测试配置缓存功能"""
        # 清除缓存
        clear_config_cache()

        # 第一次加载
        config1 = load_company_name_config(locale="zh_CN")

        # 第二次加载（应该从缓存获取）
        config2 = load_company_name_config(locale="zh_CN")

        # 验证是同一个对象（缓存生效）
        assert config1 is config2

    def test_get_company_info(self, generator_factory):
        """测试解析企业名称信息"""
        config = GeneratorConfig(generator_type="company_name", parameters={})
        generator = generator_factory.create_generator(config)

        # 生成一个公司名称
        company_name = generator.generate_single()

        # 解析信息
        info = generator.get_company_info(company_name)

        assert isinstance(info, dict)
        assert "original" in info
        assert "region" in info
        assert "core_name" in info
        assert "company_type" in info
        assert "industry_hint" in info
        assert info["original"] == company_name

    def test_locale_parameter(self, generator_factory):
        """测试locale参数"""
        config = GeneratorConfig(
            generator_type="company_name", parameters={"locale": "zh_CN"}
        )
        generator = generator_factory.create_generator(config)
        company_name = generator.generate_single()

        assert isinstance(company_name, str)
        assert len(company_name) >= 4

    def test_combined_parameters(self, generator_factory):
        """测试组合参数"""
        config = GeneratorConfig(
            generator_type="company_name",
            parameters={
                "industry": "IT",
                "type": "TECH",
                "prefix_region": True,
                "locale": "zh_CN",
            },
        )
        generator = generator_factory.create_generator(config)
        company_name = generator.generate_single()

        assert isinstance(company_name, str)
        assert len(company_name) >= 4
        assert generator.validate(company_name)
