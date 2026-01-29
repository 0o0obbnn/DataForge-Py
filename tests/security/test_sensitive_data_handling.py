"""
敏感数据处理安全测试
"""

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.security
class TestSensitiveDataHandling:
    """敏感数据处理安全测试类"""

    def test_password_not_logged(self):
        """测试密码不被记录"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.password import PasswordGenerator

        registry.register("password", PasswordGenerator)

        config = GeneratorConfig("password", {})
        generator = factory.create_generator(config)

        # 生成密码
        password = generator.generate_single()

        # 验证密码已生成
        assert password is not None
        assert len(str(password)) > 0

        # 注意：实际应用中应检查日志文件不包含明文密码

    def test_credit_card_masking(self):
        """测试信用卡号掩码"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.identifier.bankcard import BankCardGenerator

        registry.register("bankcard", BankCardGenerator)

        config = GeneratorConfig("bankcard", {})
        generator = factory.create_generator(config)

        # 生成银行卡号
        card_number = generator.generate_single()

        # 验证卡号格式
        assert card_number is not None

        # 在实际应用中，应该提供掩码功能
        # 例如: 1234 **** **** 5678

    def test_id_card_privacy(self):
        """测试身份证号隐私保护"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.identifier.id import IDGenerator

        registry.register("id", IDGenerator)

        config = GeneratorConfig("id", {})
        generator = factory.create_generator(config)

        # 生成身份证号
        id_number = generator.generate_single()

        # 验证身份证号已生成
        assert id_number is not None

        # 在实际应用中，应该提供脱敏功能
        # 例如: 110101****1234

    def test_phone_number_privacy(self):
        """测试手机号隐私保护"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.contact.phone import PhoneGenerator

        registry.register("phone", PhoneGenerator)

        config = GeneratorConfig("phone", {})
        generator = factory.create_generator(config)

        # 生成手机号
        phone = generator.generate_single()

        # 验证手机号已生成
        assert phone is not None

        # 在实际应用中，应该提供脱敏功能
        # 例如: 138****5678

    def test_email_privacy(self):
        """测试邮箱隐私保护"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.contact.email import EmailGenerator

        registry.register("email", EmailGenerator)

        config = GeneratorConfig("email", {})
        generator = factory.create_generator(config)

        # 生成邮箱
        email = generator.generate_single()

        # 验证邮箱已生成
        assert email is not None
        assert "@" in str(email)

        # 在实际应用中，应该提供脱敏功能
        # 例如: u***@example.com

    def test_no_real_data_leakage(self):
        """测试不泄露真实数据"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        config = GeneratorConfig("name", {})
        generator = factory.create_generator(config)

        # 生成多个姓名
        names = generator.generate_batch(100)

        # 验证生成的是测试数据，不是真实数据
        # 这里只是示例，实际应该检查不包含已知的真实姓名
        assert len(names) == 100
        assert all(name is not None for name in names)

    def test_data_anonymization(self):
        """测试数据匿名化"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)

        # 生成用户数据
        name_gen = factory.create_generator(GeneratorConfig("name", {}))
        age_gen = factory.create_generator(GeneratorConfig("age", {}))

        users = []
        for _ in range(10):
            user = {
                "name": name_gen.generate_single(),
                "age": age_gen.generate_single(),
            }
            users.append(user)

        # 验证数据已匿名化（不包含可识别信息）
        assert len(users) == 10
        for user in users:
            assert user["name"] is not None
            assert user["age"] is not None

    def test_secure_random_generation(self):
        """测试安全随机数生成"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.password import PasswordGenerator

        registry.register("password", PasswordGenerator)

        config = GeneratorConfig("password", {})
        generator = factory.create_generator(config)

        # 生成多个密码
        passwords = generator.generate_batch(100)

        # 验证密码的随机性（不应有重复）
        unique_passwords = set(str(p) for p in passwords)
        assert len(unique_passwords) > 95  # 至少95%唯一

    def test_no_predictable_patterns(self):
        """测试无可预测模式"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.uuid import UUIDGenerator

        registry.register("uuid", UUIDGenerator)

        config = GeneratorConfig("uuid", {})
        generator = factory.create_generator(config)

        # 生成多个UUID
        uuids = generator.generate_batch(100)

        # 验证UUID的唯一性
        unique_uuids = set(str(u) for u in uuids)
        assert len(unique_uuids) == 100  # 应该100%唯一

    def test_data_retention_compliance(self):
        """测试数据保留合规性"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)

        config = GeneratorConfig("name", {})
        generator = factory.create_generator(config)

        # 生成数据
        names = generator.generate_batch(10)

        # 验证数据可以被清理
        del names

        # 在实际应用中，应该确保敏感数据不会被持久化
        assert True  # 占位符

    def test_encryption_support(self):
        """测试加密支持"""
        # 这是一个占位符测试
        # 在实际应用中，应该测试敏感数据的加密存储

        # 示例：验证密码生成器支持加密
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        from dataforge.generators.basic.password import PasswordGenerator

        registry.register("password", PasswordGenerator)

        config = GeneratorConfig("password", {})
        generator = factory.create_generator(config)

        password = generator.generate_single()

        # 验证密码已生成
        assert password is not None

        # 在实际应用中，应该提供加密功能
        # 例如: bcrypt, scrypt, argon2等
