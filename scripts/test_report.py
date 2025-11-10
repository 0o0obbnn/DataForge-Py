#!/usr/bin/env python
"""
测试报告生成脚本

用法:
    python scripts/test_report.py              # 生成测试报告
    python scripts/test_report.py --format html # 生成HTML格式报告
    python scripts/test_report.py --format json # 生成JSON格式报告
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def collect_test_info() -> dict:
    """收集测试信息"""
    print("📊 收集测试信息...")
    
    # 运行pytest收集测试
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        capture_output=True,
        text=True
    )
    
    # 解析输出
    output = result.stdout
    test_count = 0
    for line in output.split('\n'):
        if 'collected' in line.lower():
            parts = line.split()
            if parts:
                try:
                    test_count = int(parts[0])
                except ValueError:
                    pass
    
    return {
        "total_tests": test_count,
        "collection_time": datetime.now().isoformat(),
    }


def run_tests_with_report() -> dict:
    """运行测试并收集结果"""
    print("🧪 运行测试...")
    
    # 运行测试
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    
    # 解析结果
    output = result.stdout + result.stderr
    
    passed = output.count(" PASSED")
    failed = output.count(" FAILED")
    skipped = output.count(" SKIPPED")
    errors = output.count(" ERROR")
    
    return {
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "errors": errors,
        "exit_code": result.returncode,
        "run_time": datetime.now().isoformat(),
    }


def generate_text_report(test_info: dict, test_results: dict) -> str:
    """生成文本格式报告"""
    report = []
    report.append("="*60)
    report.append("  DataForge 测试报告")
    report.append("="*60)
    report.append("")
    
    # 测试信息
    report.append("📊 测试统计:")
    report.append(f"  总测试数: {test_info['total_tests']}")
    report.append(f"  收集时间: {test_info['collection_time']}")
    report.append("")
    
    # 测试结果
    report.append("🧪 测试结果:")
    report.append(f"  ✅ 通过: {test_results['passed']}")
    report.append(f"  ❌ 失败: {test_results['failed']}")
    report.append(f"  ⏭️  跳过: {test_results['skipped']}")
    report.append(f"  ⚠️  错误: {test_results['errors']}")
    report.append(f"  运行时间: {test_results['run_time']}")
    report.append("")
    
    # 总体状态
    if test_results['exit_code'] == 0:
        report.append("✅ 所有测试通过！")
    else:
        report.append(f"❌ 测试失败 (退出码: {test_results['exit_code']})")
    
    report.append("")
    report.append("="*60)
    
    return "\n".join(report)


def generate_html_report(test_info: dict, test_results: dict) -> str:
    """生成HTML格式报告"""
    total = test_results['passed'] + test_results['failed'] + test_results['skipped']
    pass_rate = (test_results['passed'] / total * 100) if total > 0 else 0
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DataForge 测试报告</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            color: #666;
            font-size: 0.9em;
        }}
        .passed {{ color: #27ae60; }}
        .failed {{ color: #e74c3c; }}
        .skipped {{ color: #f39c12; }}
        .status {{
            padding: 20px;
            border-radius: 5px;
            text-align: center;
            font-size: 1.2em;
            font-weight: bold;
        }}
        .status.success {{
            background-color: #d4edda;
            color: #155724;
        }}
        .status.failure {{
            background-color: #f8d7da;
            color: #721c24;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>DataForge 测试报告</h1>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-label">总测试数</div>
            <div class="stat-value">{test_info['total_tests']}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">通过</div>
            <div class="stat-value passed">{test_results['passed']}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">失败</div>
            <div class="stat-value failed">{test_results['failed']}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">跳过</div>
            <div class="stat-value skipped">{test_results['skipped']}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">通过率</div>
            <div class="stat-value">{pass_rate:.1f}%</div>
        </div>
    </div>
    
    <div class="status {'success' if test_results['exit_code'] == 0 else 'failure'}">
        {'✅ 所有测试通过！' if test_results['exit_code'] == 0 else '❌ 测试失败'}
    </div>
</body>
</html>
"""
    return html


def generate_json_report(test_info: dict, test_results: dict) -> str:
    """生成JSON格式报告"""
    report = {
        "test_info": test_info,
        "test_results": test_results,
        "generated_at": datetime.now().isoformat(),
    }
    return json.dumps(report, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="DataForge测试报告生成脚本")
    parser.add_argument("--format", choices=["text", "html", "json"], default="text",
                       help="报告格式 (默认: text)")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 收集测试信息
    test_info = collect_test_info()
    
    # 运行测试
    test_results = run_tests_with_report()
    
    # 生成报告
    if args.format == "text":
        report = generate_text_report(test_info, test_results)
    elif args.format == "html":
        report = generate_html_report(test_info, test_results)
    elif args.format == "json":
        report = generate_json_report(test_info, test_results)
    
    # 输出报告
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding="utf-8")
        print(f"\n📄 报告已保存到: {output_path}")
    else:
        print(report)
    
    return test_results['exit_code']


if __name__ == "__main__":
    sys.exit(main())
