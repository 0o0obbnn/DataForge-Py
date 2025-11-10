#!/usr/bin/env python3
"""单元验证脚本 - 验证修复的功能"""

def test_generator_config():
    """验证GeneratorConfig.get()方法修复"""
    try:
        from dataforge.core.generator import GeneratorConfig
        config = GeneratorConfig('test', {'precision': 'MILLIS'})
        
        # 测试get方法
        assert config.get('precision') == 'MILLIS'
        assert config.get('missing', 'default') == 'default'
        
        # 测试字典式访问
        assert config['precision'] == 'MILLIS'
        assert 'precision' in config
        assert 'missing' not in config
        
        print('✅ GeneratorConfig.get() 方法验证通过')
        return True
    except Exception as e:
        print(f'❌ GeneratorConfig.get() 方法验证失败: {e}')
        return False

def test_generic_waybill():
    """验证generic_waybill修复"""
    try:
        from dataforge.generators.identifier.logistics import GenericWaybillGenerator
        from dataforge.core.generator import GeneratorConfig
        
        gen = GenericWaybillGenerator(GeneratorConfig('generic_waybill', {'carrier': 'SF'}))
        
        # 生成多个运单号进行验证
        for _ in range(10):
            data = gen.generate_single()
            tracking_number = data['tracking_number']
            assert gen.validate(data), f'验证失败: {tracking_number}'
        
        print('✅ generic_waybill 验证逻辑修复通过')
        return True
    except Exception as e:
        print(f'❌ generic_waybill 验证逻辑修复失败: {e}')
        return False

def test_company_name():
    """验证company_name长度修复"""
    try:
        from dataforge.generators.basic.company_name import CompanyNameGenerator
        from dataforge.core.generator import GeneratorConfig
        
        gen = CompanyNameGenerator(GeneratorConfig('company_name', {'prefix_region': False}))
        
        # 生成100个公司名称验证长度
        for _ in range(100):
            name = gen.generate_single()
            assert len(name) >= 4, f'名称过短: {name}'
        
        print('✅ company_name 长度要求验证通过')
        return True
    except Exception as e:
        print(f'❌ company_name 长度要求验证失败: {e}')
        return False

if __name__ == '__main__':
    print('开始单元验证...')
    
    results = []
    results.append(test_generator_config())
    results.append(test_generic_waybill())
    results.append(test_company_name())
    
    passed = sum(results)
    total = len(results)
    
    print(f'\n验证结果: {passed}/{total} 通过')
    
    if passed == total:
        print('🎉 所有单元验证通过!')
    else:
        print('⚠️ 部分验证失败，需要进一步检查')