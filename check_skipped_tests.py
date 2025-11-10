#!/usr/bin/env python3
"""检查跳过测试的详细信息"""

import os
import sys
import subprocess
from pathlib import Path

# 设置环境
sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

def run_pytest_collect():
    """运行pytest收集测试信息"""
    result = subprocess.run([
        'python', '-m', 'pytest', 
        'tests/unit/', 'tests/integration/test_all_generators.py', 
        '--collect-only', '-q', '--tb=no'
    ], capture_output=True, text=True, cwd='.')
    
    return result.stdout, result.stderr, result.returncode

def analyze_skipped_tests():
    """分析跳过的测试"""
    print("=== 收集测试信息 ===")
    stdout, stderr, returncode = run_pytest_collect()
    
    if returncode != 0:
        print(f"收集测试失败: {returncode}")
        print(f"错误: {stderr}")
        return
    
    lines = stdout.split('\n')
    
    # 统计各类测试
    total_tests = 0
    skipped_tests = []
    
    for line in lines:
        if '::' in line and ('test_' in line or 'Test' in line):
            total_tests += 1
        elif 'skipped' in line.lower() or 'skip' in line.lower():
            skipped_tests.append(line.strip())
    
    print(f"总测试数: {total_tests}")
    print(f"跳过测试数: {len(skipped_tests)}")
    
    print("\n=== 跳过的测试列表 ===")
    for test in skipped_tests:
        print(f"  {test}")
    
    # 检查具体的跳过原因
    print("\n=== 检查跳过原因 ===")
    
    # 查找所有包含skip的测试文件
    test_files = list(Path('tests').rglob('*.py'))
    
    skip_reasons = {}
    
    for test_file in test_files:
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 查找跳过原因
            if 'pytest.skip' in content or '@pytest.mark.skip' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'pytest.skip' in line or '@pytest.mark.skip' in line:
                        # 提取跳过原因
                        reason = "未知原因"
                        if 'reason=' in line:
                            try:
                                reason = line.split('reason=')[1].split('"')[1]
                            except:
                                pass
                        elif '"' in line and 'skip' in line:
                            try:
                                reason = line.split('"')[1]
                            except:
                                pass
                        
                        file_path = str(test_file.relative_to('.'))
                        if file_path not in skip_reasons:
                            skip_reasons[file_path] = []
                        skip_reasons[file_path].append((i+1, reason))
                        
        except Exception as e:
            print(f"处理文件 {test_file} 时出错: {e}")
    
    # 按原因分类
    reason_categories = {}
    for file_path, skips in skip_reasons.items():
        for line_num, reason in skips:
            if reason not in reason_categories:
                reason_categories[reason] = []
            reason_categories[reason].append((file_path, line_num))
    
    print("\n=== 按跳过原因分类 ===")
    for reason, files in reason_categories.items():
        print(f"\n原因: {reason} (共{len(files)}个)")
        for file_path, line_num in files:
            print(f"  - {file_path}:{line_num}")

if __name__ == "__main__":
    analyze_skipped_tests()