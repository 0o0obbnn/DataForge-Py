"""
会话ID生成器
Session ID generator for web applications.
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Any

from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GenerationContext, GeneratorType


@register_generator("session_id", ["session"])
class SessionIDGenerator(DataGenerator[str]):
    """
    会话ID生成器

    功能特性：
    - 生成高熵会话ID
    - 支持多种编码格式
    - 包含用户代理和设备信息
    - 支持会话超时机制

    返回类型：
    - 默认返回字符串（仅session_id）
    - 设置 string_only=False 返回完整字典
    """

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.AUTH

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "length",
            "encoding",
            "include_timestamp",
            "include_user_agent",
            "include_ip",
            "session_timeout",
            "device_type",
            "secure",
            "string_only",
        ]

    def _setup(self) -> None:
        """初始化设置"""
        self.default_config = {
            "length": 32,
            "encoding": "hex",
            "prefix": "",
            "expires_in": 7200,
            "max_inactive_time": 1800,
            "include_timestamp": True,
            "include_user_id": False,
            "include_ip": False,
            "include_user_agent": False,
            "device_type": "web",
            "secure": True,
            "string_only": True,  # 默认返回字符串
        }

    def _get_effective_config(self) -> dict[str, Any]:
        """获取有效配置（合并默认配置和用户参数）"""
        config = self.default_config.copy()
        config.update(self.parameters)
        return config

    def _generate_raw(
        self, context: GenerationContext | None = None
    ) -> str | dict[str, Any]:
        """生成原始会话ID数据"""
        import base64
        import random

        config = self._get_effective_config()

        length = config["length"]
        encoding = config["encoding"]
        prefix = config.get("prefix", "")
        config.get("include_timestamp", True)
        include_user_id = config.get("include_user_id", False)
        include_ip = config.get("include_ip", False)
        include_user_agent = config.get("include_user_agent", False)
        device_type = config.get("device_type", "web")
        secure = config.get("secure", True)
        string_only = config.get("string_only", True)

        # 生成随机字节序列
        if secure:
            random_bytes = secrets.token_bytes(length)
        else:
            import os

            random_bytes = os.urandom(length)

        # 根据编码格式生成会话ID
        if encoding == "hex":
            session_id = random_bytes.hex()
        elif encoding == "base64":
            session_id = (
                base64.urlsafe_b64encode(random_bytes).decode("utf-8").rstrip("=")
            )
        elif encoding == "urlsafe":
            session_id = (
                base64.urlsafe_b64encode(random_bytes).decode("utf-8").rstrip("=")
            )
        elif encoding == "base32":
            session_id = base64.b32encode(random_bytes).decode("utf-8").rstrip("=")
        else:
            session_id = random_bytes.hex()

        # 添加前缀
        if prefix:
            session_id = f"{prefix}_{session_id}"

        # 如果只需要字符串，直接返回session_id
        if string_only:
            return session_id

        # 构建会话数据
        now = datetime.now()
        result = {
            "session_id": session_id,
            "length": len(session_id),
            "encoding": encoding,
            "created_at": now.isoformat(),
            "expires_at": (
                now + timedelta(seconds=config.get("expires_in", 7200))
            ).isoformat(),
            "is_active": True,
            "user_id": None,
            "ip_address": None,
            "user_agent": None,
            "last_activity": now.isoformat(),
            "hit_count": 0,
            "max_inactive_time": config.get("max_inactive_time", 1800),
            "device_type": device_type,
        }

        # 可选信息
        if include_user_id:
            result["user_id"] = "placeholder_user_id"
        if include_ip:
            result["ip_address"] = "0.0.0.0"
        if include_user_agent:
            user_agents = {
                "web": [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                ],
                "mobile": [
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
                    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
                ],
                "tablet": [
                    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
                    "Mozilla/5.0 (Linux; Android 10; SM-T510) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Safari/537.36",
                ],
            }
            result["user_agent"] = random.choice(
                user_agents.get(device_type, user_agents["web"])
            )

        # 生成会话指纹和CSRF令牌
        fingerprint_data = f"{session_id}{now.isoformat()}"
        result["fingerprint"] = hashlib.sha256(fingerprint_data.encode()).hexdigest()[
            :16
        ]
        result["csrf_token"] = secrets.token_urlsafe(32)

        return result

    def _generate_user_agent(self, device_type: str) -> str:
        """生成用户代理字符串"""
        import random

        user_agents = {
            "web": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            ],
            "mobile": [
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
            ],
            "tablet": [
                "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; SM-T510) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Safari/537.36",
            ],
        }

        return random.choice(user_agents.get(device_type, user_agents["web"]))

    def _generate_ip_address(self) -> str:
        """生成IP地址"""
        import random

        # 生成私有IP地址段
        ip_ranges = [
            ("192.168", 0, 255, 1, 254),
            ("10", 0, 255, 1, 254),
            ("172", 16, 31, 1, 254),
        ]

        base, octet2_min, octet2_max, octet3_min, octet3_max = random.choice(ip_ranges)

        if base == "172":
            octet2 = random.randint(octet2_min, octet2_max)
            return f"{base}.{octet2}.{random.randint(octet3_min, octet3_max)}.{random.randint(1, 254)}"
        else:
            return f"{base}.{random.randint(octet2_min, octet2_max)}.{random.randint(octet3_min, octet3_max)}.{random.randint(1, 254)}"

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证会话ID数据的有效性"""
        # 如果是字符串，直接验证长度
        if isinstance(data, str):
            return len(data) >= 16

        # 如果是字典，验证完整数据
        if not isinstance(data, dict):
            return False

        session_id = data.get("session_id")
        if not session_id or not isinstance(session_id, str):
            return False

        # 检查长度
        min_length = 16
        if len(session_id) < min_length:
            return False

        # 检查过期时间
        expires_at = data.get("expires_at")
        if expires_at:
            try:
                expiry_time = datetime.fromisoformat(expires_at)
                if datetime.now() > expiry_time:
                    return False
            except ValueError:
                return False

        return True

    def is_expired(self, session_data: dict[str, Any]) -> bool:
        """检查会话是否过期"""
        expires_at = session_data.get("expires_at")
        if not expires_at:
            return True

        try:
            expiry_time = datetime.fromisoformat(expires_at)
            return datetime.now() > expiry_time
        except ValueError:
            return True

    def refresh_session(self, session_data: dict[str, Any]) -> dict[str, Any]:
        """刷新会话有效期"""
        if not self.validate(session_data):
            return session_data

        # 重新生成会话数据
        new_session = self._generate_raw()

        # 确保返回的是字典类型
        if isinstance(new_session, str):
            # 如果返回字符串，构建字典
            new_session = {
                "session_id": new_session,
                "length": len(new_session),
                "encoding": "unknown",
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(seconds=7200)).isoformat(),
            }

        # 保留原有会话ID但更新时间
        assert isinstance(new_session, dict)  # 类型守卫
        new_session["session_id"] = session_data["session_id"]
        new_session["created_at"] = session_data["created_at"]  # 保持创建时间

        return new_session

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        # 使用_generate_raw方法生成会话数据
        session_data = self._generate_raw(context)
        # 如果是字符串，直接返回
        if isinstance(session_data, str):
            return session_data
        # 如果是字典，返回session_id字段
        return session_data.get("session_id", "")
