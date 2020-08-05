import pathlib

import pandas

from mao.utils import download_file, extract_zip

UNIHAN_ZIP_URL = "https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip"
UNIHAN_BASE_PATH = pathlib.Path("data", "unihan")
UNIHAN_FILE_PATTERN = "Unihan_*.txt"


def download_unihan_zip(base_path=UNIHAN_BASE_PATH, url=UNIHAN_ZIP_URL, quiet=False):
    file_name = pathlib.Path(url).name
    file_path = pathlib.Path(base_path, file_name)
    download_file(url, file_path, quiet)
    extract_zip(file_path, base_path, quiet=False)


def read_unihan_file(path):
    column_names = ["unicode", "field", "description"]
    return pandas.read_table(path, names=column_names, comment="#")


def list_unihan_file_paths(base_path=UNIHAN_BASE_PATH):
    return list(pathlib.Path(base_path).glob(UNIHAN_FILE_PATTERN))


def read_all_unihan_files(base_path=UNIHAN_BASE_PATH):
    file_paths = list_unihan_file_paths(base_path)
    return pandas.concat([read_unihan_file(path) for path in file_paths])


def read_unihan_field_values(file_path):
    fields = []
    with open(file_path, "r") as file:
        for line in file.readlines():
            if line.startswith("#	k"):
                fields.append(line.replace("#	", "").strip())
    return fields
