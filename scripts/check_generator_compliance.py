#!/usr/bin/env python3
"""检查所有生成器是否符合接口规范"""

import ast
import os
from pathlib import Path
from typing import Set

def check_generator_file(file_path: Path) -> dict:
    """检查单个生成器文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except Exception as e:
        return {
            'file': str(file_path),
            'classes': [],
            'issues': [{'error': f'Failed to parse file: {e}'}]
        }

    results = {
        'file': str(file_path),
        'classes': [],
        'issues': []
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # 检查是否继承DataGenerator
            is_generator = any(
                (isinstance(base, ast.Name) and 'Generator' in base.id) or
                (isinstance(base, ast.Attribute) and 'Generator' in base.attr)
                for base in node.bases
            )

            if is_generator:
                class_info = {
                    'name': node.name,
                    'has_generate_single': False,
                    'has_validate': False,
                    'has_generator_type': False,
                    'has_supported_parameters': False
                }

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if item.name == 'generate_single':
                            class_info['has_generate_single'] = True
                        elif item.name == 'validate':
                            class_info['has_validate'] = True
                        elif item.name in ['generator_type', 'supported_parameters']:
                            # 检查是否有@property装饰器
                            for dec in item.decorator_list:
                                if isinstance(dec, ast.Name) and dec.id == 'property':
                                    if item.name == 'generator_type':
                                        class_info['has_generator_type'] = True
                                    elif item.name == 'supported_parameters':
                                        class_info['has_supported_parameters'] = True

                results['classes'].append(class_info)

                # 记录缺失的方法
                missing = []
                if not class_info['has_generate_single']:
                    missing.append('generate_single()')
                if not class_info['has_validate']:
                    missing.append('validate()')
                if not class_info['has_generator_type']:
                    missing.append('generator_type property')
                if not class_info['has_supported_parameters']:
                    missing.append('supported_parameters property')

                if missing:
                    results['issues'].append({
                        'class': node.name,
                        'missing': missing
                    })

    return results

def main():
    """主函数"""
    generators_dir = Path('dataforge/generators')
    all_results = []
    total_generators = 0
    compliant_generators = 0

    print("=" * 80)
    print("生成器接口合规性检查报告")
    print("=" * 80)

    if not generators_dir.exists():
        print(f"❌ 生成器目录不存在: {generators_dir}")
        return 1

    for py_file in generators_dir.rglob('*.py'):
        if py_file.name == '__init__.py':
            continue

        result = check_generator_file(py_file)
        
        # 统计生成器数量
        for class_info in result['classes']:
            total_generators += 1
            if not any(issue['class'] == class_info['name'] for issue in result['issues']):
                compliant_generators += 1
        
        if result['issues']:
            all_results.append(result)

    # 打印统计信息
    print(f"总生成器数量: {total_generators}")
    print(f"合规生成器数量: {compliant_generators}")
    print(f"不合规生成器数量: {total_generators - compliant_generators}")
    print()

    if not all_results:
        print("✅ 所有生成器都符合接口规范！")
        return 0
    else:
        print(f"❌ 发现 {len(all_results)} 个文件存在问题：\n")
        for result in all_results:
            print(f"文件: {result['file']}")
            for issue in result['issues']:
                if 'error' in issue:
                    print(f"  错误: {issue['error']}")
                else:
                    print(f"  类: {issue['class']}")
                    print(f"  缺少: {', '.join(issue['missing'])}")
            print()

        return len(all_results)

if __name__ == '__main__':
    exit(main())