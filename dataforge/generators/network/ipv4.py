"""IPv4地址生成器模块"""

import random
from typing import Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorType,
)


class IPv4Generator(DataGenerator):
    """IPv4地址生成器"""

    def _setup(self) -> None:
        """初始化设置"""
        pass

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成IPv4地址"""
        # 获取参数
        private = self.parameters.get("private", False)

        if private:
            # 生成私有IP地址
            return self._generate_private_ip()
        else:
            # 生成公共IP地址
            return self._generate_public_ip()

    def _generate_private_ip(self) -> str:
        """生成私有IP地址"""
        # 私有IP地址范围:
        # 10.0.0.0 - 10.255.255.255
        # 172.16.0.0 - 172.31.255.255
        # 192.168.0.0 - 192.168.255.255

        choice = random.randint(1, 3)

        if choice == 1:
            # 10.x.x.x
            return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        elif choice == 2:
            # 172.16-31.x.x
            return f"172.{random.randint(16, 31)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        else:
            # 192.168.x.x
            return f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"

    def _generate_public_ip(self) -> str:
        """生成公共IP地址"""
        # 避免私有IP和保留IP范围
        while True:
            octets = [random.randint(1, 254) for _ in range(4)]
            ip = f"{octets[0]}.{octets[1]}.{octets[2]}.{octets[3]}"

            # 检查是否为私有IP
            if octets[0] == 10:
                continue
            if octets[0] == 172 and 16 <= octets[1] <= 31:
                continue
            if octets[0] == 192 and octets[1] == 168:
                continue
            if octets[0] == 127:  # 回环地址
                continue
            if octets[0] >= 224:  # 组播和保留地址
                continue

            return ip

    def validate(self, data: str) -> bool:
        """验证IPv4地址"""
        if not isinstance(data, str):
            return False

        parts = data.split(".")
        if len(parts) != 4:
            return False

        try:
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            return True
        except ValueError:
            return False

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.NETWORK

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["private"]


# 注册生成器
register_generator("ipv4")(IPv4Generator)
