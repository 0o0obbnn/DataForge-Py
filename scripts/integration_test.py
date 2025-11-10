#!/usr/bin/env python3
"""
前后端联调测试脚本
测试DataForge Web Console与DataForge API的集成
"""

import time
from datetime import datetime

import requests

# 配置
FRONTEND_URL = "http://localhost:5173"
BACKEND_URL = "http://localhost:8000"

def test_backend_api():
    """测试后端API功能"""
    print("🔍 测试后端API功能...")

    # 1. 健康检查
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        health_data = response.json()
        print(f"✅ 健康检查: {health_data['status']} - {health_data['generators_count']}个生成器")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

    # 2. 获取生成器列表
    try:
        response = requests.get(f"{BACKEND_URL}/generators")
        generators = response.json()
        working_generators = [g for g in generators if 'configuration error' not in g.get('description', '').lower()]
        error_generators = [g for g in generators if 'configuration error' in g.get('description', '').lower()]

        print(f"✅ 生成器列表: {len(working_generators)}个正常, {len(error_generators)}个配置错误")
        if error_generators:
            print("   配置错误的生成器:")
            for gen in error_generators[:3]:
                print(f"   - {gen['name']}: {gen['description']}")
    except Exception as e:
        print(f"❌ 获取生成器列表失败: {e}")
        return False

    # 3. 测试单个生成器
    test_generators = ['name', 'age', 'email', 'phone']
    for gen_name in test_generators:
        try:
            payload = {
                "generator_type": gen_name,
                "count": 3,
                "parameters": {},
                "should_validate": True,
                "output_format": "json"
            }
            response = requests.post(f"{BACKEND_URL}/generate/{gen_name}", json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {gen_name}生成器: 生成{data['count']}条数据")
            else:
                print(f"❌ {gen_name}生成器失败: {response.status_code}")
        except Exception as e:
            print(f"❌ {gen_name}生成器异常: {e}")

    # 4. 测试批量生成
    try:
        payload = {
            "generators": [
                {"generator_type": "name", "parameters": {"type": "full"}},
                {"generator_type": "age", "parameters": {"min": 18, "max": 65}},
                {"generator_type": "email", "parameters": {}}
            ],
            "count": 2,
            "output_format": "json"
        }
        response = requests.post(f"{BACKEND_URL}/batch/generate", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 批量生成: 生成{data['count']}条关联数据")
            print(f"   示例数据: {data['data'][0] if data['data'] else 'N/A'}")
        else:
            print(f"❌ 批量生成失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 批量生成异常: {e}")

    return True

def test_frontend_access():
    """测试前端访问"""
    print("🌐 测试前端访问...")

    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print("✅ 前端页面可访问")
            return True
        else:
            print(f"❌ 前端访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端访问异常: {e}")
        return False

def test_cors():
    """测试CORS配置"""
    print("🔒 测试CORS配置...")

    try:
        headers = {
            'Origin': FRONTEND_URL,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{BACKEND_URL}/health", headers=headers)

        cors_headers = response.headers
        if 'Access-Control-Allow-Origin' in cors_headers:
            print(f"✅ CORS配置正常: {cors_headers.get('Access-Control-Allow-Origin')}")
            return True
        else:
            print("❌ CORS配置缺失")
            return False
    except Exception as e:
        print(f"❌ CORS测试异常: {e}")
        return False

def performance_test():
    """性能测试"""
    print("⚡ 性能测试...")

    # 测试响应时间
    test_cases = [
        ("健康检查", f"{BACKEND_URL}/health"),
        ("生成器列表", f"{BACKEND_URL}/generators"),
    ]

    for name, url in test_cases:
        try:
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()

            response_time = (end_time - start_time) * 1000
            if response.status_code == 200:
                print(f"✅ {name}: {response_time:.2f}ms")
            else:
                print(f"❌ {name}: 请求失败")
        except Exception as e:
            print(f"❌ {name}: 异常 - {e}")

def main():
    """主测试函数"""
    print("=" * 60)
    print("🚀 DataForge 前后端联调测试")
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 测试后端API
    backend_ok = test_backend_api()
    print()

    # 测试前端访问
    frontend_ok = test_frontend_access()
    print()

    # 测试CORS
    cors_ok = test_cors()
    print()

    # 性能测试
    performance_test()
    print()

    # 总结
    print("=" * 60)
    print("📊 测试总结:")
    print(f"   后端API: {'✅ 正常' if backend_ok else '❌ 异常'}")
    print(f"   前端访问: {'✅ 正常' if frontend_ok else '❌ 异常'}")
    print(f"   CORS配置: {'✅ 正常' if cors_ok else '❌ 异常'}")

    if backend_ok and frontend_ok and cors_ok:
        print("🎉 前后端联调测试通过！")
        return True
    else:
        print("⚠️  发现问题，需要修复")
        return False

if __name__ == "__main__":
    main()
