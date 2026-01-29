#!/usr/bin/env python3
"""
DataForge 生成器总览演示

这个文件展示了DataForge项目中所有生成器的概览和使用方法。
运行此文件可以快速了解DataForge的强大功能。

作者: DataForge Team
日期: 2025-11-10
"""

import os
import sys

# 设置环境
sys.path.insert(0, ".")
os.environ["JWT_SECRET_KEY"] = "test-secret-key"

from dataforge.core.factory import default_registry


def print_banner():
    """打印横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    DataForge 生成器总览演示                      ║
║                                                              ║
║  展示 DataForge 项目中所有 82 个生成器的功能和使用方法          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def get_generators_by_category():
    """按类别获取生成器"""
    generators = default_registry.list_generators()

    categories = {
        "basic": [],
        "contact": [],
        "finance": [],
        "identifier": [],
        "network": [],
        "text": [],
        "numeric": [],
        "auth": [],
        "advanced": [],
    }

    for generator in generators:
        # 根据生成器名称分类
        if generator in [
            "name",
            "age",
            "gender",
            "company_name",
            "occupation",
            "education",
            "marital_status",
        ]:
            categories["basic"].append(generator)
        elif generator in ["phone", "email", "address"]:
            categories["contact"].append(generator)
        elif generator.startswith(
            ("stock", "fund", "bond", "crypto", "bank", "financial")
        ):
            categories["finance"].append(generator)
        elif generator in [
            "idcard",
            "uscc",
            "passport",
            "license_plate",
            "generic_waybill",
        ]:
            categories["identifier"].append(generator)
        elif generator in ["ipaddress", "mac_address", "domain", "url", "port"]:
            categories["network"].append(generator)
        elif generator in ["string", "chinese_text", "english_text", "long_text"]:
            categories["text"].append(generator)
        elif generator in ["integer", "decimal", "percentage", "number"]:
            categories["numeric"].append(generator)
        elif generator in ["auth_token", "session_id", "email_verification"]:
            categories["auth"].append(generator)
        elif generator in ["advanced_timestamp", "datetime_range", "analytics"]:
            categories["advanced"].append(generator)
        else:
            # 默认归类到basic
            categories["basic"].append(generator)

    return categories


def demonstrate_generator(generator_name: str, count: int = 3):
    """演示单个生成器"""
    try:
        from dataforge.core.factory import default_registry
        from dataforge.core.generator import GeneratorConfig

        # 创建配置
        config = GeneratorConfig(
            generator_type=generator_name, parameters={}, count=count
        )

        # 使用注册表的生成方法
        generator_class = default_registry.get_generator_class(generator_name)
        if not generator_class:
            return f"❌ 生成器 {generator_name} 未找到"

        # 创建生成器实例
        generator = generator_class(config)

        # 生成数据
        if count == 1:
            result = generator.generate_single()
            return [result]
        else:
            results = generator.generate_batch(count)
            return results

    except Exception as e:
        return f"❌ 生成器 {generator_name} 演示失败: {e}"


def show_category_preview(category_name: str, generators: list[str]):
    """显示类别预览"""
    print(f"\n📂 {category_name.upper()} 模块生成器 ({len(generators)}个)")
    print("─" * 60)

    for generator in generators[:3]:  # 只显示前3个
        print(f"  • {generator}")

    if len(generators) > 3:
        print(f"  • ... 还有 {len(generators) - 3} 个生成器")

    # 演示第一个生成器
    if generators:
        first_generator = generators[0]
        print(f"\n🔧 {first_generator} 演示:")
        results = demonstrate_generator(first_generator, 2)

        if isinstance(results, list):
            for i, result in enumerate(results, 1):
                print(f"  示例 {i}: {result}")
        else:
            print(f"  {results}")


def show_statistics():
    """显示统计信息"""
    generators = default_registry.list_generators()
    categories = get_generators_by_category()

    print("\n📊 DataForge 生成器统计")
    print("─" * 40)
    print(f"总生成器数量: {len(generators)}")

    for category, gens in categories.items():
        print(f"{category:12}: {len(gens):3} 个")


def show_quick_start():
    """显示快速开始指南"""
    print(
        """
🚀 快速开始指南

1. 基础使用:
   from dataforge.core.factory import default_registry
   generator = default_registry.get_generator('name')

2. 生成单个数据:
   config = GeneratorConfig('name', {})
   gen = generator(config)
   result = gen.generate_single()

3. 批量生成:
   config = GeneratorConfig('name', {}, count=10)
   gen = generator(config)
   results = gen.generate_batch()

4. 查看所有示例:
   python examples/basic/personal_info_demo.py
   python examples/finance/banking_demo.py

📖 更多示例请查看 examples/ 目录下的各个模块演示文件
"""
    )


def main():
    """主函数"""
    print_banner()

    # 显示统计信息
    show_statistics()

    # 获取分类生成器
    categories = get_generators_by_category()

    print("\n🎯 核心模块预览")
    print("=" * 60)

    # 显示各模块预览
    priority_modules = ["basic", "contact", "finance", "identifier"]

    for module in priority_modules:
        if module in categories and categories[module]:
            show_category_preview(module, categories[module])

    print("\n🔍 其他模块")
    print("─" * 30)
    other_modules = ["network", "text", "numeric", "auth", "advanced"]
    for module in other_modules:
        if module in categories and categories[module]:
            print(f"• {module}: {len(categories[module])} 个生成器")

    # 显示快速开始指南
    show_quick_start()

    print("\n✨ DataForge 拥有强大的数据生成能力，")
    print("   涵盖个人信息、金融、网络、认证等多个领域！")
    print("\n📁 查看 examples/ 目录获取详细示例")


if __name__ == "__main__":
    main()
