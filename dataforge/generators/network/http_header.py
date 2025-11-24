"""
HTTP头生成器
"""

import random  # TODO: Convert to secrets
import re
import secrets
import string
from typing import Any, Optional

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
)
from ...core.protocols import Validator
from ...core.types import GeneratorType

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


class HTTPHeaderValidator(Validator):
    """Validator for HTTP headers."""

    def validate(self, data: dict[str, str]) -> bool:
        """校验HTTP头"""
        if not isinstance(data, dict):
            return False

        # 检查键值对类型
        for key, value in data.items():
            if not isinstance(key, str) or not isinstance(value, str):
                return False

            # 检查键名格式（应该不含特殊字符）
            if not re.match(r"^[a-zA-Z0-9\-]+$", key):
                return False

        return True

    @property
    def error_message(self) -> str:
        return "Invalid HTTP header format"


@register_generator("http_header", aliases=["headers", "user_agent"])
class HTTPHeaderGenerator(DataGenerator[dict[str, str]]):
    """HTTP头生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.header_type = "REQUEST"  # REQUEST, RESPONSE, CUSTOM
        self.include_common = True
        self.include_user_agent = True
        self.include_cookies = False
        self.include_auth = False
        self.custom_headers = {}
        self.min_headers = 3
        self.max_headers = 10
        self.validator = None

        # 常见HTTP请求头
        self.common_request_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        }

        # 常见HTTP响应头
        self.common_response_headers = {
            "Content-Type": "text/html; charset=utf-8",
            "Content-Encoding": "gzip",
            "Cache-Control": "max-age=3600",
            "Expires": self._generate_expires_header(),
            "Server": "nginx/1.18.0",
            "X-Powered-By": "PHP/7.4.0",
            "X-Frame-Options": "SAMEORIGIN",
            "X-XSS-Protection": "1; mode=block",
            "X-Content-Type-Options": "nosniff",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        }

        # 用户代理列表
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.header_type = self.parameters.get(
            "type", "REQUEST"
        )  # REQUEST, RESPONSE, CUSTOM
        self.include_common = self.parameters.get("include_common", True)
        self.include_user_agent = self.parameters.get("include_user_agent", True)
        self.include_cookies = self.parameters.get("include_cookies", False)
        self.include_auth = self.parameters.get("include_auth", False)
        self.custom_headers = self.parameters.get("custom_headers", {})
        self.min_headers = self.parameters.get("min_headers", 3)
        self.max_headers = self.parameters.get("max_headers", 10)
        self.validator = HTTPHeaderValidator()

    def generate(self, context: Optional[GenerationContext] = None) -> dict[str, str]:
        """生成原始HTTP头"""
        headers = {}

        # 添加自定义头
        headers.update(self.custom_headers)

        # 根据类型添加常见头
        if self.header_type.upper() == "REQUEST":
            headers.update(self._generate_request_headers())
        elif self.header_type.upper() == "RESPONSE":
            headers.update(self._generate_response_headers())
        else:  # CUSTOM
            # 随机选择一些头
            all_headers = {
                **self.common_request_headers,
                **self.common_response_headers,
            }
            num_headers = (
                secrets.randbelow(self.max_headers - self.min_headers + 1)
                + self.min_headers
            )
            selected_headers = random.sample(
                list(all_headers.items()), min(num_headers, len(all_headers))
            )
            headers.update(dict(selected_headers))

        return headers

    def _generate_request_headers(self) -> dict[str, str]:
        """生成请求头"""
        headers = {}

        if self.include_common:
            # 随机选择一些常见请求头
            num_common = secrets.randbelow(len(self.common_request_headers) - 3 + 1) + 3
            common_headers = random.sample(
                list(self.common_request_headers.items()), num_common
            )
            headers.update(dict(common_headers))

        if self.include_user_agent:
            headers["User-Agent"] = secrets.choice(self.user_agents)

        if self.include_cookies:
            headers["Cookie"] = self._generate_cookie_header()

        if self.include_auth:
            headers["Authorization"] = self._generate_auth_header()

        return headers

    def _generate_response_headers(self) -> dict[str, str]:
        """生成响应头"""
        headers = {}

        if self.include_common:
            # 随机选择一些常见响应头
            num_common = (
                secrets.randbelow(len(self.common_response_headers) - 3 + 1) + 3
            )
            common_headers = random.sample(
                list(self.common_response_headers.items()), num_common
            )
            headers.update(dict(common_headers))

        # 添加一些响应特有的头
        headers["Date"] = self._generate_date_header()
        headers["Content-Length"] = str(secrets.randbelow(99001) + 1000)

        # 随机添加一些缓存头
        if (secrets.randbelow(1000000) / 1000000) < 0.5:
            headers["ETag"] = self._generate_etag()

        return headers

    def _generate_cookie_header(self) -> str:
        """生成Cookie头"""
        cookies = []
        num_cookies = secrets.randbelow(5) + 1

        for _ in range(num_cookies):
            cookie_name = self._generate_random_name(4, 10)
            cookie_value = self._generate_random_name(8, 20)
            cookies.append(f"{cookie_name}={cookie_value}")

        return "; ".join(cookies)

    def _generate_auth_header(self) -> str:
        """生成认证头"""
        auth_type = secrets.choice(["Basic", "Bearer"])

        if auth_type == "Basic":
            # Basic认证
            username = self._generate_random_name(6, 12)
            password = self._generate_random_name(8, 16)
            credentials = f"{username}:{password}".encode()
            import base64

            encoded = base64.b64encode(credentials).decode("utf-8")
            return f"Basic {encoded}"
        else:
            # Bearer token
            token = self._generate_random_name(32, 64)
            return f"Bearer {token}"

    def _generate_expires_header(self) -> str:
        """生成Expires头"""
        import email.utils
        from datetime import datetime, timedelta, timezone

        expires = datetime.now(timezone.utc) + timedelta(
            hours=secrets.randbelow(24) + 1
        )
        return email.utils.formatdate(expires.timestamp(), usegmt=True)

    def _generate_date_header(self) -> str:
        """生成Date头"""
        import email.utils
        from datetime import datetime, timezone

        return email.utils.formatdate(
            datetime.now(timezone.utc).timestamp(), usegmt=True
        )

    def _generate_etag(self) -> str:
        """生成ETag"""
        etag = self._generate_random_name(8, 16)
        return f'"{etag}"'

    def _generate_random_name(self, min_len: int, max_len: int) -> str:
        """生成随机名称"""
        length = secrets.randbelow(max_len - min_len + 1) + min_len
        chars = string.ascii_letters + string.digits
        return "".join(random.choices(chars, k=length))

    def get_header_info(self, headers: dict[str, str]) -> dict[str, Any]:
        """获取HTTP头信息"""
        info = {
            "total_headers": len(headers),
            "header_types": {},
            "has_auth": False,
            "has_cookies": False,
            "content_type": None,
            "user_agent": None,
        }

        for key, value in headers.items():
            key_lower = key.lower()

            if key_lower == "authorization":
                info["has_auth"] = True
            elif key_lower == "cookie":
                info["has_cookies"] = True
            elif key_lower == "content-type":
                info["content_type"] = value
            elif key_lower == "user-agent":
                info["user_agent"] = value

            # 统计头类型
            if key_lower.startswith("x-"):
                info["header_types"]["custom"] = (
                    info["header_types"].get("custom", 0) + 1
                )
            elif key_lower in ["content-type", "content-length", "content-encoding"]:
                info["header_types"]["content"] = (
                    info["header_types"].get("content", 0) + 1
                )
            elif key_lower in ["authorization", "www-authenticate"]:
                info["header_types"]["auth"] = info["header_types"].get("auth", 0) + 1
            elif key_lower in ["cookie", "set-cookie"]:
                info["header_types"]["cookie"] = (
                    info["header_types"].get("cookie", 0) + 1
                )
            else:
                info["header_types"]["standard"] = (
                    info["header_types"].get("standard", 0) + 1
                )

        return info

    def generate_single(
        self, context: Optional[GenerationContext] = None
    ) -> dict[str, str]:
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
            "custom_headers",
            "include_auth",
            "include_common",
            "include_cookies",
            "include_user_agent",
            "max_headers",
            "min_headers",
            "type",
        ]

    def validate(self, data: dict[str, str]) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class GenericHTTPHeaderGenerator(HTTPHeaderGenerator):
    """通用HTTP头生成器注册版本"""

    def generate_single(
        self, context: Optional[GenerationContext] = None
    ) -> dict[str, str]:
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
            "type",
            "include_common",
            "include_user_agent",
            "include_cookies",
            "include_auth",
            "custom_headers",
            "min_headers",
            "max_headers",
        ]

    def validate(self, data: dict[str, str]) -> bool:
        """校验HTTP头"""
        return self.validator.validate(data)
