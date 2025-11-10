#!/usr/bin/env python3
"""快速验证脚本 - 测试所有新开发的核心生成器"""


def test_generator(name, generator_class, params=None):
    """测试单个生成器"""
    try:
        gen = generator_class(params or {})
        gen.generate()
        print(f"✅ {name}: 成功")
        return True
    except Exception as e:
        print(f"❌ {name}: 失败 - {e}")
        return False

def main():
    print("DataForge 新功能生成器验证")
    print("=" * 40)

    # 导入所有生成器
    try:
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
        from dataforge.generators.identifier.visa import GenericVisaGenerator
        from dataforge.generators.structured.media_files import (
            GenericMediaFileGenerator,
        )
        from dataforge.generators.structured.user_behavior import (
            GenericUserBehaviorGenerator,
        )
    except ImportError as e:
        print(f"导入失败: {e}")
        return

    generators = [
        ("交易日历", GenericTradingCalendarGenerator),
        ("护照号", GenericPassportGenerator),
        ("驾驶证号", GenericDriverLicenseGenerator),
        ("签证号", GenericVisaGenerator),
        ("物流单号", GenericTrackingNumberGenerator),
        ("运单号", GenericWaybillGenerator),
        ("媒体文件", GenericMediaFileGenerator),
        ("用户行为", GenericUserBehaviorGenerator),
    ]

    success_count = 0
    for name, gen_class in generators:
        if test_generator(name, gen_class):
            success_count += 1

    print("\n" + "=" * 40)
    print(f"验证完成: {success_count}/{len(generators)} 个生成器成功")

    if success_count == len(generators):
        print("🎉 所有P1-P3级功能开发完成！")
    else:
        print("⚠️  部分功能需要检查")

if __name__ == "__main__":
    main()
