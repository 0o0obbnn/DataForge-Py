#!/usr/bin/env python3
"""
修正的FastAPI接口测试
"""

import subprocess
import sys
import time
from threading import Timer

import requests


def start_api_server():
    """启动API服务器"""
    print("🚀 启动FastAPI服务器...")
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "dataforge.api.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
            "--log-level",
            "error",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def test_api_endpoints():
    """测试API端点"""
    base_url = "http://127.0.0.1:8000"

    print("=== 测试FastAPI端点 ===\n")

    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(3)

    try:
        # 1. 测试健康检查
        print("1. 健康检查:")
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   状态: {response.status_code}")
        print(f"   响应: {response.json()}")
        print()

        # 2. 测试生成器列表
        print("2. 生成器列表:")
        response = requests.get(f"{base_url}/generators", timeout=5)
        generators = response.json()
        print(f"   可用生成器数量: {len(generators)}")

        # 检查新增的生成器
        new_generators = [
            "license_plate",
            "company_name",
            "uscc",
            "organization_code",
            "lei",
        ]
        found_generators = []
        for gen in generators:
            if gen["name"] in new_generators:
                found_generators.append(gen["name"])
                print(f"   ✓ {gen['name']}: {gen['description']}")

        missing = set(new_generators) - set(found_generators)
        if missing:
            print(f"   ⚠️ 缺失生成器: {missing}")
        print()

        # 3. 测试新增生成器（修正请求格式）
        test_cases = [
            {
                "name": "车牌号",
                "generator": "license_plate",
                "params": {"type": "FUEL"},
            },
            {
                "name": "企业名称",
                "generator": "company_name",
                "params": {"industry": "IT"},
            },
            {
                "name": "统一社会信用代码",
                "generator": "uscc",
                "params": {"region": "110000"},
            },
            {"name": "组织机构代码", "generator": "organization_code", "params": {}},
            {"name": "LEI码", "generator": "lei", "params": {}},
        ]

        print("3. 测试新增生成器:")
        for case in test_cases:
            try:
                # 正确的请求格式
                payload = {
                    "generator_type": case["generator"],  # 必需字段
                    "count": 2,
                    "parameters": case["params"],
                }
                response = requests.post(
                    f"{base_url}/generate/{case['generator']}", json=payload, timeout=5
                )

                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✓ {case['name']}: {result['data']}")
                else:
                    print(f"   ✗ {case['name']}: HTTP {response.status_code}")
                    print(f"     错误: {response.text}")

            except Exception as e:
                print(f"   ✗ {case['name']}: {e}")

        print()

        # 4. 测试批量生成（修正请求格式）
        print("4. 测试批量生成:")
        batch_payload = {
            "generators": [
                {
                    "type": "license_plate",
                    "count": 2,
                    "parameters": {"type": "NEW_ENERGY"},
                },
                {
                    "type": "company_name",
                    "count": 2,
                    "parameters": {"industry": "FINANCE"},
                },
                {"type": "uscc", "count": 1, "parameters": {}},
            ]
        }

        try:
            response = requests.post(
                f"{base_url}/batch/generate", json=batch_payload, timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                print("   ✓ 批量生成成功:")
                for gen_result in result["results"]:
                    print(f"     {gen_result['generator_type']}: {gen_result['data']}")
            else:
                print(f"   ✗ 批量生成失败: HTTP {response.status_code}")
                print(f"     错误: {response.text}")
        except Exception as e:
            print(f"   ✗ 批量生成错误: {e}")

        print()

        # 5. 测试单个生成器信息
        print("5. 测试生成器信息:")
        for generator_name in ["license_plate", "company_name"]:
            try:
                response = requests.get(
                    f"{base_url}/generators/{generator_name}", timeout=5
                )
                if response.status_code == 200:
                    info = response.json()
                    print(f"   ✓ {generator_name}: {info['description']}")
                    print(f"     支持参数: {info['parameters']}")
                else:
                    print(f"   ✗ {generator_name}: HTTP {response.status_code}")
            except Exception as e:
                print(f"   ✗ {generator_name}: {e}")

        print()
        print("🎉 API测试完成！")

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器")
    except Exception as e:
        print(f"❌ API测试错误: {e}")

def main():
    """主函数"""
    server_process = None

    try:
        # 启动服务器
        server_process = start_api_server()

        # 设置超时杀死服务器
        def kill_server():
            if server_process:
                server_process.terminate()

        timer = Timer(30.0, kill_server)  # 30秒后自动关闭
        timer.start()

        # 测试API
        test_api_endpoints()

        # 取消定时器
        timer.cancel()

    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
    finally:
        # 关闭服务器
        if server_process:
            print("🛑 关闭API服务器...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()

if __name__ == "__main__":
    main()
