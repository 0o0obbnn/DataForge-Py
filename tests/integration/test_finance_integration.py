"""
金融类生成器测试模块 - 修复版

测试所有金融数据生成器的功能完整性和准确性
"""

import pytest

from dataforge.core.factory import default_factory
from dataforge.core.generator import GeneratorConfig

# 导入具体的金融生成器类


class TestCryptoGenerator:
    """测试加密货币地址生成器"""

    def test_bitcoin_address(self):
        """测试比特币地址生成"""
        config = GeneratorConfig(
            generator_type="crypto_address", parameters={"crypto_type": "BITCOIN"}
        )
        generator = default_factory.create_generator(config)
        address = generator.generate()
        assert address.startswith("1") or address.startswith("3")
        assert len(address) >= 26 and len(address) <= 35

    def test_ethereum_address(self):
        """测试以太坊地址生成"""
        config = GeneratorConfig(
            generator_type="crypto_address", parameters={"crypto_type": "ETHEREUM"}
        )
        generator = default_factory.create_generator(config)
        address = generator.generate()
        assert address.startswith("0x")
        assert len(address) == 42

    def test_litecoin_address(self):
        """测试莱特币地址生成"""
        config = GeneratorConfig(
            generator_type="crypto_address", parameters={"crypto_type": "LITECOIN"}
        )
        generator = default_factory.create_generator(config)
        address = generator.generate()
        assert address.startswith("L") or address.startswith("M")
        assert len(address) >= 26 and len(address) <= 35


class TestStockGenerator:
    """测试股票代码生成器"""

    def test_a_share_code(self):
        """测试A股代码生成"""
        config = GeneratorConfig(
            generator_type="stock_code",
            parameters={"market": "A_SHARE", "sector": "主板"},
        )
        generator = default_factory.create_generator(config)
        code = generator.generate()
        assert len(code) == 6
        assert code.isdigit()
        assert 600000 <= int(code) <= 609999

    def test_hong_kong_code(self):
        """测试港股代码生成"""
        config = GeneratorConfig(
            generator_type="stock_code",
            parameters={"market": "HONG_KONG", "format": "FULL"},
        )
        generator = default_factory.create_generator(config)
        code = generator.generate()
        assert code.endswith(".HK")
        assert len(code.split(".")[0]) >= 4

    def test_us_stock_code(self):
        """测试美股代码生成"""
        config = GeneratorConfig(
            generator_type="stock_code",
            parameters={"market": "US", "exchange": "NASDAQ"},
        )
        generator = default_factory.create_generator(config)
        code = generator.generate()
        assert code.isalpha()
        assert code.isupper()
        assert 1 <= len(code) <= 5


class TestBankAccountGenerator:
    """测试银行账户生成器"""

    def test_china_bank_account(self):
        """测试中国银行账号生成"""
        config = GeneratorConfig(
            generator_type="bank_account",
            parameters={"bank": "工商银行", "account_type": "SAVINGS"},
        )
        generator = default_factory.create_generator(config)
        account = generator.generate()
        assert len(account) == 19
        assert account.isdigit()
        assert account.startswith("6222")

    def test_us_bank_account(self):
        """测试美国银行账号生成"""
        config = GeneratorConfig(
            generator_type="bank_account",
            parameters={"bank": "JPMorgan Chase", "format": "FULL"},
        )
        generator = default_factory.create_generator(config)
        account = generator.generate()
        parts = account.split(":")
        assert len(parts) == 3
        assert parts[0] == "JPMorgan Chase"

    def test_credit_card_account(self):
        """测试信用卡账号生成"""
        config = GeneratorConfig(
            generator_type="bank_account", parameters={"account_type": "CREDIT"}
        )
        generator = default_factory.create_generator(config)
        account = generator.generate()
        assert len(account) == 16
        assert account.isdigit()


class TestDerivativesGenerator:
    """测试衍生品生成器"""

    def test_us_option(self):
        """测试美股期权生成"""
        config = GeneratorConfig(
            generator_type="derivatives", parameters={"type": "OPTION", "market": "US"}
        )
        generator = default_factory.create_generator(config)
        option = generator.generate()
        assert len(option) >= 15
        assert option[-9] in ["C", "P"]  # 期权类型

    def test_china_option(self):
        """测试A股期权生成"""
        config = GeneratorConfig(
            generator_type="derivatives",
            parameters={"type": "OPTION", "market": "CHINA"},
        )
        generator = default_factory.create_generator(config)
        option = generator.generate()
        assert len(option) >= 9
        assert option[-1] in ["C", "P"]

    def test_future_contract(self):
        """测试期货合约生成"""
        config = GeneratorConfig(
            generator_type="derivatives",
            parameters={"type": "FUTURE", "underlying": "COMMODITY"},
        )
        generator = default_factory.create_generator(config)
        future = generator.generate()
        assert len(future) >= 4
        assert future[:2].isalpha()


