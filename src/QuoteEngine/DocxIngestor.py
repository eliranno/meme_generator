"""PdfIngestor class."""

import re
from docx import Document
from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel

class DocxIngestor(IngestorInterface):
    """PdfIngestor class."""
    file_extension = '.docx'
    quote_regex = re.compile('"([^"]+)" - (.+)')

    @classmethod
    def _parse(cls, path) -> List[QuoteModel]:
        """Parse quotes from file."""
        try:
            doc = Document(path)
            return [QuoteModel(pair[0], pair[1]) for para in doc.paragraphs for pair in cls.quote_regex.finditer(para.text)]
        except Exception as e:
            print(f'error while trying to parse docx {e}')