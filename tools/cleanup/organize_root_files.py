#!/usr/bin/env python3
"""整理根目录下的测试和生成文件"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def organize_files():
    """整理根目录下的文件"""
    
    # 创建目标目录
    directories = {
        'test_exports': 'docs/reports/2025/11/test_exports',
        'templates': 'docs/reports/2025/11/templates',
        'tools': 'tools/validation'
    }
    
    for dir_name, dir_path in directories.items():
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {dir_path}")
    
    # 移动测试导出文件
    print("\n=== 移动测试导出文件 ===")
    test_files = [f for f in os.listdir('.') if f.startswith('test_export_')]
    for file in test_files:
        if os.path.isfile(file):
            src = file
            dst = f"docs/reports/2025/11/test_exports/{file}"
            shutil.move(src, dst)
            print(f"📁 {file} → {dst}")
    
    # 移动模板文件
    print("\n=== 移动模板文件 ===")
    template_files = [f for f in os.listdir('.') if f.startswith('template_')]
    for file in template_files:
        if os.path.isfile(file):
            src = file
            dst = f"docs/reports/2025/11/templates/{file}"
            shutil.move(src, dst)
            print(f"📁 {file} → {dst}")
    
    # 移动工具脚本
    print("\n=== 移动工具脚本 ===")
    tool_files = ['find_root_files.py']
    for file in tool_files:
        if os.path.isfile(file):
            src = file
            dst = f"tools/validation/{file}"
            shutil.move(src, dst)
            print(f"📁 {file} → {dst}")
    
    # 创建整理报告
    print("\n=== 生成整理报告 ===")
    report_content = f"""# 根目录文件整理报告

**整理时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**整理文件数**: {len(test_files) + len(template_files) + len(tool_files)}个

## 文件分类统计

### 📊 测试导出文件
- **数量**: {len(test_files)}个
- **目标位置**: docs/reports/2025/11/test_exports/
- **文件类型**: CSV, JSON, XML, SQL

### 📋 模板文件  
- **数量**: {len(template_files)}个
- **目标位置**: docs/reports/2025/11/templates/
- **文件类型**: JSON模板

### 🔧 工具脚本
- **数量**: {len(tool_files)}个
- **目标位置**: tools/validation/
- **文件类型**: Python脚本

## 整理效果

### ✅ 已完成
- 根目录测试文件清理
- 文件按类型分类归档
- 建立标准化的目录结构

### 📈 改进效果
- 根目录文件数量减少 {len(test_files) + len(template_files) + len(tool_files)}个
- 测试报告按日期分类存储
- 工具脚本集中管理

### 🎯 后续建议
- 定期清理临时测试文件
- 建立自动化文件整理机制
- 完善测试报告管理流程

---
**整理工具**: 自动化脚本
**整理状态**: 完成
"""
    
    with open('docs/reports/2025/11/root_cleanup_report_20251110.md', 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print("✅ 整理报告已生成: docs/reports/2025/11/root_cleanup_report_20251110.md")
    
    return {
        'test_files': len(test_files),
        'template_files': len(template_files),
        'tool_files': len(tool_files),
        'total': len(test_files) + len(template_files) + len(tool_files)
    }

if __name__ == "__main__":
    result = organize_files()
    print(f"\n🎉 整理完成! 共移动 {result['total']}个文件")
    print(f"   - 测试导出文件: {result['test_files']}个")
    print(f"   - 模板文件: {result['template_files']}个") 
    print(f"   - 工具脚本: {result['tool_files']}个")
