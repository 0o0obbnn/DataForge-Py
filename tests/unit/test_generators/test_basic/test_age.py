"""
年龄生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig
from dataforge.generators.basic.age import AgeGenerator


@pytest.mark.unit
class TestAgeGenerator:
    """年龄生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个年龄"""
        config = GeneratorConfig(
            generator_type="age",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        age = generator.generate_single()
        
        assert isinstance(age, int)
        assert 0 <= age <= 120
        assert generator.validate(age)

    def test_generate_batch(self, generator_factory):
        """测试批量生成年龄"""
        config = GeneratorConfig(
            generator_type="age",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        ages = generator.generate_batch(10)
        
        assert len(ages) == 10
        for age in ages:
            assert isinstance(age, int)
            assert 0 <= age <= 120
            assert generator.validate(age)

    def test_with_min_max_parameters(self, generator_factory):
        """测试带最小最大值参数生成"""
        config = GeneratorConfig(
            generator_type="age",
            parameters={"min": 20, "max": 30}
        )
        generator = generator_factory.create_generator(config)
        age = generator.generate_single()
        
        assert isinstance(age, int)
        assert 20 <= age <= 30
        assert generator.validate(age)

    def test_adult_age_range(self, generator_factory):
        """测试成年人年龄范围"""
        config = GeneratorConfig(
            generator_type="age",
            parameters={"min": 18, "max": 65}
        )
        generator = generator_factory.create_generator(config)
        ages = generator.generate_batch(20)
        
        for age in ages:
            assert 18 <= age <= 65

    def test_child_age_range(self, generator_factory):
        """测试儿童年龄范围"""
        config = GeneratorConfig(
            generator_type="age",
            parameters={"min": 0, "max": 17}
        )
        generator = generator_factory.create_generator(config)
        ages = generator.generate_batch(20)
        
        for age in ages:
            assert 0 <= age <= 17

    def test_elderly_age_range(self, generator_factory):
        """测试老年人年龄范围"""
        config = GeneratorConfig(
            generator_type="age",
            parameters={"min": 60, "max": 100}
        )
        generator = generator_factory.create_generator(config)
        ages = generator.generate_batch(20)
        
        for age in ages:
            assert 60 <= age <= 100

    def test_validation(self, generator_factory):
        """测试年龄验证"""
        config = GeneratorConfig(
            generator_type="age",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid ages
        assert generator.validate(0)
        assert generator.validate(18)
        assert generator.validate(65)
        assert generator.validate(100)
        
        # Invalid ages
        assert not generator.validate(-1)
        assert not generator.validate(150)
        assert not generator.validate("25")
        assert not generator.validate(25.5)

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        # Test minimum age
        config = GeneratorConfig(
            generator_type="age",
            parameters={"min": 0, "max": 0}
        )
        generator = generator_factory.create_generator(config)
        age = generator.generate_single()
        assert age == 0
        
        # Test maximum reasonable age
        config = GeneratorConfig(
            generator_type="age",
            parameters={"min": 120, "max": 120}
        )
        generator = generator_factory.create_generator(config)
        age = generator.generate_single()
        assert age == 120

    def test_distribution(self, generator_factory):
        """测试年龄分布合理性"""
        config = GeneratorConfig(
            generator_type="age",
            parameters={"min": 0, "max": 100}
        )
        generator = generator_factory.create_generator(config)
        ages = generator.generate_batch(100)
        
        # Check distribution covers the range
        assert min(ages) >= 0
        assert max(ages) <= 100
        # Should have some variety
        assert len(set(ages)) > 10
