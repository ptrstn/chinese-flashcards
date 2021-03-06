import re
from zipfile import ZipFile

import numpy
import pandas
import requests
from requests.exceptions import SSLError


def validate_png_file_signature(byte_content):
    """
    Checks if the PNG file signature is valid.

    The first eight bytes of a PNG file always contain the following values:

    (decimal)              137  80  78  71  13  10  26  10
    (hexadecimal)           89  50  4e  47  0d  0a  1a  0a
    (ASCII C notation)    \211   P   N   G  \r  \n \032 \n

    see: http://www.libpng.org/pub/png/spec/1.2/PNG-Rationale.html#R.PNG-file-signature

    :param byte_content:
    :return:
    """
    return byte_content[:7] == b"\x89PNG\r\n\x1a"


def validate_gif_file_signature(byte_content):
    return byte_content[:6] == b"GIF89a"


def download_file(url, download_to_path, quiet=False):
    if not quiet:
        print(f"Downloading {url} to {download_to_path}...")
    try:
        response = requests.get(url, allow_redirects=True)
    except SSLError:
        response = requests.get(url, allow_redirects=True, verify=False)
    download_to_path.parent.mkdir(parents=True, exist_ok=True)
    with open(download_to_path, "wb") as file:
        file.write(response.content)


def extract_zip(zip_file_path, extract_to_path, quiet=False):
    if not quiet:
        print(f"Extracting {zip_file_path} to {extract_to_path}...")
    with ZipFile(zip_file_path, "r") as zip_file:
        zip_file.extractall(extract_to_path)


def extract_unicode_notations(text, join_on=" "):
    return join_on.join(re.findall(r"U\+[0-9A-F]+", text))


def _match_encode_unicode_notation(match):
    return encode_unicode_notation(match.group())


def encode_unicode_notations_in_text(text):
    return re.sub(r"U\+[0-9a-fA-F]+", _match_encode_unicode_notation, text)


def encode_unicode_notation(unicode_notation):
    """
    Encodes a ASCII-fied unicode notation ("U+" convention)

    :param unicode_notation: string like "U+2F08"
    :return: encoded unicode character like "人"
    """
    return chr(int(unicode_notation.replace("U+", ""), 16))


def extract_encode_glyphs(value):
    if pandas.isnull(value):
        return value
    glyphs = encode_unicode_notations_in_text(extract_unicode_notations(value))
    return glyphs if glyphs else numpy.nan
