"""
Contact Information Generators

This module contains generators for contact-related data:
- Phone numbers (mobile and landline)
- Email addresses
- Physical addresses
- Postal codes
"""

# Import all contact generators to ensure registration
try:
    from .phone import ChinesePhoneGenerator
except ImportError:
    pass

try:
    from .landline import LandlineGenerator, FaxNumberGenerator, TollFreeNumberGenerator, ExtensionGenerator
except ImportError:
    pass

try:
    from .email import EmailGenerator
except ImportError:
    pass

try:
    from .address import ChineseAddressGenerator
except ImportError:
    pass
