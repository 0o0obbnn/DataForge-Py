#!/usr/bin/env python3
"""
调试金融数据生成器的脚本
"""

from dataforge.generators.finance import (
    BankCardGenerator,
    CreditCardGenerator,
    CryptoAddressGenerator,
    FinanceProfileGenerator,
    IBANGenerator,
    StockCodeGenerator,
)


def debug_finance_generators():
    """调试所有金融生成器"""
    print("🔍 调试金融数据生成器")
    print("=" * 40)

    # 测试加密货币地址生成器
    crypto_gen = CryptoAddressGenerator()
    crypto_data = crypto_gen.generate()
    print("加密货币地址:")
    print(f"  BTC: {crypto_data['btc_address']}")
    print(f"  ETH: {crypto_data['eth_address']}")
    print()

    # 测试股票代码生成器
    stock_gen = StockCodeGenerator()
    stock_data = stock_gen.generate()
    print("股票信息:")
    print(f"  代码: {stock_data['code']}")
    print(f"  名称: {stock_data['name']}")
    print(f"  市场: {stock_data['market']}")
    print()

    # 测试银行卡生成器
    bank_gen = BankCardGenerator()
    bank_data = bank_gen.generate()
    print("银行卡信息:")
    print(f"  卡号: {bank_data['card_number']}")
    print(f"  银行: {bank_data['bank_name']}")
    print(f"  有效期: {bank_data['expiry_date']}")
    print()

    # 测试IBAN生成器
    iban_gen = IBANGenerator()
    iban_data = iban_gen.generate()
    print("IBAN信息:")
    print(f"  IBAN: {iban_data['iban']}")
    print(f"  BIC: {iban_data['bic']}")
    print(f"  银行: {iban_data['bank_name']}")
    print()

    # 测试信用卡生成器
    cc_gen = CreditCardGenerator()
    cc_data = cc_gen.generate()
    print("信用卡信息:")
    print(f"  卡号: {cc_data['card_number']}")
    print(f"  类型: {cc_data['card_type']}")
    print(f"  有效期: {cc_data['expiry_date']}")
    print(f"  CVV: {cc_data['cvv']}")
    print()

    # 测试金融档案生成器
    profile_gen = FinanceProfileGenerator()
    profile_data = profile_gen.generate()
    print("金融档案:")
    print(f"  年收入: {profile_data['annual_income']}")
    print(f"  信用评分: {profile_data['credit_score']}")
    print(f"  投资偏好: {profile_data['investment_preference']}")
    print(f"  风险承受能力: {profile_data['risk_tolerance']}")


if __name__ == "__main__":
    debug_finance_generators()
