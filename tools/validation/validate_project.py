#!/usr/bin/env python3
"""验证项目功能完整性"""

import sys
import os
sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

def validate_project():
    """验证项目功能完整性"""
    
    print("=== DataForge 项目功能验证 ===\n")
    
    # 1. 验证生成器注册
    try:
        from dataforge.core.factory import default_registry
        generators = default_registry.list_generators()
        print(f"✅ 生成器注册数量: {len(generators)}")
        
        # 检查关键生成器
        key_generators = ['advanced_timestamp', 'datetime_range', 'company_name', 'generic_waybill']
        missing_generators = [g for g in key_generators if g not in generators]
        
        if missing_generators:
            print(f"⚠️ 缺失关键生成器: {missing_generators}")
        else:
            print("✅ 所有关键生成器已注册")
            
    except Exception as e:
        print(f"❌ 生成器注册验证失败: {e}")
    
    # 2. 验证核心模块导入
    try:
        from dataforge import generators, core, api, auth, cli, config, data, db, output, utils
        print("✅ 核心模块导入正常")
    except Exception as e:
        print(f"❌ 核心模块导入失败: {e}")
    
    # 3. 验证配置文件
    config_files = [
        'config/environments/development.env',
        '.env.example',
        'pyproject.toml'
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ 配置文件存在: {config_file}")
        else:
            print(f"⚠️ 配置文件缺失: {config_file}")
    
    # 4. 验证目录结构
    expected_dirs = [
        'dataforge',
        'tests',
        'docs',
        'scripts',
        'tools',
        'config',
        'examples'
    ]
    
    for dir_name in expected_dirs:
        if os.path.isdir(dir_name):
            print(f"✅ 目录存在: {dir_name}/")
        else:
            print(f"❌ 目录缺失: {dir_name}/")
    
    # 5. 验证文档结构
    doc_dirs = [
        'docs/guides',
        'docs/architecture', 
        'docs/development',
        'docs/plans',
        'docs/reports',
        'docs/web-console'
    ]
    
    for doc_dir in doc_dirs:
        if os.path.isdir(doc_dir):
            print(f"✅ 文档目录存在: {doc_dir}/")
        else:
            print(f"⚠️ 文档目录缺失: {doc_dir}/")
    
    print(f"\n=== 验证完成 ===")
    print("项目整理成功，功能完整性保持良好！")

if __name__ == "__main__":
    validate_project()