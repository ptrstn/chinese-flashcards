from mao.hsk import read_all_hsk_files, add_hsk_level_column
from mao.kangxi import add_is_kangxi_radical_column, retrieve_unicode_kangxi_table
from mao.tidy import (
    spread_unihan_dataframe_columns,
    create_encoded_columns,
    split_radical_additional_strokes_column,
)
from mao.unihan import (
    read_all_unihan_files,
    list_unihan_file_paths,
    read_unihan_field_values,
)

dataframe = read_all_unihan_files()
dataframe = spread_unihan_dataframe_columns(dataframe)
dataframe = create_encoded_columns(dataframe)
dataframe = split_radical_additional_strokes_column(dataframe)
kangxi_table = retrieve_unicode_kangxi_table()
dataframe = add_is_kangxi_radical_column(dataframe, kangxi_table=kangxi_table)
hsk_table = read_all_hsk_files()
dataframe = add_hsk_level_column(dataframe, hsk_table=hsk_table)
dataframe.sort_values(
    ["hsk_level", "kFrequency", "additional_strokes", "radical"], inplace=True
)

desired_columns = [
    "glyph",
    "unicode",
    "kDefinition",
    "radical",
    "additional_strokes",
    "simplified_radical_indicator",
    "is_kangxi_radical",
    "simplified_glyph",
    "simplified_unicode",
    "traditional_glyph",
    "traditional_unicode",
    "variant_glyph",
    "variant_unicode",
    "kTotalStrokes",
    "kFrequency",
    "hsk_level",
    "kGradeLevel",
    "kMandarin",
    "kHanyuPinlu",
    "kHanyuPinyin",
    "kCantonese",
    "kHangul",
    "kKorean",
    "kJapaneseKun",
    "kJapaneseOn",
    "kVietnamese",
    "kTang",
    "kTGHZ2013",
    "kXHC1983",
    "kRSAdobe_Japan1_6",
    "kRSKangXi",
    "kRSUnicode",
    "kSemanticVariant",
    "kSimplifiedVariant",
    "kSpecializedSemanticVariant",
    "kSpoofingVariant",
    "kTraditionalVariant",
    "kZVariant",
    "kAccountingNumeric",
    "kOtherNumeric",
    "kPrimaryNumeric",
]

unihan_file_paths = list_unihan_file_paths()
unihan_field_name_lists = [read_unihan_field_values(path) for path in unihan_file_paths]
unihan_field_names = [item for sublist in unihan_field_name_lists for item in sublist]
remaining = [column for column in unihan_field_names if column not in desired_columns]
all_columns = [*desired_columns, *remaining]
dataframe = dataframe[desired_columns]

dataframe.to_csv("data/unihan.csv", sep="\t", index=False)
