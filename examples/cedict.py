from mao.cedict import download_cedict_zip, CEDICT_PATH, read_cedict

if not CEDICT_PATH.exists():
    download_cedict_zip()

cedict_df = read_cedict()
