#!/usr/bin/env python3
"""测试生成器导入问题"""

import sys
import traceback

def test_import(module_name):
    """测试单个模块导入"""
    try:
        exec(f"from dataforge.generators import {module_name}")
        print(f"✅ {module_name} 导入成功")
        return True
    except Exception as e:
        print(f"❌ {module_name} 导入失败: {e}")
        traceback.print_exc()
        return False

def main():
    print("开始测试生成器模块导入...")
    
    modules = ["basic", "contact", "datetime", "finance", "identifier", "network", "numeric", "text"]
    
    success_count = 0
    failed_modules = []
    
    for module in modules:
        if test_import(module):
            success_count += 1
        else:
            failed_modules.append(module)
    
    print(f"\n导入测试完成:")
    print(f"成功: {success_count}/{len(modules)}")
    print(f"失败模块: {failed_modules}")
    
    if failed_modules:
        print("\n检查缺失的模块目录...")
        import os
        generators_dir = "dataforge/generators"
        for module in failed_modules:
            module_path = os.path.join(generators_dir, module)
            exists = os.path.exists(module_path)
            print(f"{module}: {'存在' if exists else '缺失'}")

if __name__ == "__main__":
    main()