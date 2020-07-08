from mao.kangxi import retrieve_unicode_kangxi_table
from mao.tidy import (
    spread_unihan_dataframe_columns,
    create_encoded_columns,
    split_radical_additional_strokes_column,
)
from mao.unihan import read_all_unihan_files


def get_kangxi_table():
    df = read_all_unihan_files()
    df = spread_unihan_dataframe_columns(df)
    df = create_encoded_columns(df)
    df = split_radical_additional_strokes_column(df)

    columns = [
        "radical",
        "glyph",
        "variant_glyph",
        "kTotalStrokes",
        "kDefinition",
        "kMandarin",
        "kVietnamese",
        "kCantonese",
        "kJapaneseKun",
        "kJapaneseOn",
        "kHangul",
        "kKorean",
        "kFrequency",
        "simplified_glyph",
        "traditional_glyph",
    ]

    radicals = df[df.additional_strokes == 0][columns]
    radicals.sort_values(["radical", "glyph"], inplace=True)
    kangxi = retrieve_unicode_kangxi_table()
    unified_table = radicals[radicals.glyph.isin(list(kangxi.unified_glyph))]

    return unified_table
