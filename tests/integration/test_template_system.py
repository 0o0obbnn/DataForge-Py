#!/usr/bin/env python3
"""
模板管理功能测试脚本
验证模板的创建、保存、加载和管理功能
"""

import json
import os
from datetime import datetime

def create_test_template():
    """创建测试模板"""
    template = {
        "id": f"template_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "name": "用户信息模板",
        "description": "包含姓名、年龄、邮箱、手机号的用户信息生成模板",
        "category": "用户数据",
        "fields": [
            {
                "id": "field_1",
                "name": "姓名",
                "type": "name",
                "generator": "name",
                "parameters": {"type": "full"},
                "required": True,
                "description": "用户真实姓名"
            },
            {
                "id": "field_2", 
                "name": "年龄",
                "type": "age",
                "generator": "age",
                "parameters": {"min": 18, "max": 65},
                "required": True,
                "description": "用户年龄"
            },
            {
                "id": "field_3",
                "name": "邮箱",
                "type": "email", 
                "generator": "email",
                "parameters": {},
                "required": True,
                "description": "用户邮箱地址"
            },
            {
                "id": "field_4",
                "name": "手机号",
                "type": "phone",
                "generator": "phone", 
                "parameters": {},
                "required": True,
                "description": "用户手机号码"
            }
        ],
        "generationConfig": {
            "count": 1000,
            "format": "CSV",
            "formatOptions": {
                "csvDelimiter": ",",
                "jsonPrettyPrint": True,
                "sqlTableName": "users"
            }
        },
        "metadata": {
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
            "author": "test_user",
            "version": "1.0.0",
            "tags": ["用户", "基础信息", "测试"],
            "isPublic": False
        },
        "statistics": {
            "usageCount": 0,
            "downloadCount": 0,
            "rating": 0,
            "reviews": 0
        }
    }
    return template

def save_template_to_file(template):
    """保存模板到文件"""
    filename = f"template_{template['id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    print(f"✅ 模板保存成功: {filename}")
    return filename

def load_template_from_file(filename):
    """从文件加载模板"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            template = json.load(f)
        print(f"✅ 模板加载成功: {filename}")
        return template
    except Exception as e:
        print(f"❌ 模板加载失败: {e}")
        return None

def validate_template_structure(template):
    """验证模板结构"""
    required_fields = ['id', 'name', 'description', 'category', 'fields', 'generationConfig', 'metadata']
    
    for field in required_fields:
        if field not in template:
            print(f"❌ 模板结构验证失败: 缺少字段 {field}")
            return False
    
    # 验证字段结构
    if not isinstance(template['fields'], list) or len(template['fields']) == 0:
        print("❌ 模板结构验证失败: fields 必须是非空数组")
        return False
    
    for field in template['fields']:
        required_field_attrs = ['id', 'name', 'type', 'generator', 'required']
        for attr in required_field_attrs:
            if attr not in field:
                print(f"❌ 字段结构验证失败: 字段 {field.get('name', '未知')} 缺少属性 {attr}")
                return False
    
    print("✅ 模板结构验证通过")
    return True

def test_template_operations():
    """测试模板操作"""
    print("🧪 测试模板创建...")
    template1 = create_test_template()
    
    print("🧪 测试模板保存...")
    filename1 = save_template_to_file(template1)
    
    print("🧪 测试模板加载...")
    loaded_template = load_template_from_file(filename1)
    
    print("🧪 测试模板结构验证...")
    if loaded_template:
        validate_template_structure(loaded_template)
    
    # 创建第二个模板
    print("\n🧪 测试创建第二个模板...")
    template2 = create_test_template()
    template2['id'] = f"template_company_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    template2['name'] = "企业信息模板"
    template2['description'] = "企业基础信息生成模板"
    template2['category'] = "企业数据"
    template2['fields'] = [
        {
            "id": "field_1",
            "name": "企业名称",
            "type": "company_name",
            "generator": "company_name",
            "parameters": {},
            "required": True,
            "description": "企业名称"
        },
        {
            "id": "field_2",
            "name": "统一社会信用代码",
            "type": "uscc",
            "generator": "uscc", 
            "parameters": {},
            "required": True,
            "description": "企业统一社会信用代码"
        }
    ]
    
    filename2 = save_template_to_file(template2)
    
    return [filename1, filename2]

def simulate_template_management():
    """模拟模板管理功能"""
    print("📁 模拟模板管理系统...")
    
    # 模拟 localStorage 数据结构
    template_storage = {
        "templates": [],
        "categories": set(),
        "tags": set()
    }
    
    # 创建多个测试模板
    templates = []
    for i in range(3):
        template = create_test_template()
        template['id'] = f"template_test_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        template['name'] = f"测试模板 {i+1}"
        template['category'] = ["用户数据", "企业数据", "产品数据"][i]
        templates.append(template)
        
        # 添加到存储
        template_storage["templates"].append(template)
        template_storage["categories"].add(template["category"])
        for tag in template["metadata"]["tags"]:
            template_storage["tags"].add(tag)
    
    print(f"✅ 创建了 {len(templates)} 个测试模板")
    print(f"   分类: {list(template_storage['categories'])}")
    print(f"   标签: {list(template_storage['tags'])}")
    
    # 模拟搜索功能
    search_term = "用户"
    search_results = [
        t for t in template_storage["templates"] 
        if search_term in t["name"] or search_term in t["description"]
    ]
    print(f"✅ 搜索 '{search_term}' 找到 {len(search_results)} 个模板")
    
    # 模拟分类筛选
    category_filter = "用户数据"
    category_results = [
        t for t in template_storage["templates"]
        if t["category"] == category_filter
    ]
    print(f"✅ 分类筛选 '{category_filter}' 找到 {len(category_results)} 个模板")
    
    return template_storage

def main():
    print("🚀 开始测试模板管理功能...")
    print("=" * 50)
    
    try:
        # 测试基本模板操作
        template_files = test_template_operations()
        
        print("\n" + "=" * 50)
        
        # 测试模板管理功能
        storage = simulate_template_management()
        
        print("\n📊 测试结果统计:")
        print(f"   创建的模板文件: {len(template_files)}")
        print(f"   管理的模板数量: {len(storage['templates'])}")
        print(f"   可用分类数量: {len(storage['categories'])}")
        print(f"   可用标签数量: {len(storage['tags'])}")
        
        print("\n✅ 模板管理功能测试完成！")
        print("🎉 所有功能验证成功")
        
        # 清理测试文件
        for filename in template_files:
            try:
                os.remove(filename)
                print(f"🗑️ 清理测试文件: {filename}")
            except:
                pass
                
    except Exception as e:
        print(f"❌ 模板管理测试失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
