# 测试简单XML解析
import re
import xml.etree.ElementTree as ET

# 测试1: 包含xmlns的XML
xml_with_ns = '<?xml version="1.0" encoding="UTF-8"?><data xmlns="http://example.com/schema" id="1" type="generated"><name>test</name></data>'
print("XML with xmlns:", xml_with_ns)
root1 = ET.fromstring(xml_with_ns)
print("Root tag:", root1.tag)
print("Root attrib:", dict(root1.attrib))
print("Has xmlns:", "xmlns" in root1.attrib)
print()

# 测试2: 不包含xmlns的XML
xml_without_ns = '<?xml version="1.0" encoding="UTF-8"?><data id="1" type="generated"><name>test</name></data>'
print("XML without xmlns:", xml_without_ns)
root2 = ET.fromstring(xml_without_ns)
print("Root tag:", root2.tag)
print("Root attrib:", dict(root2.attrib))
print("Has xmlns:", "xmlns" in root2.attrib)
print()

# 测试3: 使用正则表达式检查xmlns属性

xmlns_pattern = r'xmlns="([^"]*)"'
match1 = re.search(xmlns_pattern, xml_with_ns)
print("XML with xmlns - regex match:", match1.group(1) if match1 else None)

match2 = re.search(xmlns_pattern, xml_without_ns)
print("XML without xmlns - regex match:", match2)
