import pathlib
import random

import genanki
import pandas

from mao.data import load_radicals_dataframe

pandas.set_option("display.max_rows", 500)
pandas.set_option("display.max_columns", 500)
pandas.set_option("display.width", 1000)

print("Loading radicals from Unihan database...")
radicals_df = load_radicals_dataframe()

css = """.card {
    font-family: arial;
    font-size: 40px;
    text-align: center;
    color: black;
    background-color: white;
    margin: 10px;
}

.description{
    color: Gray;
}

.hanzi {
    font-size: 150px;
}

.hanzi2 {
    font-size: 100px;
}

.pinyin {
    color: DimGray;
    font-size: 40px;
}

.pinyin2 {
    font-size: 60px;
}

.definition {
    color: MidnightBlue;
    font-size: 50px;
}

.radical-number{
    margin-top: 10px;
    color: Grey;
    font-size: 25px;
}

.variant {
    font-size: 17px;
}

.variant-glyph {
    font-size: 65px;
}

.DarkSlateGray {
    color: DarkSlateGray;
}

.MediumVioletRed {
    color: MediumVioletRed;
}

.PaleVioletRed {
    color: PaleVioletRed;
}"""

front_formatting_1 = """<div class="description">
    Definition of
</div>

<div class="hanzi">
    {{Glyph}}
</div>

"""

back_formatting_1 = """{{FrontSide}}

<hr id="answer">

<div class="definition">
    {{Name}}
</div>

<div class="radical-number">
    Radical {{Number}}
</div>
"""


front_formatting_2 = """<div class="description">
    Pinyin of
</div>

<div class="hanzi">
    {{Glyph}}
</div>
"""

back_formatting_2 = """{{FrontSide}}

<hr id="answer">

<div>
    <span class="pinyin2"> {{Pinyin}} </span>
</div>

<div>
    {{Voice}}
</div>
"""

front_formatting_3 = """<div class="description">
    Definition of<br><br>
</div>

<div>
    <span class="pinyin2"> {{Pinyin}} </span>
</div>

<div>
    {{Voice}}
</div>
"""

back_formatting_3 = """{{FrontSide}}

<hr id="answer">

<div class="definition">
    {{Name}}
</div>

<div class="radical-number">
    Radical {{Number}}
</div>

<div class="hanzi">
    {{Glyph}}
</div>
"""

front_formatting_4 = """<div class="description">
    Hanzi of<br><br>
</div>

<div>
    <span class="pinyin2"> {{Pinyin}} </span>
</div>

<div>
    {{Voice}}
</div>
"""

back_formatting_4 = """{{FrontSide}}

<hr id="answer">

<div>
    {{#Stroke red}} {{Stroke red}} {{/Stroke red}}
    {{#Stroke order}} {{Stroke order}} {{/Stroke order}}<br>
</div>

<div class="hanzi2">
    {{Glyph}}
</div>

{{#Simplified}}
<div="variant">
    <span class="variant MediumVioletRed">Simplified: </span>
    <span class="variant-glyph MediumVioletRed">{{Simplified}}</span>
</div>
{{/Simplified}}

{{#Traditional}}
<div="variant">
    <span class="variant PaleVioletRed">Traditional: </span>
    <span class="variant-glyph PaleVioletRed">{{Traditional}}</span>
</div>
{{/Traditional}}

{{#Variant}}
<div="variant">
    <span class="variant DarkSlateGray">Variants: </span>
    <span class="variant-glyph DarkSlateGray">{{Variant}}</span>
</div>
{{/Variant}}
"""

print("Creating Anki model...")
my_model = genanki.Model(
    175638195,
    "Radical",
    fields=[
        {"name": "Glyph"},
        {"name": "Definition"},
        {"name": "Variant"},
        {"name": "Voice"},
        {"name": "Stroke order"},
        {"name": "Stroke red"},
        {"name": "Pinyin"},
        {"name": "Simplified"},
        {"name": "Traditional"},
        {"name": "Number"},
        {"name": "Name"},
    ],
    templates=[
        {"name": "Card 1", "qfmt": front_formatting_1, "afmt": back_formatting_1},
        {"name": "Card 2", "qfmt": front_formatting_2, "afmt": back_formatting_2},
        {"name": "Card 3", "qfmt": front_formatting_3, "afmt": back_formatting_3},
        {"name": "Card 4", "qfmt": front_formatting_4, "afmt": back_formatting_4},
    ],
    css=css,
)

print("Creating Deck...")
my_deck = genanki.Deck(random.randrange(11972374263), "Kangxi Radicals")

print("Iterating rows...")
for index, row in radicals_df.iterrows():
    glyph = row.glyph
    definition = row.definition
    radical_name = row.radical_name
    number = row.radical
    simplified_glyph = row.simplified_glyph if row.simplified_glyph != glyph else ""
    traditional_glyph = row.traditional_glyph if row.traditional_glyph != glyph else ""
    variant = "".join(
        [
            g
            for g in row.variant_glyph
            if g not in simplified_glyph and g not in traditional_glyph
        ]
    )
    voice = f"[sound:{glyph}.mp3]"
    stroke_red = (
        f'<img src="{glyph}-red.png">'
        if pathlib.Path(f"data/strokes/{glyph}-red.png").exists()
        else ""
    )
    stroke_order = f'<img src="{glyph}-order.gif">'
    pinyin = row.kMandarin

    my_note = genanki.Note(
        model=my_model,
        fields=[
            glyph,
            definition,
            variant,
            voice,
            stroke_order,
            stroke_red,
            pinyin,
            simplified_glyph,
            traditional_glyph,
            str(number),
            radical_name,
        ],
    )
    my_deck.add_note(my_note)

package = genanki.Package(my_deck)

glyphs = list(radicals_df.glyph)
media_files = [
    *[f"data/voices/{glyph}.mp3" for glyph in glyphs],
    *[f"data/strokes/{glyph}-order.gif" for glyph in glyphs],
    *[f"data/strokes/{glyph}-red.png" for glyph in glyphs],
]
media_files = [file for file in media_files if pathlib.Path(file).exists()]
package.media_files = media_files

package.write_to_file("radicals.apkg")
