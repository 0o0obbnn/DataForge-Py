from dataforge.generators.identifier.bankcard import BankCardGenerator, BankCardValidator
from dataforge.core.generator import GeneratorConfig

# Test with generator
config = GeneratorConfig(generator_type="bankcard", parameters={})
generator = BankCardGenerator(config)

test_card = "6222021234567890"
print(f"Testing card: {test_card}")
print(f"Length: {len(test_card)}")

# Test generator.validate()
result = generator.validate(test_card)
print(f"generator.validate(): {result}")

# Test validator directly
validator = generator.validator
print(f"\nValidator tests:")
print(f"validate(card) [default]: {validator.validate(test_card)}")
print(f"validate(card, strict=False): {validator.validate(test_card, strict=False)}")
print(f"validate(card, strict=True): {validator.validate(test_card, strict=True)}")

# Check internals
print(f"\n_is_valid_bin: {validator._is_valid_bin(test_card)}")
print(f"_validate_luhn: {validator._validate_luhn(test_card)}")

# Check what the default strict value is
import inspect
sig = inspect.signature(validator.validate)
print(f"\nvalidate signature: {sig}")
print(f"strict default: {sig.parameters['strict'].default}")
