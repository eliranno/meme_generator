"""Ingestor Interface."""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from .QuoteModel import QuoteModel

class InvalidFileFormat(Exception):
    """InvalidFileFormat Exception pass"""

class IngestorInterface(ABC):
    """Interface for all concete ingestor classes."""
    file_extension = None

    @classmethod
    def can_ingest(cls, path:Path) -> bool :
        """Check if the file can be ingested."""
        return path.suffix == cls.file_extension

    @classmethod
    def parse(cls, path:str) -> List[QuoteModel]:
        """Parse the file provided in the path."""
        if cls.can_ingest(path):
            return cls._parse(path)
        raise InvalidFileFormat()

    @classmethod
    def _parse(cls, path) -> List[QuoteModel] :
        """Parse method to be implemented by specific concerte parser."""
        raise NotImplementedError

    @classmethod
    def get_qoute_models_from_file(cls,file:Path) -> List[QuoteModel]:
        """Get QuoteModels from a given directory path."""
        return cls._parse(file) if cls.can_ingest(file) else []
