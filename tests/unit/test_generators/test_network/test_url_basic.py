#!/usr/bin/env python3
"""
URL生成器简单测试脚本
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import random
import string
from urllib.parse import urlunparse


class SimpleURLGenerator:
    """简化URL生成器"""

    def __init__(self, **kwargs):
        self.protocol = kwargs.get("protocol", "https")
        self.include_path = kwargs.get("include_path", True)
        self.include_query = kwargs.get("include_query", True)
        self.include_fragment = kwargs.get("include_fragment", False)

    def generate(self) -> str:
        """生成URL"""
        # 域名
        domains = ["example.com", "test.com", "demo.org", "sample.net"]
        domain = random.choice(domains)

        # 路径
        path = ""
        if self.include_path:
            segments = []
            for _i in range(random.randint(1, 3)):
                word = "".join(
                    random.choices(string.ascii_lowercase, k=random.randint(3, 8))
                )
                segments.append(word)
            path = "/" + "/".join(segments)

        # 查询参数
        query = ""
        if self.include_query:
            params = {}
            for _i in range(random.randint(1, 3)):
                key = random.choice(["id", "page", "search", "type", "category"])
                value = "".join(
                    random.choices(
                        string.ascii_lowercase + string.digits, k=random.randint(3, 6)
                    )
                )
                params[key] = value
            query = "&".join([f"{k}={v}" for k, v in params.items()])

        # 片段
        fragment = ""
        if self.include_fragment:
            fragment = random.choice(["section1", "top", "content", "comments"])

        # 构建URL
        url_parts = (f"{self.protocol}", domain, path, "", query, fragment)

        return urlunparse(url_parts)

def test_url_generator():
    """测试URL生成器"""
    print("=== URL生成器测试 ===")

    # 基础测试
    generator = SimpleURLGenerator()
    for i in range(5):
        url = generator.generate()
        print(f"基础URL {i + 1}: {url}")

    print()

    # 自定义测试
    custom_gen = SimpleURLGenerator(
        protocol="http", include_path=True, include_query=True, include_fragment=True
    )
    for i in range(3):
        url = custom_gen.generate()
        print(f"自定义URL {i + 1}: {url}")

if __name__ == "__main__":
    test_url_generator()
