"""
认证生成器模块
"""

try:
    # 导入所有认证生成器以触发注册
    from . import (
        auth_token,
        email_verification,
        session_id,
        sms_verification,
    )
except ImportError as e:
    print(f"警告: 部分认证生成器导入失败: {e}")

__all__ = [
    "auth_token",
    "email_verification",
    "session_id",
    "sms_verification",
]