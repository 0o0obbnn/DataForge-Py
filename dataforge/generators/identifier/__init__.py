"""
标识类生成器模块
"""

from .bankcard import GenericBankCardGenerator
from .drivers_license import GenericDriverLicenseGenerator
from .id import (
    GenericBusinessNumberGenerator,
    GenericULIDGenerator,
    GenericUUIDGenerator,
)
from .lei import LEICodeGenerator
from .logistics import GenericTrackingNumberGenerator, GenericWaybillGenerator
from .organization_code import ChineseOrganizationCodeGenerator
from .passport import GenericPassportGenerator
from .social_insurance import ChineseSocialInsuranceGenerator
from .uscc import ChineseUSCCGenerator
from .visa import GenericVisaGenerator

__all__ = [
    "GenericUUIDGenerator",
    "GenericULIDGenerator",
    "GenericBusinessNumberGenerator",
    "ChineseUSCCGenerator",
    "ChineseOrganizationCodeGenerator",
    "ChineseSocialInsuranceGenerator",
    "LEICodeGenerator",
    "GenericBankCardGenerator",
    "GenericPassportGenerator",
    "GenericDriverLicenseGenerator",
    "GenericTrackingNumberGenerator",
    "GenericWaybillGenerator",
    "GenericVisaGenerator",
]
