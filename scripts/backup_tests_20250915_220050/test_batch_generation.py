#!/usr/bin/env python3
"""
测试批量生成修正版本
"""

import os
import subprocess
import sys
import time
from threading import Timer

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


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


def test_batch_generation():
    """测试批量生成"""
    base_url = "http://127.0.0.1:8000"

    print("=== 测试批量生成 ===\n")

    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(3)

    try:
        # 测试批量生成（修正请求格式）
        print("测试批量生成:")
        batch_payload = {
            "generators": [
                {
                    "generator_type": "license_plate",
                    "count": 2,
                    "parameters": {"type": "NEW_ENERGY"},
                },
                {
                    "generator_type": "company_name",
                    "count": 2,
                    "parameters": {"industry": "FINANCE"},
                },
                {"generator_type": "uscc", "count": 1, "parameters": {}},
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
        print("🎉 批量生成测试完成！")

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器")
    except Exception as e:
        print(f"❌ 测试错误: {e}")


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

        timer = Timer(15.0, kill_server)  # 15秒后自动关闭
        timer.start()

        # 测试批量生成
        test_batch_generation()

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
