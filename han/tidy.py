import re

import numpy
import pandas

from han.utils import extract_encode_glyphs, encode_unicode_notation


def spread_unihan_dataframe_columns(dataframe):
    dataframe = dataframe.pivot(index="unicode", columns="field", values="description")
    dataframe.reset_index(inplace=True)
    return dataframe


def create_encoded_columns(dataframe):
    dataframe["glyph"] = dataframe.unicode.apply(encode_unicode_notation)
    dataframe["simplified_glyph"] = dataframe.kSimplifiedVariant.apply(
        extract_encode_glyphs
    )
    dataframe["traditional_glyph"] = dataframe.kTraditionalVariant.apply(
        extract_encode_glyphs
    )
    dataframe["variant_glyph"] = dataframe.kSemanticVariant.apply(extract_encode_glyphs)

    dataframe["simplified_variant"] = dataframe.kSimplifiedVariant.apply(
        extract_encode_glyphs
    )
    dataframe["traditional_variant"] = dataframe.kTraditionalVariant.apply(
        extract_encode_glyphs
    )
    dataframe["semantic_variant"] = dataframe.kSemanticVariant.apply(
        extract_encode_glyphs
    )
    dataframe[
        "specialized_semantic_variant"
    ] = dataframe.kSpecializedSemanticVariant.apply(extract_encode_glyphs)
    dataframe["z_variant"] = dataframe.kZVariant.apply(extract_encode_glyphs)
    dataframe["spoofing_variant"] = dataframe.kSpoofingVariant.apply(
        extract_encode_glyphs
    )

    dataframe.sort_values(by=["glyph"], inplace=True)
    return dataframe


def assure_two_columns(dataframe):
    if len(list(dataframe)) == 1:
        dataframe[1] = None
    return dataframe


def _split_kRSUnicode_column(dataframe):
    splitted = dataframe.kRSUnicode.str.split(" ", expand=True)
    return assure_two_columns(splitted)


def _split_radical_stroke_column(dataframe):
    splitted = dataframe.radical_stroke.str.split(".", expand=True)
    return assure_two_columns(splitted)


def _split_radical_column(dataframe):
    splitted = dataframe.radical.str.split("'", expand=True)
    splitted = assure_two_columns(splitted)
    splitted.loc[~splitted[1].isnull(), 1] = True
    splitted.loc[splitted[1].isnull(), 1] = False
    return splitted


def split_radical_additional_strokes_column(dataframe):
    dataframe[["radical_stroke", "second_radical_stroke"]] = _split_kRSUnicode_column(
        dataframe
    )

    dataframe[["radical", "additional_strokes"]] = _split_radical_stroke_column(
        dataframe
    )

    dataframe[["radical", "simplified_radical_indicator"]] = _split_radical_column(
        dataframe
    )

    dataframe.drop(["radical_stroke", "second_radical_stroke"], axis=1, inplace=True)
    dataframe.radical = dataframe.radical.astype(int)
    dataframe.additional_strokes = dataframe.additional_strokes.astype(int)

    return dataframe


def clean_definition(definition):
    same_as_text = re.findall(r"\(.*U\+[0-9A-F]+.*\)", definition)
    if same_as_text:
        definition = definition.lstrip(same_as_text[0])
    splitted_definition = definition.split(";")
    clean_definitions = [
        text.strip()
        for text in splitted_definition
        if (
            not text.strip().lower().startswith("kangxi radical")
            and not text.strip().lower().startswith("radical")
            and not text.strip().lower().startswith("rad.")
        )
    ]
    return "; ".join(clean_definitions)


def determine_radical_by_row(row):
    if not pandas.isna(row.kangxi_additional) and row.kangxi_additional == 0:
        return row.kangxi_radical
    if row.additional_strokes == 0:
        return row.radical
    if number := capture_radical_number(row.kDefinition):
        return number
    return numpy.nan


def capture_radical_number(string):
    if match := re.search(r"radical (?:number )?(\d+)", string):
        return int(match.group(1))
    if match := re.search(r"rad\.? (?:no\.? )?(\d+)", string):
        return int(match.group(1))
    return numpy.nan
