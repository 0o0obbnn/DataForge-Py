from ...core.types import GeneratorType

"""网络/设备类生成器"""

import random  # TODO: Convert to secrets
import secrets
import re
import socket
import struct
from typing import Any, Optional

from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
)
from ...core.protocols import Validator

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary



class IPAddressValidator(Validator):
    """Validator for IP addresses."""

    def __init__(self, version: int = 4):
        self.version = version

    def validate(self, data: str) -> bool:
        """校验IP地址"""
        if not isinstance(data, str):
            return False

        try:
            if self.version == 6:
                socket.inet_pton(socket.AF_INET6, data)
            else:
                socket.inet_pton(socket.AF_INET, data)
            return True
        except OSError:
            return False

    @property
    def error_message(self) -> str:
        return "Invalid IP address format"


class IPAddressGenerator(DataGenerator[str]):
    """IP地址生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.version = self.parameters.get("version", 4)  # 4 or 6
        self.ip_type = self.parameters.get(
            "type", "PUBLIC"
        )  # PUBLIC, PRIVATE, LOOPBACK, MULTICAST
        self.subnet = self.parameters.get("subnet", None)  # 指定子网
        self.format_style = self.parameters.get(
            "format", "STANDARD"
        )  # STANDARD, COMPRESSED (IPv6)
        self.validator = IPAddressValidator(self.version)

        # IPv4私有地址范围
        self.ipv4_private_ranges = [
            ("10.0.0.0", "10.255.255.255"),  # Class A
            ("172.16.0.0", "172.31.255.255"),  # Class B
            ("192.168.0.0", "192.168.255.255"),  # Class C
        ]

        # IPv6私有地址前缀
        self.ipv6_private_prefixes = [
            "fc00::",
            "fd00::",
            "fe80::",  # ULA和Link-local
        ]

    def _setup(self) -> None:
        self.version = self.parameters.get("version", 4)  # 4 or 6
        self.ip_type = self.parameters.get(
            "type", "PUBLIC"
        )  # PUBLIC, PRIVATE, LOOPBACK, MULTICAST
        self.subnet = self.parameters.get("subnet", None)  # 指定子网
        self.format_style = self.parameters.get(
            "format", "STANDARD"
        )  # STANDARD, COMPRESSED (IPv6)

    def generate(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始IP地址"""
        if self.version == 6:
            return self._generate_ipv6()
        else:
            return self._generate_ipv4()

    def _generate_ipv4(self) -> str:
        """生成IPv4地址"""
        if self.subnet:
            return self._generate_from_subnet()

        if self.ip_type.upper() == "PRIVATE":
            return self._generate_private_ipv4()
        elif self.ip_type.upper() == "LOOPBACK":
            return "127.0.0.1"
        elif self.ip_type.upper() == "MULTICAST":
            return self._generate_multicast_ipv4()
        else:  # PUBLIC
            return self._generate_public_ipv4()

    def _generate_private_ipv4(self) -> str:
        """生成私有IPv4地址"""
        range_type = secrets.choice(self.ipv4_private_ranges)
        start_ip = self._ip_to_int(range_type[0])
        end_ip = self._ip_to_int(range_type[1])

        random_ip = secrets.randbelow(end_ip - start_ip + 1) + start_ip
        return self._int_to_ip(random_ip)

    def _generate_public_ipv4(self) -> str:
        """生成公网IPv4地址"""
        while True:
            octets = [secrets.randbelow(254) + 1 for _ in range(4)]
            ip = ".".join(map(str, octets))

            # 确保不是私有地址或特殊地址
            if not self._is_private_ipv4(ip) and not self._is_special_ipv4(ip):
                return ip

    def _generate_multicast_ipv4(self) -> str:
        """生成组播IPv4地址 (224.0.0.0-239.255.255.255)"""
        first_octet = secrets.randbelow(16) + 224
        other_octets = [secrets.randbelow(256) for _ in range(3)]
        return f"{first_octet}.{'.'.join(map(str, other_octets))}"

    def _generate_ipv6(self) -> str:
        """生成IPv6地址"""
        if self.ip_type.upper() == "PRIVATE":
            return self._generate_private_ipv6()
        elif self.ip_type.upper() == "LOOPBACK":
            return "::1"
        else:  # PUBLIC
            return self._generate_public_ipv6()

    def _generate_private_ipv6(self) -> str:
        """生成私有IPv6地址"""
        prefix = secrets.choice(self.ipv6_private_prefixes)
        if prefix == "fe80::":
            # Link-local地址
            suffix = ":".join([f"{secrets.randbelow(65536):x}" for _ in range(4)])
            ipv6 = f"fe80::{suffix}"
        else:
            # ULA地址
            suffix = ":".join([f"{secrets.randbelow(65536):x}" for _ in range(7)])
            ipv6 = f"{prefix[:-2]}:{suffix}"

        return self._format_ipv6(ipv6)

    def _generate_public_ipv6(self) -> str:
        """生成公网IPv6地址"""
        # 生成全球单播地址 (2000::/3)
        groups = [secrets.randbelow(0x2000) + 0x2000]  # 第一组确保是全球单播
        groups.extend([secrets.randbelow(65536) for _ in range(7)])

        ipv6 = ":".join([f"{group:x}" for group in groups])
        return self._format_ipv6(ipv6)

    def _format_ipv6(self, ipv6: str) -> str:
        """格式化IPv6地址"""
        if self.format_style.upper() == "COMPRESSED":
            # 压缩连续的零
            return self._compress_ipv6(ipv6)
        return ipv6

    def _compress_ipv6(self, ipv6: str) -> str:
        """压缩IPv6地址中的连续零"""
        # 简化实现，实际应该更复杂
        parts = ipv6.split(":")

        # 找到最长的连续零序列
        max_zero_start = -1
        max_zero_length = 0
        current_zero_start = -1
        current_zero_length = 0

        for i, part in enumerate(parts):
            if part == "0" or part == "":
                if current_zero_start == -1:
                    current_zero_start = i
                    current_zero_length = 1
                else:
                    current_zero_length += 1
            else:
                if current_zero_length > max_zero_length:
                    max_zero_start = current_zero_start
                    max_zero_length = current_zero_length
                current_zero_start = -1
                current_zero_length = 0

        if current_zero_length > max_zero_length:
            max_zero_start = current_zero_start
            max_zero_length = current_zero_length

        if max_zero_length > 1:
            before = parts[:max_zero_start]
            after = parts[max_zero_start + max_zero_length :]
            if max_zero_start == 0:
                return "::" + ":".join(after)
            elif max_zero_start + max_zero_length == len(parts):
                return ":".join(before) + "::"
            else:
                return ":".join(before) + "::" + ":".join(after)

        return ipv6

    def _generate_from_subnet(self) -> str:
        """从指定子网生成IP地址"""
        # 简化实现，假设subnet格式为 "192.168.1.0/24"
        if self.subnet and "/" in self.subnet:
            network, prefix_len = self.subnet.split("/")
            prefix_len = int(prefix_len)

            if "." in network:  # IPv4
                network_int = self._ip_to_int(network)
                host_bits = 32 - prefix_len
                max_hosts = (1 << host_bits) - 2  # 减去网络地址和广播地址

                if max_hosts > 0:
                    host_num = secrets.randbelow(max_hosts) + 1
                    ip_int = network_int + host_num
                    return self._int_to_ip(ip_int)

        return self._generate_ipv4()  # 回退到普通生成

    def _ip_to_int(self, ip: str) -> int:
        """将IPv4地址转换为整数"""
        return struct.unpack("!I", socket.inet_aton(ip))[0]

    def _int_to_ip(self, ip_int: int) -> str:
        """将整数转换为IPv4地址"""
        return socket.inet_ntoa(struct.pack("!I", ip_int))

    def _is_private_ipv4(self, ip: str) -> bool:
        """检查是否为私有IPv4地址"""
        ip_int = self._ip_to_int(ip)
        for start, end in self.ipv4_private_ranges:
            if self._ip_to_int(start) <= ip_int <= self._ip_to_int(end):
                return True
        return False

    def _is_special_ipv4(self, ip: str) -> bool:
        """检查是否为特殊IPv4地址"""
        octets = list(map(int, ip.split(".")))

        # 检查各种特殊地址范围
        if octets[0] == 0:  # 本网络
            return True
        if octets[0] == 127:  # 回环地址
            return True
        if octets[0] == 169 and octets[1] == 254:  # Link-local
            return True
        if octets[0] >= 224:  # 组播和保留地址
            return True

        return False

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
        return ["format", "subnet", "type", "version"]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, 'validator') and hasattr(self.validator, 'validate'):
            return self.validator.validate(data)
        return True



