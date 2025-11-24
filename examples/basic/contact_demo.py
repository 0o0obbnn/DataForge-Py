#!/usr/bin/env python3
"""
DataForge 基础生成器示例 - 联系方式类

这个文件展示了DataForge项目中联系方式相关生成器的使用方法，包括：
- 地址 (address)
- 电话号码 (phone)
- 电子邮箱 (email)

作者: DataForge Team
日期: 2025-11-10
"""

import sys
import os
import json
import re
from typing import Dict, List, Any

# 设置环境
sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

from dataforge.core.factory import default_registry
from dataforge.core.generator import GeneratorConfig, GenerationContext


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
    
    # 演示地址生成
    print_subsection("地址生成器 (address)")
    try:
        config = GeneratorConfig('address', {}, count=3)
        generator_class = default_registry.get_generator_class('address')
        generator = generator_class(config)
        addresses = generator.generate_batch(3)
        
        for i, address in enumerate(addresses, 1):
            print(f"  示例 {i}: {address}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 演示电话号码生成
    print_subsection("电话号码生成器 (phone)")
    try:
        config = GeneratorConfig('phone', {}, count=3)
        generator_class = default_registry.get_generator_class('phone')
        generator = generator_class(config)
        phones = generator.generate_batch(3)
        
        for i, phone in enumerate(phones, 1):
            print(f"  示例 {i}: {phone}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 演示电子邮箱生成
    print_subsection("电子邮箱生成器 (email)")
    try:
        config = GeneratorConfig('email', {}, count=3)
        generator_class = default_registry.get_generator_class('email')
        generator = generator_class(config)
        emails = generator.generate_batch(3)
        
        for i, email in enumerate(emails, 1):
            print(f"  示例 {i}: {email}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")


def parameter_configuration():
    """参数配置示例"""
    print_section("2. 参数配置示例")
    
    # 地址生成器参数配置
    print_subsection("地址生成器 - 地区配置")
    try:
        # 尝试不同的地区配置
        configs = [
            {},  # 默认配置
            {"province": "北京市"},  # 指定省份
            {"city": "上海市"},  # 指定城市
            {"district": "朝阳区"},  # 指定区域
        ]
        
        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig('address', params, count=2)
            generator_class = default_registry.get_generator_class('address')
            generator = generator_class(config)
            addresses = generator.generate_batch(2)
            
            for j, address in enumerate(addresses, 1):
                print(f"    结果 {j}: {address}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 电话号码生成器参数配置
    print_subsection("电话号码生成器 - 运营商配置")
    try:
        configs = [
            {"operator": "mobile"},  # 手机号码
            {"operator": "landline"},  # 固定电话
            {"operator": "telecom"},  # 电信
        ]
        
        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig('phone', params, count=2)
            generator_class = default_registry.get_generator_class('phone')
            generator = generator_class(config)
            phones = generator.generate_batch(2)
            
            for j, phone in enumerate(phones, 1):
                print(f"    结果 {j}: {phone}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 电子邮箱生成器参数配置
    print_subsection("电子邮箱生成器 - 域名配置")
    try:
        configs = [
            {},  # 默认配置
            {"domain": "gmail.com"},  # 指定域名
            {"domain": "163.com"},  # 指定域名
            {"username_type": "chinese"},  # 中文用户名
        ]
        
        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig('email', params, count=2)
            generator_class = default_registry.get_generator_class('email')
            generator = generator_class(config)
            emails = generator.generate_batch(2)
            
            for j, email in enumerate(emails, 1):
                print(f"    结果 {j}: {email}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")


def batch_generation():
    """批量生成示例"""
    print_section("3. 批量生成示例")
    
    # 批量生成完整联系信息
    print_subsection("批量生成完整联系信息")
    try:
        contact_generators = ['name', 'phone', 'email', 'address']
        batch_size = 5
        
        print(f"  生成 {batch_size} 个人的完整联系信息:")
        print("  " + "-" * 100)
        print("  序号 | 姓名    | 电话号码      | 电子邮箱                    | 地址")
        print("  " + "-" * 100)
        
        for i in range(batch_size):
            contact_info = []
            
            # 首先生成姓名
            name_config = GeneratorConfig('name', {}, count=1)
            name_class = default_registry.get_generator_class('name')
            name_gen = name_class(name_config)
            name = name_gen.generate_single()
            contact_info.append(name)
            
            # 生成其他联系信息
            for generator_name in ['phone', 'email', 'address']:
                try:
                    config = GeneratorConfig(generator_name, {}, count=1)
                    generator_class = default_registry.get_generator_class(generator_name)
                    generator = generator_class(config)
                    result = generator.generate_single()
                    contact_info.append(str(result))
                except:
                    contact_info.append("N/A")
            
            # 格式化输出
            name = contact_info[0][:6].ljust(6)
            phone = contact_info[1][:12].ljust(12)
            email = contact_info[2][:25].ljust(25)
            address = contact_info[3][:45].ljust(45)
            
            print(f"  {i+1:2d}    | {name} | {phone} | {email} | {address}")
        
        print("  " + "-" * 100)
        
    except Exception as e:
        print(f"  ❌ 批量生成失败: {e}")


def validation_examples():
    """数据验证示例"""
    print_section("4. 数据验证示例")
    
    # 验证电话号码格式
    print_subsection("电话号码格式验证")
    try:
        config = GeneratorConfig('phone', {}, count=5)
        generator_class = default_registry.get_generator_class('phone')
        generator = generator_class(config)
        phones = generator.generate_batch(5)
        
        print("  生成的电话号码:")
        phone_pattern = re.compile(r'^1[3-9]\d{9}$')  # 简单的手机号验证
        
        for i, phone in enumerate(phones, 1):
            print(f"    {i}. {phone}")
            
            # 验证手机号格式
            is_valid = bool(phone_pattern.match(phone))
            print(f"       格式验证: {'✅ 有效' if is_valid else '❌ 无效'}")
        
    except Exception as e:
        print(f"  ❌ 电话号码验证失败: {e}")
    
    # 验证电子邮箱格式
    print_subsection("电子邮箱格式验证")
    try:
        config = GeneratorConfig('email', {}, count=5)
        generator_class = default_registry.get_generator_class('email')
        generator = generator_class(config)
        emails = generator.generate_batch(5)
        
        print("  生成的电子邮箱:")
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
        for i, email in enumerate(emails, 1):
            print(f"    {i}. {email}")
            
            # 验证邮箱格式
            is_valid = bool(email_pattern.match(email))
            print(f"       格式验证: {'✅ 有效' if is_valid else '❌ 无效'}")
        
    except Exception as e:
        print(f"  ❌ 电子邮箱验证失败: {e}")


def error_handling():
    """错误处理示例"""
    print_section("5. 错误处理示例")
    
    # 处理无效的地区参数
    print_subsection("处理无效的地区参数")
    try:
        config = GeneratorConfig('address', {"province": "不存在的省份"}, count=1)
        generator_class = default_registry.get_generator_class('address')
        generator = generator_class(config)
        address = generator.generate_single()
        print(f"  生成的地址: {address}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效地区错误: {type(e).__name__}")
    
    # 处理无效的域名参数
    print_subsection("处理无效的域名参数")
    try:
        config = GeneratorConfig('email', {"domain": "invalid.domain.format"}, count=1)
        generator_class = default_registry.get_generator_class('email')
        generator = generator_class(config)
        email = generator.generate_single()
        print(f"  生成的邮箱: {email}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效域名错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print_section("6. 最佳实践示例")
    
    # 实践1: 生成关联的联系信息
    print_subsection("实践1: 生成关联的联系信息")
    try:
        # 生成一个人物的完整联系信息
        person_data = {}
        
        # 生成基本信息
        name_config = GeneratorConfig('name', {}, count=1)
        name_class = default_registry.get_generator_class('name')
        name_gen = name_class(name_config)
        person_data['name'] = name_gen.generate_single()
        
        # 生成联系信息
        contact_configs = {
            'phone': GeneratorConfig('phone', {"operator": "mobile"}, count=1),
            'email': GeneratorConfig('email', {"domain": "gmail.com"}, count=1),
            'address': GeneratorConfig('address', {"province": "北京市"}, count=1)
        }
        
        for key, config in contact_configs.items():
            generator_class = default_registry.get_generator_class(key)
            generator = generator_class(config)
            person_data[key] = generator.generate_single()
        
        print("  生成的人物联系信息:")
        for key, value in person_data.items():
            print(f"    {key}: {value}")
        
        print("\n  💡 建议：为不同场景选择合适的参数组合")
        
    except Exception as e:
        print(f"  ❌ 关联信息生成失败: {e}")
    
    # 实践2: 批量导出格式化数据
    print_subsection("实践2: 批量导出格式化数据")
    try:
        contact_data = []
        
        # 生成多条联系信息
        for i in range(3):
            record = {}
            
            # 生成姓名
            name_config = GeneratorConfig('name', {}, count=1)
            name_class = default_registry.get_generator_class('name')
            name_gen = name_class(name_config)
            record['name'] = name_gen.generate_single()
            
            # 生成其他联系信息
            for field in ['phone', 'email', 'address']:
                config = GeneratorConfig(field, {}, count=1)
                generator_class = default_registry.get_generator_class(field)
                generator = generator_class(config)
                record[field] = generator.generate_single()
            
            contact_data.append(record)
        
        # 导出为JSON格式
        json_output = json.dumps(contact_data, ensure_ascii=False, indent=2)
        print("  JSON格式输出:")
        print(json_output)
        
    except Exception as e:
        print(f"  ❌ 格式化导出失败: {e}")


def main():
    """主函数，运行所有示例"""
    print("🎯 DataForge 基础生成器示例 - 联系方式类")
    print("本示例展示了联系方式相关生成器的各种使用方法")
    
    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        
        print_section("✅ 示例演示完成")
        print("🎉 所有联系方式类生成器示例已成功运行！")
        print("\n📚 相关文档:")
        print("  • 查看 examples/basic/personal_info_demo.py 了解个人信息生成器")
        print("  • 查看 examples/basic/profile_demo.py 了解个人档案生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")
        
    except Exception as e:
        print(f"\n❌ 示例运行出现错误: {e}")
        print("请检查DataForge环境配置是否正确")


if __name__ == "__main__":
    main()