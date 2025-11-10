from dataforge.generators.identifier.bankcard import BankCardGenerator
from dataforge.core.generator import GeneratorConfig

config = GeneratorConfig(generator_type="bankcard", parameters={})
generator = BankCardGenerator(config)

card = "6222021234567890"
result = generator.validate(card)
print(f"Card: {card}")
print(f"Length: {len(card)}")
print(f"Is digit: {card.isdigit()}")
print(f"Validate result: {result}")

# Check if validator exists
if hasattr(generator, 'validator'):
    print(f"Has validator: True")
    validator_result = generator.validator.validate(card, strict=False)
    print(f"Validator result (strict=False): {validator_result}")
else:
    print(f"Has validator: False")
