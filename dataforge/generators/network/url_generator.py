"""
URL生成器 - 完整URL地址生成
"""

import random  # TODO: Convert to secrets
import re
import secrets
from typing import TYPE_CHECKING, Any, Optional
from urllib.parse import urlencode

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


if TYPE_CHECKING:
    from ...core.generator import GeneratorConfig


class URLValidator(Validator):
    """Validator for URLs."""

    def validate(self, data: str) -> bool:
        """校验URL格式"""
        if not isinstance(data, str):
            return False

        try:
            # 基本URL格式验证
            url_pattern = r"^https?://[^\s/$.?#].[^\s]*$"
            return bool(re.match(url_pattern, data))
        except Exception:
            return False

    @property
    def error_message(self) -> str:
        return "Invalid URL format"


@register_generator("url", aliases=["uri", "link"])
class URLGenerator(DataGenerator[str]):
    """完整URL生成器"""

    def __init__(self, config: Optional["GeneratorConfig"] = None, **kwargs):
        """初始化URL生成器

        Args:
            config: 生成器配置对象
            **kwargs: 直接传入的参数，会转换为config
        """
        if config is None:
            from ...core.generator import GeneratorConfig

            config = GeneratorConfig(generator_type="url", parameters=kwargs)
        super().__init__(config)
        self.validator = URLValidator()

    def _setup(self) -> None:
        self.protocol = self.parameters.get(
            "protocol", "https"
        )  # http, https, ftp, ftps
        self.domain_type = self.parameters.get(
            "domain_type", "GENERIC"
        )  # GENERIC, COUNTRY, CUSTOM
        self.include_path = self.parameters.get("include_path", True)
        self.include_query = self.parameters.get("include_query", False)
        self.include_fragment = self.parameters.get("include_fragment", False)
        self.path_length = self.parameters.get("path_length", (1, 4))
        self.query_params_count = self.parameters.get("query_params_count", (1, 3))
        self.custom_base_url = self.parameters.get("custom_base_url", None)
        self.encode_special_chars = self.parameters.get("encode_special_chars", True)

        # URL组件配置
        self.path_style = self.parameters.get(
            "path_style", "REALISTIC"
        )  # REALISTIC, RANDOM, RESTFUL
        self.query_style = self.parameters.get(
            "query_style", "MIXED"
        )  # KEYWORD, RANDOM, MIXED

        # 常用路径片段
        self.common_paths = [
            "home",
            "about",
            "contact",
            "products",
            "services",
            "blog",
            "news",
            "gallery",
            "portfolio",
            "team",
            "pricing",
            "faq",
            "support",
            "download",
            "login",
            "register",
            "profile",
            "settings",
            "admin",
            "dashboard",
            "api",
            "v1",
            "v2",
            "v3",
            "docs",
            "help",
        ]

        # RESTful API路径
        self.restful_patterns = [
            "users",
            "posts",
            "articles",
            "comments",
            "categories",
            "tags",
            "orders",
            "customers",
            "products",
            "inventory",
            "payments",
            "reports",
        ]

        # 查询参数键
        self.query_keys = [
            "id",
            "page",
            "limit",
            "offset",
            "search",
            "q",
            "filter",
            "sort",
            "order",
            "category",
            "tag",
            "type",
            "status",
            "date",
            "from",
            "to",
            "lang",
            "locale",
            "version",
            "format",
            "callback",
            "token",
            "key",
        ]

        # 查询参数值
        self.query_values = [
            "1",
            "10",
            "20",
            "50",
            "100",
            "active",
            "inactive",
            "pending",
            "asc",
            "desc",
            "json",
            "xml",
            "html",
            "all",
            "recent",
            "popular",
            "2024",
            "2023",
            "latest",
            "featured",
            "recommended",
            "true",
            "false",
        ]

    def generate(self, context: Optional[GenerationContext] = None) -> str:
        """生成完整URL"""
        url_parts = []

        # 1. 协议部分
        protocol = self._get_protocol()
        url_parts.append(protocol)

        # 2. 域名部分
        if self.custom_base_url:
            domain = self.custom_base_url
        else:
            domain = self._generate_domain()
        url_parts.append(domain)

        # 3. 路径部分
        if self.include_path:
            path = self._generate_path()
            if path:
                url_parts.append(path)

        # 4. 查询参数部分
        if self.include_query:
            query = self._generate_query()
            if query:
                url_parts.append(f"?{query}")

        # 5. 片段标识符部分
        if self.include_fragment:
            fragment = self._generate_fragment()
            if fragment:
                url_parts.append(f"#{fragment}")

        return "".join(url_parts)

    def _get_protocol(self) -> str:
        """获取协议部分"""
        if isinstance(self.protocol, str):
            return f"{self.protocol}://"
        elif isinstance(self.protocol, list):
            return f"{secrets.choice(self.protocol)}://"
        else:
            return "https://"

    def _generate_domain(self) -> str:
        """生成域名部分"""
        if self.domain_type.upper() == "CUSTOM" and self.custom_base_url:
            return self.custom_base_url

        # 这里可以集成现有的DomainGenerator
        tlds = {
            "GENERIC": [".com", ".org", ".net", ".edu"],
            "COUNTRY": [".cn", ".us", ".uk", ".de", ".jp"],
        }

        tld_list = tlds.get(self.domain_type.upper(), tlds["GENERIC"])
        tld = secrets.choice(tld_list)

        # 生成域名主体
        import string

        length = secrets.randbelow(10) + 3
        domain_name = "".join(random.choices(string.ascii_lowercase, k=length))

        return f"{domain_name}{tld}"

    def _generate_path(self) -> str:
        """生成路径部分"""
        if not self.include_path:
            return ""

        segments_count = (
            secrets.randbelow(self.path_length[1] - self.path_length[0] + 1)
            + self.path_length[0]
        )
        if segments_count == 0:
            return ""

        segments = []

        if self.path_style.upper() == "RESTFUL":
            # RESTful API风格
            if segments_count >= 2:
                resource = secrets.choice(self.restful_patterns)
                segments.append(resource)

                # 添加ID或子资源
                if segments_count >= 3:
                    if (secrets.randbelow(1000000) / 1000000) < 0.5:
                        segments.append(str(secrets.randbelow(9999) + 1))
                        if segments_count >= 4:
                            sub_resource = secrets.choice(
                                ["comments", "likes", "shares"]
                            )
                            segments.append(sub_resource)
                    else:
                        segments.append(secrets.choice(["create", "update", "delete"]))
                else:
                    segments.append(str(secrets.randbelow(9999) + 1))
            else:
                segments.append(secrets.choice(self.restful_patterns))

        elif self.path_style.upper() == "REALISTIC":
            # 真实网站路径风格
            for _ in range(segments_count):
                segment = secrets.choice(self.common_paths)
                segments.append(segment)
        else:
            # 随机字符串路径
            import string

            for _ in range(segments_count):
                length = secrets.randbelow(6) + 3
                segment = "".join(
                    random.choices(string.ascii_lowercase + string.digits, k=length)
                )
                segments.append(segment)

        return "/" + "/".join(segments)

    def _generate_query(self) -> str:
        """生成查询参数"""
        if not self.include_query:
            return ""

        params_count = (
            secrets.randbelow(
                self.query_params_count[1] - self.query_params_count[0] + 1
            )
            + self.query_params_count[0]
        )
        if params_count == 0:
            return ""

        params = {}
        used_keys = set()

        for _ in range(params_count):
            # 确保生成唯一的key
            if self.query_style.upper() == "KEYWORD":
                # 从未使用的key中选择
                available_keys = [k for k in self.query_keys if k not in used_keys]
                if not available_keys:
                    # 如果所有key都用完了，重新开始
                    used_keys.clear()
                    available_keys = self.query_keys

                key = secrets.choice(available_keys)
                value = secrets.choice(self.query_values)
            elif self.query_style.upper() == "RANDOM":
                import string

                # 生成唯一的随机key
                while True:
                    key = "".join(
                        random.choices(
                            string.ascii_lowercase, k=secrets.randbelow(6) + 3
                        )
                    )
                    if key not in used_keys:
                        break

                value = "".join(
                    random.choices(
                        string.ascii_lowercase + string.digits,
                        k=secrets.randbelow(10) + 1,
                    )
                )
            else:  # MIXED
                if (secrets.randbelow(1000000) / 1000000) < 0.7:
                    # 从未使用的key中选择
                    available_keys = [k for k in self.query_keys if k not in used_keys]
                    if not available_keys:
                        # 如果所有key都用完了，重新开始
                        used_keys.clear()
                        available_keys = self.query_keys

                    key = secrets.choice(available_keys)
                    value = secrets.choice(self.query_values)
                else:
                    import string

                    # 生成唯一的随机key
                    while True:
                        key = "".join(
                            random.choices(
                                string.ascii_lowercase, k=secrets.randbelow(4) + 3
                            )
                        )
                        if key not in used_keys:
                            break

                    value = "".join(
                        random.choices(
                            string.ascii_lowercase + string.digits,
                            k=secrets.randbelow(8) + 1,
                        )
                    )

            params[key] = value
            used_keys.add(key)

        # 编码特殊字符
        if self.encode_special_chars:
            return urlencode(params)
        else:
            return "&".join(f"{k}={v}" for k, v in params.items())

    def _generate_fragment(self) -> str:
        """生成片段标识符"""
        fragments = [
            "top",
            "section1",
            "section2",
            "comments",
            "footer",
            "header",
            "about",
            "contact",
            "products",
            "services",
            "pricing",
            "features",
        ]

        if (secrets.randbelow(1000000) / 1000000) < 0.7:
            return secrets.choice(fragments)
        else:
            import string

            length = secrets.randbelow(8) + 3
            return "".join(random.choices(string.ascii_lowercase, k=length))

    def get_url_info(self, url: str) -> dict[str, Any]:
        """解析URL信息"""
        from urllib.parse import parse_qs, urlparse

        try:
            parsed = urlparse(url)
            return {
                "protocol": parsed.scheme,
                "domain": parsed.netloc,
                "path": parsed.path,
                "query": parse_qs(parsed.query),
                "fragment": parsed.fragment,
                "is_secure": parsed.scheme == "https",
            }
        except Exception:
            return {}

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
            "custom_base_url",
            "domain_type",
            "encode_special_chars",
            "include_fragment",
            "include_path",
            "include_query",
            "path_length",
            "path_style",
            "protocol",
            "query_params_count",
            "query_style",
        ]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class GenericURLGenerator(URLGenerator):
    """通用URL生成器注册版本"""

    def __init__(self, config: Optional["GeneratorConfig"] = None, **kwargs):
        """初始化通用URL生成器"""
        super().__init__(config, **kwargs)

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
        return []

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return isinstance(data, str) and bool(data.strip())
