import json
from typing import Any

from dataforge import GenerationContext, GeneratorConfig, default_factory

# Ensure username generator module is imported and registered
from dataforge.generators.basic.username import UsernameGenerator


def generate_record() -> dict[str, Any]:
	configs = [
		GeneratorConfig(generator_type="name", parameters={}),
		GeneratorConfig(generator_type="idcard", parameters={}),
		GeneratorConfig(generator_type="phone", parameters={"type": "MOBILE", "format": "COMPACT"}),
		GeneratorConfig(generator_type="email", parameters={"domain_type": "REAL"}),
		GeneratorConfig(generator_type="company_name", parameters={}),
		GeneratorConfig(generator_type="uscc", parameters={}),
	]

	context = GenerationContext()
	result = default_factory.generate_batch_with_relations(configs, context)

	# Generate landline separately
	landline_config = GeneratorConfig(generator_type="phone", parameters={"type": "LANDLINE", "format": "STANDARD"})
	landline = default_factory.create_generator(landline_config).generate()

	# Generate username directly
	username_gen = UsernameGenerator(GeneratorConfig(generator_type="username", parameters={"length": 10, "format": "alpha_numeric"}))
	username_value = username_gen.generate()

	return {
		"name": result.get("name"),
		"idcard": result.get("idcard"),
		"mobile": result.get("phone"),
		"landline": landline,
		"email": result.get("email"),
		"company_name": result.get("company_name"),
		"uscc": result.get("uscc"),
		"username": username_value,
	}


def main() -> None:
	record = generate_record()
	print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
	main()
