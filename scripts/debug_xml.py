import xml.etree.ElementTree as ET

from dataforge.core.generator import GeneratorConfig
from dataforge.generators.structured.xml_generator import GenericXMLGenerator

# 测试配置
config = GeneratorConfig(
    generator_type="xml",
    parameters={
        "root_name": "data",
        "use_namespace": True,
        "namespace": "http://example.com/schema"
    }
)
generator = GenericXMLGenerator(config)

# 生成XML
xml_str = generator.generate_single()
print("Generated XML:")
print(xml_str)
print()

root = ET.fromstring(xml_str)
print("Root tag:", root.tag)
print("Root attrib:", dict(root.attrib))
print("Has xmlns:", 'xmlns' in root.attrib)
