#!/usr/bin/env python3
"""
DataForge API启动脚本
"""
import os
import sys

# 设置开发环境
os.environ['DEVELOPMENT'] = 'true'

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 80)
    print("DataForge API Server")
    print("=" * 80)
    print("Environment: Development")
    print("API Docs: http://127.0.0.1:8000/docs")
    print("=" * 80)
    
    uvicorn.run(
        "dataforge.api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
