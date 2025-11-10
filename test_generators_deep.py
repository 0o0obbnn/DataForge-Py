#!/usr/bin/env python3
"""深度测试所有生成器的可用性"""

import sys
from dataforge import default_registry

def main():
    print("深度测试所有注册的生成器...")
    
    generators = default_registry._generators
    print(f"总共注册了 {len(generators)} 个生成器")
    
    success_count = 0
    failed_generators = []
    
    for name, generator_class in generators.items():
        try:
            # 尝试实例化生成器
            generator = generator_class()
            print(f"✅ {name} - {generator_class.__name__}")
            success_count += 1
        except Exception as e:
            print(f"❌ {name} - 实例化失败: {e}")
            failed_generators.append(name)
    
    print(f"\n生成器实例化测试完成:")
    print(f"成功: {success_count}/{len(generators)}")
    print(f"失败生成器: {failed_generators}")
    
    # 测试一些核心生成器的实际生成功能
    print("\n测试核心生成器功能...")
    core_generators = ["bankcard", "company_name", "generic_waybill", "person_name", "phone"]
    
    for gen_name in core_generators:
        if gen_name in generators:
            try:
                generator = generators[gen_name]()
                result = generator.generate()
                print(f"✅ {gen_name} 生成: {result}")
            except Exception as e:
                print(f"❌ {gen_name} 生成失败: {e}")
        else:
            print(f"⚠️  {gen_name} 未找到")

if __name__ == "__main__":
    main()