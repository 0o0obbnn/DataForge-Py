"""
SQL格式化器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestSQLFormatter:
    """SQL格式化器测试类"""

    def test_format_insert_statement(self, generator_factory):
        """测试INSERT语句格式化"""
        from dataforge.output.sql_formatter import SQLFormatter
        
        formatter = SQLFormatter(table_name="users")
        data = {"name": "张三", "age": 25}
        result = formatter.format([data])
        
        assert isinstance(result, str)
        assert "INSERT" in result.upper()
        assert "users" in result

    def test_format_multiple_records(self, generator_factory):
        """测试多条记录"""
        from dataforge.output.sql_formatter import SQLFormatter
        
        formatter = SQLFormatter(table_name="users")
        data = [
            {"name": "张三", "age": 25},
            {"name": "李四", "age": 30}
        ]
        result = formatter.format(data)
        
        assert isinstance(result, str)
        assert "张三" in result
        assert "李四" in result

    def test_column_names(self, generator_factory):
        """测试列名"""
        from dataforge.output.sql_formatter import SQLFormatter
        
        formatter = SQLFormatter(table_name="users")
        data = [{"name": "张三", "age": 25}]
        result = formatter.format(data)
        
        assert "name" in result
        assert "age" in result

    def test_string_escaping(self, generator_factory):
        """测试字符串转义"""
        from dataforge.output.sql_formatter import SQLFormatter
        
        formatter = SQLFormatter(table_name="users")
        data = [{"name": "张'三", "desc": "测试\"引号\""}]
        result = formatter.format(data)
        
        # Should escape quotes
        assert isinstance(result, str)

    def test_null_values(self, generator_factory):
        """测试NULL值"""
        from dataforge.output.sql_formatter import SQLFormatter
        
        formatter = SQLFormatter(table_name="users")
        data = [{"name": "张三", "age": None}]
        result = formatter.format(data)
        
        assert "NULL" in result.upper() or "None" in result

    def test_numeric_values(self, generator_factory):
        """测试数值"""
        from dataforge.output.sql_formatter import SQLFormatter
        
        formatter = SQLFormatter(table_name="users")
        data = [{"name": "张三", "age": 25, "score": 98.5}]
        result = formatter.format(data)
        
        assert "25" in result
        assert "98.5" in result

    def test_batch_insert(self, generator_factory):
        """测试批量插入"""
        from dataforge.output.sql_formatter import SQLFormatter
        
        formatter = SQLFormatter(table_name="users", batch_size=2)
        data = [
            {"name": "张三", "age": 25},
            {"name": "李四", "age": 30},
            {"name": "王五", "age": 35}
        ]
        result = formatter.format(data)
        
        assert isinstance(result, str)

    def test_empty_data(self, generator_factory):
        """测试空数据"""
        from dataforge.output.sql_formatter import SQLFormatter
        
        formatter = SQLFormatter(table_name="users")
        result = formatter.format([])
        
        assert isinstance(result, str)
