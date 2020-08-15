# Check which characters in the unihan database are radicals
import pandas

from mao.tidy import (
    spread_unihan_dataframe_columns,
    create_encoded_columns,
    split_radical_additional_strokes_column,
)
from mao.unihan import load_unihan

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
        "simplified_glyph",
        "traditional_glyph",
        "variant_glyph",
        "simplified_radical_indicator",
        "kDefinition",
        "kangxi_radical",
        "kangxi_additional",
        "radical",
        "additional_strokes",
        "kRSKangXi",
        "kRSUnicode",
        "kTotalStrokes",
        # "kSpecializedSemanticVariant",
        # "kSpoofingVariant",
        # "kZVariant",
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

kangxi_radicals = df[df.kangxi_additional == 0]
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
]

radicals = radicals.sort_values(["radical", "kangxi_radical"])

####################################################
# Differences between kRSKangXi and kRSUnicode field
####################################################

inconsistent_radicals = radicals[(radicals.kangxi_radical != radicals.radical)]
inconsistent_missing_radicals = radicals[
    (radicals.kangxi_radical != radicals.radical) | (radicals.kangxi_radical.isna())
]

# 㔾
