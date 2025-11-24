"""
金融生成器模块
"""

try:
    # 导入所有金融生成器以触发注册
    from . import (
        advanced,
        bank_account,
        bond,
        crypto,
        crypto_generator,
        fund,
        future,
        stock,
        streaming,
    )
except ImportError as e:
    print(f"警告: 部分金融生成器导入失败: {e}")

__all__ = [
    "advanced",
    "bank_account",
    "bond",
    "crypto_generator",
    "crypto",
    "fund",
    "future",
    "stock",
    "streaming",
]
