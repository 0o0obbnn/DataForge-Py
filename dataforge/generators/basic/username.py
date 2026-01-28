"""
用户名生成器

生成各种格式的用户名
"""

import secrets
import string

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorType,
)


@register_generator("username", aliases=["user", "用户名"])
class UsernameGenerator(DataGenerator[str]):
    """用户名生成器"""

    def _setup(self) -> None:
        """初始化用户名生成器参数"""
        self.prefix = self.parameters.get("prefix", "")
        self.suffix = self.parameters.get("suffix", "")
        self.min_length = self.parameters.get("min_length", 6)
        self.max_length = self.parameters.get("max_length", 16)
        self.include_numbers = self.parameters.get("include_numbers", True)
        self.include_underscores = self.parameters.get("include_underscores", True)
        self.style = self.parameters.get(
            "style", "random"
        )  # random, readable, email_style

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        """生成用户名"""
        if self.style == "readable":
            username = self._generate_readable_username()
        elif self.style == "email_style":
            username = self._generate_email_style_username()
        else:
            username = self._generate_random_username()

        return f"{self.prefix}{username}{self.suffix}"

    def _generate_random_username(self) -> str:
        """生成随机用户名"""
        # 计算实际长度（减去前缀和后缀）
        actual_min = max(3, self.min_length - len(self.prefix) - len(self.suffix))
        actual_max = max(
            actual_min, self.max_length - len(self.prefix) - len(self.suffix)
        )

        length = secrets.randbelow(actual_max - actual_min + 1) + actual_min

        # 构建字符集
        chars = string.ascii_lowercase
        if self.include_numbers:
            chars += string.digits
        if self.include_underscores:
            chars += "_"

        # 生成用户名（确保以字母开头）
        username = secrets.choice(string.ascii_lowercase)
        username += "".join(secrets.choice(chars) for _ in range(length - 1))

        return username

    def _generate_readable_username(self) -> str:
        """生成可读的用户名"""
        adjectives = [
            "happy",
            "lucky",
            "smart",
            "cool",
            "fast",
            "brave",
            "kind",
            "wise",
            "bright",
            "swift",
            "bold",
            "calm",
            "eager",
            "fair",
        ]
        nouns = [
            "cat",
            "dog",
            "fox",
            "bear",
            "lion",
            "tiger",
            "eagle",
            "wolf",
            "panda",
            "dragon",
            "phoenix",
            "hawk",
            "deer",
            "rabbit",
        ]

        adj = secrets.choice(adjectives)
        noun = secrets.choice(nouns)

        if self.include_numbers:
            number = secrets.randbelow(1000)
            return f"{adj}{noun}{number}"
        else:
            return f"{adj}{noun}"

    def _generate_email_style_username(self) -> str:
        """生成邮箱风格的用户名"""
        first_parts = [
            "john",
            "jane",
            "mike",
            "sarah",
            "david",
            "emma",
            "alex",
            "lisa",
            "tom",
            "mary",
            "chris",
            "anna",
            "james",
            "lucy",
            "robert",
            "emily",
        ]
        last_parts = [
            "smith",
            "johnson",
            "williams",
            "brown",
            "jones",
            "garcia",
            "miller",
            "davis",
            "rodriguez",
            "martinez",
            "hernandez",
            "lopez",
            "gonzalez",
        ]

        first = secrets.choice(first_parts)
        last = secrets.choice(last_parts)

        # 随机选择连接方式
        connector = secrets.choice([".", "_", ""])

        username = f"{first}{connector}{last}"

        if self.include_numbers:
            number = secrets.randbelow(100)
            username += str(number)

        return username

    def validate(self, data: str) -> bool:
        """验证用户名格式"""
        if not isinstance(data, str):
            return False

        if not data:
            return False

        # 检查长度
        if len(data) < self.min_length or len(data) > self.max_length:
            return False

        # 检查前缀和后缀
        if self.prefix and not data.startswith(self.prefix):
            return False
        if self.suffix and not data.endswith(self.suffix):
            return False

        # 检查字符集
        core_username = data[
            len(self.prefix) : (
                len(data) - len(self.suffix) if self.suffix else len(data)
            )
        ]

        if not core_username:
            return False

        # 必须以字母开头
        if not core_username[0].isalpha():
            return False

        # 检查允许的字符
        allowed_chars = set(string.ascii_letters + string.digits)
        if self.include_underscores:
            allowed_chars.add("_")
        if self.include_numbers:
            allowed_chars.update(string.digits)

        # 允许常见的用户名字符：字母、数字、下划线、点、连字符
        return all(c in allowed_chars or c in ".-" for c in core_username)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "prefix",
            "suffix",
            "min_length",
            "max_length",
            "include_numbers",
            "include_underscores",
            "style",
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)
