"""SQL output formatter for DataForge."""

from typing import Union


class SQLFormatter:
    """Formatter for SQL output."""

    def __init__(self, table_name: str = "test_data", batch_size: int = None):
        """Initialize SQL formatter.

        Args:
            table_name: Default table name for INSERT statements
            batch_size: Number of records per batch INSERT (optional)
        """
        self.table_name = table_name
        self.batch_size = batch_size

    def format(self, data: Union[dict, list], table_name: str = None, **kwargs) -> str:
        """Format data as SQL INSERT statements.

        Args:
            data: Data to format
            table_name: Table name for INSERT statements
            **kwargs: Additional formatting options

        Returns:
            SQL formatted string
        """
        if not data:
            return ""

        table = table_name or self.table_name

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list) or not data:
            return ""

        # Get columns from first item
        columns = list(data[0].keys())
        if not columns:
            return ""

        # Build SQL statements
        sql_lines = []
        for item in data:
            values = []
            for col in columns:
                value = item.get(col, "NULL")
                if value is None:
                    values.append("NULL")
                elif isinstance(value, str):
                    # Escape single quotes
                    escaped_value = value.replace("'", "''")
                    values.append(f"'{escaped_value}'")
                else:
                    values.append(str(value))

            sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)});"
            sql_lines.append(sql)

        return "\n".join(sql_lines)

    def format_to_file(
        self, data: Union[dict, list], filepath: str, table_name: str = None, **kwargs
    ) -> None:
        """Format data to SQL file.

        Args:
            data: Data to format
            filepath: Output file path
            table_name: Table name for INSERT statements
            **kwargs: Additional formatting options
        """
        sql_content = self.format(data, table_name=table_name, **kwargs)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(sql_content)
