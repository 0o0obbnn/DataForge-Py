#!/usr/bin/env python3
"""集成测试验证脚本"""

def test_dynamic_generator_detection():
    """测试动态生成器检测功能"""
    try:
        import sys
        sys.path.append('.')
        from dataforge.core.factory import default_registry
        
        generators = list(default_registry.list_generators())
        print(f'动态检测到 {len(generators)} 个生成器')
        print('前10个生成器:', generators[:10])
        
        return len(generators) > 0
    except Exception as e:
        print(f'动态生成器检测失败: {e}')
        return False

def test_registry_access():
    """测试注册表访问"""
    try:
        import sys
        sys.path.append('.')
        from dataforge.core.factory import default_registry
        
        generators = list(default_registry.list_generators())
        print(f'注册表中有 {len(generators)} 个生成器')
        print('前10个生成器:', generators[:10])
        
        return len(generators) > 0
    except Exception as e:
        print(f'注册表访问失败: {e}')
        return False

if __name__ == '__main__':
    print('开始集成验证...')
    
    results = []
    results.append(test_dynamic_generator_detection())
    results.append(test_registry_access())
    
    passed = sum(results)
    total = len(results)
    
    print(f'\n集成验证结果: {passed}/{total} 通过')
    
    if passed == total:
        print('🎉 所有集成验证通过!')
    else:
        print('⚠️ 部分验证失败，需要进一步检查')