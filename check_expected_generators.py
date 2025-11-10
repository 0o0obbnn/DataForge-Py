#!/usr/bin/env python3
"""检查测试期望的生成器"""

import sys
import os
sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

from tests.integration.test_all_generators import get_expected_generators

def main():
    expected = get_expected_generators()
    print(f'测试期望的生成器数量: {len(expected)}')
    print('\n期望的生成器列表:')
    for i, gen in enumerate(sorted(expected), 1):
        print(f'{i:2d}. {gen}')

if __name__ == "__main__":
    main()