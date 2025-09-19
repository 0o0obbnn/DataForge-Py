#!/usr/bin/env python3
"""
调试API批量生成问题
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient

from dataforge.api.main import app


def debug_batch_generation():
    client = TestClient(app)

    payload = {
        "generators": [
            {"generator_type": "name", "parameters": {"gender": "FEMALE"}},
            {"generator_type": "email", "parameters": {"type": "COMMON"}},
            {"generator_type": "age", "parameters": {"min": 25, "max": 35}},
        ],
        "count": 2,
        "output_format": "json",
    }

    print("测试批量生成...")
    response = client.post("/batch/generate", json=payload)
    print(f"状态码: {response.status_code}")

    if response.status_code != 200:
        print(f"错误响应: {response.text}")
    else:
        result = response.json()
        print(f"成功: {result['success']}")
        print(f"生成器: {result['generators']}")
        print(f"记录数: {result['count']}")


if __name__ == "__main__":
    debug_batch_generation()
