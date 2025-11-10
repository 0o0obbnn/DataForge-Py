#!/usr/bin/env python3
"""分析警告来源"""

import warnings
import sys

def analyze_warnings():
    """分析警告来源"""
    # 启用所有警告
    warnings.filterwarnings('always')
    
    try:
        import pytest_freezegun
        print("✅ pytest_freezegun导入成功")
    except Exception as e:
        print(f"❌ pytest_freezegun导入失败: {e}")
    
    # 检查distutils使用情况
    try:
        from distutils.version import LooseVersion
        print("⚠️ 检测到distutils.version.LooseVersion使用")
        print("这是DeprecationWarning的主要来源")
    except Exception as e:
        print(f"distutils检查失败: {e}")
    
    # 检查pytest_freezegun版本
    try:
        import pytest_freezegun
        if hasattr(pytest_freezegun, '__version__'):
            print(f"pytest_freezegun版本: {pytest_freezegun.__version__}")
    except:
        pass

if __name__ == "__main__":
    analyze_warnings()