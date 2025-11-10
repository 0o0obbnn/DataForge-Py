#!/usr/bin/env python3
"""
生成测试报告和覆盖率报告
"""

import sys
import os
import subprocess
import json

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def generate_coverage_report():
    """生成覆盖率报告"""
    print("生成覆盖率报告...")
    
    try:
        # 运行测试并生成覆盖率报告
        cmd = [
            sys.executable, "-m", "pytest",
            "--cov=dataforge",
            "--cov-report=html:htmlcov",
            "--cov-report=xml:coverage.xml",
            "--cov-report=term-missing",
            "tests/test_basic.py",
            "-v"
        ]
        
        result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ 覆盖率报告生成成功")
            print(f"   输出目录: {os.path.join(project_root, 'htmlcov')}")
            
            # 查找覆盖率百分比
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'TOTAL' in line and '%' in line:
                    print(f"   覆盖率摘要: {line.strip()}")
                    break
            
            return True
        else:
            print("❌ 覆盖率报告生成失败")
            print(f"   错误输出: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 覆盖率报告生成超时")
        return False
    except Exception as e:
        print(f"❌ 覆盖率报告生成出错: {e}")
        return False

def generate_test_summary():
    """生成测试摘要报告"""
    print("\n生成测试摘要报告...")
    
    try:
        # 运行测试并生成JSON报告
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/test_basic.py",
            "--json-report",
            "--json-report-file=test_report.json",
            "-v"
        ]
        
        result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True, timeout=120)
        
        # 创建摘要报告
        summary = {
            "test_summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "duration": 0
            },
            "generators_tested": [
                "phone",
                "bankcard", 
                "idcard"
            ],
            "coverage": "见htmlcov目录",
            "timestamp": "2025-11-04",
            "status": "success" if result.returncode == 0 else "failed"
        }
        
        # 保存摘要报告
        summary_file = os.path.join(project_root, "test_summary.json")
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print("✅ 测试摘要报告生成成功")
        print(f"   报告文件: {summary_file}")
        
        return True
    except Exception as e:
        print(f"❌ 测试摘要报告生成出错: {e}")
        return False

def main():
    """主函数"""
    print("开始生成测试报告和覆盖率报告...")
    
    # 生成覆盖率报告
    coverage_success = generate_coverage_report()
    
    # 生成测试摘要报告
    summary_success = generate_test_summary()
    
    overall_success = coverage_success and summary_success
    
    print(f"\n报告生成结果: {'✅ 所有报告生成成功' if overall_success else '❌ 部分报告生成失败'}")
    
    if overall_success:
        print("\n生成的报告:")
        print("  - 覆盖率报告: htmlcov/index.html")
        print("  - 覆盖率数据: coverage.xml")
        print("  - 测试摘要: test_summary.json")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)