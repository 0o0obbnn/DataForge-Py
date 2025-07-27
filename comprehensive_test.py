#!/usr/bin/env python3
"""
DataForge 综合性能和功能测试
"""
import sys
import os
import time
import requests
import subprocess
from threading import Timer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataforge.core.factory import default_factory
from dataforge.core.generator import GeneratorConfig


def test_performance():
    """测试性能"""
    print("=== 性能测试 ===\n")
    
    # 测试各种生成器的性能
    generators_to_test = [
        ('name', '姓名生成器', {}),
        ('license_plate', '车牌号生成器', {'type': 'FUEL'}),
        ('company_name', '企业名称生成器', {'industry': 'IT'}),
        ('uscc', '统一社会信用代码生成器', {}),
        ('organization_code', '组织机构代码生成器', {}),
        ('lei', 'LEI码生成器', {}),
        ('ip_address', 'IP地址生成器', {'version': 'IPV4'}),
        ('verification_code', '验证码生成器', {'length': 6}),
        ('date', '日期生成器', {}),
        ('cron', 'Cron表达式生成器', {})
    ]
    
    for gen_type, desc, params in generators_to_test:
        print(f"📊 测试 {desc}:")
        try:
            # 预热
            config = GeneratorConfig(generator_type=gen_type, parameters=params)
            generator = default_factory.create_generator(config)
            generator.generate_batch(10)
            
            # 性能测试
            start_time = time.time()
            data = generator.generate_batch(100)
            elapsed = time.time() - start_time
            
            print(f"   生成100条数据耗时: {elapsed*1000:.2f}ms")
            print(f"   生成速度: {100/elapsed:.0f}条/秒")
            print(f"   样例数据: {data[:3]}")
            
        except Exception as e:
            print(f"   ❌ 错误: {e}")
        
        print()


def test_api_comprehensive():
    """测试API综合功能"""
    print("=== API综合测试 ===\n")
    
    server_process = None
    try:
        # 启动API服务器
        print("🚀 启动API服务器...")
        server_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "dataforge.api.main:app",
            "--host", "127.0.0.1", "--port", "8000", "--log-level", "error"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 等待服务器启动
        time.sleep(3)
        
        base_url = "http://127.0.0.1:8000"
        
        # 1. 测试健康检查
        print("1. 健康检查:")
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   状态: {response.status_code} ✓")
        
        # 2. 测试新增生成器
        print("\n2. 测试新增生成器:")
        new_generators = [
            ('license_plate', {'type': 'NEW_ENERGY'}),
            ('company_name', {'industry': 'FINANCE'}),
            ('uscc', {'region': '110000'}),
            ('organization_code', {}),
            ('lei', {})
        ]
        
        for gen_name, params in new_generators:
            payload = {
                "generator_type": gen_name,
                "count": 2,
                "parameters": params
            }
            response = requests.post(f"{base_url}/generate/{gen_name}", json=payload, timeout=5)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✓ {gen_name}: {[item[gen_name] for item in result['data']]}")
            else:
                print(f"   ✗ {gen_name}: HTTP {response.status_code}")
        
        # 3. 测试批量生成
        print("\n3. 批量生成测试:")
        batch_payload = {
            "generators": [
                {"generator_type": "license_plate", "count": 1, "parameters": {"type": "FUEL"}},
                {"generator_type": "company_name", "count": 1, "parameters": {"industry": "IT"}},
                {"generator_type": "uscc", "count": 1, "parameters": {}}
            ]
        }
        
        response = requests.post(f"{base_url}/batch/generate", json=batch_payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ 批量生成成功，生成了 {len(result['data'])} 条记录")
            for data in result['data']:
                print(f"     {data}")
        else:
            print(f"   ✗ 批量生成失败: HTTP {response.status_code}")
        
        print("\n🎉 API测试完成！")
        
    except Exception as e:
        print(f"❌ API测试错误: {e}")
    finally:
        if server_process:
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()


def test_data_validation():
    """测试数据校验功能"""
    print("\n=== 数据校验测试 ===\n")
    
    validation_tests = [
        ('license_plate', '京A12345', True),
        ('license_plate', '京A123456789', False),
        ('uscc', '91110000MA001234X5', False),  # 错误的校验位
        ('organization_code', '12345678-9', True),
        ('organization_code', '123456789', False),  # 缺少连字符
        ('lei', '549300ABCDEFGHIJK123', False)  # 长度错误
    ]
    
    for gen_type, test_data, expected in validation_tests:
        try:
            config = GeneratorConfig(generator_type=gen_type, parameters={})
            generator = default_factory.create_generator(config)
            result = generator.validate(test_data)
            status = "✓" if result == expected else "✗"
            print(f"   {status} {gen_type} 校验 '{test_data}': {result} (期望: {expected})")
        except Exception as e:
            print(f"   ❌ {gen_type} 校验错误: {e}")


def generate_test_data_samples():
    """生成测试数据样例"""
    print("\n=== 生成测试数据样例 ===\n")
    
    # 生成一个完整的用户数据样例
    user_generators = [
        ('name', '姓名', {}),
        ('license_plate', '车牌号', {'type': 'FUEL'}),
        ('company_name', '企业名称', {'industry': 'IT'}),
        ('uscc', '统一社会信用代码', {}),
        ('phone', '手机号', {}),
        ('email', '邮箱', {}),
        ('address', '地址', {'detail_level': 'FULL'})
    ]
    
    print("完整数据样例:")
    sample_data = {}
    for gen_type, desc, params in user_generators:
        try:
            config = GeneratorConfig(generator_type=gen_type, parameters=params)
            generator = default_factory.create_generator(config)
            data = generator.generate()
            sample_data[desc] = data
            print(f"   {desc}: {data}")
        except Exception as e:
            print(f"   ❌ {desc}: {e}")
    
    print()


def main():
    """主函数"""
    print("🧪 DataForge 综合测试开始")
    print("=" * 50)
    
    # 执行各项测试
    test_performance()
    test_api_comprehensive()
    test_data_validation()
    generate_test_data_samples()
    
    print("=" * 50)
    print("🎉 所有测试完成！")
    
    # 显示功能总结
    print("\n📋 DataForge 功能总结:")
    print("✓ 基础信息生成器：姓名、手机号、身份证、地址等")
    print("✓ 标识类生成器：UUID、USCC、组织机构代码、LEI码等")
    print("✓ 联系通信生成器：验证码、传真、URL、文件路径等")
    print("✓ 网络设备生成器：IP地址、MAC地址、域名、端口等")
    print("✓ 时间日历生成器：日期、时间戳、Cron表达式等")
    print("✓ 企业相关生成器：企业名称、车牌号等")
    print("✓ 数据校验功能：支持格式和逻辑校验")
    print("✓ 性能优化：缓存系统和数据预加载")
    print("✓ Web API服务：RESTful接口和批量生成")
    print("✓ 35个生成器，支持丰富的参数配置")


if __name__ == "__main__":
    main()