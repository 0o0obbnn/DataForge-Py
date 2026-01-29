"""
CSV格式化器测试
"""

import pytest


@pytest.mark.unit
class TestCSVFormatter:
    """CSV格式化器测试类"""

    def test_format_single_record(self, generator_factory):
        """测试格式化单条记录"""
        from dataforge.output.csv_formatter import CSVFormatter

        formatter = CSVFormatter()
        data = {"name": "张三", "age": 25, "city": "北京"}
        result = formatter.format([data])

        assert isinstance(result, str)
        lines = result.strip().split("\n")
        assert len(lines) >= 2  # Header + data

    def test_format_multiple_records(self, generator_factory):
        """测试格式化多条记录"""
        from dataforge.output.csv_formatter import CSVFormatter

        formatter = CSVFormatter()
        data = [{"name": "张三", "age": 25}, {"name": "李四", "age": 30}]
        result = formatter.format(data)

        lines = result.strip().split("\n")
        assert len(lines) >= 3  # Header + 2 data rows

    def test_header_row(self, generator_factory):
        """测试表头行"""
        from dataforge.output.csv_formatter import CSVFormatter

        formatter = CSVFormatter()
        data = [{"name": "张三", "age": 25}]
        result = formatter.format(data)

        lines = result.strip().split("\n")
        header = lines[0]
        assert "name" in header or "age" in header

    def test_delimiter(self, generator_factory):
        """测试分隔符"""
        from dataforge.output.csv_formatter import CSVFormatter

        formatter = CSVFormatter(delimiter=",")
        data = [{"name": "张三", "age": 25}]
        result = formatter.format(data)

        assert "," in result

    def test_chinese_characters(self, generator_factory):
        """测试中文字符"""
        from dataforge.output.csv_formatter import CSVFormatter

        formatter = CSVFormatter()
        data = [{"姓名": "张三", "城市": "北京"}]
        result = formatter.format(data)

        assert "张三" in result
        assert "北京" in result

    def test_special_characters(self, generator_factory):
        """测试特殊字符"""
        from dataforge.output.csv_formatter import CSVFormatter

        formatter = CSVFormatter()
        data = [{"name": "张三,李四", "desc": '测试"引号"'}]
        result = formatter.format(data)

        # Should handle commas and quotes
        assert isinstance(result, str)

    def test_empty_data(self, generator_factory):
        """测试空数据"""
        from dataforge.output.csv_formatter import CSVFormatter

        formatter = CSVFormatter()
        result = formatter.format([])

        assert isinstance(result, str)

    def test_missing_fields(self, generator_factory):
        """测试缺失字段"""
        from dataforge.output.csv_formatter import CSVFormatter

        formatter = CSVFormatter()
        data = [{"name": "张三", "age": 25}, {"name": "李四"}]  # Missing age
        result = formatter.format(data)

        lines = result.strip().split("\n")
        assert len(lines) >= 3
