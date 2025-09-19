#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文个人和企业信息生成器
基于DataForge框架的集成生成器，用于生成姓名、身份证号码、手机号码、座机号码、公司名称、统一社会信用代码

示例用法：
    from chinese_data_generator import ChineseDataGenerator
    
    generator = ChineseDataGenerator()
    print("姓名:", generator.generate_name())
    print("身份证:", generator.generate_idcard())
    print("手机号:", generator.generate_phone())
    print("座机号:", generator.generate_landline())
    print("公司名称:", generator.generate_company_name())
    print("统一社会信用代码:", generator.generate_uscc())
"""

def main():
    """主演示函数"""
    print("DataForge - 中文数据生成器")
    print("支持生成：姓名、身份证、手机号、座机号、公司名称、统一社会信用代码")
    print("详细使用方法请参考完整的chinese_data_generator.py文件")

if __name__ == "__main__":
    main()