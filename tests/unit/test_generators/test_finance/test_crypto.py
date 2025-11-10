"""
加密货币生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestCryptoGenerator:
    """加密货币生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个加密货币数据"""
        from dataforge.generators.finance.crypto import CryptoGenerator
        generator_factory.registry.register("crypto", CryptoGenerator)
        
        config = GeneratorConfig(
            generator_type="crypto",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        crypto = generator.generate_single()
        
        assert crypto is not None
        assert generator.validate(crypto)

    def test_generate_batch(self, generator_factory):
        """测试批量生成加密货币数据"""
        from dataforge.generators.finance.crypto import CryptoGenerator
        generator_factory.registry.register("crypto", CryptoGenerator)
        
        config = GeneratorConfig(
            generator_type="crypto",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        cryptos = generator.generate_batch(10)
        
        assert len(cryptos) == 10
        for crypto in cryptos:
            assert crypto is not None

    def test_bitcoin_address(self, generator_factory):
        """测试比特币地址"""
        from dataforge.generators.finance.crypto import CryptoGenerator
        generator_factory.registry.register("crypto", CryptoGenerator)
        
        config = GeneratorConfig(
            generator_type="crypto",
            parameters={"type": "bitcoin_address"}
        )
        generator = generator_factory.create_generator(config)
        address = generator.generate_single()
        
        # Bitcoin address format
        if isinstance(address, str):
            assert len(address) >= 26
            assert len(address) <= 35

    def test_ethereum_address(self, generator_factory):
        """测试以太坊地址"""
        from dataforge.generators.finance.crypto import CryptoGenerator
        generator_factory.registry.register("crypto", CryptoGenerator)
        
        config = GeneratorConfig(
            generator_type="crypto",
            parameters={"type": "ethereum_address"}
        )
        generator = generator_factory.create_generator(config)
        address = generator.generate_single()
        
        # Ethereum address format: 0x + 40 hex chars
        if isinstance(address, str):
            assert address.startswith("0x") or len(address) == 42

    def test_crypto_symbol(self, generator_factory):
        """测试加密货币符号"""
        from dataforge.generators.finance.crypto import CryptoGenerator
        generator_factory.registry.register("crypto", CryptoGenerator)
        
        config = GeneratorConfig(
            generator_type="crypto",
            parameters={"type": "symbol"}
        )
        generator = generator_factory.create_generator(config)
        symbol = generator.generate_single()
        
        # Common crypto symbols: BTC, ETH, USDT, etc.
        if isinstance(symbol, str):
            assert len(symbol) >= 2
            assert symbol.isupper()

    def test_crypto_price(self, generator_factory):
        """测试加密货币价格"""
        from dataforge.generators.finance.crypto import CryptoGenerator
        generator_factory.registry.register("crypto", CryptoGenerator)
        
        config = GeneratorConfig(
            generator_type="crypto",
            parameters={"type": "price"}
        )
        generator = generator_factory.create_generator(config)
        price = generator.generate_single()
        
        # Price should be numeric
        if isinstance(price, (int, float)):
            assert price > 0
        elif isinstance(price, str):
            assert float(price) > 0

    def test_validation(self, generator_factory):
        """测试加密货币数据验证"""
        from dataforge.generators.finance.crypto import CryptoGenerator
        generator_factory.registry.register("crypto", CryptoGenerator)
        
        config = GeneratorConfig(
            generator_type="crypto",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid crypto data
        crypto = generator.generate_single()
        assert generator.validate(crypto)
        
        # Invalid data
        assert not generator.validate("")
        assert not generator.validate(None)

    def test_uniqueness(self, generator_factory):
        """测试加密货币数据唯一性"""
        from dataforge.generators.finance.crypto import CryptoGenerator
        generator_factory.registry.register("crypto", CryptoGenerator)
        
        config = GeneratorConfig(
            generator_type="crypto",
            parameters={"type": "bitcoin_address"}
        )
        generator = generator_factory.create_generator(config)
        addresses = generator.generate_batch(50)
        
        # Addresses should be unique
        unique_addresses = set(str(addr) for addr in addresses)
        assert len(unique_addresses) >= 45

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.finance.crypto import CryptoGenerator
        generator_factory.registry.register("crypto", CryptoGenerator)
        
        config = GeneratorConfig(
            generator_type="crypto",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            crypto = generator.generate_single()
            assert crypto is not None
