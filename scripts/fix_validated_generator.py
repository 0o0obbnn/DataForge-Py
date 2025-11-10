#!/usr/bin/env python3
"""
批量修复ValidatedDataGenerator导入
"""
import os
from pathlib import Path

def fix_file(file_path: Path):
    """修复单个文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'ValidatedDataGenerator' not in content:
        return False
    
    # 替换导入
    content = content.replace(
        'from ...core.generator import GenerationContext, ValidatedDataGenerator',
        'from ...core.generator import DataGenerator, GenerationContext'
    )
    content = content.replace(
        'from dataforge.core.generator import ValidatedDataGenerator',
        'from dataforge.core.generator import DataGenerator'
    )
    content = content.replace(
        'from ...core.generator import (\n    GenerationContext,\n    GeneratorConfig,\n    ValidatedDataGenerator,\n)',
        'from ...core.generator import (\n    DataGenerator,\n    GenerationContext,\n    GeneratorConfig,\n)'
    )
    content = content.replace(
        '    ValidatedDataGenerator,',
        '    DataGenerator,'
    )
    
    # 替换类继承
    content = content.replace('ValidatedDataGenerator', 'DataGenerator')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函数"""
    generators_dir = Path('dataforge/generators')
    fixed = 0
    
    for py_file in generators_dir.rglob('*.py'):
        if py_file.name == '__init__.py':
            continue
        
        if fix_file(py_file):
            print(f"✅ {py_file}")
            fixed += 1
    
    print(f"\n修复了 {fixed} 个文件")
    return 0

if __name__ == '__main__':
    exit(main())
