"""
车牌号生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestLicensePlateGenerator:
    """车牌号生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个车牌号"""
        config = GeneratorConfig(
            generator_type="license_plate",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()
        
        assert isinstance(plate, str)
        assert len(plate) >= 7
        assert generator.validate(plate)

    def test_generate_batch(self, generator_factory):
        """测试批量生成车牌号"""
        config = GeneratorConfig(
            generator_type="license_plate",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        plates = generator.generate_batch(10)
        
        assert len(plates) == 10
        for plate in plates:
            assert isinstance(plate, str)
            assert len(plate) >= 7

    def test_beijing_plate(self, generator_factory):
        """测试北京车牌"""
        config = GeneratorConfig(
            generator_type="license_plate",
            parameters={"province": "京"}
        )
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()
        
        assert plate.startswith("京")

    def test_shanghai_plate(self, generator_factory):
        """测试上海车牌"""
        config = GeneratorConfig(
            generator_type="license_plate",
            parameters={"province": "沪"}
        )
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()
        
        assert plate.startswith("沪")

    def test_new_energy_plate(self, generator_factory):
        """测试新能源车牌"""
        config = GeneratorConfig(
            generator_type="license_plate",
            parameters={"type": "new_energy"}
        )
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()
        
        # New energy plates are 8 characters
        assert isinstance(plate, str)
        assert len(plate) >= 7

    def test_regular_plate_format(self, generator_factory):
        """测试普通车牌格式"""
        config = GeneratorConfig(
            generator_type="license_plate",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()
        
        # Format: 省X12345 (7 chars) or 省X123456 (8 chars for new energy)
        assert len(plate) in [7, 8]
        # First char should be Chinese province
        assert '\u4e00' <= plate[0] <= '\u9fff'

    def test_validation(self, generator_factory):
        """测试车牌号验证"""
        config = GeneratorConfig(
            generator_type="license_plate",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid plates
        assert generator.validate("京A12345")
        assert generator.validate("沪B67890")
        
        # Invalid plates
        assert not generator.validate("AB12345")  # No Chinese char
        assert not generator.validate("京")  # Too short
        assert not generator.validate("")
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试车牌号唯一性"""
        config = GeneratorConfig(
            generator_type="license_plate",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        plates = generator.generate_batch(50)
        
        # Should have high uniqueness
        unique_plates = set(plates)
        assert len(unique_plates) >= 45

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        config = GeneratorConfig(
            generator_type="license_plate",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            plate = generator.generate_single()
            assert plate is not None
            assert len(plate) >= 7
            assert '\u4e00' <= plate[0] <= '\u9fff'
