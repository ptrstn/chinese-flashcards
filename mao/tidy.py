import pandas

from mao.unicode import encode_unicode_character, encode_unicode_characters


def spread_unihan_dataframe_columns(dataframe):
    dataframe = dataframe.pivot(index="unicode", columns="field", values="description")
    dataframe.reset_index(inplace=True)
    return dataframe


def create_encoded_columns(dataframe):
    dataframe.unicode = dataframe.unicode.copy()
    dataframe["glyph"] = dataframe.apply(
        lambda row: encode_unicode_character(row.unicode), axis=1
    )
    dataframe["simplified_unicode"] = dataframe.kSimplifiedVariant.copy()
    dataframe["simplified_glyph"] = dataframe.apply(
        lambda row: encode_unicode_characters(row.kSimplifiedVariant)
        if not pandas.isnull(row.kSimplifiedVariant)
        else row.kSimplifiedVariant,
        axis=1,
    )

    dataframe["traditional_unicode"] = dataframe.kTraditionalVariant.copy()
    dataframe["traditional_glyph"] = dataframe.apply(
        lambda row: encode_unicode_characters(row.kTraditionalVariant)
        if not pandas.isnull(row.kTraditionalVariant)
        else row.kTraditionalVariant,
        axis=1,
    )
    dataframe.sort_values(by=["glyph"], inplace=True)
    return dataframe


def split_radical_additional_strokes_column(dataframe):
    dataframe[
        ["radical_stroke", "second_radical_stroke"]
    ] = dataframe.kRSUnicode.str.split(" ", expand=True)
    dataframe[["radical", "additional_strokes"]] = dataframe.radical_stroke.str.split(
        ".", expand=True
    )
    dataframe[
        ["radical", "simplified_radical_indicator"]
    ] = dataframe.radical.str.split("'", expand=True)

    dataframe.radical = dataframe.radical.astype(int)
    dataframe.additional_strokes = dataframe.additional_strokes.astype(int)

    return dataframe
