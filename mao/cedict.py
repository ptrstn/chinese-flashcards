import pathlib

import pandas

from mao.utils import download_file, extract_zip

CEDICT_ZIP_URL = (
    "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip"
)
CEDICT_BASE_PATH = pathlib.Path("data", "cedict")
CEDICT_PATH = pathlib.Path(CEDICT_BASE_PATH, "cedict_ts.u8")
CEDICT_FEATHER_PATH = pathlib.Path(CEDICT_BASE_PATH, "cedict.feather")


def download_cedict_zip(base_path=CEDICT_BASE_PATH, url=CEDICT_ZIP_URL, quiet=False):
    file_name = pathlib.Path(url).name
    file_path = pathlib.Path(base_path, file_name)
    download_file(url, file_path, quiet)
    extract_zip(file_path, base_path, quiet=False)


def split_hanzi_pinyin_column(dataframe):
    dataframe[["hanzi", "pinyin"]] = dataframe.hanzi_pinyin.str.split("[", expand=True)
    dataframe[["traditional", "simplified"]] = dataframe.hanzi.str.split(expand=True)
    dataframe.pinyin = dataframe.pinyin.str.rstrip("]").str.strip().str.lower()


def _read_cedict_u8(path):
    print("Loading cedict_ts.u8 as DataFrame...")
    dataframe = pandas.read_table(
        path, sep=" /", names=["hanzi_pinyin", "english"], comment="#", engine="python",
    )
    dataframe["english"] = dataframe.english.str.rstrip("/")
    split_hanzi_pinyin_column(dataframe)
    return dataframe[["traditional", "simplified", "pinyin", "english"]]


def load_cedict(path=CEDICT_PATH, feather_path=CEDICT_FEATHER_PATH):
    try:
        return pandas.read_feather(feather_path)
    except FileNotFoundError:
        if not pathlib.Path(path).exists():
            download_cedict_zip()
        df = _read_cedict_u8(path)
        print(f"Saving dedict Dataframe in Feather format to {feather_path}...")
        df.to_feather(feather_path)
        return df
