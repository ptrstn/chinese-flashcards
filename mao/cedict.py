import pathlib
from zipfile import ZipFile

import pandas
import requests

CEDICT_ZIP_URL = (
    "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip"
)
CEDICT_BASE_PATH = pathlib.Path("data", "cedict")
CEDICT_PATH = pathlib.Path(CEDICT_BASE_PATH, "cedict_ts.u8")


def download_cedict_zip(base_path=CEDICT_BASE_PATH, url=CEDICT_ZIP_URL, quiet=False):
    file_name = pathlib.Path(url).name
    zip_file_path = pathlib.Path(base_path, file_name)

    if not quiet:
        print(f"Downloading {url} to {zip_file_path}...")

    response = requests.get(url, allow_redirects=True)
    base_path.mkdir(parents=True, exist_ok=True)
    with open(zip_file_path, "wb") as file:
        file.write(response.content)

    if not quiet:
        print(f"Extracting {zip_file_path} to {base_path}...")
    with ZipFile(zip_file_path, "r") as zip_file:
        zip_file.extractall(base_path)


def read_cedict(path=CEDICT_PATH):
    dataframe = pandas.read_table(
        path, sep=" /", names=["hanzi_pinyin", "english"], comment="#", engine="python",
    )

    dataframe[["hanzi", "pinyin"]] = dataframe.hanzi_pinyin.str.split("[", expand=True)
    dataframe[["traditional", "simplified"]] = dataframe.hanzi.str.split(expand=True)
    dataframe.pinyin = dataframe.pinyin.str.rstrip("]")
    dataframe.english = dataframe.english.str.rstrip("/")

    return dataframe[["traditional", "simplified", "pinyin", "english"]]
