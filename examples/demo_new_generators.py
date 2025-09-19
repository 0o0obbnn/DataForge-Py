#!/usr/bin/env python3
"""
DataForge新功能生成器演示脚本

演示新开发的交易日历、证件类、物流类生成器的使用
"""

import os
import sys

sys.path.insert(0, os.getcwd())

from dataforge.core.config import GeneratorConfig
from dataforge.generators.datetime.trading_calendar import (
    GenericTradingCalendarGenerator,
)
from dataforge.generators.identifier.drivers_license import (
    GenericDriverLicenseGenerator,
)
from dataforge.generators.identifier.logistics import (
    GenericTrackingNumberGenerator,
    GenericWaybillGenerator,
)
from dataforge.generators.identifier.passport import GenericPassportGenerator


def demo_trading_calendar():
    """演示交易日历生成器"""
    print("📅 交易日历生成器演示")
    print("=" * 50)

    # 创建交易日历生成器
    calendar_gen = GenericTradingCalendarGenerator()

    # 生成不同类型的交易日
    configs = [
        {"start_date": "2024-01-01", "end_date": "2024-12-31", "day_type": "TRADING"},
        {"start_date": "2024-10-01", "end_date": "2024-10-07", "day_type": "HOLIDAY"},
        {"start_date": "2024-02-04", "end_date": "2024-02-18", "day_type": "ALL", "include_weekends": True},
    ]

    for i, config in enumerate(configs, 1):
        print(f"\n配置 {i}: {config}")
        calendar_gen.parameters = config
        trading_day = calendar_gen.generate_single()
        print(f"生成结果: {trading_day}")


def demo_passport():
    """演示护照生成器"""
    print("\n🛂 护照生成器演示")
    print("=" * 50)

    # 创建护照生成器
    passport_gen = GenericPassportGenerator()

    # 生成不同类型的护照
    configs = [
        {"passport_type": "E", "country_code": "CHN", "include_dates": True, "include_name": True},
        {"passport_type": "D", "country_code": "CHN", "include_dates": True},
        {"passport_type": "G", "country_code": "USA", "include_name": True},
    ]

    for i, config in enumerate(configs, 1):
        print(f"\n配置 {i}: {config}")
        passport_gen.parameters = config
        passport = passport_gen.generate_single()
        print(f"生成结果: {passport}")


def demo_drivers_license():
    """演示驾驶证生成器"""
    print("\n🚗 驾驶证生成器演示")
    print("=" * 50)

    # 创建驾驶证生成器
    license_gen = GenericDriverLicenseGenerator()

    # 生成不同省份的驾驶证
    configs = [
        {"province": "北京", "license_class": "C1", "include_dates": True, "include_name": True},
        {"province": "上海", "license_class": "A1", "include_dates": True},
        {"province": "广东", "license_class": "B2", "include_name": True},
    ]

    for i, config in enumerate(configs, 1):
        print(f"\n配置 {i}: {config}")
        license_gen.parameters = config
        license_data = license_gen.generate_single()
        print(f"生成结果: {license_data}")


def demo_logistics():
    """演示物流单号生成器"""
    print("\n📦 物流单号生成器演示")
    print("=" * 50)

    # 创建物流单号生成器
    tracking_gen = GenericTrackingNumberGenerator()
    waybill_gen = GenericWaybillGenerator()

    # 生成不同快递公司的单号
    carriers = ["SF", "JD", "ZTO", "YTO", "STO", "YUNDA"]

    print("\n快递单号演示:")
    for carrier in carriers:
        tracking_gen.parameters = {"carrier": carrier, "include_cities": True, "include_date": True}
        tracking = tracking_gen.generate_single()
        print(f"{carrier}: {tracking}")

    print("\n运单号演示:")
    waybill_gen.parameters = {"carrier": "SF", "include_cities": True, "include_date": True}
    waybill = waybill_gen.generate_single()
    print(f"运单号: {waybill}")


def demo_batch_generation():
    """演示批量生成"""
    print("\n🔄 批量生成演示")
    print("=" * 50)

    # 使用GeneratorConfig进行批量生成
    config = GeneratorConfig(
        generator_name="passport",
        parameters={
            "passport_type": "E",
            "country_code": "CHN",
            "include_dates": True,
            "include_name": True
        },
        count=5
    )

    passport_gen = GenericPassportGenerator()
    passport_gen.parameters = config.parameters

    print("批量生成5个护照信息:")
    for i in range(5):
        passport = passport_gen.generate_single()
        print(f"{i+1}. {passport}")


def main():
    """主函数"""
    print("🚀 DataForge新功能生成器演示")
    print("=" * 60)

    try:
        # 演示各个新功能
        demo_trading_calendar()
        demo_passport()
        demo_drivers_license()
        demo_logistics()
        demo_batch_generation()

        print("\n✅ 所有演示完成！")
        print("\n新开发功能总结:")
        print("- 📅 交易日历生成器: 支持中国A股市场交易日历")
        print("- 🛂 护照生成器: 支持多种类型护照号码")
        print("- 🚗 驾驶证生成器: 支持各省份驾驶证号码")
        print("- 📦 物流单号生成器: 支持主流快递公司")
        print("- 📋 运单号生成器: 支持货运物流单号")

    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
