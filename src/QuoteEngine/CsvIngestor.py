"""CSV Ingestor class."""

import csv
from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel

class CsvIngestor(IngestorInterface):
    """PdfIngestor class."""
    file_extension = '.csv'

    @classmethod
    def _parse(cls, path) -> List[QuoteModel]:
        """Parse quotes from file."""
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [QuoteModel(row['author'],row['body']) for row in reader]