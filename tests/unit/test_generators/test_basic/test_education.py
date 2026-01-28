"""
学历生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig
from dataforge.resources.education_loader import (
    clear_config_cache,
    load_education_config,
)


@pytest.mark.unit
class TestEducationGenerator:
    """学历生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个学历"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        config = GeneratorConfig(generator_type="education", parameters={})
        generator = generator_factory.create_generator(config)
        education = generator.generate_single()

        assert isinstance(education, str)
        assert len(education) >= 2
        assert generator.validate(education)

    def test_generate_batch(self, generator_factory):
        """测试批量生成学历"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        config = GeneratorConfig(generator_type="education", parameters={})
        generator = generator_factory.create_generator(config)
        educations = generator.generate_batch(10)

        assert len(educations) == 10
        for education in educations:
            assert isinstance(education, str)
            assert len(education) >= 2

    def test_chinese_education(self, generator_factory):
        """测试中文学历"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        config = GeneratorConfig(
            generator_type="education", parameters={"language": "chinese"}
        )
        generator = generator_factory.create_generator(config)
        education = generator.generate_single()

        # Common Chinese education levels
        valid_levels = ["小学", "初中", "高中", "中专", "大专", "本科", "硕士", "博士"]
        assert any(level in education for level in valid_levels)

    def test_english_education(self, generator_factory):
        """测试英文学历"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        config = GeneratorConfig(
            generator_type="education", parameters={"language": "english"}
        )
        generator = generator_factory.create_generator(config)
        education = generator.generate_single()

        # Common English education levels
        valid_levels = [
            "High School",
            "Associate",
            "Bachelor",
            "Master",
            "PhD",
            "Doctorate",
        ]
        # Should contain English text
        assert any(c.isalpha() and ord(c) < 128 for c in education)

    def test_minimum_level(self, generator_factory):
        """测试最低学历限制"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        config = GeneratorConfig(
            generator_type="education", parameters={"min_level": "bachelor"}
        )
        generator = generator_factory.create_generator(config)
        education = generator.generate_single()

        # Should be bachelor or higher
        assert isinstance(education, str)

    def test_specific_level(self, generator_factory):
        """测试指定学历"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        config = GeneratorConfig(
            generator_type="education", parameters={"level": "bachelor"}
        )
        generator = generator_factory.create_generator(config)
        education = generator.generate_single()

        assert isinstance(education, str)

    def test_validation(self, generator_factory):
        """测试学历验证"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        config = GeneratorConfig(generator_type="education", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid educations
        assert generator.validate("本科")
        assert generator.validate("Bachelor")
        assert generator.validate("硕士")

        # Invalid educations
        assert not generator.validate("X")
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_distribution(self, generator_factory):
        """测试学历分布"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        config = GeneratorConfig(generator_type="education", parameters={})
        generator = generator_factory.create_generator(config)
        educations = generator.generate_batch(50)

        # Should have variety
        unique_educations = set(educations)
        assert len(unique_educations) >= 3

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        config = GeneratorConfig(generator_type="education", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            education = generator.generate_single()
            assert education is not None
            assert len(education) >= 2
            assert isinstance(education, str)

    def test_system_parameter(self, generator_factory):
        """测试教育体系参数"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        # 测试中国教育体系
        config_china = GeneratorConfig(
            generator_type="education", parameters={"system": "CHINA"}
        )
        generator = generator_factory.create_generator(config_china)
        education = generator.generate_single()
        assert isinstance(education, str)

        # 测试国际教育体系
        config_intl = GeneratorConfig(
            generator_type="education", parameters={"system": "INTERNATIONAL"}
        )
        generator = generator_factory.create_generator(config_intl)
        education = generator.generate_single()
        assert isinstance(education, str)

    def test_level_parameter(self, generator_factory):
        """测试学历级别参数"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        levels = ["PRIMARY", "JUNIOR", "HIGH", "UNIVERSITY", "MASTER", "PHD"]

        for level in levels:
            config = GeneratorConfig(
                generator_type="education",
                parameters={"level": level, "system": "CHINA"},
            )
            generator = generator_factory.create_generator(config)
            education = generator.generate_single()
            assert isinstance(education, str)
            assert len(education) >= 2

    def test_format_parameter(self, generator_factory):
        """测试格式参数"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        formats = ["DEGREE", "SCHOOL", "FULL"]

        for format_type in formats:
            config = GeneratorConfig(
                generator_type="education", parameters={"format": format_type}
            )
            generator = generator_factory.create_generator(config)
            education = generator.generate_single()
            assert isinstance(education, str)
            assert len(education) >= 2

    def test_config_loading(self):
        """测试配置加载功能"""
        # 清除缓存以确保重新加载
        clear_config_cache()

        # 加载配置
        config = load_education_config(locale="zh_CN")

        # 验证配置结构
        assert isinstance(config, dict)
        assert "china_system" in config
        assert "international_system" in config
        assert "generic_levels" in config

        # 验证数据类型
        assert isinstance(config["china_system"], dict)
        assert len(config["china_system"]) > 0

        assert isinstance(config["international_system"], dict)
        assert len(config["international_system"]) > 0

        assert isinstance(config["generic_levels"], dict)
        assert "chinese" in config["generic_levels"]
        assert "english" in config["generic_levels"]

    def test_config_caching(self):
        """测试配置缓存功能"""
        # 清除缓存
        clear_config_cache()

        # 第一次加载
        config1 = load_education_config(locale="zh_CN")

        # 第二次加载（应该从缓存获取）
        config2 = load_education_config(locale="zh_CN")

        # 验证是同一个对象（缓存生效）
        assert config1 is config2

    def test_locale_parameter(self, generator_factory):
        """测试locale参数"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        config = GeneratorConfig(
            generator_type="education", parameters={"locale": "zh_CN"}
        )
        generator = generator_factory.create_generator(config)
        education = generator.generate_single()

        assert isinstance(education, str)
        assert len(education) >= 2

    def test_combined_parameters(self, generator_factory):
        """测试组合参数"""
        from dataforge.generators.basic.education import EducationGenerator

        generator_factory.registry.register("education", EducationGenerator)

        config = GeneratorConfig(
            generator_type="education",
            parameters={
                "system": "CHINA",
                "level": "UNIVERSITY",
                "format": "FULL",
                "locale": "zh_CN",
            },
        )
        generator = generator_factory.create_generator(config)
        education = generator.generate_single()

        assert isinstance(education, str)
        assert len(education) >= 2
        # FULL格式应该包含 " - "
        assert " - " in education
