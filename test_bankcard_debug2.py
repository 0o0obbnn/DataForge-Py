from dataforge.generators.identifier.bankcard import BankCardValidator

validator = BankCardValidator()

test_card = "6222021234567890"
print(f"Testing card: {test_card}")
print(f"Length: {len(test_card)}")

# Test with different strict values
print(f"validate(card): {validator.validate(test_card)}")
print(f"validate(card, strict=False): {validator.validate(test_card, strict=False)}")
print(f"validate(card, strict=True): {validator.validate(test_card, strict=True)}")

# Check if it's a valid BIN
print(f"_is_valid_bin: {validator._is_valid_bin(test_card)}")

# Check Luhn
print(f"_validate_luhn: {validator._validate_luhn(test_card)}")
