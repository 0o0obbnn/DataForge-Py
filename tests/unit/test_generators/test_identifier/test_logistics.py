"""
物流单号生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestLogisticsGenerator:
    """物流单号生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个物流单号"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(generator_type="logistics", parameters={})
        generator = generator_factory.create_generator(config)
        logistics_info = generator.generate_single()

        # 生成器返回字典，包含完整的物流信息
        assert isinstance(logistics_info, dict)
        assert "tracking_number" in logistics_info
        tracking_number = logistics_info["tracking_number"]
        assert isinstance(tracking_number, str)
        assert len(tracking_number) >= 10
        assert generator.validate(logistics_info)

    def test_generate_batch(self, generator_factory):
        """测试批量生成物流单号"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(generator_type="logistics", parameters={})
        generator = generator_factory.create_generator(config)
        logistics_list = generator.generate_batch(10)

        assert len(logistics_list) == 10
        for info in logistics_list:
            assert isinstance(info, dict)
            assert "tracking_number" in info
            tracking_number = info["tracking_number"]
            assert isinstance(tracking_number, str)
            assert len(tracking_number) >= 10

    def test_sf_express(self, generator_factory):
        """测试顺丰快递单号"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(
            generator_type="logistics", parameters={"carrier": "sf_express"}
        )
        generator = generator_factory.create_generator(config)
        logistics_info = generator.generate_single()

        # 返回字典格式
        assert isinstance(logistics_info, dict)
        assert "tracking_number" in logistics_info
        tracking_number = logistics_info["tracking_number"]
        # SF Express format: 12 digits
        assert isinstance(tracking_number, str)
        assert len(tracking_number) >= 10

    def test_ems(self, generator_factory):
        """测试EMS单号"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(
            generator_type="logistics", parameters={"carrier": "ems"}
        )
        generator = generator_factory.create_generator(config)
        logistics_info = generator.generate_single()

        assert isinstance(logistics_info, dict)
        assert "tracking_number" in logistics_info
        tracking_number = logistics_info["tracking_number"]
        # EMS format: 13 characters (2 letters + 9 digits + 2 letters)
        assert isinstance(tracking_number, str)

    def test_yto_express(self, generator_factory):
        """测试圆通快递单号"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(
            generator_type="logistics", parameters={"carrier": "yto"}
        )
        generator = generator_factory.create_generator(config)
        logistics_info = generator.generate_single()

        assert isinstance(logistics_info, dict)
        assert "tracking_number" in logistics_info
        tracking_number = logistics_info["tracking_number"]
        assert isinstance(tracking_number, str)
        assert len(tracking_number) >= 10

    def test_validation(self, generator_factory):
        """测试物流单号验证"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(generator_type="logistics", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid tracking number
        logistics_info = generator.generate_single()
        assert generator.validate(logistics_info)

        # Invalid tracking numbers
        assert not generator.validate({"tracking_number": "123"})  # Too short
        assert not generator.validate({})  # Missing tracking_number
        assert not generator.validate("")  # Not a dict
        assert not generator.validate(123)  # Not a dict

    def test_uniqueness(self, generator_factory):
        """测试物流单号唯一性"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(generator_type="logistics", parameters={})
        generator = generator_factory.create_generator(config)
        logistics_list = generator.generate_batch(50)

        # All tracking numbers should be unique
        unique_numbers = {info["tracking_number"] for info in logistics_list}
        assert len(unique_numbers) == 50

    def test_format(self, generator_factory):
        """测试单号格式"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(generator_type="logistics", parameters={})
        generator = generator_factory.create_generator(config)
        logistics_info = generator.generate_single()

        # tracking_number 应该是字母数字
        tracking_number = logistics_info["tracking_number"]
        assert tracking_number.isalnum()

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.identifier.logistics import LogisticsGenerator

        generator_factory.registry.register("logistics", LogisticsGenerator)

        config = GeneratorConfig(generator_type="logistics", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            logistics_info = generator.generate_single()
            assert logistics_info is not None
            assert isinstance(logistics_info, dict)
            assert "tracking_number" in logistics_info
            tracking_number = logistics_info["tracking_number"]
            assert len(tracking_number) >= 10
            assert tracking_number.isalnum()
