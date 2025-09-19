#!/usr/bin/env python3
"""
调试批量生成响应
"""

import json
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


def debug_batch_response():
    """调试批量生成响应"""
    base_url = "http://127.0.0.1:8000"

    print("=== 调试批量生成响应 ===\n")

    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(3)

    try:
        # 测试批量生成
        print("测试批量生成:")
        batch_payload = {
            "generators": [
                {
                    "generator_type": "license_plate",
                    "count": 1,
                    "parameters": {"type": "FUEL"},
                },
                {"generator_type": "company_name", "count": 1, "parameters": {}},
            ]
        }

        response = requests.post(
            f"{base_url}/batch/generate", json=batch_payload, timeout=10
        )
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")

        if response.status_code == 200:
            result = response.json()
            print("完整响应:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"错误响应: {response.text}")

        print()
        print("🔍 调试完成！")

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器")
    except Exception as e:
        print(f"❌ 调试错误: {e}")


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

        # 调试批量生成
        debug_batch_response()

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
