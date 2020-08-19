# Check which characters in the unihan database are radicals
import pandas

from han.tidy import (
    spread_unihan_dataframe_columns,
    create_encoded_columns,
    split_radical_additional_strokes_column,
    determine_radical_by_row,
)
from han.data.unihan import load_unihan

pandas.set_option("display.max_rows", 500)
pandas.set_option("display.max_columns", 500)
pandas.set_option("display.width", 1000)

df = load_unihan()
df = spread_unihan_dataframe_columns(df)
df = create_encoded_columns(df)
df = split_radical_additional_strokes_column(df)

df[["kangxi_radical", "kangxi_additional"]] = (
    df.kRSKangXi.str.strip().str.split(".", expand=True).copy()
)

df.kangxi_radical = df.kangxi_radical.astype("float").astype("Int64")
df.kangxi_additional = df.kangxi_additional.astype("float").astype("Int64")

df = df[
    [
        "glyph",
        "simplified_variant",
        "traditional_variant",
        "semantic_variant",
        "specialized_semantic_variant",
        "z_variant",
        "spoofing_variant",
        "simplified_radical_indicator",
        "kDefinition",
        "kMandarin",
        "kangxi_radical",
        "kangxi_additional",
        "radical",
        "additional_strokes",
        "kRSKangXi",
        "kRSUnicode",
        "kTotalStrokes",
    ]
]

####################################################
# All the Radicals based on the kRSUnicode field
####################################################

unicode_radicals = df[df.additional_strokes == 0]
simplified_unicode_radicals = unicode_radicals[
    unicode_radicals.simplified_radical_indicator
]

print(
    f"There are {len(unicode_radicals)} radicals in the Unihan standard "
    f"out of which {len(simplified_unicode_radicals)} are simplified"
)

####################################################
# All the Radicals based on the kRSKangXi field
####################################################

kangxi_df = df[~df.kRSKangXi.isna()]

print(
    f"Out of the {len(df)} characters only {len(kangxi_df)} "
    f"are in the kangxi dictionary ({round(len(kangxi_df) / len(df) * 100, 1)}%)"
)

kangxi_radicals = df[df.kangxi_additional == 0].copy()
kangxi_radicals.loc[:, "radical_number"] = kangxi_radicals.kangxi_radical

simplified_kangxi_radicals = kangxi_radicals[
    kangxi_radicals.simplified_radical_indicator
]

print(
    f"There are {len(kangxi_radicals)} kangxi radicals in the Unihan standard "
    f"out of which {len(simplified_kangxi_radicals)} are simplified"
)

# 421 / 21
# 494 / 24

####################################################
# Differences between kDefinition field radicals
####################################################

df1 = df[df.kDefinition.str.contains(r"radical", case=False, na=False)]

df2 = df[df.kDefinition.str.contains(r"radical (?:number )?\d", case=False, na=False)]

differences = pandas.concat([df1, df2]).drop_duplicates(keep=False)

####################################################
# All the Radicals based on the kDefinition field
####################################################

definition_radicals = df[
    df.kDefinition.str.contains(
        r"radical (?:number )?\d|rad\.? (?:no\.? )?\d", case=False, na=False
    )
]

definition_radicals = definition_radicals[
    [
        "glyph",
        "kDefinition",
        "kangxi_radical",
        "kangxi_additional",
        "radical",
        "additional_strokes",
    ]
]

invisible_radicals = definition_radicals[
    (definition_radicals.additional_strokes != 0)
    & (definition_radicals.kangxi_additional != 0)
]

print("Radicals that can not be identified by the radical/strokes number")
print(invisible_radicals)

####################################################
# All the Radicals based on all of the methods above
####################################################

radicals = df[
    (df.kangxi_additional == 0)
    | (df.additional_strokes == 0)
    | (
        df.kDefinition.str.contains(
            r"radical (?:number )?\d|rad\.? (?:no\.? )?\d", case=False, na=False
        )
    )
].copy()

radicals = radicals.sort_values(["radical", "kangxi_radical"])

####################################################
# Differences between kRSKangXi and kRSUnicode field
####################################################

inconsistent_radicals = radicals[(radicals.kangxi_radical != radicals.radical)]

inconsistent_additional = radicals[
    (radicals.kangxi_radical == radicals.radical)
    & (radicals.kangxi_additional != radicals.additional_strokes)
]

inconsistents = radicals[
    (radicals.kangxi_radical != radicals.radical)
    | (radicals.kangxi_additional != radicals.additional_strokes)
]

inconsistent_missing_radicals = radicals[
    (radicals.kangxi_radical != radicals.radical)
    | (radicals.kangxi_additional != radicals.additional_strokes)
    | (radicals.kangxi_radical.isna())
]

# 㔾

####################################################
# Assigning radical number field to rows
####################################################

print(f"Number of rows in radicals dataframe: {len(radicals)}")
print(f"Unique glyphs in radicals dataframe: {len(set(radicals.glyph))}")

all_radical_glyphs = set(
    list(radicals.glyph)
    + list(radicals.traditional_variant)
    + list(radicals.simplified_variant)
    + list(radicals.semantic_variant)
    + list(radicals.specialized_semantic_variant)
    + list(radicals.z_variant)
    # + list(radicals.spoofing_variant)
)

all_radical_glyphs = [glyph for glyph in all_radical_glyphs if not pandas.isna(glyph)]

all_radical_glyphs = [
    glyph for text in all_radical_glyphs for glyph in text if glyph != " "
]

all_radical_glyphs = sorted(set(all_radical_glyphs))

print(f"Total number of radical glyphs: {len(all_radical_glyphs)}")

all_df = df[df.glyph.isin(all_radical_glyphs)]

# def determine_radical(row):
#     if row.kangxi_additional == 0:
#         return row.kangxi_radical
#     if row.additional_strokes == 0:
#         return row.radical
#     return numpy.nan

radicals.loc[:, "radical_number"] = radicals.apply(
    lambda row: determine_radical_by_row(row), axis=1
)

radicals.sort_values("radical_number", inplace=True)

radicals[
    [
        "glyph",
        "simplified_variant",
        "traditional_variant",
        "semantic_variant",
        "specialized_semantic_variant",
        "z_variant",
        "spoofing_variant",
        "simplified_radical_indicator",
        "kDefinition",
        "kMandarin",
        "radical_number",
    ]
].to_html("radicals_2020-08-18.html")

####################################################
# Check which radical variants are not classified
####################################################

radicals_glyph_list = list(radicals.glyph)
missing_glyphs = sorted(set(all_radical_glyphs) - set(radicals_glyph_list))

missing_df = df[df.glyph.isin(missing_glyphs)].sort()
missing_simplified = radicals[radicals.simplified_glyph.isin(missing_glyphs)]

# 兒, 卤,
