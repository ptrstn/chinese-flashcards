import pathlib

import pandas

from mao.cedict import split_hanzi_pinyin_column
from mao.utils import download_file

DEDICT_URL = "https://raw.githubusercontent.com/gugray/HanDeDict/master/handedict.u8"
DEDICT_BASE_PATH = pathlib.Path("data", "dedict")
DEDICT_PATH = pathlib.Path(DEDICT_BASE_PATH, "handedict.u8")
DEDICT_FEATHER_PATH = pathlib.Path(DEDICT_BASE_PATH, "handedict.feather")


def download_handedict(base_path=DEDICT_BASE_PATH, url=DEDICT_URL, quiet=False):
    file_name = pathlib.Path(url).name
    file_path = pathlib.Path(base_path, file_name)
    download_file(url, file_path, quiet)


def _read_dedict_u8(path):
    print("Loading handedict.u8 as DataFrame...")
    df = pandas.read_table(
        path,
        sep=" /",
        comment="#",
        engine="python",
        names=["hanzi_pinyin", "german", "A", "B", "C", "D"],
    )
    df = df.fillna("")
    df.german = df.german + df.A + df.B + df.C + df.D
    df.german = df.german.str.rstrip("/")
    split_hanzi_pinyin_column(df)
    return df[["traditional", "simplified", "pinyin", "german"]]


def load_dedict(path=DEDICT_PATH, feather_path=DEDICT_FEATHER_PATH):
    try:
        return pandas.read_feather(feather_path)
    except FileNotFoundError:
        if not pathlib.Path(path).exists():
            download_handedict()
        df = _read_dedict_u8(path)
        print(f"Saving dedict Dataframe in Feather format to {feather_path}...")
        df.to_feather(feather_path)
        return df
