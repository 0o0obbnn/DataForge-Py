"""
地理坐标生成器模块
支持生成各种地理坐标格式
"""

import random
from typing import Optional

from ...core.context import GenerationContext
from ...core.factory import register_generator
from ...core.generator import DataGenerator, GeneratorConfig
from ...core.protocols import Validator
from ...core.types import GeneratorType


class GeoCoordinatesValidator(Validator):
    """Validator for geographical coordinates."""

    def __init__(self, format: str = "decimal", include_altitude: bool = False):
        self.format = format
        self.include_altitude = include_altitude

    def validate(self, data: str) -> bool:
        """验证地理坐标格式"""
        if not data or not isinstance(data, str):
            return False

        try:
            if self.format == "decimal":
                parts = data.split(",")
                if len(parts) not in [2, 3]:
                    return False

                lat = float(parts[0])
                lon = float(parts[1])

                if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    return False

                if len(parts) == 3 and self.include_altitude:
                    float(parts[2])  # 验证海拔

            elif self.format == "dms":
                # 简化的DMS格式验证
                if not any(char in data for char in ["°", "'", '"']):
                    return False

            elif self.format == "utm":
                # 简化的UTM格式验证
                parts = data.split()
                if len(parts) != 3:
                    return False

                zone = parts[0]
                if len(zone) < 2 or not zone[:-1].isdigit() or zone[-1] not in "NnSs":
                    return False

                int(parts[1])  # 东距
                int(parts[2])  # 北距

        except (ValueError, IndexError):
            return False

        return True

    @property
    def error_message(self) -> str:
        return "Invalid geographical coordinate format"


@register_generator("geo_coordinates", aliases=["geo", "coordinates", "location"])
class GeoCoordinatesGenerator(DataGenerator[str]):
    """地理坐标生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.format = "decimal"
        self.precision = 6
        self.region = "global"
        self.include_altitude = False
        self.altitude_range = (-100, 5000)
        self.validator = None

        # 区域边界定义
        self.region_bounds = {
            "global": ((-90, 90), (-180, 180)),
            "china": ((18.0, 53.5), (73.5, 135.0)),
            "us": ((24.5, 49.5), (-125.0, -66.5)),
            "europe": ((35.0, 71.0), (-25.0, 40.0)),
            "asia": ((10.0, 55.0), (60.0, 150.0)),
        }

        # 区域边界定义
        self.region_bounds = {
            "global": ((-90, 90), (-180, 180)),
            "china": ((18.0, 53.5), (73.5, 135.0)),
            "us": ((24.5, 49.5), (-125.0, -66.5)),
            "europe": ((35.0, 71.0), (-25.0, 40.0)),
            "asia": ((10.0, 55.0), (60.0, 150.0)),
        }

    def _setup(self) -> None:
        """配置生成器参数"""
        self.format = self.parameters.get("format", "decimal")
        self.precision = self.parameters.get("precision", 6)
        self.region = self.parameters.get("region", "global")
        self.include_altitude = self.parameters.get("include_altitude", False)
        self.altitude_range = self.parameters.get("altitude_range", (-100, 5000))
        self.include_dst = self.parameters.get("include_dst", False)
        self.output_format = self.parameters.get("output_format", "decimal")
        self.validator = GeoCoordinatesValidator(self.format, self.include_altitude)

    def generate(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始地理坐标"""
        lat, lon = self._generate_coordinates()

        if self.output_format == "dict":
            # 将字典转换为字符串格式以匹配基类返回类型
            return f"{{'lat': {lat}, 'lng': {lon}}}"
        elif self.output_format == "dms":
            return self._format_dms(lat, lon)
        elif self.output_format == "utm":
            return self._format_utm(lat, lon)
        else:  # decimal (default)
            return self._format_decimal(lat, lon)

    def _generate_coordinates(self) -> tuple[float, float]:
        """生成随机坐标"""
        lat_bounds, lon_bounds = self.region_bounds[self.region]

        latitude = round(random.uniform(lat_bounds[0], lat_bounds[1]), self.precision)
        longitude = round(random.uniform(lon_bounds[0], lon_bounds[1]), self.precision)

        return latitude, longitude

    def _format_decimal(self, lat: float, lon: float) -> str:
        """格式化为十进制坐标"""
        lat_str = f"{lat:.{self.precision}f}"
        lon_str = f"{lon:.{self.precision}f}"
        return f"{lat_str},{lon_str}"

    def _format_dms(self, lat: float, lon: float) -> str:
        """格式化为度分秒坐标"""

        def decimal_to_dms(decimal: float, is_latitude: bool) -> str:
            degrees = int(abs(decimal))
            minutes_decimal = (abs(decimal) - degrees) * 60
            minutes = int(minutes_decimal)
            seconds = (minutes_decimal - minutes) * 60

            direction = (
                "N"
                if is_latitude and decimal >= 0
                else "S" if is_latitude else "E" if decimal >= 0 else "W"
            )
            return f"{degrees}°{minutes}'{seconds:.2f}\" {direction}"

        lat_dms = decimal_to_dms(lat, True)
        lon_dms = decimal_to_dms(lon, False)
        return f"{lat_dms} {lon_dms}"

    def _format_utm(self, lat: float, lon: float) -> str:
        """格式化为UTM坐标（简化版）"""
        # 简化的UTM区域计算
        zone_number = int((lon + 180) / 6) + 1
        zone_letter = "N" if lat >= 0 else "S"

        # 简化的东距和北距计算
        easting = int((lon + 180) * 100000) % 1000000
        northing = int((lat + 90) * 100000) % 10000000

        return f"{zone_number}{zone_letter} {easting} {northing}"

    def get_coordinate_info(self, value: str) -> dict:
        """获取坐标信息"""
        info = {
            "format": self.format,
            "precision": self.precision,
            "region": self.region,
            "include_altitude": self.include_altitude,
        }

        if self.format == "decimal" and "," in value:
            parts = value.split(",")
            if len(parts) >= 2:
                try:
                    info["latitude"] = float(parts[0])
                    info["longitude"] = float(parts[1])
                    if len(parts) >= 3:
                        info["altitude"] = float(parts[2])
                except ValueError:
                    pass

        return info

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.NETWORK

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["altitude_range", "format", "include_altitude", "precision", "region"]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class GenericGeoCoordinatesGenerator(GeoCoordinatesGenerator):
    """通用地理坐标生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        # 确保 validator 被正确初始化
        self.validator = GeoCoordinatesValidator(self.format, self.include_altitude)

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.NETWORK

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return [
            "format",
            "precision",
            "region",
            "include_altitude",
            "altitude_range",
        ]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if self.validator is not None and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True
