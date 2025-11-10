#!/usr/bin/env python3
"""创建环境变量来禁用pytest警告"""

import os

def create_env_file():
    """创建.env文件来配置环境变量"""
    env_content = """# DataForge 环境配置

# 测试配置
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
PYTHONWARNINGS=ignore

# JWT密钥
JWT_SECRET_KEY=test-secret-key

# 禁用特定警告
PYTHONWARNINGS="ignore::DeprecationWarning:distutils.*,ignore::DeprecationWarning:pytest_freezegun.*,ignore::UserWarning"
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ .env文件已创建")

if __name__ == "__main__":
    create_env_file()