"""Helper utilities for DataForge.

This module provides helper functions for data formatting and processing.
"""

import json
import uuid
from datetime import datetime
from typing import Union


def format_output(data: Union[dict, list], format_type: str = 'json') -> str:
    """Format data for output.

    Args:
        data: Data to format
        format_type: Output format ('json', 'csv', 'xml', 'sql')

    Returns:
        Formatted string
    """
    if format_type == 'json':
        return json.dumps(data, ensure_ascii=False, indent=2)
    elif format_type == 'csv':
        return _format_csv(data)
    elif format_type == 'xml':
        return _format_xml(data)
    elif format_type == 'sql':
        return _format_sql(data)
    else:
        return str(data)


def generate_batch_id() -> str:
    """Generate a unique batch ID for data generation.

    Returns:
        Unique batch identifier
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"batch_{timestamp}_{unique_id}"


def _format_csv(data: Union[dict, list]) -> str:
    """Format data as CSV."""
    if not data:
        return ""

    if isinstance(data, dict):
        data = [data]

    if not data or not isinstance(data, list):
        return ""

    # Get headers from first item
    headers = list(data[0].keys()) if data else []

    # Build CSV
    lines = [','.join(headers)]
    for item in data:
        row = []
        for header in headers:
            value = item.get(header, '')
            # Escape commas and quotes
            if ',' in str(value) or '"' in str(value):
                escaped_value = str(value).replace('"', '""')
                value = f'"{escaped_value}"'
            row.append(str(value))
        lines.append(','.join(row))

    return '\n'.join(lines)


def _format_xml(data: Union[dict, list]) -> str:
    """Format data as XML."""
    if isinstance(data, dict):
        return _dict_to_xml(data, 'root')
    elif isinstance(data, list):
        return _list_to_xml(data, 'root')
    else:
        return f"<root>{data}</root>"


def _dict_to_xml(d: dict, root_name: str) -> str:
    """Convert dictionary to XML."""
    xml = f"<{root_name}>"
    for key, value in d.items():
        if isinstance(value, dict):
            xml += _dict_to_xml(value, key)
        elif isinstance(value, list):
            xml += _list_to_xml(value, key)
        else:
            xml += f"<{key}>{value}</{key}>"
    xml += f"</{root_name}>"
    return xml


def _list_to_xml(lst: list, item_name: str) -> str:
    """Convert list to XML."""
    xml = ""
    for item in lst:
        if isinstance(item, dict):
            xml += _dict_to_xml(item, item_name)
        else:
            xml += f"<{item_name}>{item}</{item_name}>"
    return xml


def _format_sql(data: Union[dict, list], table_name: str = 'test_data') -> str:
    """Format data as SQL INSERT statements."""
    if not data:
        return ""

    if isinstance(data, dict):
        data = [data]

    if not data or not isinstance(data, list):
        return ""

    # Get columns from first item
    columns = list(data[0].keys()) if data else []
    if not columns:
        return ""

    # Build SQL
    sql_lines = []
    for item in data:
        values = []
        for col in columns:
            value = item.get(col, 'NULL')
            if isinstance(value, str):
                escaped_value = value.replace("'", "''")
                value = f"'{escaped_value}'"
            values.append(str(value))

        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
        sql_lines.append(sql)

    return '\n'.join(sql_lines)
