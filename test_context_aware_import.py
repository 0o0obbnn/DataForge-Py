#!/usr/bin/env python3
"""测试context_aware模块的导入和注册"""

import sys
import os
sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

def test_context_aware_import():
    try:
        from dataforge.generators.basic import context_aware
        print("✅ context_aware模块导入成功")
        
        # 检查是否有注册的生成器
        from dataforge.core.factory import default_registry
        generators = default_registry.list_generators()
        
        context_generators = [g for g in generators if 'context_aware' in g]
        print(f"找到的context_aware生成器: {context_generators}")
        
        return True
    except Exception as e:
        print(f"❌ context_aware模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_context_aware_import()