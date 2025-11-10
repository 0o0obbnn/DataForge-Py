#!/usr/bin/env python3
"""测试修复后的生成器导入"""

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
    print("开始测试修复后的生成器模块导入...")
    
    # 只测试实际存在的模块
    modules = ["basic", "contact", "finance", "identifier", "network", "numeric", "text"]
    
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
    
    # 测试整体导入
    print("\n测试整体导入...")
    try:
        import dataforge
        print("✅ dataforge 整体导入成功")
        
        # 测试默认注册表
        from dataforge import default_registry
        print(f"✅ 默认注册表导入成功，包含 {len(default_registry._generators)} 个生成器")
        
    except Exception as e:
        print(f"❌ 整体导入失败: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()