import random

import genanki
import pandas

from mao.hsk import read_all_hsk_files, add_hsk_level_column
from mao.kangxi import retrieve_unicode_kangxi_table, add_is_kangxi_radical_column
from mao.tidy import (
    spread_unihan_dataframe_columns,
    create_encoded_columns,
    split_radical_additional_strokes_column,
    clean_definition,
)
from mao.unihan import read_all_unihan_files

pandas.set_option("display.max_rows", 500)
pandas.set_option("display.max_columns", 500)
pandas.set_option("display.width", 1000)

dataframe = read_all_unihan_files()
dataframe = spread_unihan_dataframe_columns(dataframe)
dataframe = create_encoded_columns(dataframe)
dataframe = split_radical_additional_strokes_column(dataframe)
kangxi_table = retrieve_unicode_kangxi_table()
dataframe = add_is_kangxi_radical_column(dataframe, kangxi_table=kangxi_table)
hsk_table = read_all_hsk_files()
dataframe = add_hsk_level_column(dataframe, hsk_table=hsk_table)
df = dataframe[dataframe.is_kangxi_radical].copy()

# https://stackoverflow.com/a/60024263/9907540
df.loc[:, "strokes"] = df.kTotalStrokes.astype("float").astype("Int64")

df.loc[:, "definition"] = df.apply(
    lambda row: clean_definition(row.kDefinition)
    if not pandas.isnull(row.kDefinition)
    else row.kDefinition,
    axis=1,
)

df = df[["glyph", "definition", "kMandarin", "variant_glyph", "radical", "strokes"]]

df = df[df.strokes <= 4]

df.sort_values(["strokes", "radical"], inplace=True)

df.fillna("", inplace=True)

my_model = genanki.Model(
    random.randrange(1 << 30, 1 << 31),
    "Radical",
    fields=[{"name": "Glyph"}, {"name": "Definition"}, {"name": "Variant"},],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Glyph}}",
            "afmt": (
                "{{FrontSide}}"
                '<hr id="answer">'
                "{{Definition}}</br>"
                "Variants: {{Variant}"
            ),
        },
    ],
)

my_deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), "Kangxi Radicals")

for index, row in df.iterrows():
    my_note = genanki.Note(
        model=my_model, fields=[row.glyph, row.definition, row.variant_glyph]
    )
    my_deck.add_note(my_note)

package = genanki.Package(my_deck)
package.write_to_file("radicals.apkg")
