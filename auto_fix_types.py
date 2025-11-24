#!/usr/bin/env python3
"""
自动修复类型注解脚本
使用autotyping工具批量处理Python文件
"""

import subprocess
import sys
from pathlib import Path


def run_autotyping(file_path: Path) -> bool:
    """对单个文件运行autotyping"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "autotyping", str(file_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"✅ {file_path}")
            return True
        else:
            print(f"❌ {file_path}: {result.stderr}")
            return False
    except Exception as e:
        print(f"⚠️ {file_path}: {e}")
        return False


def main():
    """主函数"""
    # 定义要处理的目录
    directories = [
        "dataforge/utils",
        "dataforge/output",
        "dataforge/core",
        "dataforge/cli",
        "dataforge/config",
        "dataforge/generators/basic",
        "dataforge/generators/contact",
        "dataforge/generators/finance",
        "dataforge/generators/identifier",
        "dataforge/generators/network",
        "dataforge/generators/text",
        "dataforge/generators/numeric",
        "dataforge/generators/advanced",
        "dataforge/generators/auth",
    ]
    
    total_files = 0
    success_files = 0
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"⚠️ 目录不存在: {directory}")
            continue
        
        print(f"\n📁 处理目录: {directory}")
        print("=" * 60)
        
        # 获取所有Python文件
        py_files = list(dir_path.glob("*.py"))
        
        for py_file in py_files:
            # 跳过__init__.py
            if py_file.name == "__init__.py":
                continue
            
            total_files += 1
            if run_autotyping(py_file):
                success_files += 1
    
    print("\n" + "=" * 60)
    print(f"📊 总结:")
    print(f"   总文件数: {total_files}")
    print(f"   成功: {success_files}")
    print(f"   失败: {total_files - success_files}")
    print(f"   成功率: {success_files/total_files*100:.1f}%")


if __name__ == "__main__":
    main()
