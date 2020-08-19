import pathlib
import warnings
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup

from .kangxi import deunihanify_radical
from .utils import validate_png_file_signature, validate_gif_file_signature

STROKE_ORDER_GIF_FILE_PATTERN = "{glyph}-order.gif"
STROKE_ORDER_RED_FILE_PATTERN = "{glyph}-red.png"


class ImageNotFound(ValueError):
    pass


def download_wikimedia_image(url, image_alt):
    response = requests.get(url)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    try:
        image_url = soup.find("img", {"alt": image_alt})["src"]
    except TypeError:
        raise ImageNotFound()
    filename = unquote(image_url.split("/")[-1])
    image_response = requests.get(image_url)
    return filename, image_response.content


def download_stroke_order_animation(glyph):
    url = f"https://commons.wikimedia.org/wiki/File:{glyph}-order.gif"
    image_alt = f"File:{glyph}-order.gif"
    return download_wikimedia_image(url=url, image_alt=image_alt)


def download_stroke_order_red(glyph):
    url = f"https://commons.wikimedia.org/wiki/File:{glyph}-red.png"
    image_alt = f"File:{glyph}-red.png"
    return download_wikimedia_image(url=url, image_alt=image_alt)


def save_content_to_disk(filename, content, path="."):
    file_path = pathlib.Path(path, filename)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as file:
        file.write(content)
        print(f"Saved content to {file_path}")


def _try_downloading_stroke_order_animation(glyph, path):
    try:
        filename_gif, content_gif = download_stroke_order_animation(glyph=glyph)
        assert validate_gif_file_signature(content_gif)
    except ImageNotFound:
        # Workaround necessary for glyph '鬥'
        print(f"Couldn't find stroke order for {glyph}. Trying deunihanification...")
        deunihanified_glyph = deunihanify_radical(glyph)
        filename_gif, content_gif = download_stroke_order_animation(
            glyph=deunihanified_glyph
        )
        filename_gif = filename_gif.replace(deunihanified_glyph, glyph)

    save_content_to_disk(filename=filename_gif, content=content_gif, path=path)


def _try_downloading_stroke_order_red(glyph, path):
    try:
        filename_red, content_red = download_stroke_order_red(glyph=glyph)
        assert validate_png_file_signature(content_red)
        save_content_to_disk(filename=filename_red, content=content_red, path=path)
    except requests.exceptions.HTTPError as e:
        warnings.warn(str(e))
    except requests.exceptions.ConnectionError:
        print("Error: No internet connection")


def check_glyph_file_exists(glyph, path):
    order_filename = STROKE_ORDER_GIF_FILE_PATTERN.format(glyph=glyph)
    red_filename = STROKE_ORDER_RED_FILE_PATTERN.format(glyph=glyph)
    order_path = pathlib.Path(path, order_filename)
    red_path = pathlib.Path(path, red_filename)
    return order_path.exists() or red_path.exists()


def download_glyph_strokes_to_disk(glyphs, path, skip_exists=True):
    for idx, glyph in enumerate(glyphs):
        if skip_exists and check_glyph_file_exists(glyph, path):
            print(f"{glyph} stroke order files already exists")
        else:
            print(f"Downloading stroke order for '{glyph}' {idx + 1}/{len(glyphs)}...")
            _try_downloading_stroke_order_animation(glyph, path)
            _try_downloading_stroke_order_red(glyph, path)
