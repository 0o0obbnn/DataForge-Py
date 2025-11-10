# g:\nifa\data_forge_py\tests\test_basic_generators.py
from dataforge.core.factory import default_factory
from dataforge.core.generator import GeneratorConfig
from dataforge.generators.basic.age import AgeGenerator
from dataforge.generators.basic.email import EmailGenerator
from dataforge.generators.basic.gender import GenderGenerator
from dataforge.generators.basic.idcard import IDCardGenerator
from dataforge.generators.basic.name import NameGenerator
from dataforge.generators.basic.phone import PhoneNumberGenerator

# 注册所有生成器，以便工厂可以创建它们
# 在实际应用中，这通常通过插件或自动发现机制完成
# 为了测试，我们在这里手动导入
_ = [
    NameGenerator,
    AgeGenerator,
    GenderGenerator,
    PhoneNumberGenerator,
    EmailGenerator,
    IDCardGenerator,
]


def test_name_generator():
    """测试姓名生成器"""
    config = GeneratorConfig(generator_type="name", parameters={})
    generator = default_factory.create_generator(config)
    name = generator.generate()
    assert isinstance(name, str)
    assert 2 <= len(name) <= 4
    assert generator.validate(name)

    # 测试带参数的生成
    config_male = GeneratorConfig(
        generator_type="name", parameters={"gender": "male", "length": 3}
    )
    generator_male = default_factory.create_generator(config_male)
    male_name = generator_male.generate()
    assert 2 <= len(male_name) <= 4  # 姓名长度可以是2-4个字符
    assert generator_male.validate(male_name)


def test_age_generator():
    """测试年龄生成器"""
    config = GeneratorConfig(generator_type="age", parameters={"min": 20, "max": 30})
    generator = default_factory.create_generator(config)
    age = generator.generate()
    assert isinstance(age, int)
    assert 20 <= age <= 30
    assert generator.validate(age)


def test_gender_generator():
    """测试性别生成器"""
    config = GeneratorConfig(generator_type="gender", parameters={})
    generator = default_factory.create_generator(config)
    gender = generator.generate()
    assert gender in ["Male", "Female"]
    assert generator.validate(gender)


def test_phone_number_generator():
    """测试手机号码生成器"""
    config = GeneratorConfig(generator_type="phone", parameters={})
    generator = default_factory.create_generator(config)
    phone = generator.generate()
    assert isinstance(phone, str)
    # 手机号可能包含空格格式，验证清理后的长度
    clean_phone = phone.replace(" ", "")
    assert len(clean_phone) == 11
    assert clean_phone.isdigit()
    assert generator.validate(phone)

    # 测试指定号码类型
    config_mobile = GeneratorConfig(
        generator_type="phone", parameters={"type": "MOBILE"}
    )
    generator_mobile = default_factory.create_generator(config_mobile)
    phone_mobile = generator_mobile.generate()
    assert generator_mobile.validate(phone_mobile)
    # 清理格式后验证是手机号
    clean_phone = phone_mobile.replace(" ", "")
    assert clean_phone.startswith(("13", "14", "15", "17", "18", "19"))


def test_email_generator():
    """测试邮箱生成器"""
    config = GeneratorConfig(generator_type="email", parameters={})
    generator = default_factory.create_generator(config)
    email = generator.generate()
    assert isinstance(email, str)
    assert "@" in email
    assert "." in email.split("@")[1]
    assert generator.validate(email)

    # 测试指定域名
    config_custom = GeneratorConfig(
        generator_type="email", parameters={"domains": "test.com"}
    )
    generator_custom = default_factory.create_generator(config_custom)
    email_custom = generator_custom.generate()
    assert email_custom.endswith("@test.com")


def test_id_card_generator():
    """测试身份证号码生成器"""
    config = GeneratorConfig(generator_type="idcard", parameters={})
    generator = default_factory.create_generator(config)
    id_card = generator.generate()
    assert isinstance(id_card, str)
    assert len(id_card) == 18
    assert generator.validate(id_card)

    # 测试根据年龄生成
    config_age = GeneratorConfig(generator_type="idcard", parameters={"age": 25})
    generator_age = default_factory.create_generator(config_age)
    id_card_age = generator_age.generate()
    assert generator_age.validate(id_card_age)
    birth_year = int(id_card_age[6:10])
    from datetime import datetime

    current_year = datetime.now().year
    assert current_year - birth_year == 25

    # 测试根据性别生成
    config_gender = GeneratorConfig(
        generator_type="idcard", parameters={"gender": "female"}
    )
    generator_gender = default_factory.create_generator(config_gender)
    id_card_gender = generator_gender.generate()
    assert generator_gender.validate(id_card_gender)
    gender_digit = int(id_card_gender[16])
    assert gender_digit % 2 == 0
