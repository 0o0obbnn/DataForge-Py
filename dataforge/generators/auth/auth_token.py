"""
认证令牌生成器
Authentication token generator for JWT and API tokens.
"""

import base64
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Any

from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GenerationContext
from dataforge.core.types import GeneratorType


@register_generator("auth_token", ["token"])
class AuthTokenGenerator(DataGenerator[Any]):
    """
    认证令牌生成器

    功能特性：
    - 生成JWT格式的访问令牌
    - 支持多种哈希算法
    - 包含用户ID和权限信息
    - 支持刷新令牌机制

    返回类型：
    - 默认返回字符串（仅access_token）
    - 设置 string_only=False 返回完整字典
    """

    @property
    def generator_type(self) -> GeneratorType:
        """生成器类型"""
        return GeneratorType.AUTH

    @property
    def supported_parameters(self) -> list[str]:
        """支持的参数名称列表"""
        return [
            "algorithm",
            "expiry_hours",
            "include_refresh",
            "user_id",
            "scope",
            "issuer",
            "audience",
            "string_only",
            "format",
        ]

    def _setup(self) -> None:
        """初始化设置"""
        self.default_config = {
            "algorithm": "HS256",
            "expiry_hours": 24,
            "include_refresh": True,
            "user_id": None,
            "scope": ["read", "write"],
            "issuer": "dataforge.auth",
            "audience": "dataforge.api",
            "string_only": True,  # 默认返回字符串
            "format": "jwt",  # jwt 或 hex
        }

    def _get_effective_config(self) -> dict[str, Any]:
        """获取合并后的有效配置"""
        config = self.default_config.copy()
        config.update(self.parameters)
        return config

    def _generate_raw(
        self, context: GenerationContext | None = None
    ) -> str | dict[str, Any]:
        """生成原始认证令牌数据"""
        config = self._get_effective_config()

        algorithm = config["algorithm"]
        expiry_hours = config["expiry_hours"]
        include_refresh = config["include_refresh"]
        user_id = config["user_id"] or f"user_{secrets.token_hex(8)}"
        scope = config["scope"]
        issuer = config["issuer"]
        audience = config["audience"]
        string_only = config["string_only"]
        token_format = config["format"]

        # 如果是hex格式，直接生成hex token
        if token_format == "hex":
            return secrets.token_hex(32)

        # 生成时间戳
        now = datetime.now()
        issued_at = now
        expiry_at = now + timedelta(hours=expiry_hours)

        # 生成JWT头部
        header = {"alg": algorithm, "typ": "JWT"}

        # 生成JWT载荷
        payload = {
            "iss": issuer,
            "aud": audience,
            "sub": str(user_id),
            "exp": int(expiry_at.timestamp()),
            "iat": int(issued_at.timestamp()),
            "jti": secrets.token_urlsafe(16),  # JWT ID
            "scope": scope,
        }

        # 生成访问令牌
        access_token = self._generate_jwt(header, payload)

        # 如果只需要字符串，直接返回token
        if string_only:
            return access_token

        result = {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": expiry_hours * 3600,
            "scope": scope,
            "user_id": user_id,
            "issued_at": issued_at.isoformat(),
            "expires_at": expiry_at.isoformat(),
        }

        # 生成刷新令牌
        if include_refresh:
            refresh_payload = {
                "iss": issuer,
                "sub": str(user_id),
                "exp": int((now + timedelta(days=30)).timestamp()),
                "iat": int(issued_at.timestamp()),
                "jti": secrets.token_urlsafe(16),
                "type": "refresh",
            }

            refresh_token = self._generate_jwt(header, refresh_payload)
            result["refresh_token"] = refresh_token
            result["refresh_expires_in"] = 30 * 24 * 3600

        return result

    def _generate_jwt(self, header: dict[str, Any], payload: dict[str, Any]) -> str:
        """生成JWT令牌"""
        import json

        # 编码头部和载荷
        header_encoded = (
            base64.urlsafe_b64encode(json.dumps(header, separators=(",", ":")).encode())
            .decode()
            .rstrip("=")
        )

        payload_encoded = (
            base64.urlsafe_b64encode(
                json.dumps(payload, separators=(",", ":")).encode()
            )
            .decode()
            .rstrip("=")
        )

        # 生成签名（简化版，实际应用需要密钥）
        signature_input = f"{header_encoded}.{payload_encoded}"
        signature = (
            base64.urlsafe_b64encode(hashlib.sha256(signature_input.encode()).digest())
            .decode()
            .rstrip("=")
        )

        return f"{header_encoded}.{payload_encoded}.{signature}"

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证认证令牌数据的有效性"""
        # 如果是字符串，直接验证token格式
        if isinstance(data, str):
            parts = data.split(".")
            return len(parts) == 3 and all(len(part) > 0 for part in parts)

        # 如果是字典，验证完整数据
        if not isinstance(data, dict):
            return False

        access_token = data.get("access_token")
        if not access_token or not isinstance(access_token, str):
            return False

        # 检查令牌格式
        parts = access_token.split(".")
        if len(parts) != 3:
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

    def get_token_info(self, token_data: dict[str, Any]) -> dict[str, Any]:
        """获取令牌详细信息"""
        if not self.validate(token_data):
            return {"valid": False, "error": "Invalid token format"}

        access_token = token_data.get("access_token", "")
        try:
            # 解码JWT载荷
            payload_part = access_token.split(".")[1]
            import json

            payload = json.loads(base64.urlsafe_b64decode(payload_part + "==").decode())

            return {
                "valid": True,
                "user_id": payload.get("sub"),
                "issuer": payload.get("iss"),
                "audience": payload.get("aud"),
                "issued_at": datetime.fromtimestamp(payload.get("iat", 0)).isoformat(),
                "expires_at": datetime.fromtimestamp(payload.get("exp", 0)).isoformat(),
                "scope": payload.get("scope", []),
                "jwt_id": payload.get("jti"),
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def generate_single(
        self, context: GenerationContext | None = None
    ) -> dict[str, Any]:
        """生成单个令牌数据项（返回包含access_token等字段的字典）"""
        result = self._generate_raw(context)
        # 如果返回字符串（hex格式），包装成字典
        if isinstance(result, str):
            return {"access_token": result, "token_type": "Bearer"}
        return result  # type: ignore[return-value]
