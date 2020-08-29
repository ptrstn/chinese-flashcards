from pathlib import Path

import pandas

from .utils import load_feathered_u8_file, download_file

DEDICT_URL = "https://raw.githubusercontent.com/gugray/HanDeDict/master/handedict.u8"

DATA_BASE_PATH = Path("data")
DEDICT_BASE_PATH = DATA_BASE_PATH.joinpath("dedict")

DEDICT_U8_FILE_NAME = "handedict.u8"
DEDICT_FEATHER_FILE_NAME = "dedict.feather"


def load_dedict(base_path=DEDICT_BASE_PATH) -> pandas.DataFrame:
    u8_path = Path(base_path, DEDICT_U8_FILE_NAME)
    feather_path = Path(base_path, DEDICT_FEATHER_FILE_NAME)
    language = "german"

    try:
        return load_feathered_u8_file(u8_path, feather_path, language=language)
    except FileNotFoundError:
        download_file(url=DEDICT_URL, download_to_path=u8_path)
        return load_feathered_u8_file(u8_path, feather_path, language=language)
