#!/usr/bin/env python3
"""创建pytest配置文件以过滤警告"""

import os

def create_pytest_ini():
    """创建pytest.ini配置文件"""
    config_content = """[tool:pytest]
minversion = 6.0
addopts = 
    -ra
    --strict-markers
    --strict-config
    --tb=short
    --disable-warnings
filterwarnings =
    ignore::DeprecationWarning:distutils.*
    ignore::DeprecationWarning:pytest_freezegun.*
    ignore::UserWarning
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
"""
    
    with open('pytest.ini', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("✅ pytest.ini配置文件已创建")

def update_pyproject_toml():
    """更新pyproject.toml中的pytest配置"""
    try:
        with open('pyproject.toml', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有[tool.pytest]配置
        if '[tool.pytest]' in content:
            print("⚠️ pyproject.toml中已有pytest配置")
            return
        
        # 添加pytest配置
        pytest_config = """

[tool.pytest.ini_options]
minversion = "6.0"
addopts = [
    "-ra",
    "--strict-markers", 
    "--strict-config",
    "--tb=short",
    "--disable-warnings",
]
filterwarnings = [
    "ignore::DeprecationWarning:distutils.*",
    "ignore::DeprecationWarning:pytest_freezegun.*",
    "ignore::UserWarning",
]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
"""
        
        with open('pyproject.toml', 'a', encoding='utf-8') as f:
            f.write(pytest_config)
        
        print("✅ pyproject.toml pytest配置已添加")
        
    except Exception as e:
        print(f"❌ 更新pyproject.toml失败: {e}")

if __name__ == "__main__":
    create_pytest_ini()
    update_pyproject_toml()