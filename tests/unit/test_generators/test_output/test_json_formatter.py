"""
JSON格式化器测试
"""

import json

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestJSONFormatter:
    """JSON格式化器测试类"""

    def test_format_single_record(self, generator_factory):
        """测试格式化单条记录"""
        from dataforge.output.json_formatter import JSONFormatter

        formatter = JSONFormatter()
        data = {"name": "张三", "age": 25, "city": "北京"}
        result = formatter.format(data)

        assert isinstance(result, str)
        # Should be valid JSON
        parsed = json.loads(result)
        assert parsed == data

    def test_format_multiple_records(self, generator_factory):
        """测试格式化多条记录"""
        from dataforge.output.json_formatter import JSONFormatter

        formatter = JSONFormatter()
        data = [{"name": "张三", "age": 25}, {"name": "李四", "age": 30}]
        result = formatter.format(data)

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed == data

    def test_pretty_format(self, generator_factory):
        """测试美化格式"""
        from dataforge.output.json_formatter import JSONFormatter

        formatter = JSONFormatter(indent=2)
        data = {"name": "张三", "age": 25}
        result = formatter.format(data)

        # Pretty formatted JSON should have newlines
        assert "\n" in result
        assert "  " in result  # Indentation

    def test_compact_format(self, generator_factory):
        """测试紧凑格式"""
        from dataforge.output.json_formatter import JSONFormatter

        formatter = JSONFormatter(indent=None)
        data = {"name": "张三", "age": 25}
        result = formatter.format(data)

        # Compact JSON should not have extra whitespace
        assert "\n" not in result

    def test_chinese_characters(self, generator_factory):
        """测试中文字符处理"""
        from dataforge.output.json_formatter import JSONFormatter

        formatter = JSONFormatter(ensure_ascii=False)
        data = {"姓名": "张三", "城市": "北京"}
        result = formatter.format(data)

        # Should preserve Chinese characters
        assert "张三" in result
        assert "北京" in result

    def test_nested_objects(self, generator_factory):
        """测试嵌套对象"""
        from dataforge.output.json_formatter import JSONFormatter

        formatter = JSONFormatter()
        data = {
            "person": {
                "name": "张三",
                "address": {"city": "北京", "district": "朝阳区"},
            }
        }
        result = formatter.format(data)

        parsed = json.loads(result)
        assert parsed["person"]["name"] == "张三"
        assert parsed["person"]["address"]["city"] == "北京"

    def test_array_data(self, generator_factory):
        """测试数组数据"""
        from dataforge.output.json_formatter import JSONFormatter

        formatter = JSONFormatter()
        data = [1, 2, 3, "test", {"key": "value"}]
        result = formatter.format(data)

        parsed = json.loads(result)
        assert parsed == data

    def test_special_values(self, generator_factory):
        """测试特殊值"""
        from dataforge.output.json_formatter import JSONFormatter

        formatter = JSONFormatter()
        data = {"null_value": None, "bool_true": True, "bool_false": False}
        result = formatter.format(data)

        parsed = json.loads(result)
        assert parsed["null_value"] is None
        assert parsed["bool_true"] is True
        assert parsed["bool_false"] is False

    def test_empty_data(self, generator_factory):
        """测试空数据"""
        from dataforge.output.json_formatter import JSONFormatter

        formatter = JSONFormatter()
        result = formatter.format({})

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed == {}
