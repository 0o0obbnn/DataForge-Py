"""
Luhn算法工具模块

提供Luhn校验算法相关功能，用于验证银行卡号、IMEI等校验码
"""


def calculate_luhn_checksum(number: str) -> int:
    """
    计算Luhn校验和

    Args:
        number: 需要校验的数字字符串（不带校验位）

    Returns:
        校验和（取模10后的结果）
    """
    def digits_of(n: str | int) -> list[int]:
        """将数字转换为各位数字列表"""
        return [int(d) for d in str(n)]

    digits = digits_of(number)
    odd_digits = digits[-1::-2]  # 从右数第1,3,5...位
    even_digits = digits[-2::-2]  # 从右数第2,4,6...位

    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))

    return checksum % 10


def calculate_luhn_check_digit(number: str) -> int:
    """
    计算Luhn校验位

    Args:
        number: 基础数字字符串（不带校验位）

    Returns:
        应该添加的校验位（0-9）
    """
    # 先计算不带校验位的校验和
    checksum = calculate_luhn_checksum(number + "0")
    return (10 - checksum % 10) % 10


def validate_luhn(number: str) -> bool:
    """
    验证Luhn校验码

    Args:
        number: 完整的数字字符串（包含校验位）

    Returns:
        是否通过Luhn校验
    """
    return calculate_luhn_checksum(number) == 0


def calculate_luhn_check_digit_str(number: str) -> str:
    """
    计算Luhn校验位（返回字符串格式）

    Args:
        number: 基础数字字符串（不带校验位）

    Returns:
        应该添加的校验位（字符串格式）
    """
    return str(calculate_luhn_check_digit(number))
