#!/usr/bin/env python3
"""
DataForge 测试导入路径全面修复脚本
系统性修复所有测试文件中的导入问题
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Set


class ComprehensiveTestFixer:
    """全面的测试导入修复器"""

    def __init__(self, tests_dir: str = "tests"):
        self.project_root = Path.cwd()
        self.tests_dir = self.project_root / tests_dir
        self.fixed_files = []
        self.error_files = []
        self.analysis_results = {}

    def find_test_files(self) -> List[Path]:
        """查找所有Python测试文件"""
        test_files = []

        # 查找所有Python文件
        for pattern in ["*.py"]:
            test_files.extend(self.tests_dir.rglob(pattern))

        # 过滤掉__pycache__等目录
        filtered_files = []
        for file_path in test_files:
            if "__pycache__" not in str(file_path) and file_path.name != "__init__.py":
                filtered_files.append(file_path)

        return filtered_files

    def analyze_file_imports(self, file_path: Path) -> Dict:
        """深度分析文件中的导入问题"""
        analysis = {
            "file_path": file_path,
            "relative_path": file_path.relative_to(self.project_root),
            "sys_path_inserts": [],
            "dataforge_imports": [],
            "problematic_patterns": [],
            "needs_fix": False
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
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
        elif any(path in line for path in ["'.'", '"."', "'..'", '".."']):
            return "硬编码路径"
        else:
            return "其他"

    def fix_file_imports(self, file_path: Path, analysis: Dict) -> bool:
        """修复单个文件的导入问题"""
        if not analysis["needs_fix"]:
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            lines = content.split('\n')

            # 标记需要删除的行
            lines_to_remove = set()

            # 处理sys.path.insert语句
            for sys_path_info in analysis["sys_path_inserts"]:
                line_num = sys_path_info["line_num"] - 1  # 转换为0索引
                lines_to_remove.add(line_num)

                # 同时删除相关的import os, sys语句（如果它们只用于路径操作）
                self._mark_unused_imports_for_removal(lines, lines_to_remove, line_num)

            # 删除标记的行
            new_lines = []
            for i, line in enumerate(lines):
                if i not in lines_to_remove:
                    new_lines.append(line)

            # 清理多余的空行
            content = '\n'.join(new_lines)
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

    def _mark_unused_imports_for_removal(self, lines: List[str], lines_to_remove: Set[int], sys_path_line: int):
        """标记不再需要的import语句"""
        # 检查sys.path.insert前后的import语句
        for i in range(max(0, sys_path_line - 5), min(len(lines), sys_path_line + 2)):
            line = lines[i].strip()

            # 如果是单独的import os或import sys语句，且只用于路径操作
            if line in ['import os', 'import sys'] or line.startswith('import os,') or line.startswith('import sys,'):
                # 检查这些模块是否在其他地方使用
                if not self._is_module_used_elsewhere(lines, line, i, lines_to_remove):
                    lines_to_remove.add(i)

    def _is_module_used_elsewhere(self, lines: List[str], import_line: str, import_line_num: int, excluded_lines: Set[int]) -> bool:
        """检查模块是否在其他地方使用"""
        module_name = import_line.replace('import ', '').split(',')[0].strip()

        for i, line in enumerate(lines):
            if i == import_line_num or i in excluded_lines:
                continue

            # 检查是否使用了该模块
            if f'{module_name}.' in line and 'sys.path.insert' not in line:
                return True

        return False

    def create_missing_init_files(self):
        """创建缺失的__init__.py文件"""
        directories_to_check = []

        # 收集所有需要检查的目录
        for root, dirs, files in os.walk(self.tests_dir):
            for dir_name in dirs:
                if not dir_name.startswith('.') and dir_name != '__pycache__':
                    directories_to_check.append(Path(root) / dir_name)

        created_files = []
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

    def verify_conftest_setup(self) -> bool:
        """验证conftest.py配置是否正确"""
        conftest_path = self.tests_dir / "conftest.py"

        if not conftest_path.exists():
            print("⚠️ 警告: conftest.py 不存在")
            return False

        try:
            with open(conftest_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查关键配置
            required_elements = [
                "PROJECT_ROOT",
                "sys.path.insert",
                "dataforge",
                "pytest"
            ]

            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)

            if missing_elements:
                print(f"⚠️ conftest.py 缺少关键元素: {missing_elements}")
                return False

            return True

        except Exception as e:
            print(f"❌ 无法验证conftest.py: {e}")
            return False

    def generate_comprehensive_report(self) -> str:
        """生成全面的修复报告"""
        report = []
        report.append("# DataForge 测试导入路径全面修复报告")
        import datetime
        report.append(f"\n**执行时间:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**项目根目录:** {self.project_root}")
        report.append(f"**测试目录:** {self.tests_dir}")

        # 统计信息
        total_files = len(self.analysis_results)
        files_needing_fix = sum(1 for analysis in self.analysis_results.values() if analysis["needs_fix"])
        files_fixed = len(self.fixed_files)

        report.append(f"\n## 统计信息")
        report.append(f"- 总测试文件数: {total_files}")
        report.append(f"- 需要修复的文件数: {files_needing_fix}")
        report.append(f"- 已修复文件数: {files_fixed}")
        report.append(f"- 错误文件数: {len(self.error_files)}")

        # 详细分析
        report.append(f"\n## 导入问题详细分析")

        sys_path_count = 0
        dataforge_import_count = 0

        for file_path, analysis in self.analysis_results.items():
            if analysis["needs_fix"]:
                relative_path = analysis["relative_path"]
                report.append(f"\n### {relative_path}")

                if analysis["sys_path_inserts"]:
                    sys_path_count += len(analysis["sys_path_inserts"])
                    report.append("**sys.path.insert 语句:**")
                    for sys_path in analysis["sys_path_inserts"]:
                        report.append(f"- 第{sys_path['line_num']}行 ({sys_path['type']}): `{sys_path['content'].strip()}`")

                if analysis["dataforge_imports"]:
                    dataforge_import_count += len(analysis["dataforge_imports"])
                    report.append("**DataForge 导入:**")
                    for imp in analysis["dataforge_imports"]:
                        report.append(f"- 第{imp['line_num']}行: `{imp['content']}`")

                if analysis["problematic_patterns"]:
                    report.append("**其他问题模式:**")
                    for pattern in analysis["problematic_patterns"]:
                        report.append(f"- 第{pattern['line_num']}行 ({pattern['description']}): `{pattern['content'].strip()}`")

        report.append(f"\n**总问题统计:**")
        report.append(f"- sys.path.insert 语句: {sys_path_count}")
        report.append(f"- DataForge 导入: {dataforge_import_count}")

        # 修复结果
        if self.fixed_files:
            report.append(f"\n## 已修复文件")
            for file_path in self.fixed_files:
                report.append(f"- ✅ {file_path.relative_to(self.project_root)}")

        # 错误文件
        if self.error_files:
            report.append(f"\n## 错误文件")
            for file_path, error in self.error_files:
                if isinstance(file_path, Path):
                    report.append(f"- ❌ {file_path.relative_to(self.project_root)}: {error}")
                else:
                    report.append(f"- ❌ {file_path}: {error}")

        # 解决方案说明
        report.append(f"\n## 修复策略")
        report.append("1. **移除手动路径设置**: 删除所有 `sys.path.insert` 语句")
        report.append("2. **依赖conftest.py**: 通过pytest的conftest.py统一管理Python路径")
        report.append("3. **标准化导入**: 确保所有导入都使用标准的包导入方式")
        report.append("4. **创建__init__.py**: 为所有测试子目录创建包初始化文件")

        # 验证步骤
        report.append(f"\n## 验证步骤")
        report.append("```powershell")
        report.append("# 1. 运行所有测试")
        report.append("pytest tests/ -v")
        report.append("")
        report.append("# 2. 按类别运行测试")
        report.append("pytest tests/unit/ -v          # 单元测试")
        report.append("pytest tests/integration/ -v   # 集成测试")
        report.append("pytest tests/api/ -v           # API测试")
        report.append("")
        report.append("# 3. 运行特定标记的测试")
        report.append("pytest -m unit -v              # 只运行单元测试")
        report.append("pytest -m integration -v       # 只运行集成测试")
        report.append("")
        report.append("# 4. 检查导入问题")
        report.append("python -c \"import sys; sys.path.insert(0, '.'); import dataforge; print('✅ DataForge导入成功')\"")
        report.append("```")

        # 后续建议
        report.append(f"\n## 后续建议")
        report.append("1. **配置IDE**: 确保IDE识别项目根目录为Python路径")
        report.append("2. **CI/CD配置**: 在CI环境中设置正确的PYTHONPATH")
        report.append("3. **文档更新**: 更新开发文档，说明新的测试运行方式")
        report.append("4. **代码审查**: 在代码审查中检查新的测试文件是否遵循规范")

        return '\n'.join(report)

    def run(self) -> None:
        """执行全面修复过程"""
        print("🚀 开始全面修复测试导入路径...")
        print(f"📁 项目根目录: {self.project_root}")
        print(f"📂 测试目录: {self.tests_dir}")

        # 1. 验证conftest.py配置
        print("\n🔍 验证conftest.py配置...")
        conftest_ok = self.verify_conftest_setup()
        if conftest_ok:
            print("✅ conftest.py 配置正确")

        # 2. 查找并分析测试文件
        print("\n📋 查找和分析测试文件...")
        test_files = self.find_test_files()
        print(f"找到 {len(test_files)} 个Python文件")

        # 3. 分析每个文件
        print("\n🔍 分析导入问题...")
        for file_path in test_files:
            print(f"  分析: {file_path.relative_to(self.project_root)}")
            analysis = self.analyze_file_imports(file_path)
            self.analysis_results[file_path] = analysis

        # 4. 修复文件
        print("\n🔧 修复导入问题...")
        for file_path, analysis in self.analysis_results.items():
            if analysis["needs_fix"]:
                print(f"  修复: {analysis['relative_path']}")
                if self.fix_file_imports(file_path, analysis):
                    self.fixed_files.append(file_path)
                    print(f"    ✅ 修复成功")
                else:
                    print(f"    ℹ️ 无需修复或修复失败")

        # 5. 创建缺失的__init__.py文件
        print("\n📝 创建缺失的__init__.py文件...")
        created_init_files = self.create_missing_init_files()
        if created_init_files:
            print(f"  创建了 {len(created_init_files)} 个__init__.py文件")
            for init_file in created_init_files:
                print(f"    ✅ {init_file.relative_to(self.project_root)}")
        else:
            print("  所有必要的__init__.py文件都已存在")

        # 6. 生成报告
        print("\n📊 生成修复报告...")
        report = self.generate_comprehensive_report()
        report_path = "comprehensive_test_fix_report.md"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        # 7. 输出总结
        print(f"\n🎉 全面修复完成!")
        print(f"📄 详细报告: {report_path}")
        print(f"✅ 修复文件数: {len(self.fixed_files)}")
        print(f"❌ 错误文件数: {len(self.error_files)}")

        if created_init_files:
            print(f"📝 创建__init__.py文件数: {len(created_init_files)}")

        # 8. 提供下一步建议
        print(f"\n📋 下一步建议:")
        print("1. 运行 `pytest tests/ -v` 验证所有测试")
        print("2. 检查修复报告中的详细信息")
        print("3. 如有问题，查看错误文件列表")


def main():
    """主函数"""
    fixer = ComprehensiveTestFixer()
    fixer.run()


if __name__ == "__main__":
    main()