"""
联系/通信类生成器模块
"""
from .communication import (
    GenericVerificationCodeGenerator,
    GenericFaxNumberGenerator,
    GenericURLGenerator,
    GenericFilePathGenerator,
    GenericMimeTypeGenerator
)

__all__ = [
    'GenericVerificationCodeGenerator',
    'GenericFaxNumberGenerator',
    'GenericURLGenerator',
    'GenericFilePathGenerator',
    'GenericMimeTypeGenerator'
]