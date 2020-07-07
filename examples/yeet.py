import pandas

from mao.kangxi import retrieve_unicode_kangxi_table
from mao.tidy import (
    spread_unihan_dataframe_columns,
    create_encoded_columns,
    split_radical_additional_strokes_column,
)
from mao.unihan import read_all_unihan_files

pandas.set_option("display.max_rows", 500)
pandas.set_option("display.max_columns", 500)
pandas.set_option("display.width", 1000)

df = read_all_unihan_files()
df = spread_unihan_dataframe_columns(df)
df = create_encoded_columns(df)
df = split_radical_additional_strokes_column(df)

columns = [
    "glyph",
    "simplified_glyph",
    "traditional_glyph",
    "radical",
    "kDefinition",
    "kMandarin",
    "kCantonese",
    "kKorean",
    "kJapaneseOn",
]

radicals = df[df.additional_strokes == 0][columns]
radicals.sort_values(["radical", "glyph"], inplace=True)

kangxi = retrieve_unicode_kangxi_table()

print("Kangxi Radicals:")
original = radicals[radicals.glyph.isin(list(kangxi.glyph))]
print(original)

print("Unified Kangxi Radicals:")
unified = radicals[radicals.glyph.isin(list(kangxi.unified_glyph))]
print(unified)
