"""
多生成器协同测试
"""

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.integration
class TestMultiGeneratorCoordination:
    """多生成器协同测试类"""

    def test_generate_complete_profile(self):
        """测试生成完整用户档案"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所有需要的生成器
        from dataforge.generators.basic.address import AddressGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.contact.email import EmailGenerator
        from dataforge.generators.contact.phone import PhoneGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        registry.register("address", AddressGenerator)
        registry.register("email", EmailGenerator)
        registry.register("phone", PhoneGenerator)

        # 创建所有生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "gender": factory.create_generator(GeneratorConfig("gender", {})),
            "address": factory.create_generator(GeneratorConfig("address", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
        }

        # 生成完整档案
        profile = {
            "name": generators["name"].generate_single(),
            "age": generators["age"].generate_single(),
            "gender": generators["gender"].generate_single(),
            "address": generators["address"].generate_single(),
            "email": generators["email"].generate_single(),
            "phone": generators["phone"].generate_single(),
        }

        # 验证所有字段都已生成
        assert all(v is not None for v in profile.values())
        assert isinstance(profile["name"], str)
        assert isinstance(profile["age"], int)
        assert isinstance(profile["gender"], str)

    def test_batch_profile_generation(self):
        """测试批量生成用户档案"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)

        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "gender": factory.create_generator(GeneratorConfig("gender", {})),
        }

        # 批量生成10个档案
        profiles = []
        for _ in range(10):
            profile = {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
                "gender": generators["gender"].generate_single(),
            }
            profiles.append(profile)

        assert len(profiles) == 10
        assert all(p["name"] is not None for p in profiles)
        assert all(p["age"] is not None for p in profiles)
        assert all(p["gender"] is not None for p in profiles)

    def test_financial_data_generation(self):
        """测试生成金融数据"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.finance.bank_account import BankAccountGenerator
        from dataforge.generators.identifier.bankcard import BankCardGenerator

        registry.register("bankcard", BankCardGenerator)
        registry.register("bank_account", BankAccountGenerator)

        generators = {
            "bankcard": factory.create_generator(GeneratorConfig("bankcard", {})),
            "bank_account": factory.create_generator(
                GeneratorConfig("bank_account", {})
            ),
        }

        # 生成金融数据
        financial_data = {
            "bankcard": generators["bankcard"].generate_single(),
            "bank_account": generators["bank_account"].generate_single(),
        }

        assert financial_data["bankcard"] is not None
        assert financial_data["bank_account"] is not None

    def test_contact_info_generation(self):
        """测试生成联系信息"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.contact.email import EmailGenerator
        from dataforge.generators.contact.phone import PhoneGenerator

        registry.register("email", EmailGenerator)
        registry.register("phone", PhoneGenerator)

        generators = {
            "email": factory.create_generator(GeneratorConfig("email", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
        }

        # 生成多个联系方式
        contacts = []
        for _ in range(5):
            contact = {
                "email": generators["email"].generate_single(),
                "phone": generators["phone"].generate_single(),
            }
            contacts.append(contact)

        assert len(contacts) == 5
        assert all(c["email"] is not None for c in contacts)
        assert all(c["phone"] is not None for c in contacts)

    def test_identity_document_generation(self):
        """测试生成身份证件"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.identifier.id import IDGenerator
        from dataforge.generators.identifier.passport import PassportGenerator

        registry.register("id", IDGenerator)
        registry.register("passport", PassportGenerator)

        generators = {
            "id": factory.create_generator(GeneratorConfig("id", {})),
            "passport": factory.create_generator(GeneratorConfig("passport", {})),
        }

        # 生成身份证件
        documents = {
            "id_card": generators["id"].generate_single(),
            "passport": generators["passport"].generate_single(),
        }

        assert documents["id_card"] is not None
        assert documents["passport"] is not None

    def test_mixed_type_generation(self):
        """测试混合类型数据生成"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.advanced.datetime import (
            TimestampGenerator as DateTimeGenerator,
        )
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.uuid import UUIDGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("uuid", UUIDGenerator)
        registry.register("datetime", DateTimeGenerator)

        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "uuid": factory.create_generator(GeneratorConfig("uuid", {})),
            "datetime": factory.create_generator(GeneratorConfig("datetime", {})),
        }

        # 生成混合数据
        data = {
            "id": generators["uuid"].generate_single(),
            "name": generators["name"].generate_single(),
            "age": generators["age"].generate_single(),
            "created_at": generators["datetime"].generate_single(),
        }

        assert all(v is not None for v in data.values())

    def test_nested_data_structure(self):
        """测试嵌套数据结构生成"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.address import AddressGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.contact.email import EmailGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("address", AddressGenerator)
        registry.register("email", EmailGenerator)

        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "address": factory.create_generator(GeneratorConfig("address", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
        }

        # 生成嵌套结构
        user = {
            "personal_info": {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
            },
            "contact": {
                "email": generators["email"].generate_single(),
                "address": generators["address"].generate_single(),
            },
        }

        assert user["personal_info"]["name"] is not None
        assert user["personal_info"]["age"] is not None
        assert user["contact"]["email"] is not None
        assert user["contact"]["address"] is not None

    def test_generator_consistency(self):
        """测试生成器一致性"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        # 使用相同配置创建多个生成器
        config = GeneratorConfig("name", {"locale": "zh_CN"})
        gen1 = factory.create_generator(config)
        gen2 = factory.create_generator(config)

        # 生成数据
        names1 = gen1.generate_batch(10)
        names2 = gen2.generate_batch(10)

        # 验证数据格式一致
        assert len(names1) == len(names2) == 10
        assert all(isinstance(n, str) for n in names1)
        assert all(isinstance(n, str) for n in names2)
