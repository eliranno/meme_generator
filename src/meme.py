"""Command line meme generator module."""

import os
import random
import argparse
import tempfile
from QuoteEngine.Ingestor import Ingestor
from QuoteEngine.QuoteModel import QuoteModel
from MemeEngine.MemeEngine import MemeEngine
from pathlib import Path

current_dir = Path(__file__).parent

def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an path and a quote."""
    img = None
    quote = None

    if path is None:
        imgs = MemeEngine.find_all_images(current_dir / "_data/photos/dog/")
        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        Ingestor.register_defaults()
        quotes = Ingestor.scan(current_dir / "_data/DogQuotes")
        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception("Author Required if Body is Used")
        quote = QuoteModel(author, body)

    meme = MemeEngine(tempfile.mkdtemp(prefix="memes-"))
    path = meme.make_meme(img, quote.body, quote.author)
    return path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="meme generator.")
    parser.add_argument("--path", type=Path, help="Path to an image.")
    parser.add_argument("--body", help="Body of the test.")
    parser.add_argument("--author", help="Author name.")
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
