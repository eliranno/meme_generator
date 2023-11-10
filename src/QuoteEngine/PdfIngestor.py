"""PdfIngestor class."""

import subprocess
import tempfile
import re
import os
from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel

class PdfIngestor(IngestorInterface):
    """PdfIngestor class."""
    file_extension = '.pdf'
    quote_regex = re.compile('"([^"]+)" - (.+)')

    @classmethod
    def _parse(cls, path) -> List[QuoteModel]:
        """Parse quotes from file."""
        _, temp_path = tempfile.mkstemp(suffix=".txt")
        try:
            subprocess.run(("pdftotext", path, temp_path), check=True)
            with open(temp_path, "r") as tf_handle:
                return [
                    QuoteModel(m[1], m[2])
                    for line in tf_handle
                    for m in cls.quote_regex.finditer(line)
                    ]
        finally:
            os.remove(temp_path)

