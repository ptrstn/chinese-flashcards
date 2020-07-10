import numpy
import pandas

from mao.tidy import (
    spread_unihan_dataframe_columns,
    split_radical_additional_strokes_column,
    create_encoded_columns,
    clean_definition,
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