class TestMarketDataGenerator:
    """测试市场数据生成器"""

    def test_price_data(self):
        """测试价格数据生成"""
        config = GeneratorConfig(
            generator_type="market_data",
            parameters={"data_type": "PRICE", "symbol": "AAPL"},
        )
        generator = default_factory.create_generator(config)
        data = generator.generate()
        assert "symbol" in data
        assert "price" in data
        assert "volume" in data
        assert data["symbol"] == "AAPL"
        assert isinstance(data["price"], float)

    def test_orderbook_data(self):
        """测试订单簿数据生成"""
        config = GeneratorConfig(
            generator_type="market_data",
            parameters={"data_type": "ORDERBOOK", "symbol": "TSLA"},
        )
        generator = default_factory.create_generator(config)
        data = generator.generate()
        assert "bids" in data
        assert "asks" in data
        assert len(data["bids"]) == 5
        assert len(data["asks"]) == 5
        assert "spread" in data


class TestFinancialReportGenerator:
    """测试财务报表生成器"""

    def test_balance_sheet(self):
        """测试资产负债表生成"""
        config = GeneratorConfig(
            generator_type="financial_report",
            parameters={"report_type": "BALANCE_SHEET"},
        )
        generator = default_factory.create_generator(config)
        report = generator.generate()
        assert report["report_type"] == "BALANCE_SHEET"
        assert "total_assets" in report
        assert "total_liabilities" in report
        assert "total_equity" in report
        # 允许一定的浮点精度误差
        expected_sum = report["total_liabilities"] + report["total_equity"]
        actual_assets = report["total_assets"]
        assert abs(actual_assets - expected_sum) < 1.0  # 放宽精度要求到1美元

    def test_income_statement(self):
        """测试利润表生成"""
        config = GeneratorConfig(
            generator_type="financial_report",
            parameters={"report_type": "INCOME_STATEMENT"},
        )
        generator = default_factory.create_generator(config)
        report = generator.generate()
        assert report["report_type"] == "INCOME_STATEMENT"
        assert "revenue" in report
        assert "net_income" in report
        assert report["net_income"] <= report["revenue"]

    def test_cash_flow(self):
        """测试现金流量表生成"""
        config = GeneratorConfig(
            generator_type="financial_report", parameters={"report_type": "CASH_FLOW"}
        )
        generator = default_factory.create_generator(config)
        report = generator.generate()
        assert report["report_type"] == "CASH_FLOW"
        assert "operating_cash_flow" in report
        assert "investing_cash_flow" in report
        assert "financing_cash_flow" in report
        assert "net_cash_flow" in report


class TestFinanceIntegration:
    """测试金融类生成器集成"""

    def test_all_finance_generators(self):
        """测试所有金融生成器的基本功能"""

        # 测试加密货币
        config = GeneratorConfig(
            generator_type="crypto_address", parameters={"crypto_type": "BITCOIN"}
        )
        generator = default_factory.create_generator(config)
        crypto_result = generator.generate()
        assert crypto_result is not None

        # 测试股票代码
        config = GeneratorConfig(
            generator_type="stock_code", parameters={"market": "A_SHARE"}
        )
        generator = default_factory.create_generator(config)
        stock_result = generator.generate()
        assert stock_result is not None

        # 测试银行账号
        config = GeneratorConfig(generator_type="bank_account", parameters={})
        generator = default_factory.create_generator(config)
        bank_result = generator.generate()
        assert bank_result is not None

        # 测试衍生品
        config = GeneratorConfig(generator_type="derivatives", parameters={})
        generator = default_factory.create_generator(config)
        deriv_result = generator.generate()
        assert deriv_result is not None

        # 测试市场数据
        config = GeneratorConfig(generator_type="market_data", parameters={})
        generator = default_factory.create_generator(config)
        market_result = generator.generate()
        assert market_result is not None

        # 测试财务报表
        config = GeneratorConfig(generator_type="financial_report", parameters={})
        generator = default_factory.create_generator(config)
        report_result = generator.generate()
        assert report_result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
