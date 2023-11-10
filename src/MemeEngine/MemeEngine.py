import os
import random
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, UnidentifiedImageError
from QuoteEngine.QuoteModel import QuoteModel


class MemeEngine():
    """MemEngine class."""

    def __init__(self, root) -> None:
        self.root = root
        os.makedirs(root, exist_ok=True)

    def make_meme(self, img_path, text, author, width=500) -> str:
        """Make mem function to generate the image with the text."""
        try:
            with Image.open(img_path.resolve(),'r') as image:
                resized = image
                model = QuoteModel(author,text)
                if image.width > 500:
                    new_height = int(image.height * (width / image.width))
                    resized = image.resize((width,new_height))
                draw = ImageDraw.Draw(resized)
                draw.text((10, image.height - 10), str(model))
                _, tf = tempfile.mkstemp(dir=self.root, prefix="meme-", suffix=".jpg")
                resized.save(tf)
        except (FileNotFoundError, UnidentifiedImageError):
            raise ValueError(f"Unable to open: {os.path.abspath(img_path)}")
        return tf
 
    @classmethod
    def find_all_images(cls, path: Path):
        """Find all images within a specified root path."""
        return [path / file for d,_,files in os.walk(path) for file in files if file.lower().endswith('.jpg')]

