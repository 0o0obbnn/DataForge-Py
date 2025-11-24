"""
数据生成器模块
"""

# 导入所有生成器模块以触发注册
try:
    from . import (
        advanced,
        auth,
        basic,
        contact,
        finance,
        identifier,
        network,
        numeric,
        text,
    )

    # datetime模块暂未实现，跳过导入
except ImportError as e:
    # 某些模块可能不可用，跳过
    print(f"警告: 部分生成器模块导入失败: {e}")

__all__ = [
    "basic",
    "contact",
    "finance",
    "identifier",
    "network",
    "numeric",
    "text",
    "advanced",
    "auth",
]
