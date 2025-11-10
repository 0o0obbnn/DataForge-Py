#!/usr/bin/env python3
"""
DataForge API服务启动脚本
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dataforge.api.main import run_server


def main():
    """启动API服务"""
    print("🚀 启动DataForge API服务...")
    print("📖 API文档: http://localhost:8000/docs")
    print("🔄 健康检查: http://localhost:8000/health")
    print("📋 生成器列表: http://localhost:8000/generators")
    print("🛑 按 Ctrl+C 停止服务")
    print("-" * 50)

    try:
        run_server(host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")


if __name__ == "__main__":
    main()
