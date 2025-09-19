"""
DataForge Generators Package

This package contains all the data generators organized by category:
- basic: Basic data types (names, IDs, etc.)
- contact: Contact information (emails, phones, addresses)
- finance: Financial data (bank accounts, credit cards, etc.)
- network: Network-related data (IPs, URLs, etc.)
- datetime: Date and time data
- text: Text and content generation
"""

# Import all generator modules to ensure registration
try:
    from . import basic
except ImportError:
    pass

try:
    from . import contact
except ImportError:
    pass

try:
    from . import finance
except ImportError:
    pass

try:
    from . import network
except ImportError:
    pass

try:
    from . import datetime
except ImportError:
    pass

try:
    from . import text
except ImportError:
    pass
