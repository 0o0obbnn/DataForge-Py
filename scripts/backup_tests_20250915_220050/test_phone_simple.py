from dataforge.core.generator import GeneratorConfig
from dataforge.generators.contact.phone import (
    GenericPhoneNumberGenerator,
    PhoneNumberGenerator,
)

# 创建配置
config = GeneratorConfig(
    generator_type="phone", parameters={"type": "MOBILE", "format": "STANDARD"}
)

# 创建生成器 - 明确使用具体类型注解
phone_generator: PhoneNumberGenerator = GenericPhoneNumberGenerator(config)

# 生成号码
phone = phone_generator.generate()
print(f"生成的号码: {phone}")

# 验证号码
print(f"校验结果: {phone_generator.validate(phone)}")

# 获取号码类型
print(f"号码类型: {phone_generator.get_number_type(phone)}")
