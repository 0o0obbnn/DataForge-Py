"""
MAC地址生成器

生成符合IEEE 802标准的MAC地址，支持多种格式和厂商前缀。
"""

import secrets

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
    GeneratorType,
)


@register_generator("mac_address", aliases=["mac", "mac-address"])
class MACAddressGenerator(DataGenerator[str]):
    """
    MAC地址生成器

    支持功能：
    - 生成符合IEEE 802标准的MAC地址
    - 支持多种格式（冒号分隔、连字符分隔、无分隔符）
    - 支持指定厂商前缀
    - 支持单播/多播、全局/本地管理位控制
    - 内置MAC地址格式校验
    """

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.format = self.parameters.get("format", "colon")  # colon, hyphen, none
        self.vendor_prefix = self.parameters.get("vendor_prefix", None)
        self.unicast = self.parameters.get("unicast", True)  # True=单播, False=多播
        self.global_admin = self.parameters.get(
            "global_admin", True
        )  # True=全局, False=本地

    def _setup(self) -> None:
        """初始化设置"""
        # 常用厂商MAC前缀（OUI）
        self.common_vendor_prefixes = {
            "cisco": "00:1C:58",
            "dell": "00:1A:A0",
            "hp": "00:1A:4B",
            "intel": "00:1B:21",
            "apple": "00:1C:B3",
            "samsung": "00:1E:7D",
            "huawei": "00:1E:10",
            "microsoft": "00:15:5D",
            "vmware": "00:50:56",
            "broadcom": "00:05:B5",
        }

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成原始MAC地址"""
        # 1. 生成或使用指定的厂商前缀
        if self.vendor_prefix:
            prefix = self._get_vendor_prefix()
        else:
            prefix = self._generate_random_prefix()

        # 2. 生成后24位
        suffix = self._generate_suffix()

        # 3. 组合完整的MAC地址
        mac_bytes = prefix + suffix

        # 4. 设置管理位
        mac_bytes = self._set_management_bits(mac_bytes)

        # 5. 格式化输出
        return self._format_mac(mac_bytes)

    def _get_vendor_prefix(self) -> bytes:
        """获取厂商前缀"""
        if isinstance(self.vendor_prefix, str):
            # 如果是字符串，检查是否为已知厂商
            vendor_key = self.vendor_prefix.lower()
            if vendor_key in self.common_vendor_prefixes:
                prefix_str = self.common_vendor_prefixes[vendor_key]
                return bytes.fromhex(prefix_str.replace(":", "").replace("-", ""))
            else:
                # 尝试解析为十六进制字符串
                try:
                    clean_prefix = self.vendor_prefix.replace(":", "").replace("-", "")
                    if len(clean_prefix) == 6:  # 3字节前缀
                        return bytes.fromhex(clean_prefix)
                except ValueError:
                    pass

        # 默认生成随机前缀
        return self._generate_random_prefix()

    def _generate_random_prefix(self) -> bytes:
        """生成随机厂商前缀（3字节）"""
        return bytes([secrets.randbelow(256) for _ in range(3)])

    def _generate_suffix(self) -> bytes:
        """生成后3字节后缀"""
        return bytes([secrets.randbelow(256) for _ in range(3)])

    def _set_management_bits(self, mac_bytes: bytes) -> bytes:
        """设置MAC地址管理位"""
        if len(mac_bytes) != 6:
            return mac_bytes

        # 获取第一个字节
        first_byte = mac_bytes[0]

        # 设置单播/多播位（第0位：0=单播, 1=多播）
        if self.unicast:
            first_byte &= 0xFE  # 清除多播位
        else:
            first_byte |= 0x01  # 设置多播位

        # 设置全局/本地管理位（第1位：0=全局, 1=本地）
        if self.global_admin:
            first_byte &= 0xFD  # 清除本地管理位
        else:
            first_byte |= 0x02  # 设置本地管理位

        # 返回修改后的MAC地址
        return bytes([first_byte]) + mac_bytes[1:]

    def _format_mac(self, mac_bytes: bytes) -> str:
        """格式化MAC地址"""
        hex_str = mac_bytes.hex().upper()

        if self.format == "colon":
            return ":".join(hex_str[i : i + 2] for i in range(0, 12, 2))
        elif self.format == "hyphen":
            return "-".join(hex_str[i : i + 2] for i in range(0, 12, 2))
        elif self.format == "none":
            return hex_str
        else:  # 默认冒号格式
            return ":".join(hex_str[i : i + 2] for i in range(0, 12, 2))

    def validate(self, data: str) -> bool:
        """校验MAC地址格式"""
        if not isinstance(data, str):
            return False

        # 移除分隔符
        clean_mac = data.replace(":", "").replace("-", "")

        # 检查长度
        if len(clean_mac) != 12:
            return False

        # 检查是否为有效的十六进制
        try:
            int(clean_mac, 16)
        except ValueError:
            return False

        return True

    def _validate_management_bits(self, clean_mac: str) -> bool:
        """校验MAC地址管理位"""
        try:
            first_byte = int(clean_mac[:2], 16)

            # 检查单播/多播位
            unicast_bit = first_byte & 0x01
            if self.unicast and unicast_bit != 0:
                return False
            if not self.unicast and unicast_bit != 1:
                return False

            # 检查全局/本地管理位
            local_admin_bit = (first_byte & 0x02) >> 1
            if self.global_admin and local_admin_bit != 0:
                return False
            if not self.global_admin and local_admin_bit != 1:
                return False

        except ValueError:
            return False

        return True

    @property
    def generator_type(self) -> GeneratorType:
        """获取生成器类型"""
        return GeneratorType.NETWORK

    @property
    def supported_parameters(self) -> list[str]:
        """获取支持的参数列表"""
        return [
            "format",  # MAC地址格式：colon, hyphen, none
            "vendor_prefix",  # 厂商前缀：字符串或已知厂商名称
            "unicast",  # 单播/多播：True/False
            "global_admin",  # 全局/本地管理：True/False
            "validate",  # 是否校验
        ]


# 单元测试
if __name__ == "__main__":
    # 测试各种配置
    test_configs = [
        GeneratorConfig("mac_address", {"format": "colon"}),
        GeneratorConfig("mac_address", {"format": "hyphen"}),
        GeneratorConfig("mac_address", {"format": "none"}),
        GeneratorConfig("mac_address", {"vendor_prefix": "intel"}),
        GeneratorConfig("mac_address", {"unicast": False}),
        GeneratorConfig("mac_address", {"global_admin": False}),
    ]

    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    for config in test_configs:
        generator = MACAddressGenerator(config)
        mac = generator.generate_single()
        is_valid = generator.validate(mac)
        logger.info(f"Config: {config.parameters} -> MAC: {mac}, Valid: {is_valid}")
