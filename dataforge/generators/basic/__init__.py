"""
Basic data generators

This module contains generators for basic personal and business information:
- Chinese names
- ID cards
- Company names
- Basic identification data
"""

# Import all basic generators to ensure registration
try:
    from .name import ChineseNameGenerator
except ImportError:
    pass

try:
    from .idcard import ChineseIDCardGenerator
except ImportError:
    pass

try:
    from .company import ChineseCompanyNameGenerator
except ImportError:
    pass

try:
    from .uscc import USCCGenerator
except ImportError:
    pass
