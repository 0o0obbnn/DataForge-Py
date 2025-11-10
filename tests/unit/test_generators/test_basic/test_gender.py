"""
性别生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig
from dataforge.generators.basic.gender import GenderGenerator


@pytest.mark.unit
class TestGenderGenerator:
    """性别生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个性别"""
        generator_factory.registry.register("gender", GenderGenerator)
        config = GeneratorConfig(
            generator_type="gender",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        gender = generator.generate_single()
        
        assert isinstance(gender, str)
        assert gender in ["Male", "Female", "男", "女"]
        assert generator.validate(gender)

    def test_generate_batch(self, generator_factory):
        """测试批量生成性别"""
        generator_factory.registry.register("gender", GenderGenerator)
        config = GeneratorConfig(
            generator_type="gender",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        genders = generator.generate_batch(20)
        
        assert len(genders) == 20
        for gender in genders:
            assert isinstance(gender, str)
            assert gender in ["Male", "Female", "男", "女"]
            assert generator.validate(gender)

    def test_chinese_format(self, generator_factory):
        """测试中文格式"""
        generator_factory.registry.register("gender", GenderGenerator)
        config = GeneratorConfig(
            generator_type="gender",
            parameters={"format": "chinese"}
        )
        generator = generator_factory.create_generator(config)
        gender = generator.generate_single()
        
        assert gender in ["男", "女"]

    def test_english_format(self, generator_factory):
        """测试英文格式"""
        generator_factory.registry.register("gender", GenderGenerator)
        config = GeneratorConfig(
            generator_type="gender",
            parameters={"format": "english"}
        )
        generator = generator_factory.create_generator(config)
        gender = generator.generate_single()
        
        assert gender in ["Male", "Female"]

    def test_distribution(self, generator_factory):
        """测试性别分布"""
        generator_factory.registry.register("gender", GenderGenerator)
        config = GeneratorConfig(
            generator_type="gender",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        genders = generator.generate_batch(100)
        
        # Should have both genders in 100 samples
        unique_genders = set(genders)
        assert len(unique_genders) >= 2

    def test_validation(self, generator_factory):
        """测试性别验证"""
        generator_factory.registry.register("gender", GenderGenerator)
        config = GeneratorConfig(
            generator_type="gender",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid genders
        assert generator.validate("Male")
        assert generator.validate("Female")
        assert generator.validate("男")
        assert generator.validate("女")
        
        # Invalid genders
        assert not generator.validate("Unknown")
        assert not generator.validate("M")
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        generator_factory.registry.register("gender", GenderGenerator)
        config = GeneratorConfig(
            generator_type="gender",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times to ensure consistency
        for _ in range(10):
            gender = generator.generate_single()
            assert gender is not None
            assert len(gender) > 0
