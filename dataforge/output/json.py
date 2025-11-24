"""JSON output formatter for DataForge."""

import json
from typing import Union


class JSONFormatter:
    """Formatter for JSON output."""

    def __init__(self, indent: int = 2, ensure_ascii: bool = False):
        """Initialize JSON formatter.

        Args:
            indent: JSON indentation
            ensure_ascii: Whether to ensure ASCII encoding
        """
        self.indent = indent
        self.ensure_ascii = ensure_ascii

    def format(self, data: Union[dict, list], **kwargs) -> str:
        """Format data as JSON.

        Args:
            data: Data to format
            **kwargs: Additional formatting options

        Returns:
            JSON formatted string
        """
        return json.dumps(
            data, indent=self.indent, ensure_ascii=self.ensure_ascii, **kwargs
        )

    def format_to_file(self, data: Union[dict, list], filepath: str, **kwargs) -> None:
        """Format data to JSON file.

        Args:
            data: Data to format
            filepath: Output file path
            **kwargs: Additional formatting options
        """
        json_content = self.format(data, **kwargs)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_content)
