from unittest import mock

import numpy
import pandas
from pandas._libs.missing import NAType

from mao.tidy import (
    spread_unihan_dataframe_columns,
    split_radical_additional_strokes_column,
    create_encoded_columns,
    clean_definition,
    determine_radical_by_row,
    capture_radical_number,
)


def test_spread_unihan_dataframe_columns():
    columns = ["unicode", "field", "description"]
    data = numpy.array(
        [[1, "A", None], [1, "B", None], [3, "A", None], [3, "D", None], [3, "E", None]]
    )
    dataframe = pandas.DataFrame(data=data, columns=columns)

    assert len(dataframe) == 5
    assert len(list(dataframe)) == 3

    wide_df = spread_unihan_dataframe_columns(dataframe)
    assert len(wide_df) == 2
    assert len(list(wide_df)) == 5


def test_create_encoded_columns():
    columns = [
        "unicode",
        "kSimplifiedVariant",
        "kTraditionalVariant",
        "kSemanticVariant",
    ]

    data = numpy.array(
        [
            ["513F", None, "0x5152", None],
            ["0x5E72", None, "U+4e7e U+5E79", None],
            ["6236", "0x6237", None, None],
            ["706B", None, None, None],
            ["U+5fc3", None, None, "U+38FA<kMatthews U+5FC4<kMatthews"],
        ]
    )

    dataframe = pandas.DataFrame(data=data, columns=columns)
    encoded_dataframe = create_encoded_columns(dataframe)
    encoded_dataframe.set_index("glyph", inplace=True)

    assert encoded_dataframe.loc["儿", "simplified_glyph"] is None
    assert encoded_dataframe.loc["儿", "traditional_glyph"] == "兒"
    assert encoded_dataframe.loc["干", "simplified_glyph"] is None
    assert encoded_dataframe.loc["干", "traditional_glyph"] == "乾 幹"
    assert encoded_dataframe.loc["戶", "simplified_glyph"] == "户"
    assert encoded_dataframe.loc["戶", "traditional_glyph"] is None
    assert encoded_dataframe.loc["火", "simplified_glyph"] is None
    assert encoded_dataframe.loc["火", "traditional_glyph"] is None
    assert encoded_dataframe.loc["心", "variant_glyph"] == "㣺 忄"


def test_split_radical_additional_strokes_column():
    expected_new_columns = {
        "radical",
        "additional_strokes",
        "simplified_radical_indicator",
    }

    dataframe = pandas.DataFrame(data=["120'.3"], columns=["kRSUnicode"])
    dataframe = split_radical_additional_strokes_column(dataframe)
    assert {"kRSUnicode", *expected_new_columns} == set(dataframe)
    assert dataframe.iloc[0]["radical"] == 120
    assert dataframe.iloc[0]["additional_strokes"] == 3
    assert dataframe.iloc[0]["simplified_radical_indicator"] is True

    dataframe = pandas.DataFrame(data=["25.5 197'.0"], columns=["kRSUnicode"])
    dataframe = split_radical_additional_strokes_column(dataframe)
    assert {"kRSUnicode", *expected_new_columns} == set(dataframe)
    assert dataframe.iloc[0]["radical"] == 25
    assert dataframe.iloc[0]["additional_strokes"] == 5
    assert dataframe.iloc[0]["simplified_radical_indicator"] is False


def test_clean_definition():
    definition = "teeth; gears, cogs; age; KangXi radical 211"
    assert clean_definition(definition) == "teeth; gears, cogs; age"
    d = "(same as U+3021 HANGZHOU NUMERAL ONE 〡) number one; line; KangXi radical 2"
    assert clean_definition(d) == "number one; line"
    definition = "dog; radical number 94 "
    assert clean_definition(definition) == "dog"
    definition = "melon, gourd, cucumber; rad. 97 "
    assert clean_definition(definition) == "melon, gourd, cucumber"
    definition = "step with left foot; rad. no 60"
    assert clean_definition(definition) == "step with left foot"
    definition = "halberd, spear, lance; rad. 62"
    assert clean_definition(definition) == "halberd, spear, lance"
    definition = "scallion, leek; radical 179"
    assert clean_definition(definition) == "scallion, leek"
    definition = "cow, ox, bull; KangXi radical93"
    assert clean_definition(definition) == "cow, ox, bull"
    definition = "factory, workshop; radical 27"
    assert clean_definition(definition) == "factory, workshop"


def test_determine_radical_by_row():
    row = mock.Mock()

    row.kangxi_radical = 13
    row.kangxi_additional = 0
    row.radical = 13
    row.additional_strokes = 0
    row.kDefinition = "Blubb"
    assert determine_radical_by_row(row) == 13

    row.kangxi_radical = 13
    row.kangxi_additional = 1
    row.radical = 12
    row.additional_strokes = 0
    row.kDefinition = "Blubb"
    assert determine_radical_by_row(row) == 12

    row.kangxi_radical = 13
    row.kangxi_additional = 1
    row.radical = 12
    row.additional_strokes = 4
    row.kDefinition = "Blubb"
    assert pandas.isna(determine_radical_by_row(row))

    row.kangxi_radical = numpy.nan
    row.kangxi_additional = numpy.nan
    row.radical = 7
    row.additional_strokes = 0
    row.kDefinition = "Blubb"
    assert determine_radical_by_row(row) == 7

    row.kangxi_radical = 1
    row.kangxi_additional = 4
    row.radical = 1
    row.additional_strokes = 4
    row.kDefinition = "profession, business; GB radical 111 "
    assert determine_radical_by_row(row) == 111

    row.kangxi_radical = 128
    row.kangxi_additional = -2
    row.radical = 128
    row.additional_strokes = -2
    row.kDefinition = "pen; radical number 129 "
    assert determine_radical_by_row(row) == 129

    row.kangxi_radical = NAType()
    row.kangxi_additional = NAType()
    row.radical = 1
    row.additional_strokes = 0
    row.kDefinition = "Gongche character yi with downward slash"
    assert determine_radical_by_row(row) == 1


def test_capture_radical_number():
    assert capture_radical_number("profession, business; GB radical 111") == 111
    assert capture_radical_number("pen; radical number 129") == 129
    assert capture_radical_number("page, sheet, leaf; rad. no. 181") == 181
    assert capture_radical_number("step with left foot; rad. no 60") == 60
    assert capture_radical_number("do not; not; surname; rad. 80") == 80
    assert pandas.isna(capture_radical_number("Gongche character yi with slash"))
    assert pandas.isna(numpy.nan)
