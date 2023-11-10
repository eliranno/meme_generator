"""TxtIngestor class."""

import re
from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel

class TxtIngestor(IngestorInterface):
    """PdfIngestor class."""
    file_extension = '.txt'
    quote_regex = re.compile('"([^"]+)" - (.+)')

    @classmethod
    def _parse(cls, path) -> List[QuoteModel]:
        """Parse quotes from file."""
        with open(path, 'r', encoding='utf-8') as file:
            return [QuoteModel(*line.strip().split(" - ")) for line in file if " - " in line]

    @classmethod
    def splitLine(cls,line:str):
        """Split line into author and body."""
        author, body = line.split('-')
        return author.strip(), body.strip()