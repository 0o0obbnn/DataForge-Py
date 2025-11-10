#!/usr/bin/env python
"""
统一测试运行脚本

用法:
    python scripts/run_tests.py              # 运行所有测试
    python scripts/run_tests.py --unit       # 只运行单元测试
    python scripts/run_tests.py --integration # 只运行集成测试
    python scripts/run_tests.py --performance # 只运行性能测试
    python scripts/run_tests.py --security   # 只运行安全测试
    python scripts/run_tests.py --coverage   # 运行测试并生成覆盖率报告
    python scripts/run_tests.py --verbose    # 详细输出
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> int:
    """运行命令并返回退出码"""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="DataForge测试运行脚本")
    parser.add_argument("--unit", action="store_true", help="只运行单元测试")
    parser.add_argument("--integration", action="store_true", help="只运行集成测试")
    parser.add_argument("--performance", action="store_true", help="只运行性能测试")
    parser.add_argument("--security", action="store_true", help="只运行安全测试")
    parser.add_argument("--e2e", action="store_true", help="只运行端到端测试")
    parser.add_argument("--stress", action="store_true", help="只运行压力测试")
    parser.add_argument("--coverage", action="store_true", help="生成覆盖率报告")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--failfast", "-x", action="store_true", help="遇到第一个失败就停止")
    parser.add_argument("--markers", "-m", help="按标记运行测试")
    parser.add_argument("--keyword", "-k", help="按关键字运行测试")
    
    args = parser.parse_args()
    
    # 构建pytest命令
    cmd = [sys.executable, "-m", "pytest"]
    
    # 选择测试目录
    if args.unit:
        cmd.append("tests/unit/")
    elif args.integration:
        cmd.append("tests/integration/")
    elif args.performance:
        cmd.append("tests/performance/")
    elif args.security:
        cmd.append("tests/security/")
    elif args.e2e:
        cmd.append("tests/e2e/")
    elif args.stress:
        cmd.append("tests/stress/")
    else:
        cmd.append("tests/")
    
    # 添加选项
    if args.verbose:
        cmd.append("-v")
    
    if args.failfast:
        cmd.append("-x")
    
    if args.markers:
        cmd.extend(["-m", args.markers])
    
    if args.keyword:
        cmd.extend(["-k", args.keyword])
    
    # 覆盖率选项
    if args.coverage:
        cmd.extend([
            "--cov=dataforge",
            "--cov-report=html",
            "--cov-report=term",
            "--cov-report=xml"
        ])
    
    # 运行测试
    exit_code = run_command(cmd, "运行测试")
    
    if exit_code == 0:
        print("\n✅ 所有测试通过！")
    else:
        print(f"\n❌ 测试失败，退出码: {exit_code}")
    
    # 如果生成了覆盖率报告，显示位置
    if args.coverage and exit_code == 0:
        print("\n📊 覆盖率报告已生成:")
        print("  - HTML: htmlcov/index.html")
        print("  - XML: coverage.xml")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
