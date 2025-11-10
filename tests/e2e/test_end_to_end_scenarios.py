"""
端到端场景测试
"""

import json

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.e2e
class TestEndToEndScenarios:
    """端到端场景测试类"""

    def test_complete_user_profile_generation(self):
        """测试完整用户档案生成流程"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        # 注册所有需要的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        from dataforge.generators.basic.address import AddressGenerator
        from dataforge.generators.contact.email import EmailGenerator
        from dataforge.generators.contact.phone import PhoneGenerator
        from dataforge.generators.basic.uuid import UUIDGenerator
        
        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        registry.register("address", AddressGenerator)
        registry.register("email", EmailGenerator)
        registry.register("phone", PhoneGenerator)
        registry.register("uuid", UUIDGenerator)
        
        # 创建生成器
        generators = {
            "uuid": factory.create_generator(GeneratorConfig("uuid", {})),
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {"min": 18, "max": 65})),
            "gender": factory.create_generator(GeneratorConfig("gender", {})),
            "address": factory.create_generator(GeneratorConfig("address", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
        }
        
        # 生成完整用户档案
        user_profile = {
            "id": generators["uuid"].generate_single(),
            "name": generators["name"].generate_single(),
            "age": generators["age"].generate_single(),
            "gender": generators["gender"].generate_single(),
            "address": generators["address"].generate_single(),
            "email": generators["email"].generate_single(),
            "phone": generators["phone"].generate_single(),
        }
        
        # 验证所有字段
        assert user_profile["id"] is not None
        assert user_profile["name"] is not None
        assert 18 <= user_profile["age"] <= 65
        assert user_profile["gender"] in ["男", "女", "Male", "Female", "M", "F"]
        assert user_profile["address"] is not None
        assert user_profile["email"] is not None
        assert user_profile["phone"] is not None
        
        # 验证可以序列化为JSON
        json_str = json.dumps(user_profile, ensure_ascii=False, default=str)
        assert len(json_str) > 0

    def test_batch_user_generation_workflow(self):
        """测试批量用户生成工作流"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.contact.email import EmailGenerator
        
        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("email", EmailGenerator)
        
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
        }
        
        # 批量生成100个用户
        batch_size = 100
        users = []
        for _ in range(batch_size):
            user = {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
                "email": generators["email"].generate_single(),
            }
            users.append(user)
        
        # 验证
        assert len(users) == batch_size
        assert all(u["name"] is not None for u in users)
        assert all(u["age"] is not None for u in users)
        assert all(u["email"] is not None for u in users)
        
        # 验证唯一性
        emails = [u["email"] for u in users]
        unique_emails = set(emails)
        assert len(unique_emails) > batch_size * 0.9  # 至少90%唯一

    def test_financial_data_generation_workflow(self):
        """测试金融数据生成工作流"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.identifier.bankcard import BankCardGenerator
        from dataforge.generators.finance.bank_account import BankAccountGenerator
        from dataforge.generators.basic.name import NameGenerator
        
        registry.register("bankcard", BankCardGenerator)
        registry.register("bank_account", BankAccountGenerator)
        registry.register("name", NameGenerator)
        
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "bankcard": factory.create_generator(GeneratorConfig("bankcard", {})),
            "bank_account": factory.create_generator(GeneratorConfig("bank_account", {})),
        }
        
        # 生成金融数据
        financial_data = {
            "account_holder": generators["name"].generate_single(),
            "bank_card": generators["bankcard"].generate_single(),
            "account_number": generators["bank_account"].generate_single(),
        }
        
        # 验证
        assert financial_data["account_holder"] is not None
        assert financial_data["bank_card"] is not None
        assert financial_data["account_number"] is not None

    def test_identity_verification_workflow(self):
        """测试身份验证工作流"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.identifier.id import IDGenerator
        from dataforge.generators.contact.phone import PhoneGenerator
        
        registry.register("name", NameGenerator)
        registry.register("id", IDGenerator)
        registry.register("phone", PhoneGenerator)
        
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "id": factory.create_generator(GeneratorConfig("id", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
        }
        
        # 生成身份验证数据
        identity_data = {
            "name": generators["name"].generate_single(),
            "id_number": generators["id"].generate_single(),
            "phone": generators["phone"].generate_single(),
        }
        
        # 验证
        assert identity_data["name"] is not None
        assert identity_data["id_number"] is not None
        assert identity_data["phone"] is not None
        
        # 验证身份证格式
        id_number = identity_data["id_number"]
        assert len(str(id_number)) in [15, 18]

    def test_multi_locale_generation(self):
        """测试多地区数据生成"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.address import AddressGenerator
        
        registry.register("name", NameGenerator)
        registry.register("address", AddressGenerator)
        
        locales = ["zh_CN", "en_US"]
        
        for locale in locales:
            name_gen = factory.create_generator(
                GeneratorConfig("name", {"locale": locale})
            )
            address_gen = factory.create_generator(
                GeneratorConfig("address", {"locale": locale})
            )
            
            # 生成数据
            name = name_gen.generate_single()
            address = address_gen.generate_single()
            
            # 验证
            assert name is not None
            assert address is not None
            
            print(f"\n{locale}:")
            print(f"  姓名: {name}")
            print(f"  地址: {address}")

    def test_data_export_json(self):
        """测试数据导出为JSON"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        
        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
        }
        
        # 生成数据
        users = []
        for _ in range(10):
            user = {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
            }
            users.append(user)
        
        # 导出为JSON
        json_output = json.dumps(users, ensure_ascii=False, indent=2, default=str)
        
        # 验证
        assert len(json_output) > 0
        
        # 验证可以解析回来
        parsed_users = json.loads(json_output)
        assert len(parsed_users) == 10

    def test_complex_nested_data(self):
        """测试复杂嵌套数据生成"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.contact.email import EmailGenerator
        from dataforge.generators.basic.address import AddressGenerator
        
        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("email", EmailGenerator)
        registry.register("address", AddressGenerator)
        
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
            "address": factory.create_generator(GeneratorConfig("address", {})),
        }
        
        # 生成复杂嵌套数据
        company_data = {
            "company_name": "测试公司",
            "employees": [
                {
                    "personal_info": {
                        "name": generators["name"].generate_single(),
                        "age": generators["age"].generate_single(),
                    },
                    "contact": {
                        "email": generators["email"].generate_single(),
                        "address": generators["address"].generate_single(),
                    }
                }
                for _ in range(5)
            ]
        }
        
        # 验证
        assert company_data["company_name"] is not None
        assert len(company_data["employees"]) == 5
        for emp in company_data["employees"]:
            assert emp["personal_info"]["name"] is not None
            assert emp["personal_info"]["age"] is not None
            assert emp["contact"]["email"] is not None
            assert emp["contact"]["address"] is not None
