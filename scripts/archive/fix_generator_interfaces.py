#!/usr/bin/env python3
"""
批量修复生成器接口不一致问题的脚本
"""

import os
import re
from pathlib import Path
from typing import List, Tuple


def find_generator_files() -> List[Path]:
    """查找所有生成器文件"""
    generator_dirs = [
        "dataforge/generators/basic",
        "dataforge/generators/contact", 
        "dataforge/generators/finance",
        "dataforge/generators/identifier",
        "dataforge/generators/network",
        "dataforge/generators/text",
        "dataforge/generators/numeric",
        "dataforge/generators/auth",
        "dataforge/generators/advanced",
    ]
    
    files = []
    for dir_path in generator_dirs:
        if os.path.exists(dir_path):
            for file_path in Path(dir_path).rglob("*.py"):
                if file_path.name != "__init__.py":
                    files.append(file_path)
    
    return files


def fix_generator_type_property(content: str) -> str:
    """修复generator_type属性返回类型"""
    # 查找错误的generator_type定义
    patterns = [
        # 修复返回字符串的generator_type
        (r'(\s+)generator_type:\s*str\s*=\s*"([^"]+)"', 
         r'\1@property\n\1def generator_type(self) -> GeneratorType:\n\1    return GeneratorType.\2'),
        
        # 修复返回字符串的@property方法
        (r'(\s+)@property\s*\n\s+def generator_type\(self\)\s*->\s*str:', 
         r'\1@property\n\1def generator_type(self) -> GeneratorType:'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    return content


def fix_supported_parameters_property(content: str) -> str:
    """修复supported_parameters属性类型"""
    # 查找错误的supported_parameters定义
    patterns = [
        # 修复dict类型的supported_parameters
        (r'(\s+)supported_parameters:\s*dict\[.*?\]\s*=\s*\{.*?\}', 
         r'\1@property\n\1def supported_parameters(self) -> list[str]:\n\1    return []'),
        
        # 修复返回dict的@property方法
        (r'(\s+)@property\s*\n\s+def supported_parameters\(self\)\s*->\s*dict\[.*?\]:', 
         r'\1@property\n\1def supported_parameters(self) -> list[str]:'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    return content


def fix_generate_raw_signature(content: str) -> str:
    """修复_generate_raw方法签名"""
    # 统一_generate_raw方法签名
    patterns = [
        # 修复缺少context参数的方法
        (r'(\s+)def _generate_raw\(self\)\s*->\s*([^:]+):', 
         r'\1def _generate_raw(self, context: Optional[GenerationContext] = None) -> \2:'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    return content


def fix_generate_single_signature(content: str) -> str:
    """修复generate_single方法签名"""
    # 统一generate_single方法签名
    patterns = [
        # 修复参数类型不匹配的方法
        (r'(\s+)def generate_single\(self,\s*context:\s*GenerationContext\)\s*->\s*([^:]+):', 
         r'\1def generate_single(self, context: Optional[GenerationContext] = None) -> \2:'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    return content


def add_missing_imports(content: str) -> str:
    """添加缺失的导入"""
    # 检查是否需要添加导入
    needs_optional = "Optional[" in content and "from typing import" in content and "Optional" not in content
    needs_generator_type = "GeneratorType" in content and "from dataforge.core.generator import" in content
    
    if needs_optional:
        # 添加Optional导入
        content = re.sub(
            r'(from typing import [^\\n]*)',
            r'\1, Optional',
            content
        )
    
    if needs_generator_type and "GeneratorType" not in content:
        # 添加GeneratorType导入
        content = re.sub(
            r'(from \.\.\.core\.generator import[^\\n]*)',
            r'\1, GeneratorType',
            content
        )
    
    return content


def fix_generator_file(file_path: Path) -> bool:
    """修复单个生成器文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        content = original_content
        
        # 应用各种修复
        content = fix_generator_type_property(content)
        content = fix_supported_parameters_property(content)
        content = fix_generate_raw_signature(content)
        content = fix_generate_single_signature(content)
        content = add_missing_imports(content)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 修复: {file_path}")
            return True
        else:
            print(f"⏭️  跳过: {file_path} (无需修复)")
            return False
            
    except Exception as e:
        print(f"❌ 错误: {file_path} - {e}")
        return False


def main():
    """主函数"""
    print("开始批量修复生成器接口...")
    print("=" * 60)
    
    files = find_generator_files()
    print(f"找到 {len(files)} 个生成器文件")
    print()
    
    fixed_count = 0
    for file_path in files:
        if fix_generator_file(file_path):
            fixed_count += 1
    
    print()
    print("=" * 60)
    print(f"修复完成: {fixed_count}/{len(files)} 个文件被修复")
    
    if fixed_count > 0:
        print("\\n建议运行以下命令验证修复效果:")
        print("python -m mypy dataforge/generators/ --ignore-missing-imports --no-error-summary")


if __name__ == "__main__":
    main()