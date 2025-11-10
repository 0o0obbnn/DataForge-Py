"""
网络生成器测试模块

测试所有网络相关数据生成器的功能和性能
"""
import pytest

from dataforge.core.generator import GeneratorConfig
from dataforge.generators.network import (
    GenericDeviceIDGenerator,
    GenericDomainGenerator,
    GenericGeoCoordinatesGenerator,
    GenericHTTPHeaderGenerator,
    GenericIPAddressGenerator,
    GenericMACAddressGenerator,
    GenericPortNumberGenerator,
    GenericSessionTokenGenerator,
    GenericTimezoneGenerator,
)


class TestNetworkGenerators:
    """网络生成器测试类"""

    def test_ip_address_generator(self):
        """测试IP地址生成器"""
        config = GeneratorConfig(
            generator_type="ip_address",
            parameters={"version": "v4", "validate": True}
        )
        generator = GenericIPAddressGenerator(config)

        # 测试单次生成
        result = generator.generate_single()
        assert isinstance(result, str)
        assert generator.validate(result)

        # 测试批量生成
        results = generator.generate_batch(5)
        assert len(results) == 5
        assert all(generator.validate(ip) for ip in results)

    def test_mac_address_generator(self):
        """测试MAC地址生成器"""
        config = GeneratorConfig(
            generator_type="mac_address",
            parameters={"format": "colon", "validate": True}
        )
        generator = GenericMACAddressGenerator(config)

        result = generator.generate_single()
        assert isinstance(result, str)
        assert generator.validate(result)

        # 测试不同格式
        config_hyphen = GeneratorConfig(
            generator_type="mac_address",
            parameters={"format": "hyphen", "validate": True}
        )
        generator_hyphen = GenericMACAddressGenerator(config_hyphen)
        result_hyphen = generator_hyphen.generate_single()
        assert "-" in result_hyphen

    def test_domain_generator(self):
        """测试域名生成器"""
        config = GeneratorConfig(
            generator_type="domain",
            parameters={"custom_tlds": [".com"], "validate": True}
        )
        generator = GenericDomainGenerator(config)

        result = generator.generate_single()
        assert isinstance(result, str)
        assert result.endswith(".com")
        assert generator.validate(result)

    def test_port_number_generator(self):
        """测试端口号生成器"""
        config = GeneratorConfig(
            generator_type="port_number",
            parameters={"port_type": "well_known", "validate": True}
        )
        generator = GenericPortNumberGenerator(config)

        result = generator.generate_single()
        assert isinstance(result, int)
        assert 0 <= result <= 65535
        assert generator.validate(result)

    def test_http_header_generator(self):
        """测试HTTP头生成器"""
        config = GeneratorConfig(
            generator_type="http_header",
            parameters={"header_type": "request", "validate": True}
        )
        generator = GenericHTTPHeaderGenerator(config)

        result = generator.generate_single()
        assert isinstance(result, dict)
        assert all(isinstance(k, str) and isinstance(v, str) for k, v in result.items())
        assert generator.validate(result)

    def test_session_token_generator(self):
        """测试会话令牌生成器"""
        config = GeneratorConfig(
            generator_type="session_token",
            parameters={"token_type": "UUID", "validate": True}
        )
        generator = GenericSessionTokenGenerator(config)

        result = generator.generate_single()
        assert isinstance(result, str)
        assert len(result) >= 32
        assert generator.validate(result)

    def test_device_id_generator(self):
        """测试设备ID生成器"""
        config = GeneratorConfig(
            generator_type="device_id",
            parameters={"device_type": "IMEI", "validate": True}
        )
        generator = GenericDeviceIDGenerator(config)

        result = generator.generate_single()
        assert isinstance(result, str)
        assert len(result) >= 15
        assert generator.validate(result)

    def test_geo_coordinates_generator(self):
        """测试地理坐标生成器"""
        config = GeneratorConfig(
            generator_type="geo_coordinates",
            parameters={"format": "decimal", "validate": True}
        )
        generator = GenericGeoCoordinatesGenerator(config)

        result = generator.generate_single()
        assert isinstance(result, str)
        # 检查坐标格式
        assert "," in result
        lat, lon = map(float, result.split(","))
        assert -90 <= lat <= 90
        assert -180 <= lon <= 180
        assert generator.validate(result)

    def test_timezone_generator(self):
        """测试时区生成器"""
        config = GeneratorConfig(
            generator_type="timezone",
            parameters={"format": "iana", "validate": True}
        )
        generator = GenericTimezoneGenerator(config)

        result = generator.generate_single()
        assert isinstance(result, str)
        assert generator.validate(result)

    def test_network_generators_performance(self):
        """测试网络生成器性能"""
        generators = [
            (GenericIPAddressGenerator, {"version": "v4"}),
            (GenericMACAddressGenerator, {"format": "colon"}),
            (GenericDomainGenerator, {"tld": "com"}),
            (GenericPortNumberGenerator, {"port_type": "well_known"}),
        ]

        for gen_class, params in generators:
            config = GeneratorConfig(
                generator_type=gen_class.__name__.lower().replace("generic", "").replace("generator", ""),
                parameters=params
            )
            generator = gen_class(config)

            # 测试批量生成性能
            import time
            start_time = time.time()
            results = generator.generate_batch(100)
            end_time = time.time()

            assert len(results) == 100
            assert all(generator.validate(result) for result in results)
            assert end_time - start_time < 1.0  # 100个应该在1秒内完成

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
