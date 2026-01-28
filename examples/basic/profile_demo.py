#!/usr/bin/env python3
"""
DataForge 基础生成器示例 - 个人档案类

这个文件展示了DataForge项目中个人档案相关生成器的使用方法，包括：
- 职业 (occupation)
- 教育背景 (education)
- 婚姻状况 (marital_status)
- 公司信息 (company_name)
- 扩展档案信息 (zodiac, blood_type, ethnicity)

作者: DataForge Team
日期: 2025-11-10
"""

import json
import os
import sys

# 设置环境
sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

from dataforge.core.factory import default_registry
from dataforge.core.generator import GeneratorConfig


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

    # 演示职业生成
    print_subsection("职业生成器 (occupation)")
    try:
        config = GeneratorConfig('occupation', {}, count=3)
        generator_class = default_registry.get_generator_class('occupation')
        if generator_class is None:
            raise ValueError("找不到 'occupation' 生成器类")
        generator = generator_class(config)
        occupations = generator.generate_batch(3)

        for i, occupation in enumerate(occupations, 1):
            print(f"  示例 {i}: {occupation}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 演示教育背景生成
    print_subsection("教育背景生成器 (education)")
    try:
        config = GeneratorConfig('education', {}, count=3)
        generator_class = default_registry.get_generator_class('education')
        if generator_class is None:
            raise ValueError("找不到 'education' 生成器类")
        generator = generator_class(config)
        educations = generator.generate_batch(3)

        for i, education in enumerate(educations, 1):
            print(f"  示例 {i}: {education}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 演示婚姻状况生成
    print_subsection("婚姻状况生成器 (marital_status)")
    try:
        config = GeneratorConfig('marital_status', {}, count=3)
        generator_class = default_registry.get_generator_class('marital_status')
        if generator_class is None:
            raise ValueError("找不到 'marital_status' 生成器类")
        generator = generator_class(config)
        marital_statuses = generator.generate_batch(3)

        for i, status in enumerate(marital_statuses, 1):
            print(f"  示例 {i}: {status}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 演示公司名称生成
    print_subsection("公司名称生成器 (company_name)")
    try:
        config = GeneratorConfig('company_name', {}, count=3)
        generator_class = default_registry.get_generator_class('company_name')
        if generator_class is None:
            raise ValueError("找不到 'company_name' 生成器类")
        generator = generator_class(config)
        companies = generator.generate_batch(3)

        for i, company in enumerate(companies, 1):
            print(f"  示例 {i}: {company}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")


def parameter_configuration():
    """参数配置示例"""
    print_section("2. 参数配置示例")

    # 职业生成器参数配置
    print_subsection("职业生成器 - 行业配置")
    try:
        # 尝试不同的行业配置
        configs = [
            {},  # 默认配置
            {"industry": "technology"},  # 科技行业
            {"industry": "finance"},  # 金融行业
            {"industry": "education"},  # 教育行业
        ]

        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig('occupation', params, count=2)
            generator_class = default_registry.get_generator_class('occupation')
            if generator_class is None:
                raise ValueError("找不到 'occupation' 生成器类")
            generator = generator_class(config)
            occupations = generator.generate_batch(2)

            for j, occupation in enumerate(occupations, 1):
                print(f"    结果 {j}: {occupation}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 教育背景生成器参数配置
    print_subsection("教育背景生成器 - 等级配置")
    try:
        configs = [
            {},  # 默认配置
            {"level": "bachelor"},  # 本科
            {"level": "master"},  # 硕士
            {"level": "phd"},  # 博士
        ]

        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig('education', params, count=2)
            generator_class = default_registry.get_generator_class('education')
            if generator_class is None:
                raise ValueError("找不到 'education' 生成器类")
            generator = generator_class(config)
            educations = generator.generate_batch(2)

            for j, education in enumerate(educations, 1):
                print(f"    结果 {j}: {education}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    # 公司名称生成器参数配置
    print_subsection("公司名称生成器 - 类型配置")
    try:
        configs = [
            {},  # 默认配置
            {"company_type": "technology"},  # 科技公司
            {"company_type": "finance"},  # 金融公司
            {"company_type": "manufacturing"},  # 制造业公司
        ]

        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig('company_name', params, count=2)
            generator_class = default_registry.get_generator_class('company_name')
            if generator_class is None:
                raise ValueError("找不到 'company_name' 生成器类")
            generator = generator_class(config)
            companies = generator.generate_batch(2)

            for j, company in enumerate(companies, 1):
                print(f"    结果 {j}: {company}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")


def batch_generation():
    """批量生成示例"""
    print_section("3. 批量生成示例")

    # 批量生成完整个人档案
    print_subsection("批量生成完整个人档案")
    try:
        profile_generators = ['name', 'age', 'gender', 'occupation', 'education', 'company_name']
        batch_size = 5

        print(f"  生成 {batch_size} 个人的完整档案:")
        print("  " + "-" * 120)
        print("  序号 | 姓名    | 年龄 | 性别 | 职业        | 教育背景    | 公司名称")
        print("  " + "-" * 120)

        for i in range(batch_size):
            profile_info = []

            # 首先生成姓名
            name_config = GeneratorConfig('name', {}, count=1)
            name_class = default_registry.get_generator_class('name')
            if name_class is None:
                raise ValueError("找不到 'name' 生成器类")
            name_gen = name_class(name_config)
            name = name_gen.generate_single()
            profile_info.append(name)

            # 生成其他档案信息
            for generator_name in ['age', 'gender', 'occupation', 'education', 'company_name']:
                try:
                    config = GeneratorConfig(generator_name, {}, count=1)
                    generator_class = default_registry.get_generator_class(generator_name)
                    if generator_class is None:
                        raise ValueError(f"找不到 '{generator_name}' 生成器类")
                    generator = generator_class(config)
                    result = generator.generate_single()
                    profile_info.append(str(result))
                except:
                    profile_info.append("N/A")

            # 格式化输出
            name = profile_info[0][:6].ljust(6)
            age = profile_info[1].ljust(4)
            gender = profile_info[2].ljust(4)
            occupation = profile_info[3][:10].ljust(10)
            education = profile_info[4][:10].ljust(10)
            company = profile_info[5][:20].ljust(20)

            print(f"  {i+1:2d}    | {name} | {age} | {gender} | {occupation} | {education} | {company}")

        print("  " + "-" * 120)

    except Exception as e:
        print(f"  ❌ 批量生成失败: {e}")


def validation_examples():
    """数据验证示例"""
    print_section("4. 数据验证示例")

    # 验证生成的数据
    print_subsection("公司名称验证")
    try:
        config = GeneratorConfig('company_name', {}, count=3)
        generator_class = default_registry.get_generator_class('company_name')
        if generator_class is None:
            raise ValueError("找不到 'company_name' 生成器类")
        generator = generator_class(config)
        companies = generator.generate_batch(3)

        print("  生成的公司名称:")
        for i, company in enumerate(companies, 1):
            print(f"    {i}. {company}")

            # 验证公司名称长度
            is_valid_length = len(company) >= 4  # 最少4个字符
            print(f"       长度验证: {'✅ 有效' if is_valid_length else '❌ 无效'} (长度: {len(company)})")

            # 验证是否包含中文
            has_chinese = any('\u4e00' <= char <= '\u9fff' for char in company)
            print(f"       中文验证: {'✅ 包含中文' if has_chinese else '❌ 无中文'}")

    except Exception as e:
        print(f"  ❌ 公司名称验证失败: {e}")


def error_handling():
    """错误处理示例"""
    print_section("5. 错误处理示例")

    # 处理不存在的生成器
    print_subsection("处理不存在的生成器")
    try:
        generator_class = default_registry.get_generator_class('nonexistent_generator')
        if not generator_class:
            print("  ✅ 正确处理了不存在的生成器")
    except Exception as e:
        print(f"  ❌ 错误处理失败: {e}")

    # 处理无效参数
    print_subsection("处理无效参数")
    try:
        config = GeneratorConfig('occupation', {"industry": "不存在的行业"}, count=1)
        generator_class = default_registry.get_generator_class('occupation')
        if generator_class is None:
            raise ValueError("找不到 'occupation' 生成器类")
        generator = generator_class(config)
        occupation = generator.generate_single()
        print(f"  生成的职业: {occupation}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效参数错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print_section("6. 最佳实践示例")

    # 实践1: 生成关联的个人档案
    print_subsection("实践1: 生成关联的个人档案")
    try:
        # 生成一个人物的完整档案
        person_profile = {}

        # 生成基本信息
        name_config = GeneratorConfig('name', {}, count=1)
        name_class = default_registry.get_generator_class('name')
        if name_class is None:
            raise ValueError("找不到 'name' 生成器类")
        name_gen = name_class(name_config)
        person_profile['name'] = name_gen.generate_single()

        # 生成档案信息
        profile_configs = {
            'age': GeneratorConfig('age', {"min_age": 25, "max_age": 45}, count=1),
            'occupation': GeneratorConfig('occupation', {"industry": "technology"}, count=1),
            'education': GeneratorConfig('education', {"level": "bachelor"}, count=1),
            'company_name': GeneratorConfig('company_name', {"company_type": "technology"}, count=1)
        }

        for key, config in profile_configs.items():
            generator_class = default_registry.get_generator_class(key)
            if generator_class is None:
                raise ValueError(f"找不到 '{key}' 生成器类")
            generator = generator_class(config)
            person_profile[key] = generator.generate_single()

        print("  生成的人物档案:")
        for key, value in person_profile.items():
            print(f"    {key}: {value}")

        print("\n  💡 建议：使用相关联的参数生成更真实的档案数据")

    except Exception as e:
        print(f"  ❌ 关联档案生成失败: {e}")

    # 实践2: 批量导出格式化数据
    print_subsection("实践2: 批量导出格式化数据")
    try:
        profile_data = []

        # 生成多条个人档案
        for i in range(3):
            record = {}

            # 生成基本信息
            name_config = GeneratorConfig('name', {}, count=1)
            name_class = default_registry.get_generator_class('name')
            if name_class is None:
                raise ValueError("找不到 'name' 生成器类")
            name_gen = name_class(name_config)
            record['name'] = name_gen.generate_single()

            # 生成档案信息
            for field in ['age', 'gender', 'occupation', 'education', 'marital_status']:
                config = GeneratorConfig(field, {}, count=1)
                generator_class = default_registry.get_generator_class(field)
                if generator_class is None:
                    raise ValueError(f"找不到 '{field}' 生成器类")
                generator = generator_class(config)
                record[field] = generator.generate_single()

            profile_data.append(record)

        # 导出为JSON格式
        json_output = json.dumps(profile_data, ensure_ascii=False, indent=2)
        print("  JSON格式输出:")
        print(json_output)

    except Exception as e:
        print(f"  ❌ 格式化导出失败: {e}")


def extended_profile_demo():
    """扩展档案演示"""
    print_section("7. 扩展档案信息演示")

    # 演示扩展档案信息
    print_subsection("扩展档案信息生成")
    try:
        extended_generators = ['zodiac', 'blood_type', 'ethnicity']

        print("  生成扩展档案信息:")
        for gen_name in extended_generators:
            try:
                config = GeneratorConfig(gen_name, {}, count=3)
                generator_class = default_registry.get_generator_class(gen_name)
                if generator_class is None:
                    raise ValueError(f"找不到 '{gen_name}' 生成器类")
                generator = generator_class(config)
                results = generator.generate_batch(3)

                print(f"\n  {gen_name}:")
                for i, result in enumerate(results, 1):
                    print(f"    示例 {i}: {result}")
            except Exception as e:
                print(f"  ❌ {gen_name} 生成失败: {e}")

    except Exception as e:
        print(f"  ❌ 扩展档案演示失败: {e}")


def main():
    """主函数，运行所有示例"""
    print("🎯 DataForge 基础生成器示例 - 个人档案类")
    print("本示例展示了个人档案相关生成器的各种使用方法")

    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        extended_profile_demo()

        print_section("✅ 示例演示完成")
        print("🎉 所有个人档案类生成器示例已成功运行！")
        print("\n📚 相关文档:")
        print("  • 查看 examples/basic/personal_info_demo.py 了解个人信息生成器")
        print("  • 查看 examples/basic/contact_demo.py 了解联系方式生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")

    except Exception as e:
        print(f"\n❌ 示例运行出现错误: {e}")
        print("请检查DataForge环境配置是否正确")


if __name__ == "__main__":
    main()
