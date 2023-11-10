"""Data Model"""

from dataclasses import dataclass

class QuoteModel:
    """QuoteModel class."""
    def __init__(self, author:str, body:str) -> None:
        self.author = author
        self.body = body

    def __str__(self) -> str:
        """Return string from the given QuoteModel object."""
        return f'{self.author} - {self.body}'
