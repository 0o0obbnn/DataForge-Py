from dataforge.generators.identifier.bankcard import BankCardGenerator
from dataforge.core.generator import GeneratorConfig

config = GeneratorConfig(generator_type="bankcard", parameters={})
generator = BankCardGenerator(config)

test_card = "6222021234567890"

# Add debug to see what's happening
print(f"hasattr(generator, 'validator'): {hasattr(generator, 'validator')}")
print(f"hasattr(generator.validator, 'validate'): {hasattr(generator.validator, 'validate')}")

# Call validate with debug
print(f"\nCalling generator.validate('{test_card}')...")
result = generator.validate(test_card)
print(f"Result: {result}")

# Try calling validator.validate directly
print(f"\nCalling generator.validator.validate('{test_card}')...")
result2 = generator.validator.validate(test_card)
print(f"Result: {result2}")

# Check if there's a different validate method
import inspect
print(f"\ngenerator.validate method: {inspect.getsourcefile(generator.validate)}")
print(f"generator.validate code:")
print(inspect.getsource(generator.validate))
