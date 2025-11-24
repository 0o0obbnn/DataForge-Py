"""XML output formatter for DataForge."""

import xml.etree.ElementTree as ET
from typing import Union


class XMLFormatter:
    """Formatter for XML output."""

    def __init__(
        self, root_name: str = "data", item_name: str = "item", root_tag: str = None
    ):
        """Initialize XML formatter.

        Args:
            root_name: Root element name
            item_name: Item element name for lists
            root_tag: Alias for root_name (for backward compatibility)
        """
        self.root_name = root_tag if root_tag is not None else root_name
        self.item_name = item_name

    def format(self, data: Union[dict, list], **kwargs) -> str:
        """Format data as XML.

        Args:
            data: Data to format
            **kwargs: Additional formatting options

        Returns:
            XML formatted string
        """
        if isinstance(data, dict):
            root = self._dict_to_element(data, self.root_name)
        elif isinstance(data, list):
            root = self._list_to_element(data, self.root_name)
        else:
            root = ET.Element(self.root_name)
            root.text = str(data)

        return self._element_to_string(root)

    def format_to_file(self, data: Union[dict, list], filepath: str, **kwargs) -> None:
        """Format data to XML file.

        Args:
            data: Data to format
            filepath: Output file path
            **kwargs: Additional formatting options
        """
        xml_content = self.format(data, **kwargs)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_content)

    def _dict_to_element(self, d: dict, name: str) -> ET.Element:
        """Convert dictionary to XML element."""
        element = ET.Element(name)

        for key, value in d.items():
            if isinstance(value, dict):
                child = self._dict_to_element(value, key)
            elif isinstance(value, list):
                child = self._list_to_element(value, key)
            else:
                child = ET.Element(key)
                child.text = str(value)
            element.append(child)

        return element

    def _list_to_element(self, lst: list, name: str) -> ET.Element:
        """Convert list to XML element."""
        element = ET.Element(name)

        for item in lst:
            if isinstance(item, dict):
                child = self._dict_to_element(item, self.item_name)
            else:
                child = ET.Element(self.item_name)
                child.text = str(item)
            element.append(child)

        return element

    def _element_to_string(self, element: ET.Element) -> str:
        """Convert XML element to formatted string."""
        # Add XML declaration
        xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'

        # Convert element to string
        rough_string = ET.tostring(element, encoding="unicode")

        # Parse and pretty print
        root = ET.fromstring(rough_string)
        self._indent(root)
        xml_str += ET.tostring(root, encoding="unicode")

        return xml_str

    def _indent(self, elem: ET.Element, level: int = 0) -> None:
        """Add indentation to XML element."""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self._indent(child, level + 1)
            # 处理可能未绑定的变量情况
            if elem[-1] is not None:
                child = elem[-1]
                if not child.tail or not child.tail.strip():
                    child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
