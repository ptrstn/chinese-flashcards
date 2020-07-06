import pathlib
from zipfile import ZipFile

import pandas
import requests

UNIHAN_ZIP_URL = "https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip"
UNIHAN_BASE_PATH = pathlib.Path("data", "unihan")
UNIHAN_FILE_PATTERN = "Unihan_*.txt"


def download_unihan_zip(base_path=UNIHAN_BASE_PATH, url=UNIHAN_ZIP_URL, quiet=False):
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


def read_unihan_file(path):
    column_names = ["unicode", "field", "description"]
    return pandas.read_table(path, names=column_names, comment="#")


def read_all_unihan_files(base_path=UNIHAN_BASE_PATH):
    file_paths = list(pathlib.Path(base_path).glob(UNIHAN_FILE_PATTERN))
    return pandas.concat([read_unihan_file(path) for path in file_paths])


def read_unihan_field_values(file_path):
    fields = []
    with open(file_path, "r") as file:
        for line in file.readlines():
            if line.startswith("#	k"):
                fields.append(line.replace("#	", "").strip())
    return fields
