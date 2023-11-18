"""Main App for Meme generator webapp."""
import tempfile
import random
import requests
import os
from flask import Flask, render_template, abort, request
from pathlib import Path
from QuoteEngine.Ingestor import Ingestor
from MemeEngine.MemeEngine import MemeEngine

app = Flask(__name__)
current_dir = Path(__file__).parent
meme = MemeEngine(current_dir/Path("static"))

def setup():
    """Load all resources."""
    quote_files = ['/_data/DogQuotes/DogQuotesTXT.txt',
                   '/_data/DogQuotes/DogQuotesDOCX.docx',
                   '/_data/DogQuotes/DogQuotesPDF.pdf',
                   '/_data/DogQuotes/DogQuotesCSV.csv']
    quote_files = [str(current_dir) + file for file in quote_files]
    Ingestor.register_defaults()
    quotes = [q for file in quote_files for q in Ingestor.get_qoute_models_from_file(Path(file))]
    images_path = "_data/photos/dog/"
    imgs = MemeEngine.find_all_images(current_dir / images_path)
    return quotes, imgs

quotes, imgs = setup()

@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img, quote = (random.choice(item) for item in (imgs, quotes))
    path = meme.make_meme(img, quote.body, quote.author)
    relpath = str(current_dir)
    path = os.path.relpath(path, relpath)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    try:
        image_url = request.form.get("image_url")
        body = request.form.get("body")
        author = request.form.get("author")
        current_dir = Path(__file__).parent
        response = requests.get(image_url, allow_redirects=True)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tf:
            tf.write(response.content)
            meme_path = meme.make_meme(Path(tf.name), body, author)
            relpath = str(current_dir)
            meme_path = os.path.relpath(meme_path, relpath)
        return render_template("meme.html", path=Path(meme_path))
    except Exception as e:
        return f'error occured {e}', 400


if __name__ == "__main__":
    app.run()
