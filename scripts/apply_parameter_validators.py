#!/usr/bin/env python3
"""
应用参数验证到所有生成器
"""

import ast
import os
from pathlib import Path


def check_has_parameter_validation(file_path: Path) -> bool:
    """检查文件是否已使用参数验证"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        return 'ParameterValidator' in content or 'parameter_validators' in content


def main():
    """主函数"""
    generators_dir = Path('dataforge/generators')
    
    total = 0
    with_validation = 0
    without_validation = []
    
    for py_file in generators_dir.rglob('*.py'):
        if py_file.name == '__init__.py':
            continue
        
        total += 1
        if check_has_parameter_validation(py_file):
            with_validation += 1
        else:
            without_validation.append(str(py_file))
    
    print("=" * 80)
    print("参数验证应用情况")
    print("=" * 80)
    print(f"总文件数: {total}")
    print(f"已应用: {with_validation}")
    print(f"未应用: {len(without_validation)}")
    print(f"应用率: {with_validation / total * 100:.1f}%")
    
    if without_validation:
        print("\n未应用参数验证的文件:")
        for f in without_validation[:10]:
            print(f"  {f}")
        if len(without_validation) > 10:
            print(f"  ... 还有 {len(without_validation) - 10} 个文件")
    
    return 0


if __name__ == '__main__':
    exit(main())
