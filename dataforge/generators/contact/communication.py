"""
通讯方式生成器

支持生成电话、邮箱、社交媒体等多种通讯方式
"""

import secrets
from typing import Any, Union

from ...core.factory import register_generator
from ...core.generator import DataGenerator, GenerationContext
from ...core.types import GeneratorType


@register_generator("communication", aliases=["contact_method"])
class CommunicationGenerator(DataGenerator[Union[str, dict[str, Any]]]):
    """通讯方式生成器"""

    def _setup(self) -> None:
        """初始化通讯方式生成器参数"""
        self.comm_type = self.parameters.get(
            "type", "mixed"
        )  # phone, email, social_media, mixed
        self.include_label = self.parameters.get("include_label", False)

        # 社交媒体平台
        self.social_platforms = [
            "WeChat",
            "QQ",
            "Weibo",
            "Douyin",
            "Xiaohongshu",
            "Twitter",
            "Facebook",
            "Instagram",
            "LinkedIn",
            "WhatsApp",
        ]

    def _generate_raw(
        self, context: GenerationContext | None = None
    ) -> str | dict[str, Any]:
        """生成通讯方式数据"""
        if self.comm_type == "phone":
            return self._generate_phone()
        elif self.comm_type == "email":
            return self._generate_email()
        elif self.comm_type == "social_media":
            return self._generate_social_media()
        else:
            # mixed - 随机选择一种
            comm_type = secrets.choice(["phone", "email", "social_media"])
            if comm_type == "phone":
                return self._generate_phone()
            elif comm_type == "email":
                return self._generate_email()
            else:
                return self._generate_social_media()

    def _generate_phone(self) -> str | dict[str, str]:
        """生成电话号码"""
        # 生成手机号
        prefixes = [
            "130",
            "131",
            "132",
            "133",
            "134",
            "135",
            "136",
            "137",
            "138",
            "139",
            "150",
            "151",
            "152",
            "153",
            "155",
            "156",
            "157",
            "158",
            "159",
            "180",
            "181",
            "182",
            "183",
            "184",
            "185",
            "186",
            "187",
            "188",
            "189",
        ]
        prefix = secrets.choice(prefixes)
        suffix = "".join(str(secrets.randbelow(10)) for _ in range(8))
        phone = prefix + suffix

        if self.include_label:
            return {"type": "phone", "value": phone, "label": "手机"}
        return phone

    def _generate_email(self) -> str | dict[str, str]:
        """生成邮箱地址"""
        # 生成用户名
        username_length = secrets.randbelow(8) + 5
        username = "".join(
            secrets.choice("abcdefghijklmnopqrstuvwxyz0123456789")
            for _ in range(username_length)
        )

        # 选择域名
        domains = [
            "qq.com",
            "163.com",
            "126.com",
            "gmail.com",
            "outlook.com",
            "sina.com",
            "sohu.com",
            "foxmail.com",
        ]
        domain = secrets.choice(domains)

        email = f"{username}@{domain}"

        if self.include_label:
            return {"type": "email", "value": email, "label": "邮箱"}
        return email

    def _generate_social_media(self) -> str | dict[str, str]:
        """生成社交媒体账号"""
        platform = secrets.choice(self.social_platforms)

        # 生成账号ID
        if platform in ["WeChat", "QQ"]:
            # 数字或字母数字组合
            if secrets.randbelow(2) == 0:
                account = "".join(
                    str(secrets.randbelow(10)) for _ in range(secrets.randbelow(5) + 6)
                )
            else:
                account = "".join(
                    secrets.choice("abcdefghijklmnopqrstuvwxyz0123456789_")
                    for _ in range(secrets.randbelow(8) + 6)
                )
        else:
            # 字母数字组合
            account = "".join(
                secrets.choice("abcdefghijklmnopqrstuvwxyz0123456789_")
                for _ in range(secrets.randbelow(10) + 5)
            )

        if self.include_label:
            return {
                "type": "social_media",
                "value": account,
                "platform": platform,
                "label": platform,
            }
        return f"{platform}:{account}"

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证通讯方式数据"""
        if isinstance(data, dict):
            return "type" in data and "value" in data
        elif isinstance(data, str):
            return len(data) > 0
        return False

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT

    @property
    def supported_parameters(self) -> list[str]:
        return ["type", "include_label"]

    def generate_single(
        self, context: GenerationContext | None = None
    ) -> str | dict[str, Any]:
        """生成单个数据项"""
        return self._generate_raw(context)
