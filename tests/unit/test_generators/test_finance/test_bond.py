"""
债券代码生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestBondGenerator:
    """债券代码生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个债券代码"""
        from dataforge.generators.finance.bond import BondCodeGenerator
        generator_factory.registry.register("bond", BondCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="bond",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        bond_code = generator.generate_single()
        
        assert isinstance(bond_code, str)
        assert len(bond_code) >= 6
        assert generator.validate(bond_code)

    def test_generate_batch(self, generator_factory):
        """测试批量生成债券代码"""
        from dataforge.generators.finance.bond import BondCodeGenerator
        generator_factory.registry.register("bond", BondCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="bond",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        bond_codes = generator.generate_batch(10)
        
        assert len(bond_codes) == 10
        for code in bond_codes:
            assert isinstance(code, str)
            assert len(code) >= 6

    def test_government_bond(self, generator_factory):
        """测试国债代码"""
        from dataforge.generators.finance.bond import BondCodeGenerator
        generator_factory.registry.register("bond", BondCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="bond",
            parameters={"bond_type": "government"}
        )
        generator = generator_factory.create_generator(config)
        bond_code = generator.generate_single()
        
        assert isinstance(bond_code, str)
        # Government bonds may start with specific digits
        assert len(bond_code) >= 6

    def test_corporate_bond(self, generator_factory):
        """测试企业债代码"""
        from dataforge.generators.finance.bond import BondCodeGenerator
        generator_factory.registry.register("bond", BondCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="bond",
            parameters={"bond_type": "corporate"}
        )
        generator = generator_factory.create_generator(config)
        bond_code = generator.generate_single()
        
        assert isinstance(bond_code, str)
        assert len(bond_code) >= 6

    def test_market(self, generator_factory):
        """测试市场类型"""
        from dataforge.generators.finance.bond import BondCodeGenerator
        generator_factory.registry.register("bond", BondCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="bond",
            parameters={"market": "shanghai"}
        )
        generator = generator_factory.create_generator(config)
        bond_code = generator.generate_single()
        
        assert isinstance(bond_code, str)

    def test_validation(self, generator_factory):
        """测试债券代码验证"""
        from dataforge.generators.finance.bond import BondCodeGenerator
        generator_factory.registry.register("bond", BondCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="bond",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid bond code
        bond_code = generator.generate_single()
        assert generator.validate(bond_code)
        
        # Invalid bond codes
        assert not generator.validate("123")  # Too short
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试债券代码唯一性"""
        from dataforge.generators.finance.bond import BondCodeGenerator
        generator_factory.registry.register("bond", BondCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="bond",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        codes = generator.generate_batch(50)
        
        # Should have variety
        unique_codes = set(codes)
        assert len(unique_codes) > 30

    def test_format(self, generator_factory):
        """测试代码格式"""
        from dataforge.generators.finance.bond import BondCodeGenerator
        generator_factory.registry.register("bond", BondCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="bond",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        bond_code = generator.generate_single()
        
        # Bond code format: typically 6 digits
        assert len(bond_code) >= 6
        assert bond_code.isdigit()

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.finance.bond import BondCodeGenerator
        generator_factory.registry.register("bond", BondCodeGenerator)
        
        config = GeneratorConfig(
            generator_type="bond",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            code = generator.generate_single()
            assert code is not None
            assert len(code) >= 6
            assert code.isdigit()
