#!/usr/bin/env python3
"""
安全测试工具演示脚本 - 使用DataForge架构
演示安全生成器的正确使用方式
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataforge.core.generator import GeneratorConfig
from dataforge.generators.security.sql_injection import GenericSQLInjectionGenerator
from dataforge.generators.security.xss_payload import GenericXSSPayloadGenerator


def demo_sql_injection():
    """演示SQL注入Payload生成器"""
    print("=" * 60)
    print("SQL注入Payload生成器演示")
    print("=" * 60)

    # 创建生成器实例
    sql_gen = GenericSQLInjectionGenerator()

    # 基础payload
    print("\n1. 基础SQL注入Payload:")
    for db in ['mysql', 'postgresql', 'sqlserver']:
        config = GeneratorConfig(parameters={"database": db})
        sql_gen.config = config
        payload = sql_gen.generate_single()
        print(f"  {db.upper()}: {payload}")

    # 批量生成
    print("\n2. 批量生成Payload:")
    payloads = sql_gen.generate_batch(count=5, parameters={"database": "mysql"})
    for i, payload in enumerate(payloads, 1):
        print(f"  {i}. {payload}")

    # 验证功能
    print("\n3. Payload验证:")
    test_payloads = [
        "' OR 1=1--",
        "admin'--",
        "SELECT * FROM users",
        "hello world"
    ]

    for payload in test_payloads:
        is_valid = sql_gen.validate(payload)
        status = "✓ 有效" if is_valid else "✗ 无效"
        print(f"  {payload:<20} {status}")


def demo_xss_payload():
    """演示XSS攻击Payload生成器"""
    print("\n" + "=" * 60)
    print("XSS攻击Payload生成器演示")
    print("=" * 60)

    # 创建生成器实例
    xss_gen = GenericXSSPayloadGenerator()

    # 不同复杂度的payload
    print("\n1. 不同复杂度的XSS Payload:")
    for complexity in ['basic', 'advanced']:
        config = GeneratorConfig(parameters={"complexity": complexity})
        xss_gen.config = config
        payload = xss_gen.generate_single()
        print(f"  {complexity.upper()}: {payload}")

    # 批量生成
    print("\n2. 批量生成Payload:")
    payloads = xss_gen.generate_batch(count=5, parameters={"complexity": "basic"})
    for i, payload in enumerate(payloads, 1):
        print(f"  {i}. {payload}")

    # 验证功能
    print("\n3. XSS Payload验证:")
    test_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')",
        "hello world",
        "<div>test</div>"
    ]

    for payload in test_payloads:
        is_valid = xss_gen.validate(payload)
        status = "✓ 有效" if is_valid else "✗ 无效"
        print(f"  {payload:<35} {status}")


if __name__ == "__main__":
    try:
        demo_sql_injection()
        demo_xss_payload()

        print("\n" + "=" * 60)
        print("演示完成！所有安全测试工具已正确运行")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 运行错误: {e}")
        import traceback
        traceback.print_exc()
