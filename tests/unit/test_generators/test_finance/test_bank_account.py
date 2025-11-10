"""
银行账户生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestBankAccountGenerator:
    """银行账户生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个银行账户"""
        from dataforge.generators.finance.bank_account import BankAccountGenerator
        generator_factory.registry.register("bank_account", BankAccountGenerator)
        
        config = GeneratorConfig(
            generator_type="bank_account",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        account = generator.generate_single()
        
        assert isinstance(account, (str, dict))
        if isinstance(account, str):
            assert len(account) >= 10
        assert generator.validate(account)

    def test_generate_batch(self, generator_factory):
        """测试批量生成银行账户"""
        from dataforge.generators.finance.bank_account import BankAccountGenerator
        generator_factory.registry.register("bank_account", BankAccountGenerator)
        
        config = GeneratorConfig(
            generator_type="bank_account",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        accounts = generator.generate_batch(10)
        
        assert len(accounts) == 10
        for account in accounts:
            assert generator.validate(account)

    def test_account_number_format(self, generator_factory):
        """测试账户号码格式"""
        from dataforge.generators.finance.bank_account import BankAccountGenerator
        generator_factory.registry.register("bank_account", BankAccountGenerator)
        
        config = GeneratorConfig(
            generator_type="bank_account",
            parameters={"format": "number_only"}
        )
        generator = generator_factory.create_generator(config)
        account = generator.generate_single()
        
        if isinstance(account, str):
            assert account.isdigit()

    def test_with_bank_name(self, generator_factory):
        """测试带银行名称"""
        from dataforge.generators.finance.bank_account import BankAccountGenerator
        generator_factory.registry.register("bank_account", BankAccountGenerator)
        
        config = GeneratorConfig(
            generator_type="bank_account",
            parameters={"include_bank": True}
        )
        generator = generator_factory.create_generator(config)
        account = generator.generate_single()
        
        # May return dict with bank info
        assert account is not None

    def test_account_type(self, generator_factory):
        """测试账户类型"""
        from dataforge.generators.finance.bank_account import BankAccountGenerator
        generator_factory.registry.register("bank_account", BankAccountGenerator)
        
        config = GeneratorConfig(
            generator_type="bank_account",
            parameters={"account_type": "savings"}
        )
        generator = generator_factory.create_generator(config)
        account = generator.generate_single()
        
        assert account is not None

    def test_validation(self, generator_factory):
        """测试银行账户验证"""
        from dataforge.generators.finance.bank_account import BankAccountGenerator
        generator_factory.registry.register("bank_account", BankAccountGenerator)
        
        config = GeneratorConfig(
            generator_type="bank_account",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid account
        account = generator.generate_single()
        assert generator.validate(account)
        
        # Invalid accounts
        assert not generator.validate("")
        assert not generator.validate("123")  # Too short

    def test_uniqueness(self, generator_factory):
        """测试银行账户唯一性"""
        from dataforge.generators.finance.bank_account import BankAccountGenerator
        generator_factory.registry.register("bank_account", BankAccountGenerator)
        
        config = GeneratorConfig(
            generator_type="bank_account",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        accounts = generator.generate_batch(50)
        
        # Convert to strings for comparison
        account_strs = [str(acc) for acc in accounts]
        unique_accounts = set(account_strs)
        assert len(unique_accounts) == 50

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.finance.bank_account import BankAccountGenerator
        generator_factory.registry.register("bank_account", BankAccountGenerator)
        
        config = GeneratorConfig(
            generator_type="bank_account",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            account = generator.generate_single()
            assert account is not None
            if isinstance(account, str):
                assert len(account) >= 10
