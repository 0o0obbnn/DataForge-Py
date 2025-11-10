"""
完整工作流端到端测试
"""

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.e2e
class TestCompleteWorkflow:
    """完整工作流端到端测试类"""

    def test_user_registration_workflow(self):
        """测试用户注册完整工作流"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        # 注册所需的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        from dataforge.generators.contact.email import EmailGenerator
        from dataforge.generators.contact.phone import PhoneGenerator
        from dataforge.generators.basic.password import PasswordGenerator
        
        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        registry.register("email", EmailGenerator)
        registry.register("phone", PhoneGenerator)
        registry.register("password", PasswordGenerator)
        
        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {"min": 18, "max": 65})),
            "gender": factory.create_generator(GeneratorConfig("gender", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
            "password": factory.create_generator(GeneratorConfig("password", {})),
        }
        
        # 生成用户注册数据
        user_data = {
            "username": generators["name"].generate_single(),
            "age": generators["age"].generate_single(),
            "gender": generators["gender"].generate_single(),
            "email": generators["email"].generate_single(),
            "phone": generators["phone"].generate_single(),
            "password": generators["password"].generate_single(),
        }
        
        # 验证数据完整性
        assert all(v is not None for v in user_data.values())
        assert isinstance(user_data["username"], str)
        assert isinstance(user_data["age"], int)
        assert 18 <= user_data["age"] <= 65
        assert isinstance(user_data["gender"], str)
        assert isinstance(user_data["email"], str)
        assert "@" in user_data["email"]
        assert isinstance(user_data["phone"], str)
        assert isinstance(user_data["password"], str)
        
        print(f"\n用户注册数据:")
        for key, value in user_data.items():
            print(f"  {key}: {value}")

    def test_employee_onboarding_workflow(self):
        """测试员工入职完整工作流"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        # 注册所需的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        from dataforge.generators.identifier.id import IDGenerator
        from dataforge.generators.contact.email import EmailGenerator
        from dataforge.generators.contact.phone import PhoneGenerator
        from dataforge.generators.basic.address import AddressGenerator
        from dataforge.generators.basic.education import EducationGenerator
        
        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        registry.register("id", IDGenerator)
        registry.register("email", EmailGenerator)
        registry.register("phone", PhoneGenerator)
        registry.register("address", AddressGenerator)
        registry.register("education", EducationGenerator)
        
        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {"min": 22, "max": 60})),
            "gender": factory.create_generator(GeneratorConfig("gender", {})),
            "id": factory.create_generator(GeneratorConfig("id", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
            "address": factory.create_generator(GeneratorConfig("address", {})),
            "education": factory.create_generator(GeneratorConfig("education", {})),
        }
        
        # 生成员工入职数据
        employee_data = {
            "name": generators["name"].generate_single(),
            "age": generators["age"].generate_single(),
            "gender": generators["gender"].generate_single(),
            "id_card": generators["id"].generate_single(),
            "email": generators["email"].generate_single(),
            "phone": generators["phone"].generate_single(),
            "address": generators["address"].generate_single(),
            "education": generators["education"].generate_single(),
        }
        
        # 验证数据完整性
        assert all(v is not None for v in employee_data.values())
        
        print(f"\n员工入职数据:")
        for key, value in employee_data.items():
            print(f"  {key}: {value}")

    def test_financial_account_workflow(self):
        """测试金融账户开户完整工作流"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        # 注册所需的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.identifier.id import IDGenerator
        from dataforge.generators.contact.phone import PhoneGenerator
        from dataforge.generators.identifier.bankcard import BankCardGenerator
        from dataforge.generators.finance.bank_account import BankAccountGenerator
        
        registry.register("name", NameGenerator)
        registry.register("id", IDGenerator)
        registry.register("phone", PhoneGenerator)
        registry.register("bankcard", BankCardGenerator)
        registry.register("bank_account", BankAccountGenerator)
        
        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "id": factory.create_generator(GeneratorConfig("id", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
            "bankcard": factory.create_generator(GeneratorConfig("bankcard", {})),
            "bank_account": factory.create_generator(GeneratorConfig("bank_account", {})),
        }
        
        # 生成金融账户数据
        account_data = {
            "account_holder": generators["name"].generate_single(),
            "id_card": generators["id"].generate_single(),
            "phone": generators["phone"].generate_single(),
            "bank_card": generators["bankcard"].generate_single(),
            "account_number": generators["bank_account"].generate_single(),
        }
        
        # 验证数据完整性
        assert all(v is not None for v in account_data.values())
        
        print(f"\n金融账户数据:")
        for key, value in account_data.items():
            print(f"  {key}: {value}")

    def test_batch_user_generation_workflow(self):
        """测试批量用户生成完整工作流"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        # 注册所需的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        from dataforge.generators.contact.email import EmailGenerator
        
        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        registry.register("email", EmailGenerator)
        
        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "gender": factory.create_generator(GeneratorConfig("gender", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
        }
        
        # 批量生成用户数据
        batch_size = 100
        users = []
        for _ in range(batch_size):
            user = {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
                "gender": generators["gender"].generate_single(),
                "email": generators["email"].generate_single(),
            }
            users.append(user)
        
        # 验证批量数据
        assert len(users) == batch_size
        assert all(all(v is not None for v in user.values()) for user in users)
        
        # 验证数据多样性
        unique_names = set(user["name"] for user in users)
        unique_emails = set(user["email"] for user in users)
        
        print(f"\n批量用户生成:")
        print(f"  生成数量: {len(users)}")
        print(f"  唯一姓名: {len(unique_names)}")
        print(f"  唯一邮箱: {len(unique_emails)}")
        
        assert len(unique_names) > batch_size * 0.8  # 至少80%唯一
        assert len(unique_emails) > batch_size * 0.8

    def test_data_export_workflow(self):
        """测试数据导出完整工作流"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        # 注册所需的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.contact.email import EmailGenerator
        
        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("email", EmailGenerator)
        
        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
        }
        
        # 生成数据
        users = []
        for _ in range(10):
            user = {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
                "email": generators["email"].generate_single(),
            }
            users.append(user)
        
        # 模拟导出为JSON格式
        import json
        json_data = json.dumps(users, ensure_ascii=False, indent=2)
        
        # 验证导出数据
        assert json_data is not None
        assert len(json_data) > 0
        
        # 验证可以重新解析
        parsed_users = json.loads(json_data)
        assert len(parsed_users) == len(users)
        
        print(f"\n数据导出:")
        print(f"  导出格式: JSON")
        print(f"  数据量: {len(users)}条")
        print(f"  数据大小: {len(json_data)}字节")

    def test_multi_locale_workflow(self):
        """测试多地区数据生成工作流"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        # 注册所需的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.address import AddressGenerator
        
        registry.register("name", NameGenerator)
        registry.register("address", AddressGenerator)
        
        # 测试不同地区
        locales = ["zh_CN", "en_US"]
        
        for locale in locales:
            # 创建生成器
            name_gen = factory.create_generator(
                GeneratorConfig("name", {"locale": locale})
            )
            address_gen = factory.create_generator(
                GeneratorConfig("address", {"locale": locale})
            )
            
            # 生成数据
            data = {
                "name": name_gen.generate_single(),
                "address": address_gen.generate_single(),
            }
            
            # 验证数据
            assert data["name"] is not None
            assert data["address"] is not None
            
            print(f"\n地区 {locale}:")
            print(f"  姓名: {data['name']}")
            print(f"  地址: {data['address']}")

    def test_validation_workflow(self):
        """测试数据验证完整工作流"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        # 注册所需的生成器
        from dataforge.generators.contact.email import EmailGenerator
        from dataforge.generators.contact.phone import PhoneGenerator
        from dataforge.generators.identifier.id import IDGenerator
        
        registry.register("email", EmailGenerator)
        registry.register("phone", PhoneGenerator)
        registry.register("id", IDGenerator)
        
        # 创建生成器
        generators = {
            "email": factory.create_generator(GeneratorConfig("email", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
            "id": factory.create_generator(GeneratorConfig("id", {})),
        }
        
        # 生成并验证数据
        email = generators["email"].generate_single()
        phone = generators["phone"].generate_single()
        id_card = generators["id"].generate_single()
        
        # 使用生成器的验证方法
        assert generators["email"].validate(email)
        assert generators["phone"].validate(phone)
        assert generators["id"].validate(id_card)
        
        print(f"\n数据验证:")
        print(f"  邮箱: {email} - 有效")
        print(f"  手机: {phone} - 有效")
        print(f"  身份证: {id_card} - 有效")
