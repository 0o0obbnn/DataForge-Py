#!/usr/bin/env python3
"""统计所有生成器文件和注册情况"""

import os
from pathlib import Path

def count_generators_with_decorator():
    """统计所有带@register_generator装饰器的生成器"""
    
    generators_dir = Path("F:/projects/data_forge_py/data_forge_py/dataforge/generators")
    
    # 找到所有Python文件（排除__init__.py和备份文件）
    py_files = []
    for root, dirs, files in os.walk(generators_dir):
        for file in files:
            if file.endswith('.py') and not file.startswith('__init__') and not file.endswith('.bak'):
                py_files.append(Path(root) / file)
    
    print(f"总共找到 {len(py_files)} 个Python生成器文件")
    
    # 按模块分组
    modules = {}
    for file_path in py_files:
        relative_path = file_path.relative_to(generators_dir)
        module_name = relative_path.parts[0]  # 第一级目录名
        
        if module_name not in modules:
            modules[module_name] = []
        modules[module_name].append(file_path)
    
    # 统计每个模块的文件数和装饰器数
    decorator_counts = {}
    
    for module_name, files in modules.items():
        decorator_count = 0
        print(f"\n=== {module_name} 模块 ===")
        print(f"文件数量: {len(files)}")
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_decorator_count = content.count('@register_generator')
                    if file_decorator_count > 0:
                        decorator_count += file_decorator_count
                        print(f"  ✓ {file_path.name}: {file_decorator_count} 个装饰器")
                    else:
                        print(f"  ✗ {file_path.name}: 0 个装饰器")
            except Exception as e:
                print(f"  ERROR {file_path.name}: {e}")
        
        decorator_counts[module_name] = decorator_count
        print(f"模块总计: {decorator_count} 个装饰器")
    
    print(f"\n=== 总体统计 ===")
    total_decorators = sum(decorator_counts.values())
    print(f"总装饰器数量: {total_decorators}")
    
    # 检查哪些模块的__init__.py是空的
    print(f"\n=== __init__.py 文件状态 ===")
    for module_name in modules.keys():
        init_file = generators_dir / module_name / "__init__.py"
        if init_file.exists():
            try:
                with open(init_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        print(f"  ✗ {module_name}/__init__.py: 空文件")
                    else:
                        print(f"  ✓ {module_name}/__init__.py: 有内容 ({len(content)} 字符)")
            except Exception as e:
                print(f"  ERROR {module_name}/__init__.py: {e}")
        else:
            print(f"  ✗ {module_name}/__init__.py: 不存在")
    
    return modules, decorator_counts

if __name__ == "__main__":
    count_generators_with_decorator()