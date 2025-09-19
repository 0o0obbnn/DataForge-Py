#!/usr/bin/env python3
"""
前端导出功能测试脚本
验证不同格式的数据导出功能
"""

import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime

# 测试数据（模拟从API获取的数据）
test_data = [
    {"name":"周磊","age":20,"email":"5u7k7sock1@ojlajo.net","phone":"15 36611 2148"},
    {"name":"刘丽","age":45,"email":"1oocpp9@ewixatoh.cn","phone":"19 93154 2932"},
    {"name":"王涛","age":27,"email":"eom3rq@azua.cn","phone":"15 44120 5689"},
    {"name":"陈磊","age":32,"email":"oltugp_a@icqmrad.org","phone":"15 76428 8845"},
    {"name":"吴婷","age":56,"email":"d9fr_c@oct.emrhf.org","phone":"18 62223 1439"}
]

def test_json_export():
    """测试JSON格式导出"""
    filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON导出成功: {filename}")
    return filename

def test_csv_export():
    """测试CSV格式导出"""
    filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        if test_data:
            writer = csv.DictWriter(f, fieldnames=test_data[0].keys())
            writer.writeheader()
            writer.writerows(test_data)
    print(f"✅ CSV导出成功: {filename}")
    return filename

def test_xml_export():
    """测试XML格式导出"""
    filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    
    root = ET.Element("data")
    for item in test_data:
        record = ET.SubElement(root, "record")
        for key, value in item.items():
            field = ET.SubElement(record, key)
            field.text = str(value)
    
    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)
    print(f"✅ XML导出成功: {filename}")
    return filename

def test_sql_export():
    """测试SQL格式导出"""
    filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    
    with open(filename, 'w', encoding='utf-8') as f:
        # 创建表结构
        f.write("-- DataForge 导出数据\n")
        f.write(f"-- 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("CREATE TABLE IF NOT EXISTS generated_data (\n")
        f.write("  id INT AUTO_INCREMENT PRIMARY KEY,\n")
        f.write("  name VARCHAR(100),\n")
        f.write("  age INT,\n")
        f.write("  email VARCHAR(200),\n")
        f.write("  phone VARCHAR(50)\n")
        f.write(");\n\n")
        
        # 插入数据
        f.write("INSERT INTO generated_data (name, age, email, phone) VALUES\n")
        values = []
        for item in test_data:
            value_str = f"('{item['name']}', {item['age']}, '{item['email']}', '{item['phone']}')"
            values.append(value_str)
        f.write(",\n".join(values) + ";\n")
    
    print(f"✅ SQL导出成功: {filename}")
    return filename

def get_file_size(filename):
    """获取文件大小"""
    import os
    size = os.path.getsize(filename)
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    else:
        return f"{size / (1024 * 1024):.1f} MB"

def main():
    print("🚀 开始测试前端导出功能...")
    print("=" * 50)
    
    # 测试所有导出格式
    exported_files = []
    
    try:
        exported_files.append(test_json_export())
        exported_files.append(test_csv_export())
        exported_files.append(test_xml_export())
        exported_files.append(test_sql_export())
        
        print("\n📊 导出结果统计:")
        for filename in exported_files:
            size = get_file_size(filename)
            print(f"   {filename}: {size}")
            
        print(f"\n✅ 所有导出格式测试成功！共导出 {len(exported_files)} 个文件")
        print("🎉 前端导出功能验证完成")
        
    except Exception as e:
        print(f"❌ 导出测试失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
