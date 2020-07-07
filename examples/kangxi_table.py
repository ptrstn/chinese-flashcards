# Produces a similar table as:
# https://en.wikipedia.org/wiki/Kangxi_radical#Table_of_radicals
import subprocess

import pandas

from mao.kangxi import retrieve_unicode_kangxi_table
from mao.tidy import (
    spread_unihan_dataframe_columns,
    create_encoded_columns,
    split_radical_additional_strokes_column,
)
from mao.unihan import read_all_unihan_files

pandas.set_option("display.max_rows", 500)
pandas.set_option("display.max_columns", 500)
pandas.set_option("display.width", 1000)

df = read_all_unihan_files()
df = spread_unihan_dataframe_columns(df)
df = create_encoded_columns(df)
df = split_radical_additional_strokes_column(df)

columns = [
    "radical",
    "glyph",
    "kTotalStrokes",
    "kDefinition",
    "kMandarin",
    "kVietnamese",
    "kCantonese",
    "kJapaneseKun",
    "kJapaneseOn",
    "kHangul",
    "kKorean",
    "kFrequency",
    "simplified_glyph",
    "traditional_glyph",
]

radicals = df[df.additional_strokes == 0][columns]
radicals.sort_values(["radical", "glyph"], inplace=True)

radicals.columns = radicals.columns.str.replace("_glyph", "")

kangxi = retrieve_unicode_kangxi_table()

original = radicals[radicals.glyph.isin(list(kangxi.glyph))]
unified = radicals[radicals.glyph.isin(list(kangxi.unified_glyph))]

wiki_url = "https://en.wikipedia.org/wiki/Kangxi_radical#Table_of_radicals"
bootstrap = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"

with open("kangxi_table.html", "w") as file:
    file.write("<!DOCTYPE html><html><head>")
    file.write('<meta charset="utf-8"/>')
    file.write(f'<link rel="stylesheet" href="{bootstrap}">')
    file.write("</head><body>")
    file.write('<div class="container-fluid">')
    file.write('<h1 class="display-4">Unified Kangxi Radicals</h1>')
    file.write(f"<p class='lead'>Compare with: <a href='{wiki_url}'>{wiki_url}</a></p>")
    file.write(unified.to_html())
    file.write("</body></html>")

subprocess.call(["xdg-open", "kangxi_table.html"])
