"""
职业生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestOccupationGenerator:
    """职业生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个职业"""
        from dataforge.generators.basic.occupation import OccupationGenerator
        generator_factory.registry.register("occupation", OccupationGenerator)
        
        config = GeneratorConfig(
            generator_type="occupation",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        occupation = generator.generate_single()
        
        assert isinstance(occupation, str)
        assert len(occupation) >= 2
        assert generator.validate(occupation)

    def test_generate_batch(self, generator_factory):
        """测试批量生成职业"""
        from dataforge.generators.basic.occupation import OccupationGenerator
        generator_factory.registry.register("occupation", OccupationGenerator)
        
        config = GeneratorConfig(
            generator_type="occupation",
            parameters={}
        )
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
            generator_type="occupation",
            parameters={"language": "chinese"}
        )
        generator = generator_factory.create_generator(config)
        occupation = generator.generate_single()
        
        # Should contain Chinese characters
        assert any('\u4e00' <= char <= '\u9fff' for char in occupation)

    def test_english_occupation(self, generator_factory):
        """测试英文职业"""
        from dataforge.generators.basic.occupation import OccupationGenerator
        generator_factory.registry.register("occupation", OccupationGenerator)
        
        config = GeneratorConfig(
            generator_type="occupation",
            parameters={"language": "english"}
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
            generator_type="occupation",
            parameters={"industry": "technology"}
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
            generator_type="occupation",
            parameters={"level": "senior"}
        )
        generator = generator_factory.create_generator(config)
        occupation = generator.generate_single()
        
        assert isinstance(occupation, str)

    def test_validation(self, generator_factory):
        """测试职业验证"""
        from dataforge.generators.basic.occupation import OccupationGenerator
        generator_factory.registry.register("occupation", OccupationGenerator)
        
        config = GeneratorConfig(
            generator_type="occupation",
            parameters={}
        )
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
        
        config = GeneratorConfig(
            generator_type="occupation",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        occupations = generator.generate_batch(50)
        
        # Should have variety
        unique_occupations = set(occupations)
        assert len(unique_occupations) > 20

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.basic.occupation import OccupationGenerator
        generator_factory.registry.register("occupation", OccupationGenerator)
        
        config = GeneratorConfig(
            generator_type="occupation",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            occupation = generator.generate_single()
            assert occupation is not None
            assert len(occupation) >= 2
            assert isinstance(occupation, str)
