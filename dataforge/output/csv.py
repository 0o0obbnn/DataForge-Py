"""CSV output formatter for DataForge."""

import csv
import io
from typing import Any


class CSVFormatter:
    """Formatter for CSV output."""

    def __init__(self, delimiter: str = ",", quotechar: str = '"'):
        """Initialize CSV formatter.

        Args:
            delimiter: Field delimiter
            quotechar: Quote character
        """
        self.delimiter = delimiter
        self.quotechar = quotechar

    def format(self, data: dict[str, Any] | list[Any], **kwargs) -> str:
        """Format data as CSV.

        Args:
            data: Data to format
            **kwargs: Additional formatting options

        Returns:
            CSV formatted string
        """
        if not data:
            return ""

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list) or not data:
            return ""

        # Get headers
        headers = list(data[0].keys())

        # Create CSV
        output = io.StringIO()
        writer = csv.writer(
            output,
            delimiter=self.delimiter,
            quotechar=self.quotechar,
            quoting=csv.QUOTE_MINIMAL,
        )

        # Write headers
        writer.writerow(headers)

        # Write data rows
        for item in data:
            row = []
            for header in headers:
                value = item.get(header, "")
                row.append(str(value))
            writer.writerow(row)

        return output.getvalue()

    def format_to_file(
        self, data: dict[str, Any] | list[Any], filepath: str, **kwargs
    ) -> None:
        """Format data to CSV file.

        Args:
            data: Data to format
            filepath: Output file path
            **kwargs: Additional formatting options
        """
        csv_content = self.format(data, **kwargs)
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            f.write(csv_content)
