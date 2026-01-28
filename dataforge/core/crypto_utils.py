"""
加密学工具模块

提供密码学安全的随机数生成和相关算法工具
"""

import secrets
import string


def generate_random_string(
    length: int,
) -> str:
    """
    生成指定长度的随机数字字符串

    Args:
        length: 字符串长度

    Returns:
        随机数字字符串
    """
    return "".join(secrets.choice(string.digits) for _ in range(length))


def generate_random_alphanumeric(
    length: int,
    uppercase: bool = False,
) -> str:
    """
    生成指定长度的随机字母数字字符串

    Args:
        length: 字符串长度
        uppercase: 是否使用大写字母（默认小写）

    Returns:
        随机字母数字字符串
    """
    chars = string.ascii_uppercase if uppercase else string.ascii_lowercase
    return "".join(secrets.choice(chars + string.digits) for _ in range(length))


def generate_random_letters(
    length: int,
    uppercase: bool = False,
) -> str:
    """
    生成指定长度的随机字母字符串

    Args:
        length: 字符串长度
        uppercase: 是否使用大写字母（默认小写）

    Returns:
        随机字母字符串
    """
    chars = string.ascii_uppercase if uppercase else string.ascii_lowercase
    return "".join(secrets.choice(chars) for _ in range(length))


def generate_random_hex(
    length: int,
    uppercase: bool = False,
) -> str:
    """
    生成指定长度的随机十六进制字符串

    Args:
        length: 字符串长度
        uppercase: 是否使用大写字母（默认大写）

    Returns:
        随机十六进制字符串
    """
    chars = string.hexdigits.upper() if uppercase else string.hexdigits
    return "".join(secrets.choice(chars) for _ in range(length))
