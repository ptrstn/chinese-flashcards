# Comparison of the german/english radicals wiki article

import pandas
from pandas import DataFrame

german_radicals = pandas.read_csv("data/kangxi/wiki_radikale_german.csv", thousands=".")
german_radicals.columns = [
    "number",
    "glyph_variants",
    "pinyin",
    "meaning_german",
    "frequency",
    "simplified",
    "examples",
]

german_radicals[["glyph", "variant"]] = german_radicals.glyph_variants.str.split(
    "(", expand=True
)

german_radicals.variant = german_radicals.variant.str.rstrip(")")
german_radicals.glyph = german_radicals.glyph.str.strip()
german_radicals.variant = german_radicals.variant.str.strip()

english_radicals = pandas.read_csv(
    "data/kangxi/wiki_radicals_english.csv", thousands=","
)
english_radicals.columns = [
    "number",
    "glyph_variants",
    "strokes",
    "meaning_english",
    "pinyin",
    "sino_vietnamese",
    "hiragana_romaji",
    "hangul_romaja",
    "frequency",
    "simplified",
    "examples",
]

english_radicals[["glyph", "variant"]] = english_radicals.glyph_variants.str.split(
    "(", expand=True
)

english_radicals.variant = english_radicals.variant.str.rstrip(")")
english_radicals.glyph = english_radicals.glyph.str.strip()
english_radicals.variant = english_radicals.variant.str.strip()

df = DataFrame()

df[
    [
        "number",
        "glyph_german",
        "variant_german",
        "pinyin_german",
        "meaning_german",
        "frequency_german",
        "simplified_german",
        "examples_german",
    ]
] = german_radicals[
    [
        "number",
        "glyph",
        "variant",
        "pinyin",
        "meaning_german",
        "frequency",
        "simplified",
        "examples",
    ]
].copy()

df[
    [
        "glyph_english",
        "variant_english",
        "meaning_english",
        "pinyin_english",
        "frequency_english",
        "simplified_english",
        "examples_english",
    ]
] = english_radicals[
    [
        "glyph",
        "variant",
        "meaning_english",
        "pinyin",
        "frequency",
        "simplified",
        "examples",
    ]
].copy()

print("Inconsistent glyphs:")
glyphs = df[df.glyph_german != df.glyph_english][["glyph_german", "glyph_english"]]
print(glyphs)

print("Inconsistent variants:")
variants = df[df.variant_german != df.variant_english][
    ["variant_german", "variant_english"]
]
print(variants[(~variants.variant_german.isna()) | (~variants.variant_english.isna())])

print("Inconsistent examples:")
examples = df[df.examples_german != df.examples_english][
    ["examples_german", "examples_english"]
]
print(examples)

print("Inconsistent frequencies:")
frequencies = df[df.frequency_german != df.frequency_english][
    ["frequency_german", "frequency_english"]
]
print(frequencies)

print("Inconsistent simplified:")
simplified = df[df.simplified_german != df.simplified_english][
    ["simplified_german", "simplified_english"]
]
print(
    simplified[
        (~simplified.simplified_german.isna()) | (~simplified.simplified_english.isna())
    ]
)
