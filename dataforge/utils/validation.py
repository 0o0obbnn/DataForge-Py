"""Data validation utilities for DataForge.

This module provides validation functions for generated data and configuration.
"""

import re
from typing import Any, Callable


def validate_data(data: Any, data_type: str, **kwargs: Any) -> bool:
    """Validate generated data against expected format.

    Args:
        data: The data to validate
        data_type: Type of data (e.g., 'phone', 'email', 'idcard')
        **kwargs: Additional validation parameters

    Returns:
        True if data is valid, False otherwise
    """
    if data is None:
        return False

    validators: dict[str, Callable[..., bool]] = {
        "phone": _validate_phone,
        "email": _validate_email,
        "idcard": _validate_idcard,
        "bankcard": _validate_bankcard,
        "uscc": _validate_uscc,
    }

    validator = validators.get(data_type)
    if not validator:
        return True  # No specific validator, assume valid

    return validator(data, **kwargs)


def validate_config(config: dict[str, Any]) -> bool:
    """Validate configuration dictionary.

    Args:
        config: Configuration dictionary to validate

    Returns:
        True if config is valid, False otherwise
    """
    required_fields = ["generators", "output"]

    for field in required_fields:
        if field not in config:
            return False

    # Validate generators config
    if not isinstance(config["generators"], dict):
        return False

    # Validate output config
    if not isinstance(config["output"], dict):
        return False

    return True


def _validate_phone(phone: str, **kwargs: Any) -> bool:
    """Validate Chinese phone number format."""
    if not isinstance(phone, str):
        return False

    # Chinese mobile phone pattern
    mobile_pattern = r"^1[3-9]\d{9}$"
    # Chinese landline pattern
    landline_pattern = r"^0\d{2,3}-?\d{7,8}$"

    return bool(re.match(mobile_pattern, phone) or re.match(landline_pattern, phone))


def _validate_email(email: str, **kwargs: Any) -> bool:
    """Validate email format."""
    if not isinstance(email, str):
        return False

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def _validate_idcard(idcard: str, **kwargs: Any) -> bool:
    """Validate Chinese ID card number."""
    if not isinstance(idcard, str) or len(idcard) != 18:
        return False

    # Check format
    pattern = r"^\d{17}[\dXx]$"
    if not re.match(pattern, idcard):
        return False

    # TODO: Add checksum validation
    return True


def _validate_bankcard(card: str, **kwargs: Any) -> bool:
    """Validate bank card number using Luhn algorithm."""
    if not isinstance(card, str):
        return False

    # Remove spaces and non-digits
    card = re.sub(r"\D", "", card)

    if len(card) < 13 or len(card) > 19:
        return False

    # Luhn algorithm
    def luhn_checksum(card_num):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    return luhn_checksum(card) == 0


def _validate_uscc(uscc: str, **kwargs: Any) -> bool:
    """Validate Unified Social Credit Code."""
    if not isinstance(uscc, str) or len(uscc) != 18:
        return False

    # USCC pattern
    pattern = r"^[0-9A-HJ-NPQRTUWXY]{2}\d{6}[0-9A-HJ-NPQRTUWXY]{9}[0-9A-HJ-NPQRTUWXY]$"
    return bool(re.match(pattern, uscc))
