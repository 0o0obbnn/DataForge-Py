#!/usr/bin/env python3
"""统计所有生成器的数量"""

import sys
import os
import ast
from pathlib import Path

sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

from dataforge.core.factory import default_registry

def find_generator_classes(file_path):
    """在Python文件中查找生成器类"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        generators = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # 检查是否继承自DataGenerator
                for base in node.bases:
                    if (isinstance(base, ast.Name) and base.id == 'DataGenerator') or \
                       (isinstance(base, ast.Attribute) and base.attr == 'DataGenerator'):
                        generators.append(node.name)
                        break
        
        return generators
    except Exception as e:
        return []

def find_register_decorators(file_path):
    """在Python文件中查找注册装饰器"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        registrations = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 检查函数装饰器
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call) and \
                       isinstance(decorator.func, ast.Name) and \
                       decorator.func.id == 'register_generator':
                        # 获取注册名称
                        if decorator.args:
                            arg = decorator.args[0]
                            if isinstance(arg, ast.Constant):
                                registrations.append(arg.value)
                            elif isinstance(arg, ast.Str):
                                registrations.append(arg.s)
        
        return registrations
    except Exception as e:
        return []

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
    
    # 3. 统计各类生成器
    total_generator_classes = 0
    total_register_calls = 0
    category_stats = {}
    
    for file_path in generator_files:
        relative_path = file_path.relative_to("dataforge/generators")
        category = relative_path.parts[0]  # 第一级目录作为分类
        
        generator_classes = find_generator_classes(file_path)
        register_calls = find_register_decorators(file_path)
        
        total_generator_classes += len(generator_classes)
        total_register_calls += len(register_calls)
        
        if category not in category_stats:
            category_stats[category] = {
                'files': 0,
                'classes': 0,
                'registrations': 0
            }
        
        category_stats[category]['files'] += 1
        category_stats[category]['classes'] += len(generator_classes)
        category_stats[category]['registrations'] += len(register_calls)
        
        if generator_classes or register_calls:
            print(f"\n📂 {category}/{file_path.name}:")
            if generator_classes:
                print(f"   生成器类: {len(generator_classes)}个 - {generator_classes}")
            if register_calls:
                print(f"   注册调用: {len(register_calls)}个 - {register_calls}")
    
    print(f"\n📈 分类统计:")
    for category, stats in sorted(category_stats.items()):
        print(f"  {category:12} | 文件: {stats['files']:2} | 类: {stats['classes']:2} | 注册: {stats['registrations']:2}")
    
    print(f"\n🎯 总结:")
    print(f"  已注册生成器:     {len(registered)}个")
    print(f"  生成器文件:       {len(generator_files)}个")
    print(f"  生成器类总数:     {total_generator_classes}个")
    print(f"  注册调用总数:     {total_register_calls}个")
    print(f"  未注册的类:       {total_generator_classes - len(registered)}个")
    print(f"  注册率:           {len(registered)/total_generator_classes*100:.1f}%")

if __name__ == "__main__":
    main()