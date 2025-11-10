#!/usr/bin/env python
"""
测试覆盖率检查脚本

用法:
    python scripts/check_coverage.py              # 检查覆盖率
    python scripts/check_coverage.py --min 80     # 设置最低覆盖率阈值
    python scripts/check_coverage.py --report     # 生成详细报告
"""

import argparse
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def run_coverage() -> int:
    """运行测试并生成覆盖率"""
    print("🔍 运行测试并生成覆盖率报告...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "--cov=dataforge",
        "--cov-report=xml",
        "--cov-report=term",
        "-q"
    ]
    
    result = subprocess.run(cmd)
    return result.returncode


def parse_coverage_xml() -> dict:
    """解析覆盖率XML报告"""
    coverage_file = Path("coverage.xml")
    
    if not coverage_file.exists():
        print("❌ 覆盖率报告文件不存在: coverage.xml")
        return {}
    
    tree = ET.parse(coverage_file)
    root = tree.getroot()
    
    # 获取总体覆盖率
    coverage_data = {
        "line_rate": float(root.attrib.get("line-rate", 0)) * 100,
        "branch_rate": float(root.attrib.get("branch-rate", 0)) * 100,
        "lines_covered": int(root.attrib.get("lines-covered", 0)),
        "lines_valid": int(root.attrib.get("lines-valid", 0)),
        "branches_covered": int(root.attrib.get("branches-covered", 0)),
        "branches_valid": int(root.attrib.get("branches-valid", 0)),
    }
    
    # 获取各模块覆盖率
    packages = {}
    for package in root.findall(".//package"):
        package_name = package.attrib.get("name", "unknown")
        package_line_rate = float(package.attrib.get("line-rate", 0)) * 100
        packages[package_name] = package_line_rate
    
    coverage_data["packages"] = packages
    
    return coverage_data


def print_coverage_report(coverage_data: dict, min_coverage: float):
    """打印覆盖率报告"""
    print("\n" + "="*60)
    print("  测试覆盖率报告")
    print("="*60 + "\n")
    
    line_rate = coverage_data.get("line_rate", 0)
    branch_rate = coverage_data.get("branch_rate", 0)
    lines_covered = coverage_data.get("lines_covered", 0)
    lines_valid = coverage_data.get("lines_valid", 0)
    
    print(f"📊 总体覆盖率:")
    print(f"  行覆盖率: {line_rate:.2f}%")
    print(f"  分支覆盖率: {branch_rate:.2f}%")
    print(f"  覆盖行数: {lines_covered}/{lines_valid}")
    
    # 检查是否达到最低要求
    if line_rate >= min_coverage:
        print(f"\n✅ 覆盖率达标 (>= {min_coverage}%)")
        status = 0
    else:
        print(f"\n❌ 覆盖率不达标 (< {min_coverage}%)")
        print(f"   需要提高 {min_coverage - line_rate:.2f}%")
        status = 1
    
    # 打印各模块覆盖率
    packages = coverage_data.get("packages", {})
    if packages:
        print(f"\n📦 模块覆盖率:")
        for package, rate in sorted(packages.items(), key=lambda x: x[1]):
            status_icon = "✅" if rate >= min_coverage else "⚠️"
            print(f"  {status_icon} {package}: {rate:.2f}%")
    
    return status


def main():
    parser = argparse.ArgumentParser(description="DataForge覆盖率检查脚本")
    parser.add_argument("--min", type=float, default=80.0, help="最低覆盖率阈值 (默认: 80)")
    parser.add_argument("--report", action="store_true", help="生成详细HTML报告")
    parser.add_argument("--skip-tests", action="store_true", help="跳过测试运行，只分析现有报告")
    
    args = parser.parse_args()
    
    # 运行测试
    if not args.skip_tests:
        exit_code = run_coverage()
        if exit_code != 0:
            print("\n❌ 测试运行失败")
            return exit_code
    
    # 解析覆盖率
    coverage_data = parse_coverage_xml()
    if not coverage_data:
        return 1
    
    # 打印报告
    status = print_coverage_report(coverage_data, args.min)
    
    # 生成HTML报告
    if args.report:
        print("\n📄 生成HTML报告...")
        subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/",
            "--cov=dataforge",
            "--cov-report=html",
            "-q"
        ])
        print("  HTML报告: htmlcov/index.html")
    
    return status


if __name__ == "__main__":
    sys.exit(main())
