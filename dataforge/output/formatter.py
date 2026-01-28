"""
输出格式化器
"""

import csv
import json
import xml.etree.ElementTree as ET
from io import StringIO
from typing import Any, TextIO
from xml.dom import minidom

import yaml


class OutputFormatter:
    """输出格式化器"""

    def format(
        self,
        data,
        format_type: str = "json",
        pretty: bool = False,
        table_name: str = "data_table",
    ) -> str:
        """格式化输出数据"""
        if format_type.lower() == "json":
            return self._format_json(data, pretty)
        elif format_type.lower() == "csv":
            return self._format_csv(data)
        elif format_type.lower() == "xml":
            return self._format_xml(data, pretty)
        elif format_type.lower() == "yaml":
            return self._format_yaml(data)
        elif format_type.lower() == "sql":
            return self._format_sql(data, table_name)
        else:
            raise ValueError(f"不支持的输出格式: {format_type}")

    def _format_json(self, data, pretty: bool = False) -> str:
        """格式化为JSON"""
        if pretty:
            return json.dumps(
                data, ensure_ascii=False, indent=2, separators=(",", ": ")
            )
        else:
            return json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    def _format_csv(self, data) -> str:
        """格式化为CSV"""
        output = StringIO()

        # 处理空数据
        if not data:
            return ""

        # 判断数据格式
        if isinstance(data, list):
            # 新格式：List[Dict[str, Any]] - 记录列表
            if data and isinstance(data[0], dict):
                fieldnames = data[0].keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            else:
                # 简单值列表
                csv_writer = csv.writer(output)
                csv_writer.writerow(["value"])
                for value in data:
                    csv_writer.writerow([value])
        else:
            # 旧格式：Dict[str, List[Any]] - 按字段分组
            if len(data) == 1:
                generator_type, values = next(iter(data.items()))
                if values and isinstance(values[0], dict):
                    # 对象类型数据
                    fieldnames = list(values[0].keys())
                    csv_dict_writer: csv.DictWriter[str] = csv.DictWriter(
                        output, fieldnames=fieldnames
                    )
                    csv_dict_writer.writeheader()
                    csv_dict_writer.writerows(values)
                else:
                    # 简单类型数据
                    csv_writer = csv.writer(output)
                    csv_writer.writerow([generator_type])
                    for value in values:
                        csv_writer.writerow([value])
            else:
                # 多种数据类型，创建列式输出
                # 检查是否有数据
                if not data.values() or all(not values for values in data.values()):
                    return ""

                max_length = max(len(values) for values in data.values())
                csv_writer = csv.writer(output)

                # 写入标题行
                headers = list(data.keys())
                csv_writer.writerow(headers)

                # 写入数据行
                for i in range(max_length):
                    row = []
                    for generator_type in headers:
                        values = data[generator_type]
                        if i < len(values):
                            row.append(values[i])
                        else:
                            row.append("")
                    csv_writer.writerow(row)

        return output.getvalue()

    def _format_xml(
        self, data: dict[str, list[Any]] | list[Any], pretty: bool = False
    ) -> str:
        """格式化为XML（兼容 List[Dict] 与 Dict[str, List]）"""
        root = ET.Element("dataforge_output")

        if isinstance(data, list):
            # 新格式：记录列表 List[Dict]
            for i, record in enumerate(data):
                item_elem = ET.SubElement(root, "item")
                item_elem.set("index", str(i))
                if isinstance(record, dict):
                    for key, val in record.items():
                        field_elem = ET.SubElement(item_elem, "field")
                        field_elem.set("name", str(key))
                        field_elem.text = str(val)
                else:
                    item_elem.text = str(record)
        else:
            # 旧格式：按生成器类型聚合的 Dict[str, List]
            for generator_type, values in data.items():
                generator_elem = ET.SubElement(root, "generator")
                generator_elem.set("type", generator_type)
                generator_elem.set("count", str(len(values)))

                for i, value in enumerate(values):
                    item_elem = ET.SubElement(generator_elem, "item")
                    item_elem.set("index", str(i))

                    if isinstance(value, dict):
                        for key, val in value.items():
                            field_elem = ET.SubElement(item_elem, "field")
                            field_elem.set("name", key)
                            field_elem.text = str(val)
                    else:
                        item_elem.text = str(value)

        if pretty:
            rough_string = ET.tostring(root, encoding="unicode")
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ")
        else:
            return ET.tostring(root, encoding="unicode")

    def _format_yaml(self, data: dict[str, list[Any]]) -> str:
        """格式化为YAML"""
        result = yaml.dump(
            data, default_flow_style=False, allow_unicode=True, sort_keys=False
        )
        return result if isinstance(result, str) else str(result)

    def _format_sql(self, data, table_name: str = "data_table") -> str:
        """格式化为SQL INSERT语句"""
        sql_statements = []

        if isinstance(data, list):
            # 新格式：List[Dict[str, Any]] - 记录列表
            if data and isinstance(data[0], dict):
                columns = list(data[0].keys())
                columns_str = ", ".join(f"`{col}`" for col in columns)

                for record in data:
                    values_list = []
                    for col in columns:
                        val = record.get(col, "")
                        if isinstance(val, str):
                            values_list.append(f"'{val.replace(chr(39), chr(39) * 2)}'")
                        elif val is None:
                            values_list.append("NULL")
                        else:
                            values_list.append(str(val))

                    values_str = ", ".join(values_list)
                    sql = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({values_str});"
                    sql_statements.append(sql)

        return "\n".join(sql_statements)

    def save_to_file(
        self,
        data: dict[str, list[Any]],
        file_path: str,
        format_type: str = "json",
        pretty: bool = False,
    ) -> None:
        """保存数据到文件"""
        formatted_data = self.format(data, format_type, pretty)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(formatted_data)

    def stream_output(
        self,
        data: dict[str, list[Any]],
        output_stream: TextIO,
        format_type: str = "json",
        pretty: bool = False,
    ):
        """流式输出数据"""
        formatted_data = self.format(data, format_type, pretty)
        output_stream.write(formatted_data)
        output_stream.flush()
