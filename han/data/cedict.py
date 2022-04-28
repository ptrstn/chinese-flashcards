from pathlib import Path

import pandas

from .utils import load_feathered_u8_file, download_file, extract_zip

CEDICT_URL = "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip"

DATA_BASE_PATH = Path("data")
CEDICT_BASE_PATH = DATA_BASE_PATH.joinpath("cedict")

CEDICT_U8_FILE_NAME = "cedict_ts.u8"
CEDICT_FEATHER_FILE_NAME = "cedict.feather"


def load_cedict(base_path=CEDICT_BASE_PATH) -> pandas.DataFrame:
    u8_path = Path(base_path, CEDICT_U8_FILE_NAME)
    feather_path = Path(base_path, CEDICT_FEATHER_FILE_NAME)
    language = "english"

    try:
        return load_feathered_u8_file(u8_path, feather_path, language=language)
    except FileNotFoundError:
        u8_zip_path = Path(base_path, f"{CEDICT_U8_FILE_NAME}.zip")
        if not Path(u8_zip_path).exists():
            download_file(url=CEDICT_URL, download_to_path=u8_zip_path)
        extract_zip(
            zip_file_path=u8_zip_path, extract_to_base_path=base_path, quiet=False
        )
        return load_feathered_u8_file(u8_path, feather_path, language=language)
