"""
标识类生成器模块
"""

from .bankcard import GenericBankCardGenerator
from .china_id_types import (
    ForeignerResidenceGenerator,
    ForeignPassportGenerator,
    ForeignPermanentResidenceGenerator,
    HongKongIDGenerator,
    HouseholdRegisterGenerator,
    MacauIDGenerator,
    OfficerCardGenerator,
    PoliceOfficerCardGenerator,
    SoldierCardGenerator,
    TaiwanIDGenerator,
    TemporaryIDCardGenerator,
    WujingCardGenerator,
)
from .drivers_license import GenericDriverLicenseGenerator
from .hk_mo_tw_id import GenericHkMoTwIdGenerator
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
    "GenericHkMoTwIdGenerator",
    "HouseholdRegisterGenerator",
    "OfficerCardGenerator",
    "SoldierCardGenerator",
    "WujingCardGenerator",
    "TemporaryIDCardGenerator",
    "ForeignerResidenceGenerator",
    "PoliceOfficerCardGenerator",
    "HongKongIDGenerator",
    "MacauIDGenerator",
    "TaiwanIDGenerator",
    "ForeignPermanentResidenceGenerator",
    "ForeignPassportGenerator",
]
