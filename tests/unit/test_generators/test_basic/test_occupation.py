"""
职业生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig
from dataforge.resources.occupation_loader import (
    clear_config_cache,
    load_occupation_config,
)


@pytest.mark.unit
class TestOccupationGenerator:
    """职业生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个职业"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(generator_type="occupation", parameters={})
        generator = generator_factory.create_generator(config)
        occupation = generator.generate_single()

        assert isinstance(occupation, str)
        assert len(occupation) >= 2
        assert generator.validate(occupation)

    def test_generate_batch(self, generator_factory):
        """测试批量生成职业"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(generator_type="occupation", parameters={})
        generator = generator_factory.create_generator(config)
        occupations = generator.generate_batch(10)

        assert len(occupations) == 10
        for occupation in occupations:
            assert isinstance(occupation, str)
            assert len(occupation) >= 2

    def test_chinese_occupation(self, generator_factory):
        """测试中文职业"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(
            generator_type="occupation", parameters={"language": "chinese"}
        )
        generator = generator_factory.create_generator(config)
        occupation = generator.generate_single()

        # Should contain Chinese characters
        assert any("\u4e00" <= char <= "\u9fff" for char in occupation)

    def test_english_occupation(self, generator_factory):
        """测试英文职业"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(
            generator_type="occupation", parameters={"language": "english"}
        )
        generator = generator_factory.create_generator(config)
        occupation = generator.generate_single()

        # Should contain English letters
        assert any(c.isalpha() and ord(c) < 128 for c in occupation)

    def test_industry_filter(self, generator_factory):
        """测试行业筛选"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(
            generator_type="occupation", parameters={"industry": "technology"}
        )
        generator = generator_factory.create_generator(config)
        occupation = generator.generate_single()

        assert isinstance(occupation, str)
        # Technology occupations might include: 工程师, 程序员, Developer, etc.

    def test_level_filter(self, generator_factory):
        """测试职级筛选"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(
            generator_type="occupation", parameters={"level": "senior"}
        )
        generator = generator_factory.create_generator(config)
        occupation = generator.generate_single()

        assert isinstance(occupation, str)

    def test_validation(self, generator_factory):
        """测试职业验证"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(generator_type="occupation", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid occupations
        assert generator.validate("软件工程师")
        assert generator.validate("Software Engineer")
        assert generator.validate("医生")

        # Invalid occupations
        assert not generator.validate("A")  # Too short
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_variety(self, generator_factory):
        """测试职业多样性"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(generator_type="occupation", parameters={})
        generator = generator_factory.create_generator(config)
        occupations = generator.generate_batch(50)

        # Should have variety
        unique_occupations = set(occupations)
        assert len(unique_occupations) > 20

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(generator_type="occupation", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            occupation = generator.generate_single()
            assert occupation is not None
            assert len(occupation) >= 2
            assert isinstance(occupation, str)

    def test_industry_parameter(self, generator_factory):
        """测试行业参数"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        industries = [
            "IT",
            "FINANCE",
            "RETAIL",
            "MANUFACTURING",
            "EDUCATION",
            "MEDICAL",
            "MEDIA",
        ]

        for industry in industries:
            config = GeneratorConfig(
                generator_type="occupation", parameters={"industry": industry}
            )
            generator = generator_factory.create_generator(config)
            occupation = generator.generate_single()

            assert isinstance(occupation, str)
            assert len(occupation) >= 2
            assert generator.validate(occupation)

    def test_level_parameter(self, generator_factory):
        """测试级别参数"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        levels = ["SENIOR", "MIDDLE", "JUNIOR", "INTERN"]

        for level in levels:
            config = GeneratorConfig(
                generator_type="occupation", parameters={"level": level}
            )
            generator = generator_factory.create_generator(config)
            occupation = generator.generate_single()

            assert isinstance(occupation, str)
            assert len(occupation) >= 2

    def test_department_parameter(self, generator_factory):
        """测试部门参数"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(
            generator_type="occupation",
            parameters={"industry": "IT", "department": True},
        )
        generator = generator_factory.create_generator(config)
        occupation = generator.generate_single()

        assert isinstance(occupation, str)
        # 可能包含部门前缀
        assert len(occupation) >= 2

    def test_config_loading(self):
        """测试配置加载功能"""
        # 清除缓存以确保重新加载
        clear_config_cache()

        # 加载配置
        config = load_occupation_config(locale="zh_CN")

        # 验证配置结构
        assert isinstance(config, dict)
        assert "industries" in config
        assert "generic_positions" in config
        assert "translations" in config
        assert "common_keywords" in config

        # 验证数据类型
        assert isinstance(config["industries"], dict)
        assert len(config["industries"]) > 0

        assert isinstance(config["generic_positions"], dict)
        assert len(config["generic_positions"]) > 0

        assert isinstance(config["translations"], dict)
        assert len(config["translations"]) > 0

        assert isinstance(config["common_keywords"], list)
        assert len(config["common_keywords"]) > 0

    def test_config_caching(self):
        """测试配置缓存功能"""
        # 清除缓存
        clear_config_cache()

        # 第一次加载
        config1 = load_occupation_config(locale="zh_CN")

        # 第二次加载（应该从缓存获取）
        config2 = load_occupation_config(locale="zh_CN")

        # 验证是同一个对象（缓存生效）
        assert config1 is config2

    def test_locale_parameter(self, generator_factory):
        """测试locale参数"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(
            generator_type="occupation", parameters={"locale": "zh_CN"}
        )
        generator = generator_factory.create_generator(config)
        occupation = generator.generate_single()

        assert isinstance(occupation, str)
        assert len(occupation) >= 2

    def test_translation_functionality(self, generator_factory):
        """测试翻译功能"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(
            generator_type="occupation", parameters={"format": "ENGLISH"}
        )
        generator = generator_factory.create_generator(config)
        occupation = generator.generate_single()

        assert isinstance(occupation, str)
        # 英文职位应该包含英文字母
        assert any(c.isalpha() and ord(c) < 128 for c in occupation)

    def test_combined_parameters(self, generator_factory):
        """测试组合参数"""
        from dataforge.generators.basic.occupation import OccupationGenerator

        generator_factory.registry.register("occupation", OccupationGenerator)

        config = GeneratorConfig(
            generator_type="occupation",
            parameters={
                "industry": "IT",
                "level": "SENIOR",
                "department": True,
                "locale": "zh_CN",
            },
        )
        generator = generator_factory.create_generator(config)
        occupation = generator.generate_single()

        assert isinstance(occupation, str)
        assert len(occupation) >= 2
        assert generator.validate(occupation)
