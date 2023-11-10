"""Quote import module."""
from typing import List

from .CsvIngestor import CsvIngestor
from .DocxIngestor import DocxIngestor
from .IngestorInterface import IngestorInterface
from .PdfIngestor import PdfIngestor
from .TxtIngestor import TxtIngestor
from .QuoteModel import QuoteModel


class Ingestor(IngestorInterface):
    """Main ingestor class supporting multiple types.

    Supports registering new ingestors in order to support
    additional file types.
    """

    _ingestors = set()

    @classmethod
    def can_ingest(cls, path) -> bool:
        """Return whether the input file is supported."""
        return any(ing.can_ingest(path) for ing in cls._ingestors)

    @classmethod
    def _parse(cls, path) -> List[QuoteModel]:
        for ing in cls._ingestors:
            if ing.can_ingest(path):
                return ing.parse(path.resolve())
        raise InvalidFileFormat

    @classmethod
    def register(cls, ingestor: IngestorInterface):
        """Register a new ingestor type."""
        cls._ingestors.add(ingestor)

    @classmethod
    def deregister(cls, ingestor: IngestorInterface):
        """Deregister an ingestor type."""
        cls._ingestors.remove(ingestor)

    @classmethod
    def register_defaults(cls):
        """Register default ingestor types."""
        for ing in (CsvIngestor, DocxIngestor, PdfIngestor, TxtIngestor):
            cls.register(ing)

class InvalidFileFormat(BaseException):
    """Raised when a file with the wrong extension is passed to an ingestor."""