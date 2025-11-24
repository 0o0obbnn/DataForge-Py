"""密码生成器模块。

提供安全的密码生成策略，支持复杂度配置和强度控制。
"""

import secrets
import string
from typing import Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorType,
)


class PasswordGenerator(DataGenerator):
    """密码生成器类。

    支持多种密码策略：
    - 强密码（包含大小写字母、数字、特殊字符）
    - 中等强度密码
    - 简单密码
    - 可自定义复杂度
    """

    def _setup(self) -> None:
        """初始化设置"""
        pass

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始密码"""
        complexity = self.parameters.get("complexity", "strong")
        length = self.parameters.get("length", 12)
        min_length = 6
        max_length = 64

        actual_length = max(min_length, min(max_length, length))

        if complexity == "simple":
            return self._generate_simple_password(actual_length)
        elif complexity == "medium":
            return self._generate_medium_password(actual_length)
        elif complexity == "strong":
            return self._generate_strong_password(actual_length)
        elif complexity == "custom":
            return self._generate_custom_password(actual_length)
        else:
            return self._generate_strong_password(actual_length)

    def _generate_simple_password(self, length: int) -> str:
        """生成简单密码。

        Args:
            length: 密码长度

        Returns:
            str: 简单密码
        """
        chars = string.ascii_lowercase + string.digits
        chars = self._filter_chars(chars)
        return "".join(secrets.choice(chars) for _ in range(length))

    def _generate_medium_password(self, length: int) -> str:
        """生成中等强度密码。

        Args:
            length: 密码长度

        Returns:
            str: 中等强度密码
        """
        chars = string.ascii_letters + string.digits
        chars = self._filter_chars(chars)
        return "".join(secrets.choice(chars) for _ in range(length))

    def _generate_strong_password(self, length: int) -> str:
        """生成强密码。

        Args:
            length: 密码长度

        Returns:
            str: 强密码
        """
        # 确保包含所有类型的字符
        password_chars = []

        # 添加大写字母
        if self.parameters.get("use_uppercase", True):
            uppercase = string.ascii_uppercase
            uppercase = self._filter_chars(uppercase)
            if uppercase:
                password_chars.append(secrets.choice(uppercase))

        # 添加小写字母
        if self.parameters.get("use_lowercase", True):
            lowercase = string.ascii_lowercase
            lowercase = self._filter_chars(lowercase)
            if lowercase:
                password_chars.append(secrets.choice(lowercase))

        # 添加数字
        if self.parameters.get("use_digits", True):
            digits = string.digits
            digits = self._filter_chars(digits)
            if digits:
                password_chars.append(secrets.choice(digits))

        # 添加特殊字符
        if self.parameters.get("use_special", True):
            special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            special = self._filter_chars(special)
            if special:
                password_chars.append(secrets.choice(special))

        # 填充剩余长度
        all_chars = ""
        if self.parameters.get("use_uppercase", True):
            all_chars += string.ascii_uppercase
        if self.parameters.get("use_lowercase", True):
            all_chars += string.ascii_lowercase
        if self.parameters.get("use_digits", True):
            all_chars += string.digits
        if self.parameters.get("use_special", True):
            all_chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        all_chars = self._filter_chars(all_chars)

        remaining_length = max(0, length - len(password_chars))
        for _ in range(remaining_length):
            if all_chars:
                password_chars.append(secrets.choice(all_chars))

        # 打乱顺序 (cryptographically secure)
        secrets.SystemRandom().shuffle(password_chars)

        return "".join(password_chars)

    def _generate_custom_password(self, length: int) -> str:
        """生成自定义模式密码。

        Args:
            length: 密码长度

        Returns:
            str: 自定义密码
        """
        pattern = self.parameters.get("pattern", "")
        if pattern:
            return self._apply_pattern(pattern, length)
        else:
            return self._generate_strong_password(length)

    def _filter_chars(self, chars: str) -> str:
        """过滤易混淆和歧义字符。

        Args:
            chars: 原始字符集

        Returns:
            str: 过滤后的字符集
        """
        if self.parameters.get("exclude_similar", False):
            # 排除易混淆字符
            exclude_chars = "Il1O0"
            chars = "".join(c for c in chars if c not in exclude_chars)

        if self.parameters.get("exclude_ambiguous", False):
            # 排除歧义字符
            exclude_chars = "\"`'\\|"
            chars = "".join(c for c in chars if c not in exclude_chars)

        return chars

    def _apply_pattern(self, pattern: str, length: int) -> str:
        """应用自定义模式生成密码。

        Args:
            pattern: 模式字符串
            length: 密码长度

        Returns:
            str: 按模式生成的密码
        """
        # 简单模式支持：
        # A = 大写字母, a = 小写字母, 9 = 数字, # = 特殊字符, * = 任意字符
        char_map = {
            "A": string.ascii_uppercase,
            "a": string.ascii_lowercase,
            "9": string.digits,
            "#": "!@#$%^&*()_+-=[]{}|;:,.<>?",
            "*": string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?",
        }

        if not pattern:
            return self._generate_strong_password(length)

        # 如果模式长度与要求长度不同，重复模式
        full_pattern = (pattern * ((length // len(pattern)) + 1))[:length]

        password = []
        for char in full_pattern:
            if char in char_map:
                password.append(secrets.choice(char_map[char]))
            else:
                password.append(char)

        return "".join(password)

    def validate(self, data: str) -> bool:
        """验证密码有效性。

        Args:
            data: 要验证的密码

        Returns:
            bool: 是否有效
        """
        if not isinstance(data, str):
            return False

        if not data:
            return False

        # 从生成器参数中获取长度配置
        min_length = self.parameters.get("length", 6)
        max_length = self.parameters.get("max_length", 64)

        if len(data) < min_length or len(data) > max_length:
            return False

        # 检查复杂度要求
        complexity = self.parameters.get("complexity", "strong")

        if complexity == "strong":
            # 强密码要求
            has_upper = any(c.isupper() for c in data)
            has_lower = any(c.islower() for c in data)
            has_digit = any(c.isdigit() for c in data)
            has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in data)

            if not (has_upper and has_lower and has_digit and has_special):
                return False

        elif complexity == "medium":
            # 中等密码要求
            has_letter = any(c.isalpha() for c in data)
            has_digit = any(c.isdigit() for c in data)

            if not (has_letter and has_digit):
                return False

        return True

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        # TODO: 根据实际参数更新此列表
        return []


# 注册生成器
register_generator("password")(PasswordGenerator)


@register_generator("password", ["密码"])
class GenericPasswordGenerator(PasswordGenerator):
    """通用password生成器注册版本"""

    pass
