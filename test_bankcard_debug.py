from dataforge.generators.identifier.bankcard import BankCardGenerator
from dataforge.core.generator import GeneratorConfig

config = GeneratorConfig(generator_type="bankcard", parameters={})
generator = BankCardGenerator(config)

test_card = "6222021234567890"
print(f"Testing card: {test_card}")
print(f"Length: {len(test_card)}")
print(f"Validate result: {generator.validate(test_card)}")

# Check validator directly
if hasattr(generator, 'validator'):
    print(f"Validator exists: {generator.validator}")
    print(f"Validator validate (strict=False): {generator.validator.validate(test_card, strict=False)}")
    print(f"Validator validate (strict=True): {generator.validator.validate(test_card, strict=True)}")
