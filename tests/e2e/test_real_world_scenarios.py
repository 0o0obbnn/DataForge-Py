"""
真实世界场景端到端测试
"""

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.e2e
class TestRealWorldScenarios:
    """真实世界场景端到端测试类"""

    def test_ecommerce_order_scenario(self):
        """测试电商订单场景"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所需的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.contact.phone import PhoneGenerator
        from dataforge.generators.basic.address import AddressGenerator
        from dataforge.generators.basic.uuid import UUIDGenerator

        registry.register("name", NameGenerator)
        registry.register("phone", PhoneGenerator)
        registry.register("address", AddressGenerator)
        registry.register("uuid", UUIDGenerator)

        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
            "address": factory.create_generator(GeneratorConfig("address", {})),
            "uuid": factory.create_generator(GeneratorConfig("uuid", {})),
        }

        # 生成订单数据
        order = {
            "order_id": generators["uuid"].generate_single(),
            "customer_name": generators["name"].generate_single(),
            "phone": generators["phone"].generate_single(),
            "shipping_address": generators["address"].generate_single(),
            "billing_address": generators["address"].generate_single(),
        }

        # 验证订单数据
        assert all(v is not None for v in order.values())
        assert order["order_id"] != ""

        print(f"\n电商订单数据:")
        for key, value in order.items():
            print(f"  {key}: {value}")

    def test_healthcare_patient_scenario(self):
        """测试医疗患者场景"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所需的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        from dataforge.generators.identifier.id import IDGenerator
        from dataforge.generators.contact.phone import PhoneGenerator
        from dataforge.generators.basic.address import AddressGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        registry.register("id", IDGenerator)
        registry.register("phone", PhoneGenerator)
        registry.register("address", AddressGenerator)

        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(
                GeneratorConfig("age", {"min": 0, "max": 100})
            ),
            "gender": factory.create_generator(GeneratorConfig("gender", {})),
            "id": factory.create_generator(GeneratorConfig("id", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
            "address": factory.create_generator(GeneratorConfig("address", {})),
        }

        # 生成患者数据
        patient = {
            "patient_name": generators["name"].generate_single(),
            "age": generators["age"].generate_single(),
            "gender": generators["gender"].generate_single(),
            "id_card": generators["id"].generate_single(),
            "contact_phone": generators["phone"].generate_single(),
            "home_address": generators["address"].generate_single(),
        }

        # 验证患者数据
        assert all(v is not None for v in patient.values())
        assert 0 <= patient["age"] <= 100

        print(f"\n医疗患者数据:")
        for key, value in patient.items():
            print(f"  {key}: {value}")

    def test_education_student_scenario(self):
        """测试教育学生场景"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所需的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        from dataforge.generators.identifier.id import IDGenerator
        from dataforge.generators.contact.email import EmailGenerator
        from dataforge.generators.contact.phone import PhoneGenerator
        from dataforge.generators.basic.education import EducationGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        registry.register("id", IDGenerator)
        registry.register("email", EmailGenerator)
        registry.register("phone", PhoneGenerator)
        registry.register("education", EducationGenerator)

        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(
                GeneratorConfig("age", {"min": 6, "max": 25})
            ),
            "gender": factory.create_generator(GeneratorConfig("gender", {})),
            "id": factory.create_generator(GeneratorConfig("id", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
            "education": factory.create_generator(GeneratorConfig("education", {})),
        }

        # 生成学生数据
        student = {
            "student_name": generators["name"].generate_single(),
            "age": generators["age"].generate_single(),
            "gender": generators["gender"].generate_single(),
            "id_card": generators["id"].generate_single(),
            "email": generators["email"].generate_single(),
            "phone": generators["phone"].generate_single(),
            "education_level": generators["education"].generate_single(),
        }

        # 验证学生数据
        assert all(v is not None for v in student.values())
        assert 6 <= student["age"] <= 25

        print(f"\n教育学生数据:")
        for key, value in student.items():
            print(f"  {key}: {value}")

    def test_hr_recruitment_scenario(self):
        """测试人力资源招聘场景"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所需的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        from dataforge.generators.contact.email import EmailGenerator
        from dataforge.generators.contact.phone import PhoneGenerator
        from dataforge.generators.basic.education import EducationGenerator
        from dataforge.generators.basic.occupation import OccupationGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        registry.register("email", EmailGenerator)
        registry.register("phone", PhoneGenerator)
        registry.register("education", EducationGenerator)
        registry.register("occupation", OccupationGenerator)

        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(
                GeneratorConfig("age", {"min": 22, "max": 60})
            ),
            "gender": factory.create_generator(GeneratorConfig("gender", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
            "education": factory.create_generator(GeneratorConfig("education", {})),
            "occupation": factory.create_generator(GeneratorConfig("occupation", {})),
        }

        # 生成候选人数据
        candidate = {
            "name": generators["name"].generate_single(),
            "age": generators["age"].generate_single(),
            "gender": generators["gender"].generate_single(),
            "email": generators["email"].generate_single(),
            "phone": generators["phone"].generate_single(),
            "education": generators["education"].generate_single(),
            "current_position": generators["occupation"].generate_single(),
        }

        # 验证候选人数据
        assert all(v is not None for v in candidate.values())

        print(f"\n招聘候选人数据:")
        for key, value in candidate.items():
            print(f"  {key}: {value}")

    def test_logistics_delivery_scenario(self):
        """测试物流配送场景"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所需的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.contact.phone import PhoneGenerator
        from dataforge.generators.basic.address import AddressGenerator
        from dataforge.generators.identifier.logistics import LogisticsNumberGenerator

        registry.register("name", NameGenerator)
        registry.register("phone", PhoneGenerator)
        registry.register("address", AddressGenerator)
        registry.register("logistics", LogisticsNumberGenerator)

        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "phone": factory.create_generator(GeneratorConfig("phone", {})),
            "address": factory.create_generator(GeneratorConfig("address", {})),
            "logistics": factory.create_generator(GeneratorConfig("logistics", {})),
        }

        # 生成物流数据
        delivery = {
            "tracking_number": generators["logistics"].generate_single(),
            "recipient_name": generators["name"].generate_single(),
            "recipient_phone": generators["phone"].generate_single(),
            "delivery_address": generators["address"].generate_single(),
            "sender_name": generators["name"].generate_single(),
            "sender_phone": generators["phone"].generate_single(),
            "sender_address": generators["address"].generate_single(),
        }

        # 验证物流数据
        assert all(v is not None for v in delivery.values())

        print(f"\n物流配送数据:")
        for key, value in delivery.items():
            print(f"  {key}: {value}")

    def test_social_media_profile_scenario(self):
        """测试社交媒体档案场景"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所需的生成器
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.basic.username import UsernameGenerator
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.gender import GenderGenerator
        from dataforge.generators.contact.email import EmailGenerator
        from dataforge.generators.basic.password import PasswordGenerator

        registry.register("name", NameGenerator)
        registry.register("username", UsernameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("gender", GenderGenerator)
        registry.register("email", EmailGenerator)
        registry.register("password", PasswordGenerator)

        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "username": factory.create_generator(GeneratorConfig("username", {})),
            "age": factory.create_generator(
                GeneratorConfig("age", {"min": 13, "max": 80})
            ),
            "gender": factory.create_generator(GeneratorConfig("gender", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
            "password": factory.create_generator(GeneratorConfig("password", {})),
        }

        # 生成社交媒体档案
        profile = {
            "display_name": generators["name"].generate_single(),
            "username": generators["username"].generate_single(),
            "age": generators["age"].generate_single(),
            "gender": generators["gender"].generate_single(),
            "email": generators["email"].generate_single(),
            "password": generators["password"].generate_single(),
        }

        # 验证档案数据
        assert all(v is not None for v in profile.values())
        assert 13 <= profile["age"] <= 80

        print(f"\n社交媒体档案:")
        for key, value in profile.items():
            if key != "password":  # 不显示密码
                print(f"  {key}: {value}")
            else:
                print(f"  {key}: ********")

    def test_batch_data_migration_scenario(self):
        """测试批量数据迁移场景"""
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

        # 批量生成迁移数据
        batch_size = 1000
        migration_data = []

        for i in range(batch_size):
            record = {
                "id": i + 1,
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
                "email": generators["email"].generate_single(),
            }
            migration_data.append(record)

        # 验证迁移数据
        assert len(migration_data) == batch_size
        assert all(
            all(v is not None for v in record.values()) for record in migration_data
        )

        print(f"\n批量数据迁移:")
        print(f"  迁移记录数: {len(migration_data)}")
        print(f"  示例记录: {migration_data[0]}")
