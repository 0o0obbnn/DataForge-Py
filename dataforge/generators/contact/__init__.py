"""
联系方式生成器模块
"""

# 导入所有联系方式生成器以触发注册
from . import communication, email, landline, phone

__all__ = ["phone", "email", "landline", "communication"]
