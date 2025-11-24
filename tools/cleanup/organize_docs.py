#!/usr/bin/env python3
"""整理docs目录下的文档"""

import os
import shutil
from pathlib import Path

def organize_docs():
    """整理文档目录"""
    
    # 文档分类映射
    doc_mapping = {
        # 用户指南
        'guides': [
            'DataForge.md',
            'DataForge项目规则.md', 
            'WARP.md',
            'CONTEXT_SYSTEM_GUIDE.md'
        ],
        
        # 架构文档
        'architecture': [
            'DataForge项目架构设计.md',
            'DataForge Web 端项目工程规范 (Frontend Architecture Design).md'
        ],
        
        # 开发文档
        'development': [
            'PERFORMANCE_OPTIMIZATION.md',
            'ADVANCED_FINANCE_GENERATORS.md',
            'DATETIME_GENERATORS_GUIDE.md'
        ],
        
        # 项目计划
        'plans': [
            'DataForge 项目开发任务.md',
            'DataForge Web 端开发任务排期 (基于 Vue 3 + TS, Pinia, Axios, Ant Design Vue).md'
        ],
        
        # Web控制台相关
        'web-console': [
            '产品需求文档 (PRD) - DataForge Web控制台.md',
            '启动前后端项目并进行联调.md',
            'DataForge Web 端用户界面与交互流程最细粒度描述.md',
            'DataForge Web Console - 开发执行蓝本.md',
            'DataForge前后端联调启动.md',
            'DataForgeWeb控制台UIUX设计文档.md',
            '设计风格.md'
        ]
    }
    
    # 创建web-console目录
    web_console_dir = Path('docs/web-console')
    web_console_dir.mkdir(exist_ok=True)
    
    print("=== 整理文档目录 ===")
    
    moved_count = 0
    
    for category, files in doc_mapping.items():
        target_dir = Path(f'docs/{category}')
        target_dir.mkdir(exist_ok=True)
        
        print(f"\n📁 {category}:")
        
        for file in files:
            source_path = Path(f'docs/{file}')
            if source_path.exists():
                target_path = target_dir / file
                try:
                    shutil.move(str(source_path), str(target_path))
                    print(f"  ✅ {file} → {category}/")
                    moved_count += 1
                except Exception as e:
                    print(f"  ❌ {file}: {e}")
            else:
                print(f"  ⚠️ {file}: 文件不存在")
    
    # 移动CHANGELOG到docs根目录
    changelog_src = Path('docs/CHANGELOG.md')
    changelog_dst = Path('docs/CHANGELOG.md')
    if changelog_src.exists():
        print(f"\n✅ CHANGELOG.md 保留在docs根目录")
        moved_count += 1
    
    print(f"\n=== 文档整理完成 ===")
    print(f"📊 总计移动文档: {moved_count}个")
    
    return moved_count

if __name__ == "__main__":
    organize_docs()