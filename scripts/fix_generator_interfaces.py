#!/usr/bin/env python3
"""批量修复生成器接口合规性"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Set

# 生成器类型映射
GENERATOR_TYPE_MAPPING = {
    'basic': 'GeneratorType.BASIC',
    'auth': 'GeneratorType.AUTH', 
    'contact': 'GeneratorType.CONTACT',
    'finance': 'GeneratorType.FINANCE',
    'identifier': 'GeneratorType.IDENTIFIER',
    'network': 'GeneratorType.NETWORK',
    'numeric': 'GeneratorType.NUMERIC',
    'text': 'GeneratorType.TEXT',
    'advanced': 'GeneratorType.ADVANCED'
}

def get_generator_type_by_path(file_path: Path) -> str:
    """根据文件路径推断生成器类型"""
    path_parts = file_path.parts
    for part in path_parts:
        if part in GENERATOR_TYPE_MAPPING:
            return GENERATOR_TYPE_MAPPING[part]
    return 'GeneratorType.BASIC'  # 默认类型

def extract_class_info(file_path: Path) -> List[Dict]:
    """提取文件中的生成器类信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)
    except Exception as e:
        print(f"❌ 无法解析文件 {file_path}: {e}")
        return []

    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # 检查是否继承DataGenerator
            is_generator = any(
                (isinstance(base, ast.Name) and 'Generator' in base.id) or
                (isinstance(base, ast.Attribute) and 'Generator' in base.attr)
                for base in node.bases
            )
            
            if is_generator:
                classes.append({
                    'name': node.name,
                    'line': node.lineno
                })
    
    return classes

def add_missing_methods(file_path: Path) -> bool:
    """为文件添加缺失的方法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 无法读取文件 {file_path}: {e}")
        return False

    classes = extract_class_info(file_path)
    if not classes:
        return False

    generator_type = get_generator_type_by_path(file_path)
    
    # 检查是否已经有必需的方法
    has_generate_single = 'def generate_single(' in content
    has_validate = 'def validate(' in content
    has_generator_type = '@property' in content and 'def generator_type(' in content
    has_supported_parameters = '@property' in content and 'def supported_parameters(' in content

    if has_generate_single and has_validate and has_generator_type and has_supported_parameters:
        return True  # 已经合规

    # 准备要添加的方法
    methods_to_add = []

    if not has_generate_single:
        methods_to_add.append('''
    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        # TODO: 实现具体的生成逻辑
        return self.generate(context) if hasattr(self, 'generate') else ""''')

    if not has_validate:
        methods_to_add.append('''
    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        return isinstance(data, str) and bool(data.strip())''')

    if not has_generator_type:
        methods_to_add.append(f'''
    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return {generator_type}''')

    if not has_supported_parameters:
        methods_to_add.append('''
    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []  # TODO: 添加实际支持的参数''')

    if not methods_to_add:
        return True

    # 添加必要的导入
    imports_to_add = []
    if 'from typing import Optional' not in content and 'Optional' not in content:
        imports_to_add.append('from typing import Optional')
    
    if 'GenerationContext' not in content:
        imports_to_add.append('from dataforge.core.generator import GenerationContext')
    
    if 'GeneratorType' not in content:
        imports_to_add.append('from dataforge.core.types import GeneratorType')

    # 找到最后一个类的结束位置
    lines = content.split('\n')
    last_class_end = len(lines)
    
    # 找到第一个生成器类
    for i, line in enumerate(lines):
        if any(f'class {cls["name"]}' in line for cls in classes):
            # 找到这个类的结束位置
            indent_level = len(line) - len(line.lstrip())
            for j in range(i + 1, len(lines)):
                if lines[j].strip() and (len(lines[j]) - len(lines[j].lstrip())) <= indent_level:
                    last_class_end = j
                    break
            break

    # 在类的最后添加方法
    new_lines = lines[:last_class_end]
    for method in methods_to_add:
        new_lines.extend(method.split('\n'))
    new_lines.extend(lines[last_class_end:])

    # 添加导入到文件开头
    if imports_to_add:
        import_insert_pos = 0
        for i, line in enumerate(new_lines):
            if line.startswith('from ') or line.startswith('import '):
                import_insert_pos = i + 1
        
        for imp in reversed(imports_to_add):
            new_lines.insert(import_insert_pos, imp)

    # 写回文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f"✅ 修复了 {file_path}")
        return True
    except Exception as e:
        print(f"❌ 无法写入文件 {file_path}: {e}")
        return False

def main():
    """主函数"""
    generators_dir = Path('dataforge/generators')
    
    if not generators_dir.exists():
        print(f"❌ 生成器目录不存在: {generators_dir}")
        return 1

    print("开始批量修复生成器接口...")
    
    fixed_count = 0
    total_count = 0
    
    for py_file in generators_dir.rglob('*.py'):
        if py_file.name == '__init__.py':
            continue
            
        total_count += 1
        if add_missing_methods(py_file):
            fixed_count += 1

    print(f"\n修复完成: {fixed_count}/{total_count} 个文件")
    return 0

if __name__ == '__main__':
    exit(main())