#!/usr/bin/env python3
"""
调试FastAPI接口错误
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
            "info",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def debug_api():
    """调试API错误"""
    base_url = "http://127.0.0.1:8000"

    print("=== 调试FastAPI接口 ===\n")

    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(3)

    try:
        # 1. 测试一个已知工作的生成器
        print("1. 测试已知工作的生成器 (name):")
        payload = {"count": 2, "parameters": {}}
        response = requests.post(f"{base_url}/generate/name", json=payload, timeout=5)
        print(f"   状态: {response.status_code}")
        if response.status_code == 200:
            print(f"   响应: {response.json()}")
        else:
            print(f"   错误: {response.text}")
        print()

        # 2. 测试车牌号生成器，逐步调试
        print("2. 调试车牌号生成器:")

        # 先试试不带参数
        print("   a) 不带参数:")
        simple_payload = {"count": 1}
        response = requests.post(
            f"{base_url}/generate/license_plate", json=simple_payload, timeout=5
        )
        print(f"      状态: {response.status_code}")
        if response.status_code != 200:
            print(f"      错误: {response.text}")
        else:
            print(f"      响应: {response.json()}")

        # 再试试带参数
        print("   b) 带参数:")
        param_payload = {"count": 1, "parameters": {"type": "FUEL"}}
        response = requests.post(
            f"{base_url}/generate/license_plate", json=param_payload, timeout=5
        )
        print(f"      状态: {response.status_code}")
        if response.status_code != 200:
            print(f"      错误: {response.text}")
        else:
            print(f"      响应: {response.json()}")

        print()

        # 3. 测试API文档
        print("3. 检查API文档:")
        response = requests.get(f"{base_url}/docs", timeout=5)
        print(f"   Swagger UI状态: {response.status_code}")

        response = requests.get(f"{base_url}/openapi.json", timeout=5)
        print(f"   OpenAPI Schema状态: {response.status_code}")

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

        timer = Timer(20.0, kill_server)  # 20秒后自动关闭
        timer.start()

        # 调试API
        debug_api()

        # 取消定时器
        timer.cancel()

        # 打印服务器日志
        if server_process.poll() is None:  # 进程还在运行
            print("\n📋 服务器输出:")
            try:
                stdout, stderr = server_process.communicate(timeout=1)
                if stdout:
                    print("STDOUT:")
                    print(stdout)
                if stderr:
                    print("STDERR:")
                    print(stderr)
            except subprocess.TimeoutExpired:
                pass

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
