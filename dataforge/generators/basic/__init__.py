"""
基础数据生成器模块
"""
from .idcard import ChineseIDCardGenerator
from .bankcard import ChineseBankCardGenerator
from .phone import ChinesePhoneGenerator
from .uscc import ChineseUSCCGenerator
from .address import ChineseAddressGenerator
from .name import ChineseNameGenerator
from .age import ChineseAgeGenerator
from .email import ChineseEmailGenerator
from .gender import ChineseGenderGenerator
from .license_plate import ChineseLicensePlateGenerator
from .company_name import ChineseCompanyNameGenerator

__all__ = [
    'ChineseIDCardGenerator',
    'ChineseBankCardGenerator', 
    'ChinesePhoneGenerator',
    'ChineseUSCCGenerator',
    'ChineseAddressGenerator',
    'ChineseNameGenerator',
    'ChineseAgeGenerator',
    'ChineseEmailGenerator',
    'ChineseGenderGenerator',
    'ChineseLicensePlateGenerator',
    'ChineseCompanyNameGenerator'
]