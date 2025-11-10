#!/usr/bin/env python3
"""
DataForge 测试导入路径简化修复脚本
"""

import os
import re
from pathlib import Path


def fix_test_imports():
    """修复测试文件中的导入问题"""
    project_root = Path.cwd()
    tests_dir = project_root / "tests"

    print("🚀 开始修复测试导入路径...")
    print(f"📁 项目根目录: {project_root}")
    print(f"📂 测试目录: {tests_dir}")

    # 查找所有Python测试文件
    test_files = []
    for pattern in ["*.py"]:
        test_files.extend(tests_dir.rglob(pattern))

    # 过滤文件
    filtered_files = []
    for file_path in test_files:
        if "__pycache__" not in str(file_path) and file_path.name != "__init__.py":
            filtered_files.append(file_path)

    print(f"📋 找到 {len(filtered_files)} 个测试文件")

    fixed_files = []
    error_files = []

    # 定义需要移除的模式
    patterns_to_remove = [
        r'sys\.path\.insert\(0,\s*os\.path\.dirname\(os\.path\.abspath\(__file__\)\)\)',
        r'sys\.path\.insert\(0,\s*os\.path\.dirname\(__file__\)\)',
        r'sys\.path\.insert\(0,\s*os\.path\.join\(os\.path\.dirname\(__file__\),\s*["\'][^"\']*["\']\)\)',
        r'sys\.path\.insert\(0,\s*str\(Path\(__file__\)\.parent\)\)',
        r'sys\.path\.insert\(0,\s*os\.path\.abspath\(os\.path\.join\(os\.path\.dirname\(__file__\),\s*["\'][^"\']*["\']\)\)\)',
    ]

    comment_patterns = [
        r'#\s*添加项目根目录到.*路径.*\n',
        r'#\s*Add project root to path.*\n',
    ]

    # 修复每个文件
    for file_path in filtered_files:
        try:
            print(f"🔍 检查: {file_path.relative_to(project_root)}")

            with open(file_path, encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 移除sys.path.insert语句
            for pattern in patterns_to_remove:
                content = re.sub(pattern, '', content)

            # 移除相关注释
            for pattern in comment_patterns:
                content = re.sub(pattern, '', content)

            # 清理多余的空行
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            content = content.strip() + '\n'

            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"✅ 已修复: {file_path.name}")
            else:
                print(f"ℹ️  无需修复: {file_path.name}")

        except Exception as e:
            error_files.append((file_path, str(e)))
            print(f"❌ 修复失败: {file_path.name} - {e}")

    # 创建缺失的__init__.py文件
    print("\n📝 创建缺失的__init__.py文件...")
    created_init_files = []

    for root, dirs, files in os.walk(tests_dir):
        for dir_name in dirs:
            if not dir_name.startswith('.') and dir_name != '__pycache__':
                directory = Path(root) / dir_name
                init_file = directory / "__init__.py"
                if not init_file.exists():
                    try:
                        with open(init_file, 'w', encoding='utf-8') as f:
                            f.write('"""测试模块初始化文件"""\n')
                        created_init_files.append(init_file)
                        print(f"✅ 创建: {init_file.relative_to(project_root)}")
                    except Exception as e:
                        error_files.append((init_file, f"创建失败: {str(e)}"))

    # 生成简化报告
    print("\n🎉 修复完成!")
    print(f"✅ 修复文件数: {len(fixed_files)}")
    print(f"📝 创建__init__.py文件数: {len(created_init_files)}")
    print(f"❌ 错误文件数: {len(error_files)}")

    if fixed_files:
        print("\n📋 已修复的文件:")
        for file_path in fixed_files:
            print(f"  - {file_path.relative_to(project_root)}")

    if error_files:
        print("\n❌ 错误文件:")
        for file_path, error in error_files:
            if isinstance(file_path, Path):
                print(f"  - {file_path.relative_to(project_root)}: {error}")
            else:
                print(f"  - {file_path}: {error}")

    # 生成详细报告
    report_content = f"""# DataForge 测试导入路径修复报告

## 执行摘要
- **执行时间**: {os.popen('date /t').read().strip() if os.name == 'nt' else os.popen('date').read().strip()}
- **项目根目录**: {project_root}
- **测试目录**: {tests_dir}

## 统计信息
- 总测试文件数: {len(filtered_files)}
- 已修复文件数: {len(fixed_files)}
- 创建__init__.py文件数: {len(created_init_files)}
- 错误文件数: {len(error_files)}

## 修复策略
1. **移除手动路径设置**: 删除所有 `sys.path.insert` 语句
2. **依赖conftest.py**: 通过pytest的conftest.py统一管理Python路径
3. **创建__init__.py**: 为所有测试子目录创建包初始化文件

## 验证步骤
```bash
# 运行所有测试
pytest tests/ -v

# 按类别运行测试
pytest tests/unit/ -v          # 单元测试
pytest tests/integration/ -v   # 集成测试
pytest tests/api/ -v           # API测试

# 检查导入
python -c "import dataforge; print('✅ DataForge导入成功')"
```

## 已修复文件
"""

    for file_path in fixed_files:
        report_content += f"- {file_path.relative_to(project_root)}\n"

    if created_init_files:
        report_content += "\n## 创建的__init__.py文件\n"
        for init_file in created_init_files:
            report_content += f"- {init_file.relative_to(project_root)}\n"

    if error_files:
        report_content += "\n## 错误文件\n"
        for file_path, error in error_files:
            if isinstance(file_path, Path):
                report_content += f"- {file_path.relative_to(project_root)}: {error}\n"
            else:
                report_content += f"- {file_path}: {error}\n"

    # 写入报告
    report_path = "simple_test_fix_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"\n📄 详细报告已保存: {report_path}")
    print("\n📋 下一步建议:")
    print("1. 运行 `pytest tests/ -v` 验证所有测试")
    print("2. 检查修复报告中的详细信息")
    print("3. 如有问题，查看错误文件列表")


if __name__ == "__main__":
    fix_test_imports()
