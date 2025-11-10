#!/usr/bin/env python3
"""正确统计所有生成器的数量"""

import sys
import os
import re
from pathlib import Path

sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

from dataforge.core.factory import default_registry

def main():
    # 1. 已注册的生成器
    registered = default_registry.list_generators()
    print(f"📊 已注册的生成器: {len(registered)}个")
    
    # 2. 查找所有生成器文件
    generators_dir = Path("dataforge/generators")
    py_files = list(generators_dir.rglob("*.py"))
    
    # 排除__init__.py和其他非生成器文件
    generator_files = [f for f in py_files if f.name != "__init__.py" and f.name != "validation_base.py"]
    
    print(f"📁 生成器文件总数: {len(generator_files)}个")
    
    # 3. 统计每个文件中的@register_generator调用
    total_registrations = 0
    category_stats = {}
    
    for file_path in generator_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找@register_generator装饰器
            register_pattern = r'@register_generator\(\s*"([^"]+)"'
            matches = re.findall(register_pattern, content)
            
            relative_path = file_path.relative_to("dataforge/generators")
            category = relative_path.parts[0]  # 第一级目录作为分类
            
            total_registrations += len(matches)
            
            if category not in category_stats:
                category_stats[category] = {
                    'files': 0,
                    'registrations': 0,
                    'generators': []
                }
            
            category_stats[category]['files'] += 1
            category_stats[category]['registrations'] += len(matches)
            category_stats[category]['generators'].extend(matches)
            
            if matches:
                print(f"📂 {category}/{file_path.name}: {len(matches)}个注册")
                for gen_name in matches:
                    print(f"   - {gen_name}")
                    
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
    
    print(f"\n📈 分类统计:")
    for category, stats in sorted(category_stats.items()):
        print(f"  {category:12} | 文件: {stats['files']:2} | 注册: {stats['registrations']:2}")
    
    print(f"\n🎯 总结:")
    print(f"  已注册生成器:     {len(registered)}个")
    print(f"  生成器文件:       {len(generator_files)}个")
    print(f"  注册装饰器总数:   {total_registrations}个")
    print(f"  实际注册率:       {len(registered)}/{total_registrations}")
    
    # 4. 检查差异
    registered_set = set(registered)
    all_decorated = set()
    for stats in category_stats.values():
        all_decorated.update(stats['generators'])
    
    missing_from_registry = all_decorated - registered_set
    extra_in_registry = registered_set - all_decorated
    
    if missing_from_registry:
        print(f"\n❌ 有装饰器但未注册: {len(missing_from_registry)}个")
        for gen in sorted(missing_from_registry):
            print(f"   - {gen}")
    
    if extra_in_registry:
        print(f"\n✅ 已注册但无装饰器: {len(extra_in_registry)}个")
        for gen in sorted(extra_in_registry):
            print(f"   - {gen}")

if __name__ == "__main__":
    main()