#!/usr/bin/env python3
"""
检查生成器注册情况
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def check_generators():
    """检查生成器注册情况"""
    print("检查生成器注册情况...")
    
    try:
        from dataforge.core.factory import default_registry
        generators = default_registry.list_generators()
        print(f"已注册生成器数量: {len(generators)}")
        print(f"已注册生成器列表: {sorted(generators)}")
        
        # 检查关键生成器
        key_generators = ["name", "phone", "bankcard", "idcard"]
        for gen in key_generators:
            if gen in generators:
                print(f"✅ 生成器 '{gen}' 已注册")
            else:
                print(f"❌ 生成器 '{gen}' 未注册")
        
        return generators
    except Exception as e:
        print(f"检查生成器注册情况失败: {e}")
        import traceback
        traceback.print_exc()
        return []

def main():
    """主函数"""
    print("开始检查生成器注册情况...")
    generators = check_generators()
    
    if generators:
        print(f"\n✅ 成功获取生成器列表，共 {len(generators)} 个生成器")
        return True
    else:
        print("\n❌ 获取生成器列表失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
