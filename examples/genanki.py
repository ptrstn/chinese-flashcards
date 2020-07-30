import random

import genanki
import pandas

from mao.data import load_radicals_dataframe

pandas.set_option("display.max_rows", 500)
pandas.set_option("display.max_columns", 500)
pandas.set_option("display.width", 1000)

radicals_df = load_radicals_dataframe()

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

for index, row in radicals_df.iterrows():
    my_note = genanki.Note(
        model=my_model, fields=[row.glyph, row.definition, row.variant_glyph]
    )
    my_deck.add_note(my_note)

package = genanki.Package(my_deck)
package.write_to_file("radicals.apkg")
