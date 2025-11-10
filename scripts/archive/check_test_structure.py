#!/usr/bin/env python3
"""
检查测试目录结构
"""

import os

def list_test_structure():
    """列出测试目录结构"""
    test_root = "tests"
    
    if not os.path.exists(test_root):
        print(f"测试目录 {test_root} 不存在")
        return
    
    print(f"测试目录结构 ({test_root}):")
    print("-" * 40)
    
    for root, dirs, files in os.walk(test_root):
        level = root.replace(test_root, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                print(f"{subindent}{file}")

if __name__ == "__main__":
    list_test_structure()