class MACAddressValidator(Validator):
    """Validator for MAC addresses."""

    def validate(self, data: str) -> bool:
        """校验MAC地址"""
        if not isinstance(data, str):
            return False

        # 移除分隔符
        clean_mac = data.replace(":", "").replace("-", "").replace(" ", "")

        # 检查长度和字符
        if len(clean_mac) != 12:
            return False

        try:
            int(clean_mac, 16)
            return True
        except ValueError:
            return False

    @property
    def error_message(self) -> str:
        return "Invalid MAC address format"


class MACAddressGenerator(DataGenerator[str]):
    """MAC地址生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.format_style = self.parameters.get(
            "format", "COLON"
        )  # COLON, HYPHEN, NONE
        self.case_style = self.parameters.get("case", "LOWER")  # UPPER, LOWER
        self.vendor_oui = self.parameters.get("vendor_oui", None)  # 厂商OUI前缀
        self.locally_administered = self.parameters.get("locally_administered", False)
        self.validator = MACAddressValidator()

        # 一些知名厂商的OUI前缀
        self.vendor_ouis = {
            "Intel": ["00:15:17", "00:16:76", "00:19:D1"],
            "Apple": ["00:03:93", "00:0A:95", "00:0D:93"],
            "Cisco": ["00:01:42", "00:01:C7", "00:02:4A"],
            "Dell": ["00:08:74", "00:0B:DB", "00:11:43"],
            "HP": ["00:01:E6", "00:02:A5", "00:08:02"],
            "Broadcom": ["00:10:18", "00:11:95", "00:14:A5"],
        }

    def _setup(self) -> None:
        self.format_style = self.parameters.get(
            "format", "COLON"
        )  # COLON, HYPHEN, NONE
        self.case_style = self.parameters.get("case", "LOWER")  # UPPER, LOWER
        self.vendor_oui = self.parameters.get("vendor_oui", None)  # 厂商OUI前缀
        self.locally_administered = self.parameters.get("locally_administered", False)

    def generate(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始MAC地址"""
        if self.vendor_oui:
            # 使用指定的厂商OUI
            if isinstance(self.vendor_oui, str):
                oui_prefix = self.vendor_oui.replace(":", "").replace("-", "")[:6]
            else:
                # 从厂商名称获取OUI
                vendor_ouis = self.vendor_ouis.get(self.vendor_oui, ["00:00:00"])
                oui_prefix = secrets.choice(vendor_ouis).replace(":", "")
        else:
            # 生成随机OUI
            oui_prefix = "".join([f"{secrets.randbelow(256):02x}" for _ in range(3)])

        # 生成后三个字节
        suffix = "".join([f"{secrets.randbelow(256):02x}" for _ in range(3)])

        # 组合完整MAC地址
        mac_bytes = oui_prefix + suffix

        # 处理本地管理位
        if self.locally_administered:
            # 设置第二位的最低位为1
            first_byte = int(mac_bytes[:2], 16)
            first_byte |= 0x02  # 设置本地管理位
            mac_bytes = f"{first_byte:02x}" + mac_bytes[2:]

        # 格式化输出
        return self._format_mac(mac_bytes)

    def _format_mac(self, mac_bytes: str) -> str:
        """格式化MAC地址"""
        # 分割为6个2位字节
        bytes_list = [mac_bytes[i : i + 2] for i in range(0, 12, 2)]

        # 应用大小写
        if self.case_style.upper() == "UPPER":
            bytes_list = [b.upper() for b in bytes_list]
        else:
            bytes_list = [b.lower() for b in bytes_list]

        # 应用格式
        if self.format_style.upper() == "HYPHEN":
            return "-".join(bytes_list)
        elif self.format_style.upper() == "NONE":
            return "".join(bytes_list)
        else:  # COLON (默认)
            return ":".join(bytes_list)

    def get_vendor_info(self, mac: str) -> dict[str, str]:
        """获取厂商信息"""
        clean_mac = mac.replace(":", "").replace("-", "").upper()
        oui = clean_mac[:6]

        # 格式化OUI为标准格式
        formatted_oui = ":".join([oui[i : i + 2] for i in range(0, 6, 2)])

        # 查找厂商
        for vendor, ouis in self.vendor_ouis.items():
            if formatted_oui in ouis:
                return {"vendor": vendor, "oui": formatted_oui}

        return {"vendor": "Unknown", "oui": formatted_oui}

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
        return ["case", "format", "locally_administered", "vendor_oui"]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, 'validator') and hasattr(self.validator, 'validate'):
            return self.validator.validate(data)
        return True



