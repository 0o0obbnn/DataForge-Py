#!/usr/bin/env python3
"""检查注册的生成器数量"""

import sys
import os
sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

from dataforge.core.factory import default_registry

def main():
    generators = default_registry.list_generators()
    print(f'实际注册的生成器数量: {len(generators)}')
    print('\n注册的生成器列表:')
    for i, gen in enumerate(sorted(generators), 1):
        print(f'{i:2d}. {gen}')
    
    print(f'\n按类型分类:')
    # 按前缀分类
    categories = {}
    for gen in generators:
        prefix = gen.split('_')[0] if '_' in gen else 'other'
        if prefix not in categories:
            categories[prefix] = []
        categories[prefix].append(gen)
    
    for prefix, gens in sorted(categories.items()):
        print(f'{prefix}: {len(gens)}个')
        for gen in sorted(gens):
            print(f'  - {gen}')

if __name__ == "__main__":
    main()