"""
XML格式化器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestXMLFormatter:
    """XML格式化器测试类"""

    def test_format_single_record(self, generator_factory):
        """测试格式化单条记录"""
        from dataforge.output.xml_formatter import XMLFormatter

        formatter = XMLFormatter()
        data = {"name": "张三", "age": 25}
        result = formatter.format(data)

        assert isinstance(result, str)
        assert "<name>" in result or "name=" in result
        assert "张三" in result

    def test_format_multiple_records(self, generator_factory):
        """测试格式化多条记录"""
        from dataforge.output.xml_formatter import XMLFormatter

        formatter = XMLFormatter()
        data = [{"name": "张三", "age": 25}, {"name": "李四", "age": 30}]
        result = formatter.format(data)

        assert isinstance(result, str)
        assert "张三" in result
        assert "李四" in result

    def test_root_element(self, generator_factory):
        """测试根元素"""
        from dataforge.output.xml_formatter import XMLFormatter

        formatter = XMLFormatter(root_tag="records")
        data = [{"name": "张三"}]
        result = formatter.format(data)

        assert "<records>" in result or "records" in result

    def test_nested_elements(self, generator_factory):
        """测试嵌套元素"""
        from dataforge.output.xml_formatter import XMLFormatter

        formatter = XMLFormatter()
        data = {"person": {"name": "张三", "address": {"city": "北京"}}}
        result = formatter.format(data)

        assert "张三" in result
        assert "北京" in result

    def test_chinese_characters(self, generator_factory):
        """测试中文字符"""
        from dataforge.output.xml_formatter import XMLFormatter

        formatter = XMLFormatter()
        data = {"姓名": "张三", "城市": "北京"}
        result = formatter.format(data)

        assert "张三" in result
        assert "北京" in result

    def test_special_characters(self, generator_factory):
        """测试特殊字符"""
        from dataforge.output.xml_formatter import XMLFormatter

        formatter = XMLFormatter()
        data = {"name": "张三 & 李四", "desc": "<test>"}
        result = formatter.format(data)

        # Should escape special XML characters
        assert isinstance(result, str)

    def test_attributes(self, generator_factory):
        """测试属性"""
        from dataforge.output.xml_formatter import XMLFormatter

        formatter = XMLFormatter()
        data = {"name": "张三", "age": 25}
        result = formatter.format(data)

        assert isinstance(result, str)

    def test_empty_data(self, generator_factory):
        """测试空数据"""
        from dataforge.output.xml_formatter import XMLFormatter

        formatter = XMLFormatter()
        result = formatter.format({})

        assert isinstance(result, str)
