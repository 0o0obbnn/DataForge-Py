#!/usr/bin/env python3
"""
DataForge 基础生成器示例 - 个人信息类

这个文件展示了DataForge项目中个人信息相关生成器的使用方法，包括：
- 姓名 (name)
- 年龄 (age)
- 性别 (gender)
- 身份证号 (idcard)
- 职业 (occupation)
- 教育背景 (education)
- 婚姻状况 (marital_status)

作者: DataForge Team
日期: 2025-11-10
"""

import os
import sys

# 设置环境
sys.path.insert(0, ".")
os.environ["JWT_SECRET_KEY"] = "test-secret-key"

from dataforge.core.factory import default_registry
from dataforge.core.generator import GenerationContext, GeneratorConfig


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_subsection(title: str):
    """打印子章节标题"""
    print(f"\n{'─'*40}")
    print(f"  {title}")
    print(f"{'─'*40}")


def basic_usage():
    """基础用法示例"""
    print_section("1. 基础用法示例")

    # 演示姓名生成
    print_subsection("姓名生成器 (name)")
    try:
        config = GeneratorConfig("name", {}, count=3)
        generator_class = default_registry.get_generator_class("name")
        if generator_class is None:
            raise RuntimeError("Generator 'name' not registered")
        generator = generator_class(config)
        names = generator.generate_batch(3)

        for i, name in enumerate(names, 1):
            print(f"  示例 {i}: {name}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 演示年龄生成
    print_subsection("年龄生成器 (age)")
    try:
        config = GeneratorConfig("age", {}, count=3)
        generator_class = default_registry.get_generator_class("age")
        if generator_class is None:
            raise RuntimeError("Generator 'age' not registered")
        generator = generator_class(config)
        ages = generator.generate_batch(3)

        for i, age in enumerate(ages, 1):
            print(f"  示例 {i}: {age}岁")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 演示性别生成
    print_subsection("性别生成器 (gender)")
    try:
        config = GeneratorConfig("gender", {}, count=3)
        generator_class = default_registry.get_generator_class("gender")
        if generator_class is None:
            raise RuntimeError("Generator 'gender' not registered")
        generator = generator_class(config)
        genders = generator.generate_batch(3)

        for i, gender in enumerate(genders, 1):
            print(f"  示例 {i}: {gender}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")


def parameter_configuration():
    """参数配置示例"""
    print_section("2. 参数配置示例")

    # 姓名生成器参数配置
    print_subsection("姓名生成器 - 带参数配置")
    try:
        # 尝试不同的参数配置
        configs = [
            {},  # 默认配置
            {"gender": "male"},  # 生成男性姓名
            {"gender": "female"},  # 生成女性姓名
        ]

        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig("name", params, count=2)
            generator_class = default_registry.get_generator_class("name")
            if generator_class is None:
                print("    ⚠️ Generator 'name' 未注册，跳过")
                continue
            generator = generator_class(config)
            names = generator.generate_batch(2)

            for j, name in enumerate(names, 1):
                print(f"    结果 {j}: {name}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 年龄生成器参数配置
    print_subsection("年龄生成器 - 带参数配置")
    try:
        configs = [
            {"min_age": 18, "max_age": 25},  # 青年
            {"min_age": 30, "max_age": 45},  # 中年
            {"min_age": 60, "max_age": 80},  # 老年
        ]

        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig("age", params, count=2)
            generator_class = default_registry.get_generator_class("age")
            if generator_class is None:
                print("    ⚠️ Generator 'age' 未注册，跳过")
                continue
            generator = generator_class(config)
            ages = generator.generate_batch(2)

            for j, age in enumerate(ages, 1):
                print(f"    结果 {j}: {age}岁")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")


def batch_generation():
    """批量生成示例"""
    print_section("3. 批量生成示例")

    # 批量生成个人信息
    print_subsection("批量生成完整个人信息")
    try:
        personal_info_generators = ["name", "age", "gender", "occupation", "education"]
        batch_size = 5

        print(f"  生成 {batch_size} 个人的基本信息:")
        print("  " + "-" * 80)
        print("  序号 | 姓名      | 年龄 | 性别 | 职业        | 教育背景")
        print("  " + "-" * 80)

        for i in range(batch_size):
            person_info = []

            for generator_name in personal_info_generators:
                config = GeneratorConfig(generator_name, {}, count=1)
                generator_class = default_registry.get_generator_class(generator_name)
                if generator_class is None:
                    person_info.append("N/A")
                    continue
                try:
                    generator = generator_class(config)
                    result = generator.generate_single()
                    person_info.append(str(result))
                except Exception:
                    person_info.append("N/A")

            # 格式化输出
            name = person_info[0][:8].ljust(8)
            age = person_info[1].ljust(4)
            gender = person_info[2].ljust(4)
            occupation = person_info[3][:10].ljust(10)
            education = person_info[4][:8].ljust(8)

            print(
                f"  {i+1:2d}    | {name} | {age} | {gender} | {occupation} | {education}"
            )

        print("  " + "-" * 80)

    except Exception as e:
        print(f"  ❌ 批量生成失败: {e}")


def validation_examples():
    """数据验证示例"""
    print_section("4. 数据验证示例")

    # 验证生成的数据
    print_subsection("身份证号生成和验证")
    try:
        config = GeneratorConfig("idcard", {}, count=3)
        generator_class = default_registry.get_generator_class("idcard")
        if generator_class is None:
            raise RuntimeError("Generator 'idcard' not registered")
        generator = generator_class(config)
        idcards = generator.generate_batch(3)

        print("  生成的身份证号:")
        for i, idcard in enumerate(idcards, 1):
            print(f"    {i}. {idcard}")

            # 验证身份证号
            try:
                is_valid = generator.validate(idcard)
                print(f"       验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
            except:
                print("       验证结果: ⚠️ 无法验证")

    except Exception as e:
        print(f"  ❌ 身份证生成失败: {e}")


def error_handling():
    """错误处理示例"""
    print_section("5. 错误处理示例")

    # 处理不存在的生成器
    print_subsection("处理不存在的生成器")
    try:
        generator_class = default_registry.get_generator_class("nonexistent_generator")
        if not generator_class:
            print("  ✅ 正确处理了不存在的生成器")
    except Exception as e:
        print(f"  ❌ 错误处理失败: {e}")

    # 处理无效参数
    print_subsection("处理无效参数")
    try:
        config = GeneratorConfig(
            "age", {"min_age": 100, "max_age": 50}, count=1
        )  # 无效范围
        generator_class = default_registry.get_generator_class("age")
        if generator_class is None:
            raise RuntimeError("Generator 'age' not registered")
        generator = generator_class(config)
        age = generator.generate_single()
        print(f"  生成的年龄: {age}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效参数错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print_section("6. 最佳实践示例")

    # 实践1: 使用上下文生成关联数据
    print_subsection("实践1: 使用上下文生成关联数据")
    try:
        context = GenerationContext()

        # 生成姓名
        name_config = GeneratorConfig("name", {}, count=1)
        name_class = default_registry.get_generator_class("name")
        if name_class is None:
            raise RuntimeError("Generator 'name' not registered")
        name_gen = name_class(name_config)
        name = name_gen.generate_single()

        print(f"  生成姓名: {name}")

        # 使用姓名上下文生成其他信息
        # 注意：这里需要根据实际的上下文感知生成器来调整
        print("  💡 建议：使用上下文感知生成器生成关联性更强的数据")

    except Exception as e:
        print(f"  ❌ 上下文生成失败: {e}")

    # 实践2: 配置重用
    print_subsection("实践2: 配置重用")
    try:
        # 创建可重用的配置
        base_config = {"count": 2}

        generators_to_test = ["name", "age", "gender"]

        for gen_name in generators_to_test:
            config = GeneratorConfig(gen_name, base_config)
            generator_class = default_registry.get_generator_class(gen_name)
            if generator_class is None:
                print(f"  {gen_name}: ['N/A', 'N/A']")
                continue
            generator = generator_class(config)
            results = generator.generate_batch(2)
            print(f"  {gen_name}: {results}")

    except Exception as e:
        print(f"  ❌ 配置重用失败: {e}")


def main():
    """主函数，运行所有示例"""
    print("🎯 DataForge 基础生成器示例 - 个人信息类")
    print("本示例展示了个人信息相关生成器的各种使用方法")

    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()

        print_section("✅ 示例演示完成")
        print("🎉 所有个人信息类生成器示例已成功运行！")
        print("\n📚 相关文档:")
        print("  • 查看 examples/contact/contact_demo.py 了解联系方式生成器")
        print("  • 查看 examples/profile/profile_demo.py 了解个人档案生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")

    except Exception as e:
        print(f"\n❌ 示例运行出现错误: {e}")
        print("请检查DataForge环境配置是否正确")


if __name__ == "__main__":
    main()
