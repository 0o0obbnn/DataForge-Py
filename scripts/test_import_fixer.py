#!/usr/bin/env python3
"""
DataForge 测试导入路径修复脚本
修复所有测试文件中的导入问题
"""

import datetime
import re
from pathlib import Path
from typing import Any


class TestImportFixer:
    """测试导入修复器"""

    def __init__(self, tests_dir: str = "tests") -> None:
        self.project_root: Path = Path.cwd()
        self.tests_dir: Path = self.project_root / tests_dir
        self.fixed_files: list[Path] = []
        self.error_files: list[tuple[Path | str, str]] = []
        self.analysis_results: dict[Path, dict[str, Any]] = {}

    def find_test_files(self) -> list[Path]:
        """查找所有Python测试文件"""
        test_files: list[Path] = []

        # 查找所有Python文件
        for pattern in ["*.py"]:
            test_files.extend(self.tests_dir.rglob(pattern))

        # 过滤掉__pycache__等目录
        filtered_files: list[Path] = []
        for file_path in test_files:
            if "__pycache__" not in str(file_path) and file_path.name != "__init__.py":
                filtered_files.append(file_path)

        return filtered_files

    def analyze_file_imports(self, file_path: Path) -> dict[str, Any]:
        """分析文件中的导入问题"""
        analysis: dict[str, Any] = {
            "file_path": file_path,
            "relative_path": file_path.relative_to(self.project_root),
            "sys_path_inserts": [],
            "dataforge_imports": [],
            "problematic_patterns": [],
            "needs_fix": False
        }

        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()

                # 检查sys.path.insert语句
                if 'sys.path.insert' in line:
                    analysis["sys_path_inserts"].append({
                        "line_num": i,
                        "content": line,
                        "type": self._classify_sys_path_insert(line)
                    })
                    analysis["needs_fix"] = True

                # 检查dataforge导入
                if re.match(r'^from dataforge\.|^import dataforge', line_stripped):
                    analysis["dataforge_imports"].append({
                        "line_num": i,
                        "content": line_stripped
                    })

                # 检查其他问题模式
                problematic_patterns = [
                    (r'os\.path\.dirname\(__file__\)', "使用__file__相对路径"),
                    (r'os\.path\.abspath\(.*__file__', "使用绝对路径转换"),
                    (r'sys\.path\.append', "使用append而非insert"),
                ]

                for pattern, description in problematic_patterns:
                    if re.search(pattern, line):
                        analysis["problematic_patterns"].append({
                            "line_num": i,
                            "content": line,
                            "description": description
                        })
                        analysis["needs_fix"] = True

        except Exception as e:
            self.error_files.append((file_path, f"分析失败: {str(e)}"))

        return analysis

    def _classify_sys_path_insert(self, line: str) -> str:
        """分类sys.path.insert语句的类型"""
        if 'os.path.dirname(__file__)' in line:
            if '..' in line:
                return "相对父目录"
            else:
                return "当前目录"
        elif 'os.path.abspath' in line:
            return "绝对路径"
        elif '"."' in line or "'." in line or '".."' in line or "'.." in line:
            return "硬编码路径"
        else:
            return "其他"

    def fix_file_imports(self, file_path: Path, analysis: dict[str, Any]) -> bool:
        """修复单个文件的导入问题"""
        if not analysis["needs_fix"]:
            return False

        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 使用正则表达式移除sys.path.insert语句
            patterns_to_remove = [
                r'sys\.path\.insert\(0,\s*os\.path\.dirname\(os\.path\.abspath\(__file__\)\)\)',
                r'sys\.path\.insert\(0,\s*os\.path\.dirname\(__file__\)\)',
                r'sys\.path\.insert\(0,\s*os\.path\.join\(os\.path\.dirname\(__file__\),\s*["\'][^"\']*["\']\)\)',
                r'sys\.path\.insert\(0,\s*str\(Path\(__file__\)\.parent\)\)',
                r'sys\.path\.insert\(0,\s*["\'][^"\']*["\']\)',
            ]

            for pattern in patterns_to_remove:
                content = re.sub(pattern, '', content)

            # 移除相关的注释行
            comment_patterns = [
                r'#\s*添加项目根目录到.*路径.*\n',
                r'#\s*Add project root to path.*\n',
            ]

            for pattern in comment_patterns:
                content = re.sub(pattern, '', content)

            # 清理多余的空行
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            content = content.strip() + '\n'

            # 如果内容有变化，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True

        except Exception as e:
            self.error_files.append((file_path, f"修复失败: {str(e)}"))

        return False

    def create_missing_init_files(self) -> list[Path]:
        """创建缺失的__init__.py文件"""
        directories_to_check: list[Path] = []

        # 收集所有需要检查的目录
        for root_path in self.tests_dir.rglob("*"):
            if root_path.is_dir() and not root_path.name.startswith('.') and root_path.name != '__pycache__':
                directories_to_check.append(root_path)

        created_files: list[Path] = []
        for directory in directories_to_check:
            init_file = directory / "__init__.py"
            if not init_file.exists():
                try:
                    with open(init_file, 'w', encoding='utf-8') as f:
                        f.write('"""测试模块初始化文件"""\n')
                    created_files.append(init_file)
                except Exception as e:
                    self.error_files.append((init_file, f"创建失败: {str(e)}"))

        return created_files

    def generate_report(self) -> str:
        """生成修复报告"""
        report: list[str] = []
        report.append("# DataForge 测试导入路径修复报告")
        report.append(f"\n**执行时间:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**项目根目录:** {self.project_root}")
        report.append(f"**测试目录:** {self.tests_dir}")

        # 统计信息
        total_files = len(self.analysis_results)
        files_needing_fix = sum(1 for analysis in self.analysis_results.values() if analysis["needs_fix"])
        files_fixed = len(self.fixed_files)

        report.append("\n## 统计信息")
        report.append(f"- 总测试文件数: {total_files}")
        report.append(f"- 需要修复的文件数: {files_needing_fix}")
        report.append(f"- 已修复文件数: {files_fixed}")
        report.append(f"- 错误文件数: {len(self.error_files)}")

        # 修复结果
        if self.fixed_files:
            report.append("\n## 已修复文件")
            for file_path in self.fixed_files:
                report.append(f"- ✅ {file_path.relative_to(self.project_root)}")

        # 错误文件
        if self.error_files:
            report.append("\n## 错误文件")
            for file_path, error in self.error_files:
                if isinstance(file_path, Path):
                    report.append(f"- ❌ {file_path.relative_to(self.project_root)}: {error}")
                else:
                    report.append(f"- ❌ {file_path}: {error}")

        return '\n'.join(report)

    def run(self) -> None:
        """执行修复过程"""
        print("🚀 开始修复测试导入路径...")
        print(f"📁 项目根目录: {self.project_root}")
        print(f"📂 测试目录: {self.tests_dir}")

        # 1. 查找并分析测试文件
        print("\n📋 查找和分析测试文件...")
        test_files = self.find_test_files()
        print(f"找到 {len(test_files)} 个Python文件")

        # 2. 分析每个文件
        print("\n🔍 分析导入问题...")
        for file_path in test_files:
            print(f"  分析: {file_path.relative_to(self.project_root)}")
            analysis = self.analyze_file_imports(file_path)
            self.analysis_results[file_path] = analysis

        # 3. 修复文件
        print("\n🔧 修复导入问题...")
        for file_path, analysis in self.analysis_results.items():
            if analysis["needs_fix"]:
                print(f"  修复: {analysis['relative_path']}")
                if self.fix_file_imports(file_path, analysis):
                    self.fixed_files.append(file_path)
                    print("    ✅ 修复成功")
                else:
                    print("    ℹ️ 无需修复或修复失败")

        # 4. 创建缺失的__init__.py文件
        print("\n📝 创建缺失的__init__.py文件...")
        created_init_files = self.create_missing_init_files()
        if created_init_files:
            print(f"  创建了 {len(created_init_files)} 个__init__.py文件")
            for init_file in created_init_files:
                print(f"    ✅ {init_file.relative_to(self.project_root)}")
        else:
            print("  所有必要的__init__.py文件都已存在")

        # 5. 生成报告
        print("\n📊 生成修复报告...")
        report = self.generate_report()
        report_path = "test_import_fix_report.md"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        # 6. 输出总结
        print("\n🎉 修复完成!")
        print(f"📄 详细报告: {report_path}")
        print(f"✅ 修复文件数: {len(self.fixed_files)}")
        print(f"❌ 错误文件数: {len(self.error_files)}")

        if created_init_files:
            print(f"📝 创建__init__.py文件数: {len(created_init_files)}")

        # 7. 提供下一步建议
        print("\n📋 下一步建议:")
        print("1. 运行 `pytest tests/ -v` 验证所有测试")
        print("2. 检查修复报告中的详细信息")
        print("3. 如有问题，查看错误文件列表")


def main() -> None:
    """主函数"""
    fixer = TestImportFixer()
    fixer.run()


if __name__ == "__main__":
    main()
