from pathlib import Path
from zipfile import ZipFile

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
    download_to_path = Path(download_to_path)
    download_to_path.parent.mkdir(parents=True, exist_ok=True)
    with open(download_to_path, "wb") as file:
        file.write(response.content)


def extract_zip(zip_file_path, extract_to_base_path, quiet=False):
    if not quiet:
        print(f"Extracting {zip_file_path} to {extract_to_base_path}...")
    with ZipFile(zip_file_path, "r") as zip_file:
        zip_file.extractall(extract_to_base_path)


def read_u8_file(path, translation_language):
    # Cannot use the comment parameter, because it will cut lines that use that char
    # Cannot use the sep parameter, because it can be used in translation text
    dataframe = pandas.read_table(path, names=["line"], comment="#")
    dataframe = dataframe.line.str.extract(r"^\s*(.+)\s(.+)\s\[(.*)\]\s*/(.*)/\s*$")
    column_names = ["traditional", "simplified", "pinyin", translation_language]
    dataframe.columns = column_names
    return dataframe


def load_feathered_u8_file(u8_path, feather_path, language):
    try:
        return pandas.read_feather(feather_path)
    except FileNotFoundError:
        df = read_u8_file(u8_path, language)
        print(f"Saving DataFrame in Feather format to {feather_path}...")
        df.to_feather(feather_path)
        return df
