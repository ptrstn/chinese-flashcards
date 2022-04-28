import pathlib

import pandas

HSK_BASE_PATH = pathlib.Path("data", "hsk")
HSK_FILE_PATTERN = "hsk*.txt"


def read_hsk_file(path):
    hsk_level = pathlib.Path(path).name.lstrip("hsk").rstrip(".txt")
    with open(path, "r") as file:
        content = file.read().strip()
        characters = [character for character in content]
        dataframe = pandas.DataFrame(characters, columns=["glyph"])
        dataframe.loc[:, "hsk_level"] = int(hsk_level)
        dataframe.hsk_level = dataframe.hsk_level.astype("Int64")
        return dataframe


def list_hsk_file_paths(base_path=HSK_BASE_PATH):
    paths = pathlib.Path(base_path).glob(HSK_FILE_PATTERN)
    return sorted(paths)


def read_all_hsk_files(base_path=HSK_BASE_PATH):
    file_paths = list_hsk_file_paths(base_path)
    hsk_files = [read_hsk_file(path) for path in file_paths]
    dataframe = pandas.concat(hsk_files)
    return dataframe


def add_hsk_level_column(dataframe, hsk_table):
    return dataframe.merge(hsk_table, how="left", on="glyph")


def load_hsk(base_path=HSK_BASE_PATH) -> pandas.DataFrame:
    return read_all_hsk_files(base_path)