class DomainValidator(Validator):
    """Validator for domain names."""

    def validate(self, data: str) -> bool:
        """校验域名"""
        if not isinstance(data, str):
            return False

        # 基本域名格式验证
        domain_pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$"
        return bool(re.match(domain_pattern, data))

    @property
    def error_message(self) -> str:
        return "Invalid domain name format"


class DomainGenerator(DataGenerator[str]):
    """域名生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.tld_type = self.parameters.get(
            "tld_type", "COMMON"
        )  # COMMON, COUNTRY, ALL
        self.subdomain_levels = self.parameters.get("subdomain_levels", (0, 2))
        self.domain_length = self.parameters.get("domain_length", (3, 15))
        self.use_real_words = self.parameters.get("use_real_words", True)
        self.custom_tlds = self.parameters.get("custom_tlds", None)
        self.validator = DomainValidator()

        # TLD分类
        self.common_tlds = [".com", ".org", ".net", ".edu", ".gov"]
        self.country_tlds = [".cn", ".us", ".uk", ".de", ".fr", ".jp", ".kr", ".au"]
        self.new_tlds = [".io", ".tech", ".dev", ".app", ".cloud", ".ai", ".ml"]

        # 常用单词
        self.common_words = [
            "tech",
            "data",
            "cloud",
            "web",
            "app",
            "soft",
            "sys",
            "info",
            "global",
            "world",
            "net",
            "online",
            "digital",
            "smart",
            "pro",
            "fast",
            "secure",
            "easy",
            "simple",
            "quick",
            "best",
            "top",
        ]

    def _setup(self) -> None:
        self.tld_type = self.parameters.get(
            "tld_type", "COMMON"
        )  # COMMON, COUNTRY, ALL
        self.subdomain_levels = self.parameters.get("subdomain_levels", (0, 2))
        self.domain_length = self.parameters.get("domain_length", (3, 15))
        self.use_real_words = self.parameters.get("use_real_words", True)
        self.custom_tlds = self.parameters.get("custom_tlds", None)

    def generate(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始域名"""
        # 生成子域名
        subdomains = self._generate_subdomains()

        # 生成主域名
        main_domain = self._generate_main_domain()

        # 选择TLD
        tld = self._select_tld()

        # 组合域名
        if subdomains:
            return f"{'.'.join(subdomains)}.{main_domain}{tld}"
        else:
            return f"{main_domain}{tld}"

    def _generate_subdomains(self) -> list[str]:
        """生成子域名列表"""
        levels = secrets.randbelow(self.subdomain_levels[1] - self.subdomain_levels[0] + 1) + self.subdomain_levels[0]
        subdomains = []

        for _ in range(levels):
            if self.use_real_words and (secrets.randbelow(1000000) / 1000000) < 0.6:
                subdomain = secrets.choice(
                    ["www", "api", "mail", "ftp", "blog", "shop", "news"]
                )
            else:
                subdomain = self._generate_word((2, 8))
            subdomains.append(subdomain)

        return subdomains

    def _generate_main_domain(self) -> str:
        """生成主域名"""
        if self.use_real_words and (secrets.randbelow(1000000) / 1000000) < 0.7:
            # 使用真实单词
            if (secrets.randbelow(1000000) / 1000000) < 0.5:
                # 单个单词
                return secrets.choice(self.common_words)
            else:
                # 组合单词
                word1 = secrets.choice(self.common_words)
                word2 = secrets.choice(self.common_words)
                return word1 + word2
        else:
            # 生成随机字符串
            length = secrets.randbelow(self.domain_length[1] - self.domain_length[0] + 1) + self.domain_length[0]
            return self._generate_word((length, length))

    def _generate_word(self, length_range) -> str:
        """生成单词"""
        import string

        length = secrets.randbelow(length_range[1] - length_range[0] + 1) + length_range[0]
        return "".join(random.choices(string.ascii_lowercase, k=length))

    def _select_tld(self) -> str:
        """选择顶级域名"""
        if self.custom_tlds:
            return secrets.choice(self.custom_tlds)

        if self.tld_type.upper() == "COUNTRY":
            return secrets.choice(self.country_tlds)
        elif self.tld_type.upper() == "ALL":
            all_tlds = self.common_tlds + self.country_tlds + self.new_tlds
            return secrets.choice(all_tlds)
        else:  # COMMON
            return secrets.choice(self.common_tlds)

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
        return ["custom_tlds", "domain_length", "subdomain_levels", "tld_type", "use_real_words"]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, 'validator') and hasattr(self.validator, 'validate'):
            return self.validator.validate(data)
        return True



