import pandas

from mao.hsk import read_all_hsk_files, add_hsk_level_column
from mao.kangxi import (
    retrieve_unicode_kangxi_table,
    add_is_kangxi_radical_column,
    load_kangxi_radicals_table,
)
from mao.tidy import (
    spread_unihan_dataframe_columns,
    create_encoded_columns,
    split_radical_additional_strokes_column,
    clean_definition,
)
from mao.unihan import UNIHAN_BASE_PATH, load_unihan


def get_kangxi_radicals_table(unihan_base_path=UNIHAN_BASE_PATH):
    df = load_unihan(unihan_base_path)
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


def load_radicals_dataframe():
    dataframe = load_unihan()
    dataframe = spread_unihan_dataframe_columns(dataframe)
    dataframe = create_encoded_columns(dataframe)
    dataframe = split_radical_additional_strokes_column(dataframe)
    kangxi_table = load_kangxi_radicals_table()
    dataframe = add_is_kangxi_radical_column(dataframe, kangxi_table=kangxi_table)
    hsk_table = read_all_hsk_files()
    dataframe = add_hsk_level_column(dataframe, hsk_table=hsk_table)
    radicals_df = dataframe[dataframe.is_kangxi_radical].copy()

    # https://stackoverflow.com/a/60024263/9907540
    radicals_df.loc[:, "strokes"] = radicals_df.kTotalStrokes.astype("float").astype(
        "Int64"
    )

    radicals_df.loc[:, "definition"] = radicals_df.apply(
        lambda row: clean_definition(row.kDefinition)
        if not pandas.isnull(row.kDefinition)
        else row.kDefinition,
        axis=1,
    )

    radicals_df = pandas.merge(
        radicals_df,
        kangxi_table[["unified_glyph", "meaning"]],
        left_on="glyph",
        right_on="unified_glyph",
    )

    radicals_df.kFrequency = radicals_df.kFrequency.fillna(value="9")
    radicals_df[["kFrequency"]] = radicals_df[["kFrequency"]].fillna(value=9)
    radicals_df.kFrequency = radicals_df.kFrequency.astype("int")

    german_radicals = pandas.read_csv("data/kangxi/radikale.csv")
    german_radicals.columns = [
        "number",
        "glyph_variants",
        "pinyin",
        "meaning_german",
        "frequency",
        "abbreviation",
        "examples",
    ]

    german_radicals = german_radicals[["number", "meaning_german"]]

    radicals_df = pandas.merge(
        radicals_df, german_radicals, left_on="radical", right_on="number",
    )

    radicals_df = radicals_df[
        [
            "glyph",
            "meaning",
            "meaning_german",
            "definition",
            "kMandarin",
            "variant_glyph",
            "simplified_glyph",
            "traditional_glyph",
            "radical",
            "strokes",
            "kFrequency",
        ]
    ]

    radicals_df.sort_values(["strokes", "kFrequency", "radical"], inplace=True)
    radicals_df.fillna("", inplace=True)
    return radicals_df
