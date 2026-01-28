"""
Session ID/Token 生成器模块
支持生成各种类型的会话标识符和令牌
"""

import secrets
import string
import time
import uuid

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
)
from ...core.protocols import Validator
from ...core.types import GeneratorType


class SessionTokenValidator(Validator):
    """Validator for session tokens."""

    def __init__(self, token_type: str, prefix: str, suffix: str):
        self.token_type = token_type
        self.prefix = prefix
        self.suffix = suffix

    def validate(self, data: str) -> bool:
        """验证Session ID/Token格式"""
        if not data or not isinstance(data, str):
            return False

        if self.token_type == "UUID":
            try:
                uuid.UUID(data)
                return True
            except ValueError:
                return False

        elif self.token_type == "JWT_LIKE":
            parts = data.split(".")
            if len(parts) != 3:
                return False
            # 简单的格式检查
            return all(part for part in parts)

        # 其他类型的通用验证
        if self.prefix and not data.startswith(self.prefix):
            return False
        if self.suffix and not data.endswith(self.suffix):
            return False

        return True

    @property
    def error_message(self) -> str:
        return "Invalid session token format"


@register_generator("session_token", aliases=["session", "token", "session_id"])
class SessionTokenGenerator(DataGenerator[str]):
    """Session ID/Token 生成器"""

    # 类级别属性声明，帮助类型检查器
    token_type: str
    length: int
    include_timestamp: bool
    characters: str
    prefix: str
    suffix: str
    validator: SessionTokenValidator | None

    def __init__(self, config: GeneratorConfig):
        # 先初始化实例属性，避免类型检查器警告
        self.token_type = "SESSION_ID"
        self.length = 32
        self.include_timestamp = False
        self.characters = "ALPHANUMERIC"
        self.prefix = ""
        self.suffix = ""
        self.validator = None

        # 字符集配置
        self.char_sets = {
            "ALPHANUMERIC": string.ascii_letters + string.digits,
            "ALPHANUMERIC_UPPER": string.ascii_uppercase + string.digits,
            "ALPHANUMERIC_LOWER": string.ascii_lowercase + string.digits,
            "ALPHABETIC": string.ascii_letters,
            "NUMERIC": string.digits,
            "HEX": string.hexdigits.lower(),
            "HEX_UPPER": string.hexdigits.upper(),
            "BASE64": string.ascii_letters + string.digits + "+/",
            "URL_SAFE": string.ascii_letters + string.digits + "-_",
        }

        # 调用父类初始化（会调用 _setup()）
        super().__init__(config)

    def _setup(self) -> None:
        """配置生成器参数"""
        self.token_type = self.parameters.get("type", "SESSION_ID")
        self.length = self.parameters.get("length", 32)
        self.include_timestamp = self.parameters.get("include_timestamp", False)
        self.characters = self.parameters.get("characters", "ALPHANUMERIC")
        self.prefix = self.parameters.get("prefix", "")
        self.suffix = self.parameters.get("suffix", "")
        self.validator = SessionTokenValidator(
            self.token_type, self.prefix, self.suffix
        )

    def generate(self, context: GenerationContext | None = None) -> str:
        """生成原始Session ID/Token"""
        if self.token_type == "UUID":
            return str(uuid.uuid4())
        elif self.token_type == "SESSION_ID":
            return self._generate_session_id()
        elif self.token_type == "JWT_LIKE":
            return self._generate_jwt_like()
        elif self.token_type == "RANDOM":
            return self._generate_random_token()
        else:
            return self._generate_random_token()

    def _generate_session_id(self) -> str:
        """生成会话ID"""
        chars = self.char_sets.get(self.characters, self.char_sets["ALPHANUMERIC"])
        token = "".join(secrets.choice(chars) for _ in range(self.length))

        if self.include_timestamp:
            timestamp = str(int(time.time()))
            token = f"{timestamp}_{token}"

        return f"{self.prefix}{token}{self.suffix}"

    def _generate_jwt_like(self) -> str:
        """生成JWT风格的token"""
        # Header
        header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

        # Payload (包含时间戳)
        payload_chars = string.ascii_letters + string.digits + "-_"
        payload = "".join(
            secrets.choice(payload_chars) for _ in range(self.length // 2)
        )

        # Signature
        sig_chars = string.ascii_letters + string.digits + "-_"
        signature = "".join(secrets.choice(sig_chars) for _ in range(self.length // 2))

        return f"{header}.{payload}.{signature}"

    def _generate_random_token(self) -> str:
        """生成随机token"""
        chars = self.char_sets.get(self.characters, self.char_sets["ALPHANUMERIC"])
        token = "".join(secrets.choice(chars) for _ in range(self.length))
        return f"{self.prefix}{token}{self.suffix}"

    def get_token_info(self, value: str) -> dict:
        """获取token信息"""
        info = {
            "type": self.token_type,
            "length": len(value),
            "has_prefix": bool(self.prefix),
            "has_suffix": bool(self.suffix),
        }

        if self.token_type == "UUID":
            info["version"] = "UUIDv4"
        elif self.token_type == "JWT_LIKE":
            info["parts"] = len(value.split("."))

        return info

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.NETWORK

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["characters", "include_timestamp", "length", "prefix", "suffix", "type"]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if self.validator is not None and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class GenericSessionTokenGenerator(SessionTokenGenerator):
    """通用Session ID/Token生成器"""

    # 类级别属性声明，帮助类型检查器
    token_type: str
    length: int
    include_timestamp: bool
    characters: str
    prefix: str
    suffix: str
    validator: SessionTokenValidator | None

    def __init__(self, config: GeneratorConfig):
        # 父类的 __init__ 已经调用了 _setup()，所以属性已经初始化
        super().__init__(config)
        # 重新创建 validator 以确保使用最新的属性值
        self.validator = SessionTokenValidator(
            self.token_type, self.prefix, self.suffix
        )

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.NETWORK

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if self.validator is not None and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return isinstance(data, str) and bool(data.strip())
