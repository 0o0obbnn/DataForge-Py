"""IPv6地址生成器模块"""

import random

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorType,
)


class IPv6Generator(DataGenerator):
    """IPv6地址生成器"""

    def _setup(self) -> None:
        """初始化设置"""
        pass

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        """生成IPv6地址"""
        format_type = self.parameters.get("format", "compressed")

        if format_type == "full":
            return self._generate_full_format()
        else:
            return self._generate_compressed_format()

    def _generate_full_format(self) -> str:
        """生成完整格式的IPv6地址"""
        # 生成8组16位十六进制数
        groups = []
        for _ in range(8):
            group = format(random.randint(0, 0xFFFF), "04x")
            groups.append(group)
        return ":".join(groups)

    def _generate_compressed_format(self) -> str:
        """生成压缩格式的IPv6地址"""
        # 生成8组16位十六进制数
        groups = []
        for _ in range(8):
            group = format(random.randint(0, 0xFFFF), "x")
            groups.append(group)

        # 随机决定是否压缩连续的0
        if random.random() < 0.5:
            # 找到最长的连续0序列并压缩
            ipv6 = ":".join(groups)
            # 简单压缩：将连续的:0:替换为::
            if "0:0" in ipv6:
                ipv6 = ipv6.replace(":0:0:0:0:0:0:0:", "::")
                ipv6 = ipv6.replace(":0:0:0:0:0:0:", "::")
                ipv6 = ipv6.replace(":0:0:0:0:0:", "::")
                ipv6 = ipv6.replace(":0:0:0:0:", "::")
                ipv6 = ipv6.replace(":0:0:0:", "::")
                ipv6 = ipv6.replace(":0:0:", "::")
            return ipv6
        else:
            return ":".join(groups)

    def validate(self, data: str) -> bool:
        """验证IPv6地址"""
        if not isinstance(data, str):
            return False

        if not data:
            return False

        # 基本格式检查
        if ":::" in data:  # 不允许三个连续冒号
            return False

        # 检查是否包含冒号
        if ":" not in data:
            return False

        # 检查双冒号出现次数（最多一次）
        if data.count("::") > 1:
            return False

        # 分割并验证每个部分
        if "::" in data:
            # 处理压缩格式
            parts = data.split("::")
            if len(parts) > 2:
                return False
            all_groups = []
            for part in parts:
                if part:
                    all_groups.extend(part.split(":"))
        else:
            all_groups = data.split(":")
            if len(all_groups) != 8:
                return False

        # 验证每个组
        for group in all_groups:
            if not group:
                continue
            if len(group) > 4:
                return False
            try:
                int(group, 16)
            except ValueError:
                return False

        return True

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.NETWORK

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["format"]


# 注册生成器
register_generator("ipv6")(IPv6Generator)