class PortNumberValidator(Validator):
    """Validator for port numbers."""

    def validate(self, data: int) -> bool:
        """校验端口号"""
        if not isinstance(data, int):
            return False

        return 1 <= data <= 65535

    @property
    def error_message(self) -> str:
        return "Port number must be an integer between 1 and 65535"


class PortNumberGenerator(DataGenerator[int]):
    """端口号生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.port_type = self.parameters.get(
            "type", "USER"
        )  # SYSTEM, USER, DYNAMIC, COMMON
        self.protocol = self.parameters.get("protocol", "ANY")  # TCP, UDP, ANY
        self.exclude_well_known = self.parameters.get("exclude_well_known", False)
        self.validator = PortNumberValidator()

        # 端口范围定义
        self.port_ranges = {
            "SYSTEM": (1, 1023),  # 系统端口
            "USER": (1024, 49151),  # 用户端口
            "DYNAMIC": (49152, 65535),  # 动态端口
            "ALL": (1, 65535),
        }

        # 常用端口
        self.common_ports = {
            "TCP": [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995],
            "UDP": [53, 67, 68, 69, 123, 161, 162, 514],
            "BOTH": [53, 80, 443],
        }

    def _setup(self) -> None:
        self.port_type = self.parameters.get(
            "type", "USER"
        )  # SYSTEM, USER, DYNAMIC, COMMON
        self.protocol = self.parameters.get("protocol", "ANY")  # TCP, UDP, ANY
        self.exclude_well_known = self.parameters.get("exclude_well_known", False)

    def generate(self, context: Optional[GenerationContext] = None) -> int:
        """生成原始端口号"""
        if self.port_type.upper() == "COMMON":
            return self._generate_common_port()

        # 获取端口范围
        port_range = self.port_ranges.get(
            self.port_type.upper(), self.port_ranges["USER"]
        )

        while True:
            port = secrets.randbelow(port_range[1] - port_range[0] + 1) + port_range[0]

            # 如果要排除知名端口，检查是否在知名端口列表中
            if self.exclude_well_known and self._is_well_known_port(port):
                continue

            return port

    def _generate_common_port(self) -> int:
        """生成常用端口"""
        if self.protocol.upper() == "TCP":
            return secrets.choice(self.common_ports["TCP"])
        elif self.protocol.upper() == "UDP":
            return secrets.choice(self.common_ports["UDP"])
        else:  # ANY
            all_common = (
                self.common_ports["TCP"]
                + self.common_ports["UDP"]
                + self.common_ports["BOTH"]
            )
            return secrets.choice(all_common)

    def _is_well_known_port(self, port: int) -> bool:
        """检查是否为知名端口"""
        all_common = (
            self.common_ports["TCP"]
            + self.common_ports["UDP"]
            + self.common_ports["BOTH"]
        )
        return port in all_common

    def get_port_info(self, port: int) -> dict[str, Any]:
        """获取端口信息"""
        info = {"port": port, "type": "UNKNOWN", "protocol": [], "service": "Unknown"}

        if port < 1024:
            info["type"] = "SYSTEM"
        elif port < 49152:
            info["type"] = "USER"
        else:
            info["type"] = "DYNAMIC"

        # 检查常用服务
        service_map = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            993: "IMAPS",
            995: "POP3S",
        }

        if port in service_map:
            info["service"] = service_map[port]

        # 检查协议
        if port in self.common_ports["TCP"]:
            info["protocol"].append("TCP")
        if port in self.common_ports["UDP"]:
            info["protocol"].append("UDP")
        if port in self.common_ports["BOTH"]:
            info["protocol"] = ["TCP", "UDP"]

        if not info["protocol"]:
            info["protocol"] = ["TCP", "UDP"]  # 默认支持两种协议

        return info

    def generate_single(self, context: Optional[GenerationContext] = None) -> int:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.NETWORK

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["exclude_well_known", "protocol", "type"]

    def validate(self, data: int) -> bool:
        """验证生成的数据"""
        if hasattr(self, 'validator') and hasattr(self.validator, 'validate'):
            return self.validator.validate(data)
        return True



class GenericIPAddressGenerator(IPAddressGenerator):
    """通用IP地址生成器注册版本"""

    pass


class GenericMACAddressGenerator(MACAddressGenerator):
    """通用MAC地址生成器注册版本"""

    pass


class GenericDomainGenerator(DomainGenerator):
    """通用域名生成器注册版本"""

    pass


class GenericPortNumberGenerator(PortNumberGenerator):
    """通用端口号生成器注册版本"""

    pass