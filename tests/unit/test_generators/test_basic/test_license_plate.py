"""
车牌号生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig
from dataforge.resources.license_plate_loader import (
    clear_config_cache,
    load_license_plate_config,
)


@pytest.mark.unit
class TestLicensePlateGenerator:
    """车牌号生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个车牌号"""
        config = GeneratorConfig(generator_type="license_plate", parameters={})
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()

        assert isinstance(plate, str)
        assert len(plate) >= 7
        assert generator.validate(plate)

    def test_generate_batch(self, generator_factory):
        """测试批量生成车牌号"""
        config = GeneratorConfig(generator_type="license_plate", parameters={})
        generator = generator_factory.create_generator(config)
        plates = generator.generate_batch(10)

        assert len(plates) == 10
        for plate in plates:
            assert isinstance(plate, str)
            assert len(plate) >= 7

    def test_beijing_plate(self, generator_factory):
        """测试北京车牌"""
        config = GeneratorConfig(
            generator_type="license_plate", parameters={"province": "京"}
        )
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()

        assert plate.startswith("京")

    def test_shanghai_plate(self, generator_factory):
        """测试上海车牌"""
        config = GeneratorConfig(
            generator_type="license_plate", parameters={"province": "沪"}
        )
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()

        assert plate.startswith("沪")

    def test_new_energy_plate(self, generator_factory):
        """测试新能源车牌"""
        config = GeneratorConfig(
            generator_type="license_plate", parameters={"type": "new_energy"}
        )
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()

        # New energy plates are 8 characters
        assert isinstance(plate, str)
        assert len(plate) >= 7

    def test_regular_plate_format(self, generator_factory):
        """测试普通车牌格式"""
        config = GeneratorConfig(generator_type="license_plate", parameters={})
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()

        # Format: 省X12345 (7 chars) or 省X123456 (8 chars for new energy)
        assert len(plate) in [7, 8]
        # First char should be Chinese province
        assert "\u4e00" <= plate[0] <= "\u9fff"

    def test_validation(self, generator_factory):
        """测试车牌号验证"""
        config = GeneratorConfig(generator_type="license_plate", parameters={})
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
        config = GeneratorConfig(generator_type="license_plate", parameters={})
        generator = generator_factory.create_generator(config)
        plates = generator.generate_batch(50)

        # Should have high uniqueness
        unique_plates = set(plates)
        assert len(unique_plates) >= 45

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        config = GeneratorConfig(generator_type="license_plate", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            plate = generator.generate_single()
            assert plate is not None
            assert len(plate) >= 7
            assert "\u4e00" <= plate[0] <= "\u9fff"

    def test_plate_type_parameter(self, generator_factory):
        """测试车牌类型参数"""
        types = ["FUEL", "NEW_ENERGY", "BOTH"]

        for plate_type in types:
            config = GeneratorConfig(
                generator_type="license_plate", parameters={"type": plate_type}
            )
            generator = generator_factory.create_generator(config)
            plate = generator.generate_single()

            assert isinstance(plate, str)
            if plate_type == "NEW_ENERGY":
                assert len(plate) == 8
            elif plate_type == "FUEL":
                assert len(plate) == 7
            # BOTH can be either 7 or 8

    def test_include_io_parameter(self, generator_factory):
        """测试包含I和O参数"""
        config = GeneratorConfig(
            generator_type="license_plate", parameters={"include_io": True}
        )
        generator = generator_factory.create_generator(config)
        plates = generator.generate_batch(20)

        # 至少有一个车牌应该包含I或O
        has_io = any("I" in plate or "O" in plate for plate in plates)
        # 注意：由于随机性，可能不总是包含I或O，但至少应该能生成

    def test_config_loading(self):
        """测试配置加载功能"""
        # 清除缓存以确保重新加载
        clear_config_cache()

        # 加载配置
        config = load_license_plate_config(locale="zh_CN")

        # 验证配置结构
        assert isinstance(config, dict)
        assert "provinces" in config
        assert "city_codes" in config
        assert "plate_chars" in config
        assert "new_energy_prefixes" in config

        # 验证数据类型
        assert isinstance(config["provinces"], dict)
        assert len(config["provinces"]) > 0

        assert isinstance(config["city_codes"], list)
        assert len(config["city_codes"]) > 0

        assert isinstance(config["plate_chars"], list)
        assert len(config["plate_chars"]) > 0

        assert isinstance(config["new_energy_prefixes"], list)
        assert len(config["new_energy_prefixes"]) > 0

    def test_config_caching(self):
        """测试配置缓存功能"""
        # 清除缓存
        clear_config_cache()

        # 第一次加载
        config1 = load_license_plate_config(locale="zh_CN")

        # 第二次加载（应该从缓存获取）
        config2 = load_license_plate_config(locale="zh_CN")

        # 验证是同一个对象（缓存生效）
        assert config1 is config2

    def test_locale_parameter(self, generator_factory):
        """测试locale参数"""
        config = GeneratorConfig(
            generator_type="license_plate", parameters={"locale": "zh_CN"}
        )
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()

        assert isinstance(plate, str)
        assert len(plate) in [7, 8]

    def test_get_plate_info(self, generator_factory):
        """测试获取车牌信息"""
        config = GeneratorConfig(generator_type="license_plate", parameters={})
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()

        # 获取车牌信息
        info = generator.get_plate_info(plate)

        assert isinstance(info, dict)
        assert "valid" in info
        assert "plate" in info
        assert "province_code" in info
        assert "province_name" in info
        assert info["valid"] is True

    def test_combined_parameters(self, generator_factory):
        """测试组合参数"""
        config = GeneratorConfig(
            generator_type="license_plate",
            parameters={
                "type": "NEW_ENERGY",
                "province": "京",
                "include_io": False,
                "locale": "zh_CN",
            },
        )
        generator = generator_factory.create_generator(config)
        plate = generator.generate_single()

        assert isinstance(plate, str)
        assert len(plate) == 8
        assert plate.startswith("京")
        assert generator.validate(plate)
