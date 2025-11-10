#!/usr/bin/env python3
"""
简化的API批量测试
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient

from dataforge.api.main import app


def test_simple_batch():
    client = TestClient(app)

    # 先测试路由是否能被正确匹配
    print("1. 测试batch路由匹配...")
    response = client.post("/batch/generate", json={})
    print(f"空请求状态码: {response.status_code}")
    print(f"错误详情: {response.text}")

    # 测试最小化的有效请求
    print("\n2. 测试最小化有效请求...")
    minimal_payload = {"generators": [{"generator_type": "uuid"}], "count": 1}

    response = client.post("/batch/generate", json=minimal_payload)
    print(f"最小请求状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"成功: {result.get('success', False)}")
    else:
        print(f"错误: {response.text}")


if __name__ == "__main__":
    test_simple_batch()
