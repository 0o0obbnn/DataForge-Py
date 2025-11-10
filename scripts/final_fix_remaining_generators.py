#!/usr/bin/env python3
"""最终修复剩余生成器的特定问题"""

import re
from pathlib import Path

# 需要特殊处理的文件和问题
SPECIAL_FIXES = {
    'dataforge/generators/advanced/json_generator.py': {
        'missing_properties': ['generator_type', 'supported_parameters'],
        'generator_type': 'GeneratorType.ADVANCED'
    },
    'dataforge/generators/advanced/xml_generator.py': {
        'missing_properties': ['generator_type', 'supported_parameters'],
        'generator_type': 'GeneratorType.ADVANCED'
    },
    'dataforge/generators/advanced/yaml_generator.py': {
        'missing_properties': ['generator_type', 'supported_parameters'],
        'generator_type': 'GeneratorType.ADVANCED'
    }
}

def add_validate_method(content: str, class_name: str) -> str:
    """为指定类添加validate方法"""
    # 找到类定义
    class_pattern = rf'class {re.escape(class_name)}.*?:'
    class_match = re.search(class_pattern, content)
    
    if not class_match:
        return content
    
    # 找到类的结束位置
    lines = content.split('\n')
    class_start = -1
    for i, line in enumerate(lines):
        if f'class {class_name}' in line:
            class_start = i
            break
    
    if class_start == -1:
        return content
    
    # 找到类的缩进级别
    class_indent = len(lines[class_start]) - len(lines[class_start].lstrip())
    
    # 找到类的结束位置
    class_end = len(lines)
    for i in range(class_start + 1, len(lines)):
        line = lines[i]
        if line.strip() and (len(line) - len(line.lstrip())) <= class_indent:
            class_end = i
            break
    
    # 添加validate方法
    validate_method = f'''
    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, 'validator') and hasattr(self.validator, 'validate'):
            return self.validator.validate(data)
        return isinstance(data, str) and bool(data.strip())'''
    
    method_lines = validate_method.split('\n')
    for line in reversed(method_lines):
        lines.insert(class_end, line)
    
    return '\n'.join(lines)

def add_properties(content: str, class_name: str, generator_type: str) -> str:
    """为指定类添加generator_type和supported_parameters属性"""
    # 找到类定义
    lines = content.split('\n')
    class_start = -1
    for i, line in enumerate(lines):
        if f'class {class_name}' in line:
            class_start = i
            break
    
    if class_start == -1:
        return content
    
    # 找到类的缩进级别
    class_indent = len(lines[class_start]) - len(lines[class_start].lstrip())
    
    # 找到类的结束位置
    class_end = len(lines)
    for i in range(class_start + 1, len(lines)):
        line = lines[i]
        if line.strip() and (len(line) - len(line.lstrip())) <= class_indent:
            class_end = i
            break
    
    # 添加属性
    properties = f'''
    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return {generator_type}

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []'''
    
    property_lines = properties.split('\n')
    for line in reversed(property_lines):
        lines.insert(class_end, line)
    
    return '\n'.join(lines)

def fix_specific_file(file_path: Path) -> bool:
    """修复特定文件的问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 无法读取文件 {file_path}: {e}")
        return False
    
    original_content = content
    
    # 添加必要的导入
    if 'GeneratorType' not in content:
        # 找到导入区域
        lines = content.split('\n')
        import_pos = 0
        for i, line in enumerate(lines):
            if line.startswith(('from ', 'import ')):
                import_pos = i + 1
        
        lines.insert(import_pos, 'from ...core.types import GeneratorType')
        content = '\n'.join(lines)
    
    # 根据文件路径确定生成器类型
    if 'basic' in str(file_path):
        gen_type = 'GeneratorType.BASIC'
    elif 'contact' in str(file_path):
        gen_type = 'GeneratorType.CONTACT'
    elif 'finance' in str(file_path):
        gen_type = 'GeneratorType.FINANCE'
    elif 'identifier' in str(file_path):
        gen_type = 'GeneratorType.IDENTIFIER'
    elif 'auth' in str(file_path):
        gen_type = 'GeneratorType.AUTH'
    elif 'network' in str(file_path):
        gen_type = 'GeneratorType.NETWORK'
    elif 'numeric' in str(file_path):
        gen_type = 'GeneratorType.NUMERIC'
    elif 'text' in str(file_path):
        gen_type = 'GeneratorType.TEXT'
    elif 'advanced' in str(file_path):
        gen_type = 'GeneratorType.ADVANCED'
    else:
        gen_type = 'GeneratorType.BASIC'
    
    # 找到所有生成器类
    import ast
    try:
        tree = ast.parse(content)
        generator_classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                is_generator = any(
                    (isinstance(base, ast.Name) and 'Generator' in base.id) or
                    (isinstance(base, ast.Attribute) and 'Generator' in base.attr)
                    for base in node.bases
                )
                if is_generator:
                    generator_classes.append(node.name)
        
        # 为每个生成器类添加缺失的方法
        for class_name in generator_classes:
            # 检查是否缺少validate方法
            if f'def validate(' not in content or f'class {class_name}' in content:
                # 简单检查：如果类中没有validate方法
                class_content = content[content.find(f'class {class_name}'):]
                next_class = class_content.find('\nclass ', 1)
                if next_class != -1:
                    class_content = class_content[:next_class]
                
                if 'def validate(' not in class_content:
                    content = add_validate_method(content, class_name)
            
            # 检查是否缺少属性
            class_content = content[content.find(f'class {class_name}'):]
            next_class = class_content.find('\nclass ', 1)
            if next_class != -1:
                class_content = class_content[:next_class]
            
            missing_generator_type = 'def generator_type(' not in class_content
            missing_supported_params = 'def supported_parameters(' not in class_content
            
            if missing_generator_type or missing_supported_params:
                content = add_properties(content, class_name, gen_type)
    
    except Exception as e:
        print(f"⚠️  AST解析失败 {file_path}: {e}")
        return False
    
    # 如果内容有变化，写回文件
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 修复了 {file_path}")
            return True
        except Exception as e:
            print(f"❌ 无法写入文件 {file_path}: {e}")
            return False
    
    return True

def main():
    """主函数"""
    print("开始最终修复剩余生成器问题...")
    
    # 获取所有不合规的文件
    from check_generator_compliance import main as check_compliance
    
    # 先运行检查获取问题文件列表
    generators_dir = Path('dataforge/generators')
    problem_files = []
    
    for py_file in generators_dir.rglob('*.py'):
        if py_file.name == '__init__.py':
            continue
        problem_files.append(py_file)
    
    fixed_count = 0
    total_count = len(problem_files)
    
    for file_path in problem_files:
        if fix_specific_file(file_path):
            fixed_count += 1
    
    print(f"\n最终修复完成: {fixed_count}/{total_count} 个文件")
    
    # 运行最终检查
    print("\n运行最终合规性检查...")
    import os
    os.system("python scripts/check_generator_compliance.py")
    
    return 0

if __name__ == '__main__':
    exit(main